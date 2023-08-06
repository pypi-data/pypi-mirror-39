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

from agglo_tk import trace




# criteria.match(data)
#  -> compare criteria a data
#  -> # on peut matcher sur un objet composite data|kwargs
#  -> avantage du bound : modulation du comportmnt, sans toucher au match
#  -> avantage du getattr : ? La lambda de match pourrait remplir ce role. Mais si la fonction match est trop complexe pour une lambda,
 # on peut definir une fonction generique dans la classe, et moduler la fonction de recuperer la donnee via un extract_data
 # ex  : AtkCriteria(match=lambda crit, data:data.attr > crit.bound, bound=5) => pas d'interete au extract data
 # mais : AtkStringCriteria(extract_data=lambda crit, data : data.attr, bound=5) permet de moduler le comportement de AtkStringCriteria, sans avoir a modifier _match qui est complexe

# selector.match(data)
#  -> avantage de l'arbre de critere par rapport a une fonction de filtre
#     -> gestion du undecided : une eval peut echouer et pourtant on continue le match. Avec une lambda ou une fonction classique, 
        # le moindre undecided fait echouer l'eval alors qu'on aurait pu evaluer le match (ex Or(Failure, OK)) 
      # -> gestion du stop on found
# selector.select(data)
#  -> avantage par rapport a liste en intention : gestion du undecided : on peut inclure meme si exception sur une eval

# criterelayer
# -> bound = "layer"
# -> match(data)=lambda x:bound in x

# critere layer_field
# -> bound = "layer", "field", "value"
# -> match(data)=lambda x: bound["layer"] in x and x[bound["layer"]].bound["field"] = bound["value"]

# multi_crit_layer
# selector.criteria["icmp].layer=....
# selector.criteria["ip1"].value=...
# selector.criteria["ip2"].value=...
# selector.criteria = And(selector.criteria, ip2,And(ip1,icmp))
# selector.add_criteria(ip=Or(ip2=criteria, ip1=And(ip1, icmp)), tcp=criteria)

# from agglo_tk._private.selector_match_visitor import AtkSelectorMatchVisitor

# class AtkComplexCriteria(AtkCriteria):
#     def __init__(self, name, node, *args, **kwargs):
#         boundaries = {criteria.name:criteria for criteria in args}

#         super(AtkCriteria).__init__(self, name, kwargs.update(boundaries))
#         self._node = node(*args)


#     def _match(self, data, stop_on_found=True):
#         trace(trace_class="ATK", info="AtkComplexCriteria:match " + repr(self) + " against " + repr(data))

#         visitor = AtkSelectorMatchVisitor(stop_on_found, obj, **kwargs)
#         result = self._node.accept(visitor)
#         trace(trace_class="ATK", info="AtkComplexCriteria:match " + ("succeeded" if result else "failed"))
        
#         return result

from peak.util.proxies import ObjectWrapper


__all__ = ["AtkCriteria"]

class AtkCriteria():
    def __init__(self, match=None, extract_data=None, **kwargs):
        # Set boundaries
        object.__setattr__(self, "_boundaries", {})
        self._boundaries.update(kwargs)

        if match is not None:
            self.change_behavior(match=match)

        if extract_data is not None:
            self.change_behavior(extract_data=extract_data)


    def __repr__(self):
        params = [boundary_name +"=" + repr(boundary) for boundary_name, boundary in self._boundaries.items()]

        if self._extract_data.__func__ is not self.__class__._extract_data:
            params.insert(0, "extract_data=" + self._extract_data.__name__)
        if self._match.__func__ is not self.__class__._match:
            params.insert(0, "match=" + self._match.__name__)

        result = "{}({})".format(self.__class__.__name__, ", ".join(params))
            
        return result


    def __getattr__(self, attr_name):
        try:
            return self._boundaries[attr_name]
        except KeyError:
            raise AttributeError("'" + str(type(self)) + "' object has no attribute '" + attr_name + "'")
    

    def __setattr__(self, attr_name, value):
        if attr_name in self._boundaries:
            self._boundaries[attr_name] = value
        else:
            object.__setattr__(self, attr_name, value)

        
    @property
    def boundary(self):
        if len(self._boundaries) != 1:
            raise ValueError("Not only one boundary found")

        return list(self._boundaries.values())[0]

        
    @boundary.setter
    def boundary(self, value):
        if len(self._boundaries) != 1:
            raise ValueError("Not only one boundary found")

        self._boundaries[list(self._boundaries)[0]] = value


    @property
    def boundaries(self):
        return self._boundaries


    def change_behavior(self, **kwargs):
        if "match" in kwargs:
            self._match = MethodType(kwargs["match"], self)
        if "extract_data" in kwargs:
            self._extract_data = MethodType(kwargs["extract_data"], self)


    def match(self, data=None, **kwargs):
        # If there are extra datas in kwargs
        if kwargs:
            # Container is a proxy on data, plus attributes set on extra datas
            class Container(ObjectWrapper):
                def __init__(self, obj, **kwargs):
                    ObjectWrapper.__init__(self, obj)

                    for attr_name, value in kwargs.items():
                        if not hasattr(obj, attr_name):
                            object.__setattr__(self, attr_name, value)

            data = Container(data, **kwargs)

        extracted_data = self._extract_data(data)
        result = self._match(extracted_data)

        trace(trace_class="ATK", info="AtkCriteria:match provided data (" + \
                                      repr(extracted_data) + ") against boundary (" + repr(self._boundaries) + \
                                      (") succeeded" if result else ") failed"))
        return result


    def _match(self, data):
        return self.boundary == data


    def _extract_data(self, data):
        return data

