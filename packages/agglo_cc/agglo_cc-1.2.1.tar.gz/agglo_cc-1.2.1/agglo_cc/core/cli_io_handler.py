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

from agglo_tk.friend import friend
from agglo_tk.friend import has_friends

from .._private.cli_io_parser import AccCliIOParser
from .cli_io_types import *


__all__ = ["AccCliInputHandler"]

DEFAULT_PROMPT_REG_EXPR = ".*>"

# TODO separer en 2, CliIOHandler|CliIOLogger(CliIOHandler) ?
@has_friends
class AccCliInputHandler():

    def __init__(self, cli_io_logs, prompt_reg_expr=DEFAULT_PROMPT_REG_EXPR):
        self.__cli_io_logs = cli_io_logs
        self.__cli_io_parser = AccCliIOParser(self, prompt_reg_expr)
        # TODO comment reseter le parser sur 2 open successif ?


    def add_parser_reg_expr(self, **kwargs):
        self.__cli_io_parser.add_reg_expr(**kwargs)

        
    def remove_parser_reg_expr(self, **kwargs):
        self.__cli_io_parser.remove_reg_expr(**kwargs)


    def handle_input(self, data):
        # Parse received datas to extract prompt, commands...
        self.__cli_io_parser.parse(data)


    @friend("AccCliIOParser")
    def __handle_new_prompt(self, prompt):
        self.__add_cli_io(IO_TYPE_CLI_PROMPT, prompt)


    @friend("AccCliIOParser")
    def __handle_new_command(self, command):
        self.__add_cli_io(IO_TYPE_CLI_COMMAND, command)


    @friend("AccCliIOParser")
    def __handle_new_command_result(self, command_result):
        self.__add_cli_io(IO_TYPE_CLI_COMMAND_RESULT, command_result)


    @friend("AccCliIOParser")
    def __handle_new_asynchronous(self, async_input):
        self.__add_cli_io(IO_TYPE_CLI_ASYNC, async_input)


    def __add_cli_io(self, io_type, data):
        # TODO est-ce qu'il faudrait pas faire ca pour prompt plutot (nouveau prompt=>nouvelle commande + result)?
        # If io is not a result
        if (io_type != IO_TYPE_CLI_COMMAND_RESULT):
            # Create the entry
            self.__cli_io_logs[io_type].add_io(data)
            
            # If received entry is a command
            if (io_type == IO_TYPE_CLI_COMMAND):
                # Create corresponding result entry at the same time
                self.__cli_io_logs[IO_TYPE_CLI_COMMAND_RESULT].add_io("")
                
        # If io is a result
        else:
            # Result entry has been created at the same time than corresponding command
            # Simply append existing entry
            self.__cli_io_logs[IO_TYPE_CLI_COMMAND_RESULT].append_last_io(data)
