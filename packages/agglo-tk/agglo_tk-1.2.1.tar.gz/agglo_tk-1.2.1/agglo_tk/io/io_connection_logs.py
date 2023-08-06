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

from copy import copy as clone

from .io_logs import AtkIOLogs
from .io_selector import AtkIOSelector
from ..selector.criteria import AtkCriteria


__all__ = ["AtkIOConnectionLogs"]

class AtkIOConnectionLogs():

    def __init__(self, *args):
        self.__io_logs = {}

        # TODO remplacer le systeme de callback par un listener generique, pouvant filter les notif avec event matchant selector associe au listener
        self.__callbacks = {}

        for io_type in args:
            self.add_io_logs(io_type)


    def __iter__(self):
        for io_logs in self.__io_logs.values():
            yield io_logs

        
    def __getitem__(self, value):
        result = []

        # If value is an instance of AtkCriteria
        if isinstance(value, AtkCriteria):
            # Build a selector using criteria
            io_selector = AtkIOSelector(value)

            # Select ios with this selector
            result = io_selector.select(self)
        else:
            # Assume value is an io_type
            result = self.__io_logs[value]
        
        return result


    def add_io_logs(self, io_type, owner=None):
        unique_io_type = self.__get_unique_io_type(io_type, owner)

        if unique_io_type in self.__io_logs:
            raise ValueError

        io_logs = AtkIOLogs(unique_io_type)
        self.__io_logs[unique_io_type] = io_logs

        return io_logs


    def get_io_type(self, io_type, owner):
        unique_io_type = self.__get_unique_io_type(io_type, owner)

        if unique_io_type not in self.__io_logs:
            raise IndexError

        return unique_io_type


    def check(self, io_criteria, **kwargs):
        io_selector = AtkIOSelector(io_criteria)

        return io_selector.check(self, **kwargs)


    def __get_unique_io_type(self, io_type, owner):
        owner_name = "" if owner is None else owner.name + "_"
        
        return owner_name + io_type


    def add_callback(self, io_criteria, callback, nb_occurrences=-1):
    
        callbacks = self.__callbacks.setdefault(io_criteria, [])
        
        for current_callback in callbacks:
            if (current_callback[0] == callback):
                callbacks.remove(current_callback)
                break
                    
        callbacks.append((callback, nb_occurrences))

        
    def remove_callback(self, io_criteria, callback):
        callbacks = self.__callbacks.get(io_criteria, [])
        
        for current_callback in callbacks:
            if (current_callback[0] == callback):
                callbacks.remove(current_callback)
                break
        
        if callbacks:
            self.__callbacks.pop(io_criteria, None)    


    def execute_callbacks(self):
        # Iterate on selectors associated to end user callback
        for io_criteria in self.__callbacks:
            # Notify end user of io reception
            self.__execute_callbacks(io_criteria, -1)

            
    def __execute_callbacks(self, io_criteria, rank):
        last_io_criteria = clone(io_criteria)
        # TODO c'est pas bon : il faut que rank soit entre first et last
        last_io_criteria.first_rank = rank
        
        # If selector matches last received entry
        if (self.check(last_io_criteria)):
            # Iterate on all end user callbacks associated to current selector
            for callback, nb_occurrences in self.__callbacks[io_criteria]:
                # Notify end user
                callback(self[io_criteria.io_type][rank])
            
                # If end user expects other entries
                if (nb_occurrences > 1):
                    # Decrement number of expected entries
                    self.add_callback(io_criteria, callback, nb_occurrences - 1)
                # If received entry is the last expected
                elif (1 == nb_occurrences > 1):
                    # TODO notifier l'utilisateur
                    # Remove callback 
                    self.remove_callback(io_criteria, callback)
                # No limitation on number of expected entries: do nothing
                # else (-1 == nb_occurrences)
        # TODO si le selecteur ne peut plus matcher, supprimer les callbacks et notifier l'utilisateur
        #else if wont match anymore


    # TODO ce serait bien de retrouver le resultat correspondant a une commande
    # de maniere generale, la generation automatique de commande ne facilite pas l'inspection des resultats : quand 
    # on genere 5 commandes d'un coup, sans meme savoir ce qu'on genere (ex serialization), comment checker que les
    # resultats sont corrects (startTime peut etre?
    # def __select(self, io_criteria):
    #     return self._io_logs[io_criteria.io_type].select(io_criteria, self)
    
    
    # def select_related(self, io_criteria, aui_new_io_type):
    #     # TODO selectionner sur la base des io matchant le selecteur les io correspondantes dans le nouveau type de donnees
    #     pass
