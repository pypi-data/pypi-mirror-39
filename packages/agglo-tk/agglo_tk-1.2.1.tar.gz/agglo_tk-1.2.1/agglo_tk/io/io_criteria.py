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

from time import time
from copy import deepcopy as copy
from types import MethodType
import re

from ..selector import AtkCriteria
from ..exceptions import AtkIOSelectorError


__all__ = ["AtkIOCriteria"]

class AtkIOCriteria(AtkCriteria):
    # TODO changer en io_types
    BOUNDARIES = ["io_type", "first_rank", "last_rank", "start_time", "end_time"]

    def __init__(self, match_io_data=None, **kwargs):
        # Ensure all io boundaries have a value
        for bound_name in AtkIOCriteria.BOUNDARIES:
            kwargs.setdefault(bound_name, None)

        # Init criteria with io boundaries
        super(AtkIOCriteria, self).__init__(**kwargs)

        # Set match io data function
        if match_io_data is not None:
            self.change_behavior(match_io_data=match_io_data)


    def __repr__(self):
        io_boundaries = "({})".format("|".join(AtkIOCriteria.BOUNDARIES))
        valid_params = []

        result = super(AtkIOCriteria, self).__repr__()
        params = re.search("[^\(]*(.*)", result).group(1)
        params = params.split(", ")
        for param in params:
            if not re.search(".*{}=None.*".format(io_boundaries), param):
                valid_params.append(param)

        result = "{}({})".format(self.__class__.__name__, ", ".join(valid_params))

        return result

    
    @property
    def ranks(self):
        first_rank = self.first_rank
        last_rank = self.last_rank

        if first_rank is None:
            first_rank = 0
        if (last_rank is not None) and (last_rank != - 1):
            last_rank += 1

        return slice(first_rank, last_rank)


    @ranks.setter
    def ranks(self, value):
        self.first_rank = value[0]
        self.last_rank = value[1]

    
    def rank(self, rank, new_instance=False):
        result = self
        
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)

        result.first_rank = rank
        result.last_rank = rank

        return result


    # TODO ajouter un attribut io_logs ? le changement d'io_type peut ensuite modifier l'io_logs au besoin   
    # Ca impacterait egalement le match sur les negative ranks     
    def from_current_tail(self, io_logs, rank_span=None, new_instance=False):
        result = self
        
        if (rank_span is not None) and (rank_span < 0):
            raise ValueError

        # TODO creer un decorateur pour ce code
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)
            
        result.first_rank = len(io_logs)
        
        if rank_span is not None:
            result.last_rank = result.first_rank + rank_span
        else:
            result.last_rank = None

        return result

        
    def until_current_tail(self, io_logs, rank_span=None, new_instance=False):
        result = self
        
        if (rank_span is not None) and (rank_span < 0):
            raise ValueError
        
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)
            
        result.last_rank = len(io_logs)
        
        if rank_span is not None:
            result.first_rank = result.last_rank - rank_span
            
            # Since last index is in this case a positive absolute index, 
            # first index must also be a positive absolute index
            result.first_rank = max(0, result.first_rank)
        else:
            result.first_rank = None

        return result
   
    
    def offset_rank(self, offset, new_instance=False):
        result = self
        
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)
            
        return result
    
    
    def from_now(self, time_span_ms=None, new_instance=False):
        result = self
        
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)
            
        result.start_time = time()
        
        if time_span_ms is not None:
            result.end_time = result.start_time + (time_span_ms / 1000)
        else:
            result.end_time = None

        return result

    def until_now(self, time_span_ms=None, new_instance=False):
        result = self
        
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)
            
        result.end_time = time()
        
        if time_span_ms is not None:
            result.start_time = result.end_time - (time_span_ms / 1000)
        else:
            result.start_time = None

        return result
   
    
    def offset_time(self, offset, new_instance=False):
        result = self
        
        # If a new selector instance has been required
        if new_instance:
            # Instanciate a copy of self
            result = copy(self)
            
        return result

        
    # TOD return a selector which cannot match anything. ca a un interet ?
    # def no_match(self):
    #     pass


    def match(self, data=None, **kwargs):
        nb_ios = kwargs.pop("nb_ios", None)

        # Convert negative first and last rank in positive values
        converter = self.convert_negative_ranks(nb_ios)
        next(converter)

        result = super(AtkIOCriteria, self).match(data, **kwargs)
        
        # Restore first and last rank initial values
        try:
            next(converter)
        except StopIteration:
            pass

        return result

        
    def _match(self, io, **kwargs):
        result =  ((self.io_type is None) or (self.io_type == io.io_type)) and \
                  ((self.first_rank is None) or (self.first_rank <= io.rank)) and \
                  ((self.last_rank is None) or (self.last_rank >= io.rank)) and \
                  ((self.start_time is None) or (self.start_time <= io.time)) and \
                  ((self.end_time is None) or (self.end_time >= io.time)) and \
                  self._match_io_data(io.data, **kwargs)

        return result


    def convert_negative_ranks(self, nb_ios):
        save_first_rank = {}
        save_last_rank = {}

        # Convert negative first and last rank in positive values
        if (self.first_rank is not None) and (self.first_rank < 0):
            if nb_ios is not None:
                save_first_rank[0] = self.first_rank
                self.first_rank += nb_ios
            else:
                raise AtkIOSelectorError(self)

        if (self.last_rank is not None) and(self.last_rank < 0):
            if nb_ios is not None:
                save_last_rank[0] = self.last_rank
                self.last_rank += nb_ios
            else:
                raise AtkIOSelectorError(self)

        # Function will exit at this point. Next step will restore ranks values
        yield

        # Restore first and last rank initial values
        if save_first_rank:
            self.first_rank = save_first_rank[0]
        if save_last_rank:
            self.last_rank = save_last_rank[0]


    def change_behavior(self, **kwargs):
        if "match_io_data" in kwargs:
            self._match_io_data = MethodType(kwargs["match_io_data"], self)

        super(AtkIOCriteria, self).change_behavior(**kwargs)


    def _match_io_data(self, io_data, **kwargs):
        return True
