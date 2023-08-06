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

from .menu_path import AccMenuPath

__all__ = ["AccMenu"]

class AccMenu():

    # Constructor
    def __init__(self, menu_name, parent_menu=None):
        # Attributes
        parent_menu_path = parent_menu.path if (parent_menu is not None) else None
        
        self.__parent_menu = parent_menu
        self.__path = AccMenuPath(menu_name, parent_menu_path)
        self.__children_menus = []

        # TODO : c'est bizarre de modifier aaccp_ParentMenu dans le constructeur du child
        # Il vaudrait mieux construire le child, lier les 2 dans add_child_menu (renommer addLink)
        if (None != parent_menu):
            parent_menu.add_child_menu(self)
    
    
#    def    initRootMenu(self, sRootMenuName):
#        __init__(self, None, MENUSEPARATOR + sRootMenuName)

    def __str__(self):
         return self.__path.path


    @property
    def parent_menu(self):
        return self.__parent_menu


    @property
    def path(self):
        return self.__path

        
    @property
    def name(self):
        return self.__path.menu_name        


    ###
    # @function : add_child_menu
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Creates the pointer from the parent to the child
    # @param : aaccNewChildMenu : child menu
    # @return: void
    ###
    def add_child_menu(self, aaccNewChildMenu):
        # TODO assert &aaccNewChildMenu absent
        # TODO cette fonction est bancale puisque on modifie le parent, modifier le child
        self.__children_menus.append(aaccNewChildMenu)


    # def addChildMenu2(self, sChildMenuName):
    #     accNewChildMenu = None
    #     bContinue = ("" != sChildMenuName) and (-1 == sChildMenuName.find(MENUSEPARATOR)) and (self.__get_child_menu(sChildMenuName) is not None)
        
    #     if (bContinue):
    #         accNewChildMenuPath = AccMenuPath(sChildMenuName, self.__path)
    #         # TODO ce constructeur ne devrait pas etre disponible en public
    #         accNewChildMenu = CaccMenu(accNewChildMenuPath, self)
    #         self.__children_menus.append(aaccNewChildMenu)
        
    #     return accNewChildMenu


    ###
    # @function : get_child_menu
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Gets the next child menu step on the way to a given path
    # @param : descendant_menu_path : path of a descendant menu. It can be a child menu,
    #          or a descendant of a child menu
    # @return: Child menu of self, NULL if there is no way to descendant_menu_path
    ###
    def get_child_menu(self, descendant_menu_path):
        result = None
        
        # self must be an ancestor of descendant_menu_path
        if ((descendant_menu_path != self.__path) and (self.__path.is_ancestor_of(descendant_menu_path))):
            for current_menu in self.__children_menus:
                if (current_menu.path.is_ancestor_of(descendant_menu_path)):
                    result = current_menu
                    break

        return result

        
    def __get_child_menu(self, child_menu_name):
        result = None
        
        for current_menu in self.__children_menus:
            if (current_menu.menu_name == child_menu_name):
                result = current_menu
                break

        return result
        

    @staticmethod
    def get_exit_command():
        return "exit\n"
        
