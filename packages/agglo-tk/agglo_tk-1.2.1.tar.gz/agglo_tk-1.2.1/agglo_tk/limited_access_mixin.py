############################################################################
##
## Copyright (C) 2013 Plaisic and/or its subsidiary(-ies).
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

from .ro_referencer import AtkROReferencer
from .limited_access_proxy import AtkLimitedAccessProxy
from .exceptions import AtkLimitedAccessError
from .trace import trace


__all__ = ["AtkLimitedAccessMixIn"]

class AtkLimitedAccessMixIn(AtkROReferencer, AtkLimitedAccessProxy):

    def __init__(self, item, **kwargs):
        AtkROReferencer.__init__(self)
        AtkLimitedAccessProxy.__init__(self, item, **kwargs)


    # TODO ou __getattribute__?
    def __getattr__(self, attr_name):
        try:
            # return AtkROReferencer.__getattr__(self, attr_name)
            referenced_items = object.__getattribute__(self, "_referenced_items")
            return AtkROReferencer._get_reference_list(attr_name, referenced_items)[attr_name]
        # except (AttributeError, KeyError):
        except KeyError:
            return AtkLimitedAccessProxy.__getattr__(self, attr_name)


    def __setattr__(self, attr_name, value):
        try:
            AtkROReferencer._get_reference_list(attr_name, self._referenced_items)
            raise AtkLimitedAccessError(AtkLimitedAccessError.CANNOT_SET_REF)
        except KeyError:
            AtkLimitedAccessProxy.__setattr__(self, attr_name, value)


    def __delattr__(self, attr_name):
        try:
            AtkROReferencer._get_reference_list(attr_name, self._referenced_items)
            raise AtkLimitedAccessError(AtkLimitedAccessError.CANNOT_DEL_REF)
        except KeyError:
            AtkLimitedAccessProxy.__delattr__(self, attr_name)


    def add_attr(self, attr_name, value):
        try:
            AtkROReferencer._get_reference_list(attr_name, self._referenced_items)
            raise AtkLimitedAccessError(AtkLimitedAccessError.CANNOT_SET_REF)
        except KeyError:
            AtkLimitedAccessProxy.add_attr(self, attr_name, value)
