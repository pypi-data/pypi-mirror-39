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

from peak.util.proxies import ObjectWrapper

from ..visitor import AtkVisitable


__all__ = ["set_tree_element_attr", "AtkTreeElement"]

def set_tree_element_attr(tree_element, attr, value):
    object.__setattr__(tree_element, attr, value)


# TODO ajouter parent/ancestor
# @composite(AtkTreeLeaf, AtkTreeNode)
class AtkTreeElement(ObjectWrapper, AtkVisitable):
    tag = ""

    def __init__(self, value=None):
        # TODO c'est une bonne idee ca ? pour eviter elem.attr = truc <=>elem.value.attr avec value a None
        if value is None:
            class Container(object):
                pass
            value = Container()

        # TODO parent
        ObjectWrapper.__init__(self, value)
        object.__setattr__(self, "_parent", None)


    # def __getattribute__(self, name):
    #     result = None

    #     try:
    #         result = object.__getattribute__(self, name)
    #     except AttributeError:
    #         result = ObjectWrapper.__getattr__(self, name)
            
    #     return result



    def get_node(self, value):
        result = None
        found = False

        if (value is self) or (value is self.value):
            result = self
            found = True
        else:
            try:
                for child in self.children:
                    try:
                        result = child.get_node(value)
                        found = True
                    except ValueError:
                        pass
            # Case where value is not a tree element
            except AttributeError:
                raise ValueError

        if not found:
            # TODO definir une exception
            raise ValueError

        return result

        
    @property
    def value(self):
        return self.__subject__

    
    # tODO a test    
    @value.setter
    def value(self, value):
        ObjectWrapper.__init__(self, value)

        
    @property
    def parent(self):
        return self._parent

        
    @property
    def ancestors(self):
        result = []
        
        if self._parent is not None:
            result.append(self._parent)
            result += self._parent.ancestors
        
        return result
