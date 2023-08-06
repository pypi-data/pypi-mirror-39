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

from serial import Serial


__all__ = ["IODeviceSerial"]

class IODeviceSerial():

    NB_BYTES_READ_AT_ONCE = 1024
    
    def  __init__(self, as_port, aui_baudrate):
        self.__s_port = as_port
        self.__ui_baudrate = aui_baudrate
        self.__py_serial = None

        
    def __del__(self):
        if (self.isOpen()):
            self.close()

        
    def open(self):
        b_res = (not self.isOpen())

        if (b_res):
            try:
                self.__py_serial = Serial(port=self.__s_port, baudrate=self.__ui_baudrate, timeout=self.__timeout)
                b_res = self.isOpen()
            except:
                self.__py_serial = None
                b_res = False
            
        return b_res


    def close(self):
        b_res = self.isOpen()

        if (b_res):
            self.__py_serial.close()
            self.__py_serial = None

        return b_res


    def isOpen(self):
        return ((self.__py_serial is not None ) and (self.__py_serial.isOpen()))


    def write(self, as_output):
        b_res = self.isOpen()
        
        if (b_res):
            try:
                self.__py_serial.write(as_output)
                b_res = True
            except:
                b_res = False
            
        return b_res


    def read(self, ai_timeout_ms=0):
        sReadData = ""
        
        if (self.isOpen()):
            readable, writable, exceptional = select.select([self.__py_serial.fileno()], [], [], ai_timeout_ms)
            if (len(readable) > 0):
                sReadData = self.__py_serial.recv(NB_BYTES_READ_AT_ONCE)
            
        return sReadData
            
