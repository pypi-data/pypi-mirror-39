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

import time
from threading import Timer

from .input_handler import AtkInputHandler
from .io_hub import AtkIOHub
from .io_connection_logs import AtkIOConnectionLogs
from ..exceptions import AtkSelectorError
from ..trace import trace


__all__ = ["AtkIOConnection", "IO_TYPE_INPUT", "IO_TYPE_OUTPUT"]

IO_TYPE_INPUT = "input"
IO_TYPE_OUTPUT = "output"

class AtkIOConnection(AtkInputHandler):

    WAIT_IO_SLEEP_TIME_S = 0.1

    # TODO ajouter du code pour activer/desactiver le logging
    def __init__(self, name, io_device, io_logs=None, io_hub=None):
        if io_logs is None:
            io_logs = AtkIOConnectionLogs()

        # Create input logs
        self.__name = name
        input_logs = io_logs.add_io_logs(IO_TYPE_INPUT, owner=self)
        io_logs.add_io_logs(IO_TYPE_OUTPUT, owner=self)
        
        # Init input handler
        super(AtkIOConnection, self).__init__(input_logs)

        self._io_logs = io_logs
        self._io_device = io_device
        self.__io_hub = io_hub if io_hub is not None else AtkIOHub()
        self.__io_hub.attach(self._io_device, self)


    @property
    def name(self):
        return self.__name


    @property
    def io_logs(self):
        return self._io_logs


    @property
    def io_hub(self):
        return self.__io_hub


    @property
    def opened(self):
        return self.io_hub.is_opened(self._io_device)


    def __getattr__(self, attr_name):
        result = None
        io_type_pattern = "io_type_"
        pattern_len = len(io_type_pattern)

        try:
            # Make sure attr_name begins by io_type_pattern
            attr_name.index(io_type_pattern, 0, pattern_len)

            # Retrieve io_type
            result = self._io_logs.get_io_type(attr_name[pattern_len:], self)
        # Case where attr_name doesn't begin by io_type_pattern
        # Case where io handler did not define an io_type in io_logs
        except (ValueError, IndexError):
            raise AttributeError("'" + str(type(self)) + "' object has no attribute '" + attr_name + "'")

        return result


    def open(self):
        self.io_hub.open(self._io_device)


    def close(self):
        self.io_hub.close(self._io_device)


    def handle_input(self, io_device, data):
        if io_device is not self._io_device:
            # Should not happen
            raise ValueError

        # TODO ajouter un selecteur filtre a la reception
        super(AtkIOConnection, self).handle_input(io_device, data)

        self._io_logs.execute_callbacks()


    def send(self, output):
        try:
            # Send datas
            self._io_device.write(output)
        # Even if write has failed, register output
        finally:
            # TODO ajouter du code pour activer/desactiver le logging
            # TODO ajouter un selecteur filtre a l'emission
            # Add output to io logs and execute callbacks
            self.io_logs[self.io_type_output].add_io(output)
            self._io_logs.execute_callbacks()


    # TODO : modifier cette fonction en prenant en compte qu'il peut y avoir une callback d'enregistree pour ce selecteur.
    # dans ce cas, la callback doit etre inoperante le temps du wait_io
    def wait_io(self, io_criteria, nb_occurrences=1):
        result = None
        _continue = False
        # TODO ?
        # start_time, end_time = io_criteria.selecting_times
        start_time = io_criteria.start_time
        end_time = io_criteria.end_time
        now = time.time()

        trace(trace_class="ATK", info="AtkIOHandler::wait " + str(nb_occurrences) + " io(s) matching selector " + str(io_criteria))

        # TODO c'est pas bon, retourner une exception ?
        # TODO Est-ce qu'on autoriserait pas ca ?
        # Check that wait_io will actually have to wait: it is not meant to parse 
        # only already received IO(use selector's check  method instead)
        _continue = (end_time is not None) and (end_time > now)

        # If now is in the future
        if _continue and (start_time is not None):
            _continue = (end_time > start_time)
            
            # If start_time is in the future
            if _continue and (start_time > now):
                # Wait until now, without matching the IOs
                time.sleep(start_time - now)

        # TODO definir plutot une callback, avec self en attribut, et un pipe. ensuite on fait le select(pipe, timeout) sur le type pour debloquer wait_io
        # on remove la callback apres le select
        while "IO is not received and timeout not elapsed":
            try:
                # TODO optim : ne faire le check que sur les nouvelles occurences (toutes  pour le 1er appel)
                result = self._io_logs.check(io_criteria, nb_occurrences=nb_occurrences)
                # If check method doesn't raise, it means nb_occurrences have been found
                break
            except AtkSelectorError:
                # If maximum time is elapsed
                if (end_time < time.time()):
                    # TODO plutot raise AtkTimeoutError
                    trace(trace_class="ATK", info="AtkIOHandler::wait_io failed")
                    raise

                time.sleep(AtkIOConnection.WAIT_IO_SLEEP_TIME_S)

        return result


    def start_periodic_io(self, timeout_ms, *args, **kwargs):
        io_timers = []
        fn_periodic_ios = args
        output = kwargs.get("output", None)
        input_selector = kwargs.get("input_selector", None)

        # If output is given
        if output is not None:
            # Add a send output function as periodic io
            def send_periodic_io():
                self.send(output)
            fn_periodic_ios.append(send_periodic_io)
        if input_selector is not None:
            # Add a validate input function as periodic io
            def receive_periodic_io():
                # TODO il faut moduler le input_selector start_time/end_time => ajouter un accesseur time_span (end_time-start_time), un setter offset (decale start_time et/ou end_time)
                self.check_io(input_selector)
            fn_periodic_ios.append(receive_periodic_io)
        
        # Start periodic_io timers
        for current_periodic_io in fn_periodic_ios:
            current_timer = Timer(timeout_ms/1000, current_periodic_io)
            current_timer.start()
            io_timers.append(current_timer)
        
        # Return first io timer if only on has been peiordic io created, otherwise return all io timers
        return io_timers[0] if (len(fn_periodic_ios) == 1) else io_timers

        
    def stop_periodic_io(self, periodic_io):
        periodic_io.cancel()
        