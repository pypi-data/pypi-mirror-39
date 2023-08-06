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

import select

from scapy.config import conf
from scapy.data import ETH_P_ALL
from scapy.all import L3RawSocket
# from scapy.arch.linux import L2Socket
# from scapy.arch.linux import L3PacketSocket
# from scapy.arch.linux import L2ListenSocket
# from scapy.all import send
# from scapy.all import recv

from ..io_device import AtkIODeviceFd
from ...exceptions import AtkTimeoutError
from ...exceptions import AtkIODeviceError
from ...trace import trace


__all__ = ["OSI_LAYER2", "OSI_LAYER3", "AtkIODeviceScapy"]

OSI_LAYER2 = 0
OSI_LAYER3 = 1

# TODO supprimer cet heritage des que IOHub cesse d'utiliser des FDDevice (plutot des worker/asyncio)
class AtkIODeviceScapy(AtkIODeviceFd):

    NB_BYTES_READ_AT_ONCE = 1514
    loopback_itfs = ["lo"]

    def  __init__(self, itf_name, osi_layer=OSI_LAYER3):
        if (osi_layer != OSI_LAYER2) and (osi_layer != OSI_LAYER3):
            raise ValueError("Invalid OSI layer: use either OSI_LAYER2 or OSI_LAYER3")
        if (osi_layer == OSI_LAYER2) and (itf_name == AtkIODeviceScapy.loopback_itfs):
            raise ValueError("Invalid OSI layer: use OSI_LAYER3 for loopback interface")

        super(AtkIODeviceScapy, self).__init__()
        self.__itf_name = itf_name
        self.__osi_layer = osi_layer
        self.__scapy_input = None
        self.__scapy_output = None
        self.fd_in = -1
        self.fd_out = -1

    @property        
    def itf_name(self):
        return self.__itf_name


    @property        
    def osi_layer(self):
        return self.__osi_layer

        
    # def __del__(self):
    #     if (self.opened()):
    #         self.close()


    # @property        
    # def fd_in(self):
    #     result = -1
        
    #     try:
    #         result = self.__scapy_input.fileno()
    #     # Case where io device is not opened
    #     except AttributeError:
    #         pass

    #     return result


    # @property        
    # def fd_out(self):
    #     result = -1
        
    #     try:
    #         result = self.__scapy_output.fileno()
    #     # Case where io device is not opened
    #     except AttributeError:
    #         pass

    #     return result


    # @property
    # def opened(self):
    #     return ((self.__scapy_input is not None) and (self.__scapy_output is not None))

        
    def open(self):
        trace(trace_class="ATK", info="AtkIODeviceScapy::open " + self.itf_name)

        try:
            if not self.opened:
                if (self.osi_layer == OSI_LAYER2):
                    # self.__scapy_input = L2ListenSocket(iface=self.itf_name, type=ETH_P_ALL)
                    self.__scapy_output = conf.L2Socket(iface=self.itf_name, type=ETH_P_ALL)
                else:
                    cls_l3_socket = conf.L3socket
                    
                    # If io device works on local loop
                    if (self.itf_name in self.loopback_itfs):
                        # We gonna need a raw socket in this special case
                        cls_l3_socket = L3RawSocket

                    # Allocate layer 3 socket
                    self.__scapy_output = cls_l3_socket(iface=self.itf_name, type=ETH_P_ALL)
                # TODO a supprimer
                self.__scapy_input = self.__scapy_output
                    
                self.fd_in = self.__scapy_input.fileno()
                self.fd_out = self.__scapy_output.fileno()
            else:
                raise AtkIODeviceError(AtkIODeviceError.ALREADY_OPENED)
        except AtkIODeviceError:
            raise
        except:
            self.__scapy_input = None
            self.fd_in = -1
            self.__scapy_output = None
            self.fd_out = -1
            raise


    def close(self):
        trace(trace_class="ATK", info="AtkIODeviceScapy::close " + self.itf_name)

        self.__scapy_input = None
        self.fd_in = -1
        self.__scapy_output = None
        self.fd_out = -1


    def write(self, output):
        for packet in output:
            trace(trace_class="ATK", info="AtkIODeviceScapy::write: send " + repr(packet))
            self.__scapy_output.send(packet)
        # super(AtkIODeviceScapy, self).write(str(output))


    def read(self, timeout_s=0):
        result = None
        found = False

        # TODO implementer le timeout
        while not found:
            result = self.__scapy_input.recv()
            found = result is not None

        trace(trace_class="ATK", info="AtkIODeviceScapy::read received " + repr(result))
        # TODO renvoyer le ACK
        # if TCP in result:
        #     if result[TCP].len:
        #         ack = TCP()
        #         self.write()

        return result
        # TODO conversion au format scapy
        # return super(AtkIODeviceScapy, self).read()


    # def write(self, output):
    #     trace(trace_class="ATK", info="AtkIODeviceScapy::write  " + str(len(output)) + \
    #                                   " bytes on " + self.name + ": " + repr(read_datas))

    #     try:
    #         self.__scapy_output.send(ascaFrame)
    #     # Case where scapy output is None
    #     except AttributeError:
    #         raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)
    #     except Exception as exception:
    #         trace(trace_class="ATK", warning="AtkIODeviceScapy::write error " + str(exception))
    #         raise


    # def read(self, timeout_ms=0):
    #     # pyReadData = None
        
    #     # if (self.opened()):
    #     #     readable, writable, exceptional = select.select([self.__scapy_input.fileno()], [], [], timeout_ms)
    #     #     if (len(readable) > 0):
    #     #         pyReadData = self.__scapy_input.recv(CatcIODeviceEthernet.NB_BYTES_READ_AT_ONCE)
                
    #     # return pyReadData


    #     read_datas = ""
        
    #     trace(trace_class="ATK", info="AtkIODeviceScapy::read on " + self.name)
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
