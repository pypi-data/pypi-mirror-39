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


__all__ = ["AtkSerializable"]

class AtkSerializable():

    def __init__(self):
        self.__map_serializable_attr = OrderedDict()
        self.__unserializable_attr = OrderedDict()
        self.__modified_attributes = OrderedDict()

        
    def __setattr__(self, attr_name, value):
        self._setattr(attr_name, value)

        
    def set_attr_furtive(self, attr_name, value):
        self._setattr(attr_name, value, False)

        
    def _setattr(self, attr_name, value, ab_set_serialization_needed=True):
        # TODO gerer le cas du positionnement de l'attribut via une property.setter : definir un decorateur pour les properties ? ou un Descriptor dedie qui ferait le __setattr__?
        # TODO quid du cas d'un attribut heritant de serializable (ex operator =) ?
        if (ab_set_serialization_needed) and \
           ("_AtkSerializable__map_serializable_attr" != attr_name) and \
           (attr_name in self.__map_serializable_attr):
            self.set_serialization_needed(attr_name, needed=True)
                
        self.__dict__[attr_name] = value

        
    def is_serialization_needed(self, attr_name=None):
        result = False
        
        if (attr_name is not None):
            result = attr_name in self.__modified_attributes
        else:
            result = (len(self.__modified_attributes) > 0)
        
        return result


    # TODO prendre une liste de attr names en parametres
    # TODO ajouter  TU
    def set_serialization_needed(self, *args, **kwargs):
        if kwargs is not None:
            # TODO si needed n'est pas present, ne rien faire
            needed = kwargs.get("needed", True)

        for attr_name in args:
            # If attribute is serializable
            if (attr_name in self.__map_serializable_attr):
                if needed:
                    # Put attr_name in ordered dictionary of modified attribute
                    self.__modified_attributes[attr_name] = None
                else:
                    # Remove attr_name from from modified attribute dictionary
                    if (attr_name in self.__modified_attributes):
                        del self.__modified_attributes[attr_name]
        
        
    def add_serialize_method(self, afn_serialize, *args):
        return self.__define_serialization_method(afn_serialize, self.__map_serializable_attr, args)
    
    
    def add_unserialize_method(self, afn_unserialize, *args):
        return self.__define_serialization_method(afn_unserialize, self.__unserializable_attr, args)
    
    
    # TODO gerer le cas du append (definition en 2 fois d'une methode)
    def __define_serialization_method(self, afn_method, amap_methods, attr_names):
        result = True
        
        # Check that attributes exist
        # TODO checker que ce n'est pas un attrbut de AccSerializable
        for attr_name in attr_names:
            # TODO il faut verifier que c'est bien un attribut getattr()
            result = result and (self.__dict__.get(attr_name, None) is not None)
            
        if (result):
            # For each attribute name
            for attr_name in attr_names:
                # Add method (serialize or unserialize) in the ordered dictionary
                # of methods associated with this attribute
                amap_methods.setdefault(attr_name, OrderedDict())[afn_method] = None
                
                # Save serialization state of attribute
                self.set_serialization_needed(attr_name, needed=True)
            
        return result

        
    def serialize(self, *args, **kwargs):
        if kwargs is not None:
            b_force = kwargs.get("ab_force", False)
        return self.__serialize(args, serialization=True, ab_force=b_force)
        
        
    def unserialize(self, *args):
        return self.__serialize(args, serialization=False)

        
    def __serialize(self, attr_names, serialization, ab_force=False):
        result = self._create_result()
        set_serialized_attr = set()
        set_failed_attr = set()

        # Get ordered list of (un)serializable attributes which have to be (un)serialized, 
        # depending on ab_force parameter in the case of serialization
        ls_filtered_attr_names = self.__filter_attributes(attr_names, serialization, not ab_force)
        
        # Get ordered list of (un)serialization methods corresponding to filtered attributes
        ls_serialization_methods = self.__get_serialization_methods(ls_filtered_attr_names, serialization)
        
        # Iterate on (un)serialization methods
        for fn_serialize in ls_serialization_methods:
            # Execute serialization method
            cmd_result = fn_serialize(self)
            self._append_result(result, cmd_result)
            
            # Register attributes (un)successully serialized
            ls_attrs = self.__get_serialized_attributes(fn_serialize, serialization)
            if (cmd_result):
                set_serialized_attr.update(ls_attrs)
            else:
                set_failed_attr.update(ls_attrs)

            # TODO serialize children serializable
            
        # For each attribute successfully serialized
        for s_attr in set_serialized_attr.difference(set_failed_attr):
            # Attribute doesn't have to be serialized anymore
            self.set_serialization_needed(s_attr, needed=False)
        
        return result        
        
        
    def __filter_attributes(self, attr_names, serialization, modified_only=False):
        map_filtered_attrs = OrderedDict()
        
        # If we're looking for serializable attributes
        if (serialization):
            # If base attributes list is not defined
            if (len(attr_names) == 0):
                # Add in filtered attribute ordered dictionary the modified attributes first, 
                # if the modify attribute belongs to serializable attributes
                map_filtered_attrs.update([(attr_name, None) for attr_name in self.__modified_attributes \
                                                                               if attr_name in self.__map_serializable_attr])
                
                # If unmodified attributes are allowed
                if (not modified_only):
                    # Add in filtered attribute ordered dictionary other (un)serializable attributes
                    map_filtered_attrs.update([attr for attr in self.__map_serializable_attr.items()])
                    
            # If base attributes list is defined
            else:
                # Add in filtered attribute ordered dictionary the user defined modified attributes 
                # first, if the modify attribute belongs to (un)serializable attributes
                map_filtered_attrs.update([(attr_name, None) for attr_name in attr_names \
                                                                               if attr_name in self.__modified_attributes \
                                                                               and attr_name in self.__map_serializable_attr])
                                                                               
                # If unmodified attributes are allowed
                if (not modified_only):
                    # Add in filtered attribute ordered dictionary other user defined serializable attributes
                    map_filtered_attrs.update([(attr_name, None) for attr_name in attr_names \
                                                                                   if attr_name in self.__map_serializable_attr])
        
        # If we're looking for unserializable attributes
        else:
            # If base attributes list is not defined
            if (len(attr_names) == 0):
                # Select all unserializable attributes
                map_filtered_attrs = self.__unserializable_attr
                    
            # If base attributes list is defined
            else:
                # Select all unserializable attributes given as parameters
                map_filtered_attrs.update([(attr_name, None) for attr_name in attr_names \
                                                                               if attr_name in self.__unserializable_attr])
            
        return (list(map_filtered_attrs))        
        
        
    def __get_serialization_methods(self, filtered_attr_names, serialization):
        map_methods = OrderedDict()
        map_attrs = self.__map_serializable_attr if serialization else self.__unserializable_attr

        # Iterate on filtered attributes
        for attr_name in filtered_attr_names:
            map_methods.update(map_attrs[attr_name])
        
        return list(map_methods)
        
        
    def __get_serialized_attributes(self, afn_method, serialization):
        map_attrs = self.__map_serializable_attr if serialization else self.__unserializable_attr
        ls_res = [attr_name for attr_name, map_methods in map_attrs.items() if afn_method in map_methods]
        
        return ls_res

