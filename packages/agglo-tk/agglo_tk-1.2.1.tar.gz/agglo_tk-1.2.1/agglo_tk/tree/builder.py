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

# from redbaron import CallNode

from ..rewrite_function import rewrite
       

# tree=RedBaron("a.And(b.And(c))")    
# tree=RedBaron("a.And1(b, d).And2(c)")
# node = tree[0].value[2]
# call = node
# instance = call.parent.value[:call.previous.index_on_parent]
# instance = [str(instance) for instance in instance]
# instance = "".join(instance)
# param = call.value[0]
# call.parent.value.insert(0, node.previous.value)
# call.parent.value.insert(1, "(" + instance + ", " + str(param) + ")")
# del call.parent.value[2:call.index_on_parent + 1]
# node = tree[0].value[3]


__all__ = ["tree_builder", "TreeVisitor"]

def tree_builder(tree_spec):
    return rewrite(tree_visitor(tree_spec))

    
class TreeVisitor():
    # TODO autoriser param nom_tree=TreeClass ou nom_tree=instance_class, ou juste tree_spec
    # ainsi on peut instancier le tree a la volee, ou affecter un node construit au root du tree
    def __init__(self, tree_spec):
        self.__tree_spec = tree_spec


    @staticmethod
    def _get_instance(call_node):
        dot_idx = call_node.previous.index_on_parent
        instances = call_node.parent.value[:dot_idx]
        result = [str(instance) for instance in instances]
        result = "".join(result)

        return result


    def visit(self, tree):
        # Iterate on all subnodes of tree
        for node in tree:
            # First handle current node subnodes (like method call parameters)
            try:
                self.visit(node.value)
            except:
                pass                

            # Then handle current node
            try:
                # If current node is a call corresponding to one of the declared tree types
                if (type(node) is CallNode) and self.__tree_spec.is_node(str(node.previous.value)):
                    # Retrieve tree node elements, instance and params (ie instance.TreeType(params))
                    call = node
                    instance = tree_visitor._get_instance(call)
                    params = str(call)[1:-1]
                    if (instance != "") and (params != ""):
                        params = instance + ", " + params
                    else:
                        params = instance + params

                    # Modify node in the form TreeType(instance, params)
                    call.parent.value.insert(0, node.previous.value)
                    call.parent.value.insert(1, "(" + params + ")")
                    del call.parent.value[2:call.index_on_parent + 1]
            except:
                pass
