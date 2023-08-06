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

from ..exceptions import AtkSelectorError
from ..trace import trace


__all__ = ["AtkSelector"]

class AtkSelector():
    # le selector permet un acces facilite aux criteres et aux boundary, une modification facilite de la fonction de match
    # Comment desactiver facilmenet un critere ? en modifiant le criteria
    def __init__(self, criteria):
        object.__setattr__(self, "criteria", criteria)


    def __getattr__(self, attr_name):
        return getattr(self.criteria, attr_name)


    def __setattr__(self, attr_name, value):
        if hasattr(self.criteria, attr_name):
            setattr(self.criteria, attr_name, value)
        else:
            object.__setattr__(self, attr_name, value)


    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.criteria) + ")"


    def match(self, data=None, **kwargs):
        return self.criteria.match(data, **kwargs)


    def select(self, iterable, **kwargs):
        result = []
        _iterable= iterable

        # First retrieve nb_occurrences and reverse modifiers
        nb_occurrences = kwargs.pop("nb_occurrences", 0)
        reverse = kwargs.pop("reverse", False)
        if reverse:
            _iterable = reversed(iterable)

        # Iterate on elements
        for elem in _iterable:
            if self.match(elem, **kwargs):
                result.append(elem)
            if (nb_occurrences > 0) and (len(result) >= nb_occurrences):
                break
            
        return result 


    # TODO moduler nb_occurrences avec un param exact/min/max, ajouter un parametre reverse
    def check(self, iterable, **kwargs):
        # TODO problem : on pourrait arreter le select des qu'on depasse le nombre d'occurence max
        kwargs.setdefault("nb_occurrences", 1)
        nb_occurrences = kwargs["nb_occurrences"]

        # If check wants to make sure there is no occurrence in iterable
        if nb_occurrences == 0:
            # Look for at least one instance
            kwargs["nb_occurrences"] = 1
        found_occurences = self.select(iterable, **kwargs)
        trace(trace_class="ATK", info="AtkSelector::check found " + str(len(found_occurences)) + 
                                      " out of " + str(nb_occurrences) + " occurences")

        # Check that number of occurence found is correct
        if (len(found_occurences) < nb_occurrences) or ((nb_occurrences == 0) and found_occurences):
            raise AtkSelectorError(self, found_occurences, nb_occurrences)

        # If only one result is searched
        if nb_occurrences == 1:
            # Return only found entry instead of a list
            found_occurences = found_occurences[0]

        return found_occurences
