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
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA, OR
## PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
## AGGLO_END_LICENSE
##
############################################################################

from threading import Thread
from time import sleep
import socket
from select import select
from socketserver import TCPServer
from socketserver import BaseRequestHandler

from agglo_tk.trace import trace


__all__ = ["DEFAULT_MIRROR_TCP_PORT", "AtkMirroringServer"]

DEFAULT_MIRROR_TCP_PORT = 22222

# TODO attraper le Ctrl+C
class AtkMirroringServer(TCPServer):

    def __init__(self, port=DEFAULT_MIRROR_TCP_PORT):
        TCPServer.__init__(self, ("localhost", port), AtkMirroringServer.MirrorHandler)
        self.run = False


    class MirrorHandler(BaseRequestHandler):
        def handle(self):
            try:
                while self.server.run:
                    # TODO ca ne bloque pas sur le select, apres recv trouve 0 bytes
                    readable, writable, exceptional = select([self.request.fileno()], [], [], 0.5)
                    if readable:
                        data = self.request.recv(4096)
                        trace(trace_class="ATK_UT", info="AtkMirroringServer::received " + \
                                                         str(len(data)) + " bytes: '" + str(data) + "'")
                        self.request.sendall(data)
            except:
                pass


    def server_bind(self):
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.allow_reuse_address = True
        TCPServer.server_bind(self)


    def start(self):
        server_thread = Thread(target=self.serve_forever)

        # server_thread.dameon = True
        self.run = True
        server_thread.start()
        sleep(0.2)


    def stop(self):
        self.run = False
        self.shutdown()
        self.server_close()
