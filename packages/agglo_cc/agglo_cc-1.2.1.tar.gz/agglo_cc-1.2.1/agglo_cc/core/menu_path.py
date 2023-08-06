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

__all__ = ["AccMenuPath"]

DEFAULT_MENU_SEPARATOR = "\\"

class AccMenuPath():

    ## Constructor
    def __init__(self, menu_name, parent_path=None):
        # Build the path with parent menu path and child menu name
        parent_path = "" if (parent_path is None) else str(parent_path)
        self.__path = parent_path + DEFAULT_MENU_SEPARATOR + menu_name


    def __str__(self):
         return self.__path
         
    ###
    # @function : AccMenuPath.operator ==
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Compares 2 path
    # @param : other_path : path to compare
    # @return: True if the 2 AccMenuPath have the same path
    def __eq__(self, other_path):
        return (self.__path == str(other_path))



    ###
    # @function : AccMenuPath.operator !=
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Compares 2 path
    # @param : other_path : path to compare
    # @return: True if the 2 AccMenuPath have different path
    def __ne__(self, other_path):
        return not(self  == other_path)


    ###
    # @function : AccMenuPath.menu_name
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Gets the name of the menu, separator or parent path
    # @return: name of the menu
    @property
    def menu_name(self):
        last_separator_idx = self.__path.rfind(DEFAULT_MENU_SEPARATOR)
        last_separator_idx = 0 if (last_separator_idx == -1) else (last_separator_idx + 1)

        return self.__path[last_separator_idx:]

    
    ###
    # @function : AccMenuPath.get_common_ancestor
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Gets the common ancestor of 2 paths. A path is considered common ancestor of itself
    # @param : _Path : path to compare with self
    # @return: Common ancestor, menu separator if no ancestor has been found
    def get_common_ancestor(self, other_path):
        common_ancestor = AccMenuPath("")
        path2 = str(other_path)

        # self is common ancestor of itself
        if (self.__path == path2):
            common_ancestor = self
        else:
            next_separator_path1 = 0
            next_separator_path2 = 0
            _continue = True

            # Iterate on path, from root
            while _continue:
                # Find position of next separator. If there is no separator left, means that we
                # are on the last menu ; consider there is an extra separator is a the end of the path
                next_separator_path1 = self.__path.find(DEFAULT_MENU_SEPARATOR, next_separator_path1)
                if (-1 == next_separator_path1):
                    next_separator_path1 = len(self.__path)
                next_separator_path2 = path2.find(DEFAULT_MENU_SEPARATOR, next_separator_path2)
                if (-1 == next_separator_path2):
                    next_separator_path2 = len(path2)

                # Check that next separator is on the same position on both path
                _continue = (next_separator_path1 == next_separator_path2)
                if _continue:
                    # Check that path until next separator is the same on both path
                    #_continue = self.__path.startswith(path2, 0, next_separator_path1)
                    _continue = (self.__path[0:next_separator_path1] == path2[0:next_separator_path2])

                if _continue:
                    if (next_separator_path1 > 0):
                        # Extract path from root until next separator
                        common_ancestor.__path = self.__path[0:next_separator_path1]

                    # Now we gonna look next menu level
                    next_separator_path1 += 1
                    next_separator_path2 += 1

        return common_ancestor


    ###
    # @function : AccMenuPath.is_descendant_of
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Check wether a path is descendant of self. As a path is common ancester
    #          with itself, is considered descendant of itself
    # @param : _Path : path to compare with self
    # @return: True if _path is a descendant of self
    def is_descendant_of(self, menu_path):
        path = str(menu_path) + DEFAULT_MENU_SEPARATOR

        return ((self == menu_path) or (self.__path.find(path) == 0))


    ###
    # @function : AccMenuPath.is_ancestor_of()
    # @requirement :
    # @file  : CaccMenuNavigator.cpp
    # @brief : Check wether a path is ancestor of self. As a path is common ancester
    #          with itself, is considered ancestor of itself
    # @param : _Path : path to compare with self
    # @return: True if _path is a ancestor of self
    def is_ancestor_of(self, menu_path):
        return menu_path.is_descendant_of(self)
