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

from .node import AtkTreeNode
from .tree import AtkTree
from .._private.tree_element import set_tree_element_attr


__all__ = ["AtkBoolNode", "And", "Or", "Xor", "Not", "AtkBoolTree", "AtkBoolTreeEvalVisitor"]

class AtkBoolNode(AtkTreeNode):
    def __init__(self, *args):
        AtkTreeNode.__init__(self)
        for operand in args:
            self.append(operand)

    @property
    def conditions(self):
        return self.children


class And(AtkBoolNode):
    tag="And"

      
class Or(AtkBoolNode):
    tag="Or"

      
class Xor(AtkBoolNode):
    tag="Xor"


class Not(AtkBoolNode):
    tag="Not"

    def __init__(self, operand):
        AtkBoolNode.__init__(self, operand)
            

    @property
    def condition(self):
        result = None

        try:
            result = self.children[0]
        except IndexError:
            pass

        return result
        
        
    @condition.setter
    def condition(self, value):
        self.append(value)

        
    def append(self, child):
        for old_child in self.children:
            set_tree_element_attr(old_child, "_parent", None)
        set_tree_element_attr(self, "_children", [])
        AtkTreeNode.append(self, child)
        
        
class AtkBoolTree(AtkTree):
    # TODO trouver un moyen d'utiliser plutot AtkTree::_add_node_type a la creation de la classe fille AtkBoolTree
    _node_types = set([And, Or, Xor, Not])

    def __init__(self, root):
        AtkTree.__init__(self, root)

    def eval(self):
        return self.root.accept(AtkBoolTreeEvalVisitor())

        
class AtkBoolTreeEvalVisitor(object):

    def __init__(self, stop_on_found=True):
        self._stop_on_found = stop_on_found
        
        
    def visit_And(self, visitable, *args, **kwargs):
        result = True
        
        for child in visitable:
            result = child.accept(self, *args, **kwargs) and result
            if not result and self._stop_on_found:
                break
                
        return result

        
    def visit_Or(self, visitable, *args, **kwargs):
        result = False
        
        for child in visitable:
            result = child.accept(self, *args, **kwargs)
            if result and self._stop_on_found:
                break
                
        return result

        
    def visit_Xor(self, visitable, *args, **kwargs):
        nbFound = 0
        
        for child in visitable:
            current_result = child.accept(self, *args, **kwargs)
            if current_result:
                nbFound += 1
                
                if (nbFound > 1) and self._stop_on_found:
                    break
                
        return (1 == nbFound)

            
    def visit_Not(self, visitable, *args, **kwargs):
        return not visitable.condition.accept(self, *args, **kwargs)

        
    def visit_AtkTreeLeaf(self, visitable, *args, **kwargs):
        return bool(visitable)
        

        

# class Condition():
#     def __init__(self, value):
#         self.__value = value

# class And(AtkNode):
#   def __init__(obj):
#       AtkNode.__init__("And", obj)...

# class Not(AtkLeaf):
#   def __init__(obj):
#       AtkLeaf.__init__("Node", obj)...
          
# class BoolTree(AtkTree):
#   def __init__():
#       self.add_type(And, arity max="*")
#       self.add_type(Not)
     
# @build_tree(BoolTree)
#    genere class ExtraCallClassCreator()
#         modifie la methode __call__ des instance de class cree dans la methode decoree
#         ne suffit pas : il faut connaitre la classe des objets crees.
#         Comment faire pour les objets instancies prealablement ? (parametre de classe/variable globale/variable recuperee par appel de methode)?
#         a priori il faudrait plutot un rewrite (d'autant plus que la classe est deja cree)
#         genr def build_tree
#             def decorator(f):
#                 f' = rewrite(f) =>remplace les appels a obj.And() par And(obj)
#                 return f'
#         def __call__():
#             save_call=__call__
#             if func_name in BoolTree.TreeNode.tag
#                 On instancie un nouveau node
#                 return BoolTree.Node[func_name](self)
#             else 
#                 __save_call__()


                
# def tree_builder(tree_spec):
#     def decorator(f):
        
#         class AtkTreeBuilder():
#             def __init__(self, tree_spec)
#                 self.__tree_spec = tree_spec
                
#             def visit(self, inspected):
#                 if inspected.name in self.__tree_spec
#                 pass
        
#         decorated = rewrite_function(AtkTreeBuilder(tree_spec))(f)
            
#         return decorated
    
#     return decorator
        