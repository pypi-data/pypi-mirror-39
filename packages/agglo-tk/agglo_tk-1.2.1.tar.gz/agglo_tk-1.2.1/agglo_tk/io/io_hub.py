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

import os
from threading import Thread
from threading import Event
import time
from select import select

from ..exceptions import AtkIOHubError
from ..exceptions import AtkTimeoutError
from ..trace import trace


__all__ = ["AtkIOHub"]

class AtkIOHub():

    OPEN_CLOSE_TIMEOUT_S = 10
    READ_TIMEOUT_S = 0.5
    # SLEEP_TIME_S = 0.2

    def __init__(self):
        self._io_devices = {}
        self.__opened_devices = []
        self.__read_thread = None
        self.__stop_thread = True
        self.__unlock_read_thread_pipein, self.__unlock_read_thread_pipeout = os.pipe()

        
    # def __del__(self):
    #     trace(trace_class="ATK", info="AtkIOHub::delete")

    #     self.close()
    #     os.close(self.__unlock_read_thread_pipein)
    #     self.__unlock_read_thread_pipein = 0
    #     os.close(self.__unlock_read_thread_pipeout)
    #     self.__unlock_read_thread_pipeout = 0


    # TODO valeur smart : open si des iodevices sont deja open)
    def attach(self, io_device, handler, do_open=False):
        trace(trace_class="ATK", info="AtkIOHub::attach " + str(id(io_device)) + " do_open=" + str(do_open))

        if io_device not in self._io_devices:
            self._io_devices[io_device] = handler
        # TODO
        # elif (self._io_devices[io_device] is not handler) and (self.is_opened()):
        #     raise AtkIOHubError.CONFLICT

        # TODO gerer le cas ou l'io device est deja opened
        if do_open:
            self.open(io_device)

            # Unlock read thread
            self.__unlock_read_thread()

        
    def open(self, io_device=None):
        trace(trace_class="ATK", info="AtkIOHub::open " + (str(id(io_device)) if io_device is not None else "all devices"))

        if io_device is None:
            # Open all IODevice
            not_opened_devices = [device for device in list(self._io_devices) if device not in self.__opened_devices]
            for current_device in not_opened_devices:
                current_device.open()
                self.__opened_devices.append(current_device)
        else:
            # TODO mieux gerer les exceptions
            # Open provided IODevice
            if io_device not in self._io_devices:
                raise AtkIOHubError(AtkIOHubError.UNKNOWN_DEVICE)
            else:
                io_device.open()
                self.__opened_devices.append(io_device)

        # If reading thread is started
        if self.__read_thread is None:
            trace(trace_class="ATK", info="start io hub reading thread")

            # TODO permettre au user de fournir son propre read afin de catcher les exceptions?
            # Start a thread whose task will be to read on IODevice
            ready_event = Event()
            self.__read_thread = Thread(name="AtkIOHub_read_thread", target=AtkIOHub.__read, args=(self, ready_event))
            self.__read_thread.start()

            # Wait OPEN_CLOSE_TIMEOUT_S for reading thread to be actually opened
            ready_event.wait(AtkIOHub.OPEN_CLOSE_TIMEOUT_S)
            # start_time = time.time()
            # while not self.__read_thread.is_alive() and (time.time() - start_time < AtkIOHub.OPEN_CLOSE_TIMEOUT_S):
            #     time.sleep(AtkIOHub.SLEEP_TIME_S)
                
            # if not self.__read_thread.is_alive():
            if not ready_event.is_set():
                trace(trace_class="ATK", info="io hub reading thread failed to start")
                raise AtkTimeoutError

            trace(trace_class="ATK", info="io hub reading thread started")

        trace(trace_class="ATK", info="open suceeded")


    def close(self, io_device=None):
        trace(trace_class="ATK", info="AtkIOHub::close " + (str(id(io_device)) if io_device is not None else "all devices"))

        if io_device is None:
            opened_devices = list(self.__opened_devices)

            # Close all IODevice
            for current_device in opened_devices:
                current_device.close()
                self.__opened_devices.remove(current_device)

        else:
            # TODO mieux gerer les exceptions
            # Close provided IODevice
            if io_device not in self._io_devices:
                raise AtkIOHubError(AtkIOHubError.UNKNOWN_DEVICE)
            try:
                self.__opened_devices.remove(io_device)
                io_device.close()
            # Case where io device is not in opened devices list
            except ValueError:
                if io_device.opened:
                    raise AtkIOHubError(AtkIOHubError.CONFLICT)

        # If there is no more opened devices
        if not self.__opened_devices:
            try:
                trace(trace_class="ATK", info="stop io hub reading thread " + str(id(self.__read_thread)))

                # Close reading thread
                self.__stop_thread = True
                self.__unlock_read_thread()

                # Wait OPEN_CLOSE_TIMEOUT_S for reading thread to be actually closed
                self.__read_thread.join(AtkIOHub.OPEN_CLOSE_TIMEOUT_S)
                # start_time = time.time()
                # while ((self.__read_thread.is_alive()) and (time.time() - start_time < AtkIOHub.OPEN_CLOSE_TIMEOUT_S)):
                #     trace(trace_class="ATK", info=str(time.time() - start_time))
                #     time.sleep(AtkIOHub.SLEEP_TIME_S)
                    
                if self.__read_thread.is_alive():
                    trace(trace_class="ATK", info="io hub reading thread failed to stop")
                    raise AtkTimeoutError

                self.__read_thread = None
                trace(trace_class="ATK", info="io hub reading thread stopped")
            # reading thread is None (not started)
            except AttributeError:
                pass

        trace(trace_class="ATK", info="close suceeded")


    def is_opened(self, io_device=None):
        ''' Checks that the provided device is opened and handled by io hub read thread
        '''
        # Check that there are opened devices and thar read thread is started
        result = self.__opened_devices and self.__read_thread.is_alive()

        # If an io device is provided
        if result and (io_device is not None):
            if io_device not in self._io_devices:
                raise AtkIOHubError(AtkIOHubError.UNKNOWN_DEVICE)
            else:
                # IO device must be opened and handled by read thread
                # result = io_device.opened and (io_device in self.__opened_devices)
                result = io_device in self.__opened_devices
        
        return result

        
    def __read(self, ready_event):
        read_datas = None

        # Unlock open() call
        ready_event.set()

        # Thread is going to loop on IODevice until it's told to stop
        self.__stop_thread = False
        while (not self.__stop_thread):
            # Read on IODevice
            # TODO ameliorer : blocker sur un event emis par tous les io_device, les io device sont des worker qui emettent l'evenement
            # Comme ca plus besoin de fd
            fds = {io_device.fd:io_device for io_device in self.__opened_devices}
            fds[self.__unlock_read_thread_pipein] = None

            # TODO ce serait mieux d'avoir pas de timeout mais un pipe pour debloquer le select au besoin
            # Wait for an io device to be ready to read
            trace(trace_class="ATK", info="read waiting on " + str(len(fds) - 1) + " io devices")
            readable, writable, exceptional = select(list(fds), [], [], AtkIOHub.READ_TIMEOUT_S)
            # TODO en cas d'erreur sur un fd, fermer le device et le retirer des opened et sortirs du thread si fds vide ?

            # If select exited because of unlock pipe (case of io device added or remove)
            if self.__unlock_read_thread_pipein in readable:
                # Flush unlock pipe, then we'll loop again
                os.read(self.__unlock_read_thread_pipein, 1024)
            else:
                # For each io device ready to read
                for fd in readable:
                    io_device = fds[fd]
                    read_datas = io_device.read(AtkIOHub.READ_TIMEOUT_S)
                    # trace(trace_class="ATK", info="read " + str(len(read_datas)) + " bytes on fd " + \
                    #                               str(io_device.fd) + ": " + repr(read_datas))
                    # TODO cas bizarre a verifier : en cas de non gestion par l'ioparser du cas du welcome, on ne sort pas de parse.
                    # pourtant la trace "read client:" est execute une 2eme fois. Par quel thread ?
                    # print "read client:", threading.current_thread(), sReadData
                    # TODO bizarre des fois on a un read qui retourne 0. Ca veut dire que la socket est morte ?
                    if read_datas:
                        self._io_devices[io_device].handle_input(io_device, read_datas)
            readable = None


    def __unlock_read_thread(self):
        if self.is_opened():
            os.write(self.__unlock_read_thread_pipeout, "0")
