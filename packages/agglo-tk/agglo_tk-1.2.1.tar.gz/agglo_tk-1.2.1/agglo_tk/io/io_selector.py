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

from ..selector import AtkSelector
from ..trace import trace


__all__ = ["AtkIOSelector"]

class AtkIOSelector(AtkSelector):

    def select(self, iterable, **kwargs):
        result = []

        # TODO envoyer une map io_type, liste d'io selectionne ?
        try:
            # Assume iterable is an AtkIOLogs instance (we can not import AtkIOLogs so we need to do it that way)
            # Check that iterable has the correct io_type if io_type is a selection criteria
            if (self.io_type == iterable.io_type) or (self.io_type is None):
                # Convert negative first and last rank in positive values
                converter = self.criteria.convert_negative_ranks(len(iterable))
                next(converter)

                # TODO remplacer self.ranks par indexes
                result = super(AtkIOSelector, self).select(iterable[self.ranks], io_type=iterable.io_type, **kwargs)

                # Restore first and last rank initial values
                try:
                    next(converter)
                except StopIteration:
                    pass
                    
        # Case where iterable is an AtkIOConnectionLogs instance
        except AttributeError as exception:
            # If io_type is a selection criteria 
            if self.io_type is not None:
                try:
                    # Select ios only in corresponding io_logs
                    result = self.select(iterable[self.io_type], **kwargs)
                # Case where there is no io_logs of type io_type in AtkIOConnectionLogs iterable
                except KeyError:
                    pass
            # If io_type is not a selection criteria 
            else:
                # Iterate on all io_logs of iterable
                for io_logs in iterable:
                    # TODO utiliser un merge pour avoir les io tries chronologiquement
                    result.extend(self.select(io_logs))
                    

        return result
