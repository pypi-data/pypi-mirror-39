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

from agglo_tk.io import AtkIOConnection
from agglo_tk.io import AtkIOStringCriteria
from agglo_tk.trace import trace

from agglo_tk.exceptions import AtkSelectorError
from ..exceptions import AccError
from ..exceptions import AccExecutionError

from .menu_navigator import AccMenuNavigator
from .menu_path import AccMenuPath
from .cli_io_handler import IO_TYPES_CLI
from .cli_io_handler import AccCliInputHandler
from .command_results import *
from ..utils.script_recorder import AccScriptRecorder


__all__ = ["WAIT_TIMEOUT_MS", "AccCliClient"]

WAIT_TIMEOUT_MS = 500

class AccCliClient(AtkIOConnection):

    def __init__(self, name, root_menu, io_device, io_logs=None, io_hub=None):
        trace(trace_class="ACC", info="AccCliClient::instantiate " + name)

        super(AccCliClient, self).__init__(name, io_device, io_logs, io_hub)

        # Create buffers for parsed cli ios
        cli_io_logs = {}
        for io_type_cli in IO_TYPES_CLI:
            cli_io_logs[io_type_cli] = self._io_logs.add_io_logs(io_type_cli, owner=self)

        self._menu_navigator = AccMenuNavigator(root_menu, self)
        # TODO comment l'utilisateur de cli cient accede au set reg expr ?
        self.__input_handler = AccCliInputHandler(cli_io_logs)
        self.__script_recorder = None
        self.__open_timeout_ms = WAIT_TIMEOUT_MS

        #     #TODO il faut vraiment faire ce reset?a quel moment on relache les buffers de io logs?
        #     self.cli_io_logs.reset()


    @property
    def io_type_all(self):
        return self.io_type_input


    @property
    def open_timeout_ms(self):
        return self.__open_timeout_ms


    @open_timeout_ms.setter
    def open_timeout_ms(self, value):
        self.__open_timeout_ms = value


    def add_parser_reg_expr(self, **kwargs):
        self.__input_handler.add_parser_reg_expr(**kwargs)

        
    def remove_parser_reg_expr(self, **kwargs):
        self.__input_handler.remove_parser_reg_expr(**kwargs)


    def handle_input(self, io_device, data):
        # First parse received data
        self.__input_handler.handle_input(data)

        # Then add input to self.io_type_input and execute callbacks
        super(AccCliClient, self).handle_input(io_device, data)


    # def __cleanCliConnection(self):
        # result = True
        
        # if (self.__io_hub is None):
            # while (isOpen)
                # close
            # self.__io_hub = None
            # self._menu_navigator = None
            # self.cli_io_logs = None
            

        # return result
    

    # TODO rapporcher cli client de physical interface.
    # Beaucoup de similitude : io_hub, io_handler..
    # particularite principale : wait apres le open
    # TODO: ce code ressemble beaucoup a celui de conductor.open
    # faire une classe IORunner ?
    def open(self):
        result = None
        
        trace(trace_class="ACC", info="AccCliClient::open")

        # TODO c'est quoi ca?
        # self.cli_io_logs._addLog(self.io_type_command, "AggloCliClient:pending command at client connection")

        self._menu_navigator.reset()
        super(AccCliClient, self).open()

        # If we must wait for first prompt
        if (self.open_timeout_ms > 0):
            # Wait no more than sec_wait_prompt until the first prompt reception
            result = self.wait_io(AtkIOStringCriteria(io_type=self.io_type_prompt).from_now(self.open_timeout_ms))

        return result
        

    def send(self, data):
        trace(trace_class="ACC", info="AccCliClient::send: " + repr(data))

        # Record raw datas (even in case of a later failure)
        try:
            self.__script_recorder.record(data)
        # Case where recording is disabled
        except AttributeError:
            pass

        super(AccCliClient, self).send(data)


    # TODO ajouter une callback en parametre , qu'on enregistre dans les logs, associe au selecteur qui va bien, si la commande n'a pas terminee
    # TODO utiliser plutot des selecteurs pour return et prompt ?
    # TODO il vaudrait pas mieux utiliser le mecanisme ordinaire de callback plutot que cb_on_command_done ?
    # TODO integrer param timeout dans selectors ?
    def executeCommand(self, command, 
                       expected_return=None, expected_prompt=None, 
                       timeout_ms=WAIT_TIMEOUT_MS, cb_on_command_done=None):
        command_result = AccCommandResults("Execute command " + command)
        # TODO c'est pas logique que le current tail doivent se faire en passant le io_type,
        #  puisque ila deja servi a instancier le selector. Pas beau
        wait_prompt_criteria = AtkIOStringCriteria(io_type=self.io_type_prompt)
        command_io = None
        
        trace(trace_class="ACC", info="AccCliClient::executeCommand: " + repr(command))
        
        # Insert a \n at the end of command if needed
        if (("" == command) or ("\n" != command[-1])):
            command += "\n"

        # Instantiate a selector to check command echo
        # TODO c'est pas bon. Dans le cas du login, l'echo ne correspond pas a la commande
        command_regexpr = command.replace("*", "\*")
        command_echo_criteria = AtkIOStringCriteria(io_type=self.io_type_command, reg_expr=command_regexpr)
        command_echo_criteria.from_current_tail(self.io_logs[self.io_type_command])

        # Selectors with timeout must be configured before command is sent, 
        # in order to have a consistent timeout value
        command_echo_criteria.from_now(min(WAIT_TIMEOUT_MS, timeout_ms))
        wait_prompt_criteria.from_now(timeout_ms)
        
        # Send command on Cli IODevice
        self.send(command)
        try:
            # Command rank cannot be guessed from io lenght, since there 
            # can be other running commands (sent by executeCommand  
            # or by send method)
            # Hence wait until we've received echo command, so that we can 
            # know  command rank
            command_io = self.wait_io(command_echo_criteria)
        except AtkSelectorError:
            command_result.result = COMMAND_ERROR_TIMEOUT
            raise AccExecutionError(command_result)

        command_criteria = AtkIOStringCriteria(io_type=self.io_type_command).rank(command_io.rank)
        result_criteria = AtkIOStringCriteria(io_type=self.io_type_command_result).rank(command_io.rank)
        # TODO le selecteur prompt devrait contenir egalement le prompt precedent
        next_prompt_criteria = AtkIOStringCriteria(io_type=self.io_type_prompt).rank(command_io.rank + 1)
        
        if (timeout_ms > 0):
            trace(trace_class="ACC", info="AccCliClient::executeCommand: wait next prompt")
            try:
                # Wait no more than timeout_ms until the end of the command
                wait_prompt_criteria.rank(command_io.rank + 1)
                self.wait_io(wait_prompt_criteria)
            except AtkSelectorError:
                command_result.result = COMMAND_ERROR_TIMEOUT
                raise AccExecutionError(command_result)
        
        # TODO ajouter les TU
        # Check that received result and next prompt are compliant with expectations
        if expected_return is not None:
            trace(trace_class="ACC", info="AccCliClient::match command result against expected result '" + expected_return + "'")

            check_result_criteria = clone(result_criteria)
            check_result_criteria.reg_expr = expected_return
            try:
                self.io_logs.check(check_result_criteria)
            except AtkSelectorError:
                trace(trace_class="ACC", info="AccCliClient::match command result failed")
                command_result.result = COMMAND_ERROR_MATCH
                raise AccExecutionError(command_result)
            
        if expected_prompt is not None:
            trace(trace_class="ACC", info="AccCliClient::match final prompt against expected prompt '" + expected_prompt + "'")

            check_prompt_criteria = clone(next_prompt_criteria)
            check_prompt_criteria.reg_expr = expected_prompt
            try:
                self.io_logs.check(check_prompt_criteria)
            except AtkSelectorError:
                trace(trace_class="ACC", info="AccCliClient::match final prompt failed")
                command_result.result = COMMAND_ERROR_MATCH
                raise AccExecutionError(command_result)
        
        # Return a named tuple (res, selectors), with selectors as a map allowing 
        # end user to retrieve command, result and next prompt IOs associated to 
        # the method call (only if command has been successfully sent)
        command_result.selectors[self.io_type_command] = command_criteria
        command_result.selectors[self.io_type_command_result] = result_criteria
        # TODO le selecteur ne devrait il pas aussi retourner le previous prompt, en plus du next ?
        command_result.selectors[self.io_type_prompt] = next_prompt_criteria

        return command_result

 
    # TODO ajouter context handler en parametre (gestion des exceptions. Idem sur cliserializable)
    def execute_script(self, file_path, timeout_ms=WAIT_TIMEOUT_MS):
        command_result = AccCommandResults("Execute script " + file_path)
        trace(trace_class="ACC", info="AccCliClient::execute_script: " + file_path)

        file = open(file_path, "r")
        
        for current_line in file:
            command_result.append_child(self.executeCommand(current_line, timeout_ms=timeout_ms))

        return result

        
    def navigate_to_menu(self, menu_path, expected_prompt=None):
        trace(trace_class="ACC", info="AccCliClient::navigate_to_menu: " + str(menu_path))

        command_result = self._menu_navigator.navigate_to_menu(menu_path)
        
        # TODO ajouter les TU
        if expected_prompt is not None:
            trace(trace_class="ACC", info="AccCliClient::match final prompt against expected prompt " + expected_prompt)

            # TODO c'est pas bon ca si le navigate n'a produit aucune commande. De plus results contient le selecteur du prompt
            try:
                check_prompt_criteria = AtkIOStringCriteria(io_type=self.io_type_prompt, reg_expr=expected_prompt).rank(-1)
                self.io_logs.check(check_prompt_criteria)
            except AtkSelectorError:
                trace(trace_class="ACC", info="AccCliClient::match final prompt failed")
                command_result.result = COMMAND_ERROR_MATCH
                raise AccExecutionError(command_result)
        
        return command_result

    
    ###
    # @function : getCurrentMenu
    # @requirement :
    # @file  : AccMenuNavigator.cpp
    # @brief : Retrieves the instance of the current menu during Cli navigation
    # @param : abGeneratePwdCommand : True if the pwd command can be used to get current menu. If set to False,
    #          the registered current menu will be used, it can be wrong (for instance, to an automatic
    #          menu change due to a timeout)
    # @return: pointer to the menu itself if found, NULL (should not happen)
    ###
    # TODO rediger les TU
    def update_current_menu(self, new_current_menu_path=None):
        trace(trace_class="ACC", info="AccCliClient::update_current_menu: " + str(new_current_menu_path))

        # If new menu is not specified
        if new_current_menu_path is None:
            # Execute pwd command to retrieve current menu
            pwm_result = self.executeCommand("pwm")
            pwm_result = self.io_logs.select(pwm_result.selectors[self.io_type_command_result])[-1].data
            new_current_menu_path = AccMenuPath(pwm_result)
        
        if (result):
            self._menu_navigator.current_menu = new_current_menu_path
        
        return result
                

    # TODO on pourrait se contenter d'une property recorder set/del (get inutile)
    #TODO ajouter addTrace(self, asTrace), eventuellement modifier la facon dont le script active le recorder (instanciation par le script? permet un pilotage des traces par le script)
    def start_script_recording(self, file_path, append_file=False):
        result = self.__script_recorder is None
        
        if self.__script_recorder is None:
            self.__script_recorder = AccScriptRecorder(file_path)
            self.__script_recorder.start(append_file)
        else:
            raise AccError(ALREADY_OPENED)
            
        return result


    def pause_script_recording(self, pause):
        self.__script_recorder.pause(pause)
        

    def stop_script_recording(self):
        try:
            self.__script_recorder.stop()
            self.__script_recorder = None
        # Case where script recorder is not started
        except AttributeError:
            pass
        

    # TODO activer ce code et supprimer property io_handler?
    # def add_reg_expr(self, **kwargs):
    #     self.io_handler.add_reg_expr(**kwargs)
        

    # def remove_reg_expr(self, **kwargs):
    #     self.io_handler.remove_reg_expr(**kwargs)
