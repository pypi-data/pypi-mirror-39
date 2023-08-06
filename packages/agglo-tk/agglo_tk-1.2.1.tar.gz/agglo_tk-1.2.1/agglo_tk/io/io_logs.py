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

from .io import AtkIO
from .io_selector import AtkIOSelector

from ..trace import trace
from ..selector.criteria import AtkCriteria


__all__ = ["AtkIOLogs"]

class AtkIOLogs():

    # TODO ajouter une liste de ios en param d'init?
    def __init__(self, io_type):
        self.__ios = []
        self.__io_type = io_type

        
    def __len__(self):
        return len(self.__ios)


    def __getitem__(self, value):
        result = []

        # If value is an instance of AtkCriteria
        if isinstance(value, AtkCriteria):
            # Build a selector using criteria
            io_selector = AtkIOSelector(value)

            # Select ios with this selector
            result = io_selector.select(self)
        else:
            # Assume value is an io_type
            result = self.__ios[value]
        
        return result

    
    def __iter__(self):
        for io in self.__ios:
            yield io
        

    # TODO ou on renvoi tout?
    def __str__(self):
        result = ""
        nb_ios = len(self.__ios)
        
        for io in self.__ios[:5]:
            result += str(io) + "\n"
            
        if (nb_ios > 5):
            result += "... (" + str(nb_ios - 5) + " ios left)"
        
        return result


    @property
    def io_type(self):
        return self.__io_type
        
        
    def add_io(self, data):
        new_io = AtkIO(data, len(self.__ios))

        trace(trace_class="ATK", info="AtkIOLogs: add io(type {}) {} at rank {}".format(self.io_type, repr(data), new_io.rank))
        self.__ios.append(new_io)
        
        return new_io


    def append_last_io(self, data):
        trace(trace_class="ATK", info="AtkIOLogs: append last io with " + repr(data) + " at rank " + str(len(self.__ios)))
        self.__ios[-1].append(data)


    def check(self, io_criteria, **kwargs):
        io_selector = AtkIOSelector(io_criteria)

        return io_selector.check(self, **kwargs)
