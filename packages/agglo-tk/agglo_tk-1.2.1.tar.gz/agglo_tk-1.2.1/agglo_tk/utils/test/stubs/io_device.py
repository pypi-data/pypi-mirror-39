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

import os
from select import select

from ....io.io_device import AtkIODevice
from ....exceptions import AtkIODeviceError

from ....trace import trace


class AtkStubIODevice(AtkIODevice):
    def __init__(self):
        super(AtkStubIODevice, self).__init__()

        self.pipein = -1
        self.pipeout = -1
        self.sent = ""
        self.received = ""


    @property
    def fd(self):
        return self.pipein


    @property
    def opened(self):
        return (self.pipein != -1) and (self.pipeout != -1)


    def open(self):
        if self.opened:
            raise AtkIODeviceError(AtkIODeviceError.ALREADY_OPENED)
        else:
            self.pipein, self.pipeout = os.pipe()


    def close(self):
        if self.opened:
            os.close(self.pipein)
            self.pipein = -1
            os.close(self.pipeout)
            self.pipeout = -1


    def write(self, data):
        trace(trace_class="ATK", info="AtkStubIODevice::write " + repr(data))

        try:
            self.sent = data
            if self.encoding is not None:
                data = data.encode(self.encoding)
            os.write(self.pipeout, data)
        except OSError:
            raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)


    def read(self, timeout_s=0):
        result = ""
        
        trace(trace_class="ATK", info="AtkStubIODevice::read")
        try:
            readable, writable, exceptional = select([self.fd], [], [], timeout_s)
            if readable:
                result = os.read(self.pipein, 1024)
                if self.encoding is not None:
                    result = result.decode(self.encoding)
                trace(trace_class="ATK", info="AtkStubIODevice::read: " + str(len(result)) + " bytes read: " + repr(result))
                self.received = result
            elif not writable and not exceptional:
                raise AtkTimeoutError
        except ValueError:
            raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)

        return result
