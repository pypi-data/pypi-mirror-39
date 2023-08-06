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

from pytest import fixture

from ...io import AtkIOCriteria
from ...io.io_selector import AtkIOSelector
from ...io.io_dumper_txt import AtkIODumperTxt
from .mirroring_server import *


__all__ = ["pytest_plugins", "mirroring_server", "dump", "dump_failed"]

pytest_plugins = "agglo_tk.utils.test.add_report_plugin"

@fixture
def mirroring_server(request):
    server = AtkMirroringServer()

    server.start()

    def close():
        server.stop()
    request.addfinalizer(close)

    return server

    
@fixture
def dump(request):
    class dumper():
        def __init__(self):
            self.io_logs = None

    
    def dump_any():
        # TODO sortir une trace d'execution avec le path du fichier
        io_dumper = AtkIODumperTxt("dump_" + request.function.__name__ +".txt", 
                                   request.dumper.io_logs, AtkIOCriteria())

        # Dump IOLogs in a text file
        io_dumper.start(False)
        request.dumper.io_logs = None
        
    request.addfinalizer(dump_any)
    
    request.dumper = dumper()
    return request.dumper


# TODO mettre autouse=True
@fixture
def dump_failed(request):
    class dumper:
        pass

    def dump():
        # TODO sortir une trace d'execution avec le path du fichier
        try:
            if request.node.report_call.failed:
                io_dumper = AtkIODumperTxt("dump_" + request.function.__name__ +".txt", 
                                           request.dumper.io_logs, AtkIOCriteria())

                # Dump IOLogs in a text file
                io_dumper.start(False)
                del request.dumper.io_logs
        # Case where report_call was not found
        except AttributeError as exception:
            if exception.message == "dumper instance has no attribute 'io_logs'":
                helper_msg = ": set io_logs attribute on dump_failed fixture"
            else:
                helper_msg = ": when using dump_failed fixture, the whole module content should be imported: 'from agglo_tk.utils.test.fixtures import*'"
            
            raise AttributeError(exception.message + helper_msg)

    request.addfinalizer(dump)

    request.dumper = dumper()
    return request.dumper
