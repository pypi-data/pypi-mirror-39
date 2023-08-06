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

from collections import OrderedDict

from .exceptions import AtkLimitedAccessError
from .trace import trace


__all__ = ["AtkROReferencer"]

# TODO deplacer dans atk.misc
class AtkROReferencer():

    DEFAULT_LIST_ID = 0

    def __init__(self):
        # Use an ordered dict since AtkROReferencer user might 
        # have to retrieve an ordered list of referenced items
        # Use object.__setattr__ since this class can be used 
        # in conjunction with AtkLimitedAccessProxy
        # TODO il faudrait que _referenced_items soit une liste de OrderedDict afin qu'on puisse
        # referencer dans plusieurs tableaux
        # TODO renommer en referenced_lists;
        object.__setattr__(self, "_referenced_items", {AtkROReferencer.DEFAULT_LIST_ID:OrderedDict()})
        # TODO essayer de reactiver cette ligne avec les TU AtkMixLimitedAccessProxy
        # self._referenced_items = OrderedDict()

    # TODO
    def __contains__(self, value):
        pass


    # TODO ou __getattr__?
    def __getattribute__(self, attr_name):
        result = None

        try:
            referenced_items = object.__getattribute__(self, "_referenced_items")
            result = AtkROReferencer._get_reference_list(attr_name, referenced_items)[attr_name]
        except KeyError:
            result = object.__getattribute__(self, attr_name)

        return result


    def __setattr__(self, attr_name, value):
        try:
            AtkROReferencer._get_reference_list(attr_name, self._referenced_items)
            raise AtkLimitedAccessError(AtkLimitedAccessError.CANNOT_SET_REF)
        except KeyError:
            object.__setattr__(self, attr_name, value)


    def __delattr__(self, attr_name):
        try:
            AtkROReferencer._get_reference_list(attr_name, self._referenced_items)
            raise AtkLimitedAccessError(AtkLimitedAccessError.CANNOT_DEL_REF)
        except KeyError:
            object.__delattr__(self, attr_name)


    def reference(self, item, item_name, reference_list_id=DEFAULT_LIST_ID):
        trace(trace_class="ATK", info="AtkROReferencer::create reference " + item_name)

        # TODO TU reference_list_id
        # If there is a reference or an attribute with this name
        if hasattr(self, item_name):
            try:
                # Try to retrieve the reference
                if AtkROReferencer._get_reference_list(item_name, self._referenced_items)[item_name] is not item:
                    # Case where a reference with same name already exists on another item
                    raise AtkLimitedAccessError(AtkLimitedAccessError.CONFLICT)
            # Case where item_name is an attribute, not a reference
            except KeyError:
                raise AtkLimitedAccessError(AtkLimitedAccessError.CONFLICT)
        else:
            reference_list = self._referenced_items.setdefault(reference_list_id, OrderedDict())
            reference_list[item_name] = item


    def rename_reference(self, item_name, item_new_name):
        trace(trace_class="ATK", info="AtkROReferencer::rename_reference from " + \
                                      item_name + " to " + item_new_name)

        # TODO TU
        item = self.unreference(item_name)
        self.reference(item, item_new_name, item)

        
    def unreference(self, item_name):
        # TODO TU
        trace(trace_class="ATK", info="AtkROReferencer::remove reference " + item_name)

        return AtkROReferencer._get_reference_list(item_name, self._referenced_items).pop(item_name)


    # TODO TU
    def get_reference_name(self, item):
        result = None
        found = False

        # TODO en cas de doublon, que faire ?
        for reference_list in self._referenced_items.values():
            try:
                result = list(reference_list)[list(reference_list.values()).index(item)]
                found = True
                break
            except ValueError:
                pass

        if not found:
            raise ValueError

        return result


    @staticmethod
    def _get_reference_list(item_name, referenced_items):
        result = None
        found = False

        for reference_list in referenced_items.values():
            if item_name in reference_list:
                result = reference_list
                found = True
                break

        if not found:
            raise KeyError(item_name)

        return result


    def _add_reference_list(self, reference_list_id):
        self._referenced_items[reference_list_id] = OrderedDict()
