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

import re
import time


__all__ = ["AccCliIOParser"]

class AccCliIOParser():
    
    def __init__(self, cli_io_handler, default_prompt_reg_expr):
        self.__cli_io_handler = cli_io_handler
        self.__prompt_reg_expr = set()
        self.__async_reg_expr = set()
        self.resetParsing()
        
        self.add_reg_expr(prompt_reg_expr=default_prompt_reg_expr)


    def resetParsing(self):
        self.__first_prompt_received = False
        self.__state_wait_command = False
        self.__unparsed_data = ""
    
    
    def add_reg_expr(self, **kwargs):
        prompt_reg_expr = kwargs.get("prompt_reg_expr")
        async_reg_expr = kwargs.get("async_reg_expr")

        if prompt_reg_expr is not None:
            self.__prompt_reg_expr.add(prompt_reg_expr)
        if async_reg_expr is not None:
            self.__async_reg_expr.add(async_reg_expr)


    def remove_reg_expr(self, **kwargs):
        prompt_reg_expr = kwargs.get("prompt_reg_expr")
        async_reg_expr = kwargs.get("async_reg_expr")

        if prompt_reg_expr is not None:
            if (len(self.__prompt_reg_expr) > 1):
                self.__prompt_reg_expr.remove(prompt_reg_expr)
            else:
                if prompt_reg_expr in self.__prompt_reg_expr:
                    raise ValueError
                else:
                    raise KeyError(prompt_reg_expr)

        if async_reg_expr is not None:
            self.__async_reg_expr.remove(async_reg_expr)

        
    def parse(self, _input):
        datas = self.__unparsed_data + _input
        lines = datas.splitlines(True)
        match = None
        unparsed_datas = ""
        
        # Parse datas (previously unparsed + received)
        for i, current_line in enumerate(lines):

            unparsed_datas = current_line
            _continue = True
            while (_continue):
                
                # TODO utiliser une liste d'objet IOParserAsync,IOParserPrompt... et iterer dessus
                # Match the current line with various regexpr
                match = self.__check_new_asynchronous_io(unparsed_datas)
                if not match:
                    match = self.__check_new_prompt(unparsed_datas)
                if not match:
                    match = self.__check_new_command(unparsed_datas)
                if not match:
                    match = self.__check_new_partial_command_result(unparsed_datas)

                # If there is a match
                _continue = (match is not None)
                if _continue:
                    # If there remains unmatched characters in the current line, keep matching
                    unparsed_datas = unparsed_datas[:match.start()] + unparsed_datas[match.end():]
                    _continue = ("" != unparsed_datas)
            
        # If the last line is not completely parsed and does'n't end with \n, save it for further parse
        self.__unparsed_data = unparsed_datas if ("\n" != lines[-1][-1]) else ""
      
            
    def __check_new_prompt(self, data):
        match = None

        if (self.__is_running_command() or not self.__first_prompt_received):

            for sCurrentRegExpr in self.__prompt_reg_expr:
                match = re.search(sCurrentRegExpr, data)
                if match:
                    break
            
        if match:
            self.__handle_new_prompt(data[match.start():match.end()])
        
        return (match)

        
    def __handle_new_prompt(self, asNewPrompt):
        self.__cli_io_handler.handle_new_prompt(asNewPrompt)
        self.__state_wait_command = True
        self.__first_prompt_received = True

        
    def __check_new_command(self, data):
        match = None

        if (not self.__is_running_command() and  self.__first_prompt_received):
            # There is no way to distinct an incomplete command from an incomplete asynch IO
            # Therefore, we need to receive the complete command (with \n) before recognizing 
            # a command.
            match = re.search(".*\n", data)
            
        if match:
            self.__handle_new_command(data[match.start():match.end()])
        
        return (match)
        
        
    def __handle_new_command(self, new_command):
        self.__cli_io_handler.handle_new_command(new_command)
        self.__state_wait_command = False

        
    def __check_new_asynchronous_io(self, data):
        match = None

        for sCurrentRegExpr in self.__async_reg_expr:
            match = re.search(sCurrentRegExpr, data)
            if match:
                break
            
        if match:
            self.__handle_new_asynchronous_io(data[match.start():match.end()])
        
        return (match)
    

    def __handle_new_asynchronous_io(self, new_async_io):
        self.__cli_io_handler.handle_new_asynchronous(new_async_io)

        
    def __check_new_partial_command_result(self, data):
        match = None

        # TODO gerer le cas du welcome dans une methode a part
        if (not self.__first_prompt_received):
            match = re.search(".*\n", data)
            # TODO gerer pour que le welcome se retrouve dans une seule entree IOLogs
            # No need to add match in IOTYPE_LOGS, it will be done by parse() if match is not None
        elif (self.__is_running_command()):
            # \n must be included in reg expr, otherwise an incomplete prompt 
            # or async would be seen as a partial command result
            match = re.search(".*\n", data)
            if match:
                self.__handle_new_partial_command_result(data[match.start():match.end()])
        
        return (match)
    
    
    def __handle_new_partial_command_result(self, new_partial_command_result):
        self.__cli_io_handler.handle_new_command_result(new_partial_command_result)

        
    # TODO cette methode est elle bien necessaire ?
    def __is_running_command(self):
        return (not self.__state_wait_command and self.__first_prompt_received)

        