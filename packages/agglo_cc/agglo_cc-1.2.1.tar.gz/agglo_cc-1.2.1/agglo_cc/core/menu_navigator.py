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

from .command_results import * 
from ..exceptions import AccExecutionError


__all__ = ["AccMenuNavigator"]

class AccMenuNavigator():
    
    def __init__(self, root_menu, cli_client):
        self.__root_menu = root_menu
        self.__cli_client = cli_client
        self.__current_menu = root_menu

        
    @property
    def current_menu(self):
        return self.__current_menu

        
    ###
    # @function : setCurrentMenu
    # @requirement :
    # @file  : AccMenuNavigator.cpp
    # @brief : Retrieves the instance of the current menu during CLI navigation
    # @param : abGeneratePwdCommand : True if the pwd command can be used to get current menu. If set to False,
    #          the registered current menu will be used, it can be wrong (for instance, to an automatic
    #          menu change due to a timeout)
    # @return: pointer to the menu itself if found, NULL (should not happen)
    ###
    # TODO rediger les TU
    # TODO on garde ca ? ou en private ?
    @current_menu.setter
    def current_menu(self, menu_path):
        new_current_menu = self.__get_descendant_menu(self.__root_menu, menu_path, False)[1]
        
        if new_current_menu is None:
            raise AccError(AccError.UNKNOWN)

        self.__current_menu = new_current_menu


    def reset(self):
        self.__current_menu = self.__root_menu


    ###
    # @function : getDescendantMenu
    # @requirement :
    # @file  : AccMenuNavigator.cpp
    # @brief : Retrieves the CaccMenu instance of a descendant of a given menu
    # @param : source_menu : source menu from which menu lookup start
    # @param : descendant_menu_path : path of the aimed menu. It must be included in the menu tree of source_menu
    # @param : abGenerateCommands : True if the commands to navigate to descendant_menu_path are generated during menu lookup
    # @return: pointer to the descendant menu itself if found, NULL
    ###
    # TODO ce serait pas mieux plutot de rendre menu visitable ?
    # ici on fait de la navigation dans les menu, ce serait donc plutot du code de menu
    def __get_descendant_menu(self, source_menu, descendant_menu_path, generate_command):
        command_results = None
        menu_result = None
        current_menu = source_menu
        next_child_menu = source_menu.get_child_menu(descendant_menu_path)
        _continue = True

        if next_child_menu is None:
            raise AccError(AccError.UNKNOWN)
        
        if generate_command:
            command_results = AccCommandResults()

        # Keep looking to descendant menu if current menu is not descendant menu and
        # if source_menu and descendant_menu_path have the same common root
        if (source_menu.path == descendant_menu_path):
            menu_result = source_menu
        _continue = (menu_result is None) and  \
                    (next_child_menu is not None) and \
                    (source_menu.path.is_ancestor_of(descendant_menu_path))

        # Iterate on descendant menus
        while (_continue):
            # Go one level down : generate enter command for current menu, get next child menu
            if (generate_command):
                # TODO ajouter le menu courant au get_enter_command
                # =>1 menu peut etre accessible depuis 2 menus parents differents = Coherent XML Cli
                # => get_enter_command peut dependre du menu parent
                #  => objectif : les classes menus ne sont plus hierarchisees, factorisation de code
                #  => objectif : facilite acces au getCommand des differents menus, pour une recuperation du format des commandes depuis le script
                # TODO rendre get_enter_command statique (methode de classe)
                enter_command = next_child_menu.get_enter_command()

                try:
                    # Go one level down: generate enter command for next menu
                    enter_result = self.__cli_client.executeCommand(enter_command)
                except AccExecutionError as exception:
                    enter_result = exception.command_results
                    raise AccExecutionError(command_results)
                finally:
                    enter_result.name = "Enter from " + current_menu.name + " into " + next_child_menu.name
                    command_results.append_child(enter_result)

            # Update current and child menu
            if generate_command:
                self.__current_menu = next_child_menu
            current_menu = next_child_menu
            next_child_menu = next_child_menu.get_child_menu(descendant_menu_path)

            # Check if current menu is looked-up menu
            if (current_menu.path == descendant_menu_path):
                menu_result = current_menu

            # Stop if there is no more child, if lookedup menu has been found
            _continue = (next_child_menu is not None) and (menu_result is None)

        # If final menu could not be found, but every generated command has succeeded
        if (menu_result is None) and  command_results:
            command_results.result = COMMAND_ERROR_MATCH
            raise AccExecutionError(command_results)
            
        return command_results, menu_result

    ###
    # @function : navigate_to_menu
    # @requirement :
    # @file  : AccMenuNavigator.cpp
    # @brief : Execute the commands to navigate from a source menu to another menu, the path of destination menu
    # @param : source_menu : source menu from which navigation start;if set to None, 
    #          the source menu is the current menu, retrieved either by pwd recorder in self
    # @param : dest_path : path of the aimed menu
    # @return: pointer to the dest menu itself if found, NULL
    ###
    def navigate_to_menu(self, dest_path):
        source_path = self.__current_menu.path
        commands_results = AccCommandResults("Navigate from " + source_path.menu_name + " to " + dest_path.menu_name)
            
        # If we're not already set on common ancestor menu
        common_parent_path = source_path.get_common_ancestor(dest_path)
        if (common_parent_path != source_path):
            # Go up to common ancestor menu
            navigate_up_results = self.__navigate_to_ancestor_menu(self.__current_menu, common_parent_path)
            
            # Register exit commands results
            for current_result in navigate_up_results.children:
                commands_results.append_child(current_result)

        if commands_results:
            # If we're not already set on destination menu
            if (self.__current_menu.path != dest_path):
                # Navigate down to descendant menu
                navigate_down_results = self.__navigate_to_descendant_menu(self.__current_menu, dest_path)
                
                # Register enter commands results
                for current_result in navigate_down_results.children:
                    commands_results.append_child(current_result)

        return commands_results


    ###
    # @function : navigateToDescendantMenu
    # @requirement :
    # @file  : AccMenuNavigator.cpp
    # @brief : Execute the commands to navigate from a source menu to an ancestor menu, the path of destination menu
    # @param : source_menu : source menu from which navigation start
    # @param : descendant_menu_path : path of the aimed menu. It must be included in the menu tree of source_menu
    # @return: pointer to the dest menu itself if found, NULL
    ###
    def __navigate_to_descendant_menu(self, source_menu, descendant_menu_path):
        return self.__get_descendant_menu(source_menu, descendant_menu_path, True)[0]


    ###
    # @function : navigateToAncestorMenu
    # @requirement :
    # @file  : AccMenuNavigator.cpp
    # @brief : Generate the commands to navigate from a source menu to an ancestor menu, the path of destination menu
    # @param : source_menu : source menu from which navigation start
    # @param : ancestor_menu_path : path of the aimed menu. source_menu must be included in the menu tree of ancestor_menu_path
    # @return: pointer to the dest menu itself if found, NULL
    ###
    def __navigate_to_ancestor_menu(self, source_menu, ancestor_menu_path):
        command_results = AccCommandResults()
        current_menu = source_menu
        next_parent_menu = source_menu.parent_menu
        found = (current_menu.path == ancestor_menu_path)
        _continue = True

        #TODO : rendre la commande safe : pas de exit si ancestor path inexistant

        # Keep looking to ancestor menu if current menu is not ancestor menu and 
        # if source_menu and ancestor_menu_path have the same common root
        _continue = (not found) and (next_parent_menu is not None) and \
                    (ancestor_menu_path.is_ancestor_of(source_menu.path))

        # Iterate on ancestor menus
        while _continue:
            exit_cmd = current_menu.get_exit_command()
            try:
                # Go one level up : generate exit command for current menu, get next parent menu
                exit_result = self.__cli_client.executeCommand(exit_cmd)
            except AccExecutionError as exception:
                exit_result = exception.command_results
                raise AccExecutionError(command_results)
            finally:
                exit_result.name = "Exit from " + current_menu.name + " to " + next_parent_menu.name
                command_results.append_child(exit_result)
            
            # If exit command has succeeded, update current and parent menu
            self.__current_menu = next_parent_menu
            current_menu = next_parent_menu
            next_parent_menu = current_menu.parent_menu

            # Stop if there is no more parent or if looked-up menu has been found
            found = (current_menu.path == ancestor_menu_path)
            _continue = (next_parent_menu is not None) and (not found)

        # If final menu could not be found, but every generated command has succeeded
        if (not found) and command_results:
            command_results.result = COMMAND_ERROR_MATCH
            raise AccExecutionError(command_results)

        return command_results