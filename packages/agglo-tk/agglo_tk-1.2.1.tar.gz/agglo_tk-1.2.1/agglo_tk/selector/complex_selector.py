############################################################################
## 
## Copyright (C) 2025 Plaisic and/or its subsidiary(-ies).
## Contact: eti.laurent@gmail.com
## 
## This file is part of the Agglo project.
## 
## AGGLO_BEGIN_LICENSE
## Commercial License Usage
## Licensees holding valid commercial Agglo licenses may use this file in 
## accordance with the commercial license agreement provided with the 
## Software or, alternatively, in accordance with the terms contained in 
## a written agreement between you and Plaisic.  For licensing terms and 
## conditions contact eti.laurent@gmail.com.
## 
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
## 
## In addition, the following conditions apply: 
##     * Redistributions in binary form must reproduce the above copyright 
##       notice, this list of conditions and the following disclaimer in 
##       the documentation and/or other materials provided with the 
##       distribution.
##     * Neither the name of the Agglo project nor the names of its  
##       contributors may be used to endorse or promote products derived 
##       from this software without specific prior written permission.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED 
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
## 
## AGGLO_END_LICENSE
## 
############################################################################

from types import MethodType

from ..tree.tree_bool import AtkBoolTree
# from agglo_tk.tree.tree_bool import And
# from agglo_tk.tree.tree_bool import Or
# from agglo_tk.tree.tree_bool import Xor
# from agglo_tk.tree.tree_bool import Not
from .._private.selector_match_visitor import AtkSelectorMatchVisitor
from ..exceptions import AtkUndecidedError
from ..exceptions import AtkSelectorError
from ..trace import trace


__all__ = ["AtkComplexSelector"]

# Fail Safe selector. Le critere est passe dans un arbre. Ainsi on beneficie de la continuation sur echec, et des actions sur le visit
class AtkComplexSelector(object):

    def __init__(self, criteria=None):
        self.__set_criteria(criteria)
        # self.criteria = criteria

    
    @property    
    def criteria(self):
        result = None
        try:
            result = self._criteria.root
        except AttributeError:
            pass

        return result

    
    @criteria.setter
    def criteria(self, value):
        self.__set_criteria(value)


    def __set_criteria(self, value):
        if value is None:
            # vars(self)["_criteria"] = None
            self._criteria = None
        else:
            # vars(self)["_criteria"] = AtkBoolTree(value)
            # TODO pourquoi un booltree ? qu'est-ce que ca apporte ?
            # self._criteria = AtkBoolTree(value)
            object.__setattr__(self, "_criteria", AtkBoolTree(value))


    # TODO a supprimer
    def __getitem__(self, name):
        criterias = [criteria for criteria in self.criteria.leaves(lambda x:list(x.boundaries)[0] == name)]

        if criterias:
            return criterias
        else:
            raise KeyError(name)


    def __getattr__(self, name):
        result = None
        criterias = {}

        # # TODO faire plutot la liste des criteres avec name comme critere
        # # TODO raise exception si plusieurs criteres avec le meme nom
        # try:
        #     criterias = self[name]
        #     if len(criterias) == 1:
        #         result = criterias[name].boundary
        #     else:
        #         raise ValueError("several criterias with this name")
        # except KeyError:
        #     raise AttributeError(name)

        criterias = {list(criteria.boundaries)[0]:criteria for criteria in object.__getattribute__(self, "_criteria").leaves()}
        # try:
        #     criterias = {criteria.name:criteria for criteria in object.__getattribute__(self, "_criteria").leaves()}
        # except AttributeError:
        #     # Case where _criteria is not defined yet
        #     pass
        
        # TODO utiliser l'objet referencer?
        if name in criterias:
            result = criterias[name].boundary
        else:
            result = object.__getattribute__(self, name)
            
        return result


    def __setattr__(self, name, value):
        criterias = {}

        try:
            criterias = {list(criteria.boundaries)[0]:criteria for criteria in object.__getattribute__(self, "_criteria").leaves()}
        except AttributeError:
            # Case where _criteria is not defined yet
            pass
        
        # TODO raise exception si plusieurs criteres avec le meme nom
        if name in criterias:
            criterias[name].boundary = value
        else:
            object.__setattr__(self, name, value)


    # TODO a supprimer ? On pourrait faire selector.select(data)<=>selector.match(data) modulo stop_on found
    def match(self, obj=None, **kwargs):
        stop_on_found = kwargs.pop("stop_on_found", True)

        str_trace = repr(obj) if obj is not None else repr(kwargs)
        trace(trace_class="ATK", info="AtkComplexSelector:match " + repr(self) + " against " + str_trace)

        visitor = AtkSelectorMatchVisitor(stop_on_found, obj, **kwargs)
        result = self.criteria.accept(visitor)
        trace(trace_class="ATK", info="AtkComplexSelector:match " + ("succeeded" if result else "failed"))
        
        return result
    
    
    # TODO faire la meme chose mais en renvoyant un iterator
    def select(self, iterable, **kwargs):
        result = []
        include_undecided = kwargs.pop("include_undecided", False)

        trace(trace_class="ATK", info="AtkComplexSelector:select datas amongst " + repr(iterable))
        for data in iterable:
            append = False
            try:
                append = self.match(data, **kwargs)
            except AtkUndecidedError:
                trace(trace_class="ATK", info="AtkComplexSelector:match could not decide, " + 
                                              ("include" if include_undecided else "exclude") + " by default")
                append = include_undecided
        
            if append:
                result.append(data)

        return result


    # TODO moduler nb_occurence avec un param exact/min/max
    def check(self, iterable, nb_ocurrences=1, **kwargs):
        # TODO problem : on pourrait arreter le select des qu'on depasse le nombre d'occurence max
        found_ios = self.select(iterable, **kwargs)

        trace(trace_class="ATK", info="AtkComplexSelector::check found " + str(len(found_ios)) + 
                                      " out of " + str(nb_ocurrences) + " occurences")
        if (len(found_ios) != nb_ocurrences):
            raise AtkSelectorError(self, found_ios)

        # If only one result is searched
        if (nb_ocurrences == 1):
            # Return only found entry instead of a list
            found_ios = found_ios[0]

        return found_ios
