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

from .exceptions import AtkLimitedAccessError
from .trace import trace


__all__ = ["AtkLimitedAccessProxy"]

class AtkLimitedAccessProxy(ObjectWrapper):
    # TODO distinguer acces en lecture/ecriture
    def __init__(self, item, **kwargs):
        if ("allowed" in kwargs) and ("forbidden" in kwargs):
            raise ValueError("allowed and forbidden keyword args are exclusive")

        trace_access = "allowed=all" 
        if "forbidden" in kwargs:
            trace_access = "forbidden=[" + ", ".join(kwargs.get("forbidden", [])) + "]"
        elif  "allowed" in kwargs:
            trace_access = "allowed=[" + ", ".join(kwargs.get("allowed", [])) + "]"
        trace(trace_class="ATK", info="AtkLimitedAccessProxy::instantiate proxy with access rights: " + trace_access)

        ObjectWrapper.__init__(self, item)
        self.add_attr("_allowed", set(kwargs.get("allowed", [])))
        self.add_attr("_forbidden", set(kwargs.get("forbidden", [])))
        self.add_attr("_allow_by_default", True)


    # TODO ou __getattribute__?
    def __getattr__(self, attr_name):
        if self.__is_forbidden(attr_name):
            raise AtkLimitedAccessError(AtkLimitedAccessError.MASKED)
        else:
            return ObjectWrapper.__getattr__(self, attr_name)


    def __setattr__(self, attr_name, value):
        try:
            # Check if attr_name is a parent (rather than __subject__) attribute
            object.__getattribute__(self, attr_name)

            # If attr_name is a parent attribute, set it
            object.__setattr__(self, attr_name, value)

        # If attr_name is not known by parent
        except AttributeError:
            # If access to attr_name is forbidden
            if self.__is_forbidden(attr_name):
                raise AtkLimitedAccessError(AtkLimitedAccessError.MASKED)
            else:
                ObjectWrapper.__setattr__(self, attr_name, value)


    def __delattr__(self, attr_name):
        if self.__is_forbidden(attr_name):
            raise AtkLimitedAccessError(AtkLimitedAccessError.MASKED)
        else:
            try:
                object.__delattr__(self, attr_name)
            except AttributeError:
                ObjectWrapper.__delattr__(self, attr_name)


    def allow_access(self, attr_name):
        trace(trace_class="ATK", info="AtkLimitedAccessProxy::allow_access on attribute " + \
                                      attr_name + " of " + str(id(self.__subject__)))

        # TODO passage d'une liste d'attribut
        if self.__is_forbidden(attr_name):
            if attr_name in self._forbidden:
                self._forbidden.remove(attr_name)
            else:
                self._allowed.add(attr_name)
                self._allow_by_default = True


    def forbid_access(self, attr_name):
        # TODO passage d'une liste d'attribut
        trace(trace_class="ATK", info="AtkLimitedAccessProxy::forbid_access on attribute " + \
                                      attr_name + " of " + str(id(self.__subject__)))

        if not self.__is_forbidden(attr_name):
            if attr_name in self._allowed:
                self._allowed.remove(attr_name)
                if not self._allowed:
                    self._allow_by_default = False
            else:
                self._forbidden.add(attr_name)


    def add_attr(self, attr_name, value):
        # trace(trace_class="ATK", info="AtkLimitedAccessProxy::add_attr " + attr_name + \
        #                               " to proxy on " + str(id(self.__subject__)))
        object.__setattr__(self, attr_name, value)


    def __is_forbidden(self, attr_name):
        result = False

        try:
            forbidden = object.__getattribute__(self, "_forbidden")
            allowed = object.__getattribute__(self, "_allowed")
            allow_by_default = object.__getattribute__(self, "_allow_by_default")

            # Return true if explicitly forbidden, or if there are allowance rules not including attr_name
            result = (attr_name in forbidden) or \
                     (allowed and (attr_name not in allowed)) or \
                     (not allowed and not allow_by_default)
        # Case where _forbidden and _allowed are not created yet, during init
        except AttributeError:
            pass

        return result

