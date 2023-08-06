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
## TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, io_DATA, OR
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
## AGGLO_END_LICENSE
##
############################################################################

from .. import AtkIOCriteria


__all__ = ["AtkIOScapyCriteria"]

class AtkIOScapyCriteria(AtkIOCriteria):
    def match_field(self, io_data, protocol, field=None, value=None, **kwargs):
        ''' 
        Use Case : 
        crit.match_field(io_data, TCP, "sport", 22) <=> TCP in io_data and io_data[TCP].sport == 22
        crit.match_field(io_data, TCP, sport=22) <=> TCP in io_data and io_data[TCP].sport == 22
        crit.match_field(io_data, "protocol", sport=22) <=> crit.protocol in io_data and io_data[crit.protocol].sport == 22
        crit.match_field(io_data, TCP, "dst") <=> TCP in io_data and io_data[TCP].sport == crit.sport
        crit.match_field(io_data TCP, "matched_field", 22) <=> TCP in io_data and getattr(io_data[TCP], crit.matched_field) == 22
        crit.match_field(io_data, TCP, "sport", "expected_sport") <=> TCP in io_data and io_data[TCP].sport == crit.expected_sport
        crit.match_field(io_data, "protocol", "matched_field", "expected_value") <=> crit.protocol in io_data and getattr(io_data[crit.protocol], crit.matched_field) == crit.expected_value
        '''
        # If protocol is a boundary name, retrieve boundary value, else return 
        # protocol parameter (supposed to be a scapy protocol class)
        protocol = self.boundaries.get(protocol, protocol)

        # If field name and values are not given in default arg
        if (field is None) and (value is None):
            # Field name and value are the first keyword argRetrieve
            field = list(kwargs)[0]
            value = list(kwargs.values())[0]
        else:
            # If value is not given
            if value is None:
                # value is the field boundary value
                value = self.boundaries[field]
            else:
                # field and value are either boundaries name containing actual field/value, or directly field/value to be used
                value = self.boundaries.get(value, value)
                field = self.boundaries.get(field, field)

        return (protocol in io_data) and (getattr(io_data[protocol], field) == value)

