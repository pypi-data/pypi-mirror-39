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
## Software or, alternatively, in accordance with the terms containeded in 
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

from pathlib2 import Path

from .criteria import AtkCriteria


__all__ = ["AtkCriteriaPath"]

class AtkCriteriaPath(AtkCriteria):
    '''Criteria checking if a given data belongs to a path'''

    def __init__(self, recursive=True, **kwargs):
        '''path: directory path, can be relative. Can contain wildcards. Can be unexisting'''
        # TODO ajouter property ancestor
        super(AtkCriteriaPath, self).__init__(**kwargs)
        self.recursive = recursive
        self.or_self = True


    def _match(self, data):
        # TODO corriger pour accepter relative and wildcards
        '''data: file or directory path, must be absolute. Can not contain wildcard. Can be unexisting'''

        result = False
        boundary = self.boundary
        is_file = False
        data_abs = Path(data).absolute()

        # Convert relative path in absolute. Works even if data directory doesn't exist
        if is_file or not self.or_self:
            data_abs = data_abs.parent

        # Resolve wildcards if any
        if "*" in boundary:
            boundaries = [matching_dir.absolute()() for matching_dir in Path("").glob(boundary)]
            boundaries = [matching_dir for matching_dir in boundaries if not matching_dir.isfile()]
        else:
            boundaries = [Path(boundary).absolute()]

        # Try to find data in matching directories
        result = (data_abs in boundaries)

        # If not found and recursive search is activated
        if not result and self.recursive:
            parents = [parent for parent in boundaries if data_abs.as_posix().startswith(parent.as_posix() + "/")]
            result = bool(parents)

        return result
