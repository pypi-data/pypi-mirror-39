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

from select import select
from os import write
from os import read

from ..exceptions import AtkTimeoutError
from ..exceptions import AtkIODeviceError

from ..trace import trace


class AtkIODevice(object):

    NB_BYTES_READ_AT_ONCE = 1024

    def __init__(self):
        self.encoding = "utf-8"

    @property
    def opened(self):
        raise NotImplementedError


    def open(self):
        raise NotImplementedError


    def close(self):
        raise NotImplementedError


    def write(self, output):
        raise NotImplementedError


    def read(self, timeout_s=0):
        raise NotImplementedError


class AtkIODeviceFd(AtkIODevice):

    def __init__(self):
        super(AtkIODeviceFd, self).__init__()


    @property
    def fd(self):
        return self.fd_in


    @property
    def opened(self):
        return (self.fd_in != -1) and (self.fd_out != -1)


    def write(self, output):
        trace(trace_class="ATK", info="AtkIODevice::write  " + str(len(output)) + \
                                      " bytes on " + str(id(self)) + ": " + repr(output))

        try:
            if self.encoding is not None:
                output = output.encode(self.encoding)
            write(self.fd_out, output)
        # Case where fd_out is not opened
        except OSError as exception:
            if (exception.errno == 9):
                raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)
            else:
                trace(trace_class="ATK", warning="AtkIODevice::write error " + str(exception))
                raise
        except Exception as exception:
            trace(trace_class="ATK", warning="AtkIODevice::write error " + str(exception))
            raise


    def read(self, timeout_s=0):
        read_datas = ""
        
        trace(trace_class="ATK", info="AtkIODevice::read on " + repr(self))
        try:
            readable, writable, exceptional = select([self.fd_in], [], [], timeout_s)

            if readable:
                read_datas = read(self.fd_in, AtkIODevice.NB_BYTES_READ_AT_ONCE)
                if self.encoding is not None:
                    read_datas = read_datas.decode(self.encoding)
                trace(trace_class="ATK", info="AtkIODevice::read: " + str(len(read_datas)) + \
                                              " bytes read: " + repr(read_datas))
            elif not writable and not exceptional:
                raise AtkTimeoutError
        except OSError as exception:
            if (exception.errno == 9):
                raise AtkIODeviceError(AtkIODeviceError.NOT_OPENED)
            else:
                trace(trace_class="ATK", warning="AtkIODevice::read error " + str(exception))
                raise
        except Exception as exception:
            trace(trace_class="ATK", warning="AtkIODevice::read error " + str(exception))
            raise
            
        return read_datas
