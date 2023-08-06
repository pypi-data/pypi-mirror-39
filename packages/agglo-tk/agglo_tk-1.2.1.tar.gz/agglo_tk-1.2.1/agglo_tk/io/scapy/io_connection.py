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

import subprocess
from time import sleep
from random import randint

from scapy.all import Ether
from scapy.all import IP
from scapy.all import TCP

from ..io_connection import AtkIOConnection
from .io_device import AtkIODeviceScapy
from .io_device import OSI_LAYER2
from .io_device import OSI_LAYER3
from .io_criteria import AtkIOScapyCriteria
from ...exceptions import AtkTimeoutError
from ...trace import trace


__all__ = ["AtkIOConnectionScapy"]

# TODO cette classe n'est pas en capacite de logger sur tout tout ce qui sort de l'interface, mais uniquement ce qui est ecrit via io_device.send()
# Il faudrait modifier cette classe, ou au moins son heritage dans ATC
class AtkIOConnectionScapy(AtkIOConnection):

    DEFAULT_TCP_TIMEOUT_MS = 2000

    def __init__(self, itf_name, io_logs=None, io_hub=None, osi_layer=OSI_LAYER3):
        super(AtkIOConnectionScapy, self).__init__(itf_name, AtkIODeviceScapy(itf_name, osi_layer), io_logs, io_hub)
        self.__opened_tcp = {}

        
    def __del__(self):
        for tcp_ports in self.__opened_tcp:
            self.close_tcp(tcp_ports)

            
    # def handle_input(self, io_device, data):
    #     # TODO check que io device est le meme que self.io device, factorise dans io connection
    #     pass
        

    def open_tcp(self, ip_addr, remote_port, local_port=None, timeout_ms=DEFAULT_TCP_TIMEOUT_MS):
        if local_port is None:
            local_port = randint(1024,65535)

        trace(trace_class="ATK", info="AtkIOConnectionScapy::open TCP session with {}, local_port={} remote_port={}"\
                                       .format(ip_addr, local_port, remote_port))

        ip = IP(dst=ip_addr)
        def match_syn_ack(crit, io_data):
            tcp = io_data.getlayer(TCP)
            return tcp and (tcp.flags == 18) and (tcp.dport == local_port) and (tcp.sport == remote_port)
        syn_ack_criteria = AtkIOScapyCriteria(io_type=self.io_type_input, match_io_data=match_syn_ack)

        # Configure ip tables to empeach kernel to reset the connection we're opening
         # --tcp-flags RST RST
        # TODO gestion seq/ack automatique : https://isc.sans.edu/forums/diary/TCP+Fuzzing+with+Scapy/14080/
        subprocess.check_output(args=["iptables", "--table", "raw", "--append", "PREROUTING", 
                                      "--protocol", "tcp", "--dport", str(local_port), "--jump", "DROP"])
        sleep(0.1)
        
        try:
            # Send SYN frame
            # TODO ce serait pas mal from_current_tail(self.input) ?
            syn_ack_criteria.from_now(timeout_ms).from_current_tail(self.io_logs[self.io_type_input])
            self.send_ip(ip/TCP(sport=local_port, dport=remote_port, flags="S", seq=0))

            # Wait for SYN_ACK frame
            syn_ack = self.wait_io(syn_ack_criteria).data

            # Send ACK frame
            ack = ip/TCP(sport=local_port, dport=remote_port, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
            self.send_ip(ack)
        except:
            subprocess.check_output(args=["iptables", "--table", "raw", "--delete", 
                                          "PREROUTING", "--protocol", "tcp", "--dport", 
                                          str(local_port), "--jump", "DROP"])
            raise

        # Register TCP connection
        self.__opened_tcp[local_port, remote_port] = ip_addr

        return ack


    def close_tcp(self, tcp_ports, timeout_ms=DEFAULT_TCP_TIMEOUT_MS):
        local_port, remote_port = tcp_ports
        ip_addr = self.__opened_tcp[tcp_ports]
        def match_last_received_tcp(crit, io_data):
            tcp = io_data.getlayer(TCP)
            return tcp and (tcp.dport == local_port) and (tcp.sport == remote_port)
        def match_fin_ack(crit, io_data):
            return match_last_received_tcp(crit, io_data) and (io_data[TCP].flags == 16)
        tcp_criteria = AtkIOScapyCriteria(io_type=self.io_type_input, match_io_data=match_last_received_tcp)
        last_tcp = self.io_logs.check(tcp_criteria, nb_occurrences=1, reverse=True).data

        trace(trace_class="ATK", info="AtkIOConnectionScapy::close TCP session with {}, local_port={} remote_port={}"\
                                       .format(ip_addr, local_port, remote_port))
        ip = IP(dst=ip_addr)
        remove_tcp = (timeout_ms <= 0)
        
        # Send FIN frame
        tcp_criteria.change_behavior(match_io_data=match_fin_ack)
        tcp_criteria.from_now(timeout_ms).from_current_tail(self.io_logs[self.io_type_input])
        self.send_ip(ip/TCP(sport=local_port, dport=remote_port, flags="FA", seq=last_tcp.ack, ack=last_tcp.seq+1))

        try:
            # Wait for FIN_ACK frame
            fin_ack = self.wait_io(tcp_criteria).data
            remove_tcp = True

            # Send ACK frame
            ack = ip/TCP(sport=local_port, dport=remote_port, flags="A", seq=fin_ack.ack, ack=fin_ack.seq + 1)
            self.send_ip(ack)
        # Case where RST_ACK was not received
        except AtkTimeoutError:
            if timeout_ms > 0:
                raise
        finally:
            # Remove tcp ports from iptables
            if remove_tcp and (tcp_ports in self.__opened_tcp):
                subprocess.check_output(args=["iptables", "--table", "raw", "--delete", 
                                              "PREROUTING", "--protocol", "tcp", "--dport", 
                                              str(local_port), "--jump", "DROP"])
                del self.__opened_tcp[tcp_ports]


    # TODO
    # def send_tcp(self, tcp_frame):
    #     if tcp_frame.payload:
    #         tcp_frame.flags += "P"



    def send_ip(self, ip_frame):
        if (self._io_device.osi_layer == OSI_LAYER2):
            self.send(Ether()/ip_frame)
        else:
            self.send(ip_frame)


# class AtkIOConnectionCAN(AtkIOConnection):

#     def __init__(self, io_hub=None, can_io_handler=None):
#         if can_io_handler is None:
#             can_io_handler = AtkIOHandlerCAN()
#         super(AtkIOConnectionCAN, self).__init__(AtkIODeviceCAN(), can_io_handler, io_hub)
