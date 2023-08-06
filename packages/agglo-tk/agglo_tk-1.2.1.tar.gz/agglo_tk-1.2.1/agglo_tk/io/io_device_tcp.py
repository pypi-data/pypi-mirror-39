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

import socket
from select import select

from .io_device import AtkIODeviceFd
from ..exceptions import AtkTimeoutError
from ..exceptions import AtkIODeviceError
from ..trace import trace


__all__ = ["IODeviceSsh"]

class AtkIODeviceTCP(AtkIODeviceFd):
    def  __init__(self, address, port):
        super(AtkIODeviceTCP, self).__init__()

        self.__address = address
        self.__port = port
        self.__socket = None

        
    # def __del__(self):
    #     try:
    #         self.close()
    #     except AtkIODeviceError:
    #         pass


    @property        
    def fd_in(self):
        result = -1
        
        try:
            result = self.__socket.fileno()
        # Case where io device is not opened
        except AttributeError:
            pass

        return result


    @property        
    def fd_out(self):
        return self.fd_in


    # @property
    # def opened(self):
    #     return (self.fd != -1)

        
    def open(self):
        trace(trace_class="ATK", info="AtkIODeviceTcp::open " + repr(self))

        try:
            if not self.opened:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__socket.connect((self.__address, self.__port))
                self.__socket.setblocking(False)
            else:
                raise AtkIODeviceError(AtkIODeviceError.ALREADY_OPENED)
        except AtkIODeviceError:
            raise
        except:
            self.__socket = None
            raise


    def close(self):
        trace(trace_class="ATK", info="AtkIODeviceTcp::close " + repr(self))

        try:
            self.__socket.close()
            self.__socket = None
        except AttributeError:
            pass


    # def write(self, output):
    #     trace(trace_class="ATK", info="AtkIODeviceTcp::write  " + str(len(output)) + \
    #                                   " bytes on " + repr(self) + ": " + repr(read_datas))

    #     try:
    #         self.__socket.sendall(output)
    #     # Case where socket is None
    #     except AttributeError:
    #         raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)
    #     except Exception as exception:
    #         trace(trace_class="ATK", warning="AtkIODeviceTcp::write error " + str(exception))
    #         raise


    # # TODO deplacer dans une classe mere
    # def read(self, timeout_s=0):
    #     read_datas = ""
        
    #     trace(trace_class="ATK", info="AtkIODeviceTcp::read on " + repr(self))
    #     try:
    #         readable, writable, exceptional = select([self.fd], [], [], timeout_s)
    #         if readable:
    #             read_datas = self.__socket.recv(AtkIODeviceTcp.NB_BYTES_READ_AT_ONCE)
    #             trace(trace_class="ATK", info="AtkIODeviceTcp::read: " + str(len(read_datas)) + " bytes read: " + repr(read_datas))
    #         elif not writable and not exceptional:
    #             raise AtkTimeoutError
    #     except ValueError:
    #         raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)
            
    #     return read_datas
