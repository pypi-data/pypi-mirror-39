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

import logging
from os import remove


__all__ = ["trace", "set_log_level", "enable_log", "disable_log", "add_file_handler", "add_handler", "enable_handler", "disable_handler"]

handler_added = False
default_handler = None
# TODO ajouter method name/line
default_formatter = logging.Formatter('%(asctime)s::%(name)s::%(levelname)s::%(message)s')
DEFAULT_TRACE_FILE = "agglo_logs.txt"
# DEFAULT_LEVEL = logging.WARNING
DEFAULT_LEVEL = logging.INFO
ROOT_CLASS = ""


def trace(**kwargs):
    global handler_added
    trace_class = kwargs.get("trace_class", None)
    logger = _get_logger(trace_class)

    # If no handler exists (case of first trace call without previous add_handler)
    if not handler_added:
        # Create a default one
        _create_default_handler()

    # TODO plusieurs loggers, en s'assurant que le même handler ne va pas afficher plusieurs fois le log
    # loggers = [logging.getLogger(current_trace_class) for current_trace_class in trace_class.split("|")]
    
    kwargs.pop("trace_class", None)
    for level, msg in kwargs.items():
        getattr(logger, level)(msg)

        
def set_log_level(level, trace_class=ROOT_CLASS, recursive=False):
    _set_logger(level, trace_class=trace_class, recursive=recursive, \
                setter=lambda logger, level:logger.setLevel(level))
        
    
def enable_log(trace_class=ROOT_CLASS, recursive=False):
    _set_logger(trace_class=trace_class, recursive=recursive, \
                setter=lambda logger:setattr(logger, "disabled", False))


def disable_log(trace_class=ROOT_CLASS, recursive=False):
    _set_logger(trace_class=trace_class, recursive=recursive, \
                setter=lambda logger:setattr(logger, "disabled", True))


def add_file_handler(file_path, reset_file=True, trace_class=ROOT_CLASS):
    if reset_file:
        try:
            remove(file_path)
        except OSError:
            pass

    handler = logging.FileHandler(file_path)
    add_handler(handler, trace_class)

    return handler


def add_handler(handler, trace_class=ROOT_CLASS, exclusive=False):
    global default_handler
    global handler_added
    logger = _get_logger(trace_class)

    # If formatter is not specified
    if handler.formatter is None:
        # Associate default formatter to handler
        handler.setFormatter(default_formatter)

    # Associate handler to logger
    logger.addHandler(handler)
    if exclusive:
        logger.propagate = False
        
    # If this is a handler for root logger and default handler is activated
    if (trace_class == "") and (default_handler is not None) and (handler is not default_handler):
        # Remove default handler
        logging.getLogger().removeHandler(default_handler)
        default_handler = None

    # Do not create default handler in further trace calls
    handler_added = True
    
    
def enable_handler(handler):
    try:
        if handler.disable_filter:
            handler.removeFilter(handler.disable_filter)
            handler.disable_filter = None
    # Case where disable_filter doesn't exists
    except AttributeError:
        pass

    
def disable_handler(handler):
    try:
        if not handler.disable_filter:
            class DisableFilter(logging.Filter):
                def __init__(self):
                    logging.Filter.__init__(self)
                
                def filter(self, record):
                    return False
            
            disable_filter = DisableFilter()
            handler.addFilter(disable_filter)
            handler.disable_filter = disable_filter
    # Case where disable_filter doesn't exists
    except AttributeError:
        pass

        
def _create_default_handler():
    global default_handler
    
    class HasHandlerFilter(logging.Filter):
        def __init__(self):
            logging.Filter.__init__(self)
        
        def filter(self, record):
            result = True
            logger = logging.getLogger(record.name)
            ancestors_or_self = _get_ancestors(logger)
            
            for logger in ancestors_or_self:
                if ((default_handler not in logger.handlers) and (len(logger.handlers) == 1) or
                   (len(logger.handlers) >= 2)):
                    result = False
                    break
                    
            return result
            
    has_handler_filter = HasHandlerFilter()
    default_handler = add_file_handler(DEFAULT_TRACE_FILE)
    default_handler.addFilter(has_handler_filter)

            
def _set_logger(*args, **kwargs):
    trace_class = kwargs.get("trace_class", None)
    recursive = kwargs.get("recursive", False)
    setter = kwargs.get("setter")

    # Retrieve logger and execute setter function on it
    logger = _get_logger(trace_class)
    setter(logger, *args)

    # If recursivity is set
    if recursive:
        # Recursively apply setter to all children
        for child in logger.children:
            _set_logger(*args, trace_class=child.name, recursive=True, setter=setter)

        
def _get_ancestors(logger, or_self=True, propagate_only=True):
    ancestors = []

    if or_self:
        ancestors = [logger]
    if (logger.parent is not None) and (logger.propagate or not propagate_only):
        ancestors += _get_ancestors(logger.parent)
        
    return ancestors


def _get_logger(trace_class):
    # If trace class is not specified
    if trace_class is None:
        # TODO sur ? on utilise pas plutot root logger, le formatter contient le calling module, eventuellement des filter si on veut filtrer les logs par module ?
        # Use calling module as trace class
        trace_class = _get_calling_module()

    # Get existing or new logger
    logger = logging.getLogger(trace_class)

    # If logger has just been created
    if logger.level == logging.NOTSET:
         logger.setLevel(DEFAULT_LEVEL)
    
    return logger


def _get_calling_module():
    # TODO return __name__
    return ROOT_CLASS
