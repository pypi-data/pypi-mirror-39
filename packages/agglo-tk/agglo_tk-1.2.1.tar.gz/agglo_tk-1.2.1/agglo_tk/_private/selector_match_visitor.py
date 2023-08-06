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

from ..exceptions import AtkUndecidedError
from ..trace import trace


__all__ = ["AtkSelectorMatchVisitor"]

# class MatchVisitor(AtkBoolTreeEvalVisitor):
class AtkSelectorMatchVisitor(object):

    def __init__(self, stop_on_found, obj, **kwargs):
        class Container(ObjectWrapper):
            def __init__(self, obj, **kwargs):
                ObjectWrapper.__init__(self, obj)

                for key, value in kwargs.items():
                    if not hasattr(obj, key):
                        object.__setattr__(self, key, value)

        self.__datas = Container(obj, **kwargs)
        self.__match_done = False
        self.__stop_on_found = stop_on_found

        
    def visit_And(self, visitable, *args, **kwargs):
        result = True
        exception = None
        
        for child in visitable:
            try:
                # If one of the children is False
                result = child.accept(self, *args, **kwargs) and result
                if not result and self.__stop_on_found:
                    # And is False
                    trace(trace_class="ATK", info="AtkSelector:visit_And failed, stop searching")
                    break
            except AtkUndecidedError as _exception:
                exception = _exception

        # If no child is False, and one child at least is undecided
        if result and exception is not None:
            raise exception

        trace(trace_class="ATK", info="AtkSelector:visit_And " + ("succeeded" if result else "failed"))
        return result

        
    def visit_Or(self, visitable, *args, **kwargs):
        result = False
        exception = None
        
        for child in visitable:
            try:
                # If one of the children is True
                result = child.accept(self, *args, **kwargs) or result
                if result and self.__stop_on_found:
                    trace(trace_class="ATK", info="AtkSelector:visit_Or succeeded, stop searching")
                    break
            except AtkUndecidedError as _exception:
                exception = _exception

        # If no child is True, and one child at least is undecided
        if not result and exception is not None:
            raise exception
                
        trace(trace_class="ATK", info="AtkSelector:visit_Or " + ("succeeded" if result else "failed"))
        return result

        
    def visit_Xor(self, visitable, *args, **kwargs):
        nb_found = 0
        exception = None
        
        for child in visitable:
            try:
                current_result = child.accept(self, *args, **kwargs)
                if current_result:
                    nb_found += 1
                    
                    # If two of the children are True
                    if (nb_found > 1) and  self.__stop_on_found:
                        trace(trace_class="ATK", info="AtkSelector:visit_Xor failed, stop searching")
                        break
            except AtkUndecidedError as _exception:
                exception = _exception

        # If only one or zero child is True, and one child at least is undecided
        if (nb_found <= 1) and exception is not None:
            raise exception
        
        trace(trace_class="ATK", info="AtkSelector:visit_Xor found " + str(nb_found) + (": succeeded" if (nb_found == 1) else ": failed"))
        return (1 == nb_found)

        
    def visit_Not(self, visitable, *args, **kwargs):
        result = not visitable.condition.accept(self, *args, **kwargs)

        trace(trace_class="ATK", info="AtkSelector:visit_Not " + ("succeeded" if result else "failed"))
        return result 


    def visit_AtkTreeLeaf(self, visitable, *args, **kwargs):
        result = False
        criteria = visitable

        try:
            result = criteria.match(self.__datas)
        except Exception as exception:
            raise AtkUndecidedError(self.__datas)
                
        return result
