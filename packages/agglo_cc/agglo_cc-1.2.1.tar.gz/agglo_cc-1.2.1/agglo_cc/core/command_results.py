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

__all__ = ["AccCommandResults", "COMMAND_OK", "COMMAND_ERROR_TIMEOUT", "COMMAND_ERROR_MATCH", "COMMAND_ERROR_CONNECTION", "COMMAND_ERROR_CONFIGURATION"]

COMMAND_OK = 0 
COMMAND_ERROR_TIMEOUT = 1 
COMMAND_ERROR_MATCH = 2 
COMMAND_ERROR_CONNECTION = 3 
COMMAND_ERROR_CONFIGURATION = 4 

# TODO renommer en AccCommandResultsTree
class AccCommandResults():

    # TODO gerer les cas : executeCommand, navigateToMenu, code genere cli client (navigate + execute), serialize/unserialize 
    # defini par user (potentiellement plusieurs invocations de methodes cli client), cliserializable::serialize/unserialize
    # (invocation successive de plusieurs) user defined serialize
    def __init__(self, name="", result=COMMAND_OK):
        self.name = name
        self.parent = None
        self.result = result
        self.__selectors = {}
        self.__children_results = []

        
    def __str__(self):
        result = "succeded" if self.succeeded else "failed"

        return self.name + ": " + result + ", " + str(len(self.children)) + \
               " children, " + str(len(self.selectors)) + " selectors"

        
    def __bool__(self):
        return (COMMAND_OK == self.__result)


    @property 
    def result(self, ): 
        return self.__result


    @result.setter 
    def result(self, value): 
        self.__result = value 
         
        # If parent is succeeded, and new result is failed 
        if (COMMAND_OK != value) and (self.parent is not None) and self.parent: 
            # Update parent result as well. This will lead to the whole ancestors list's results update 
            self.parent.result = value 


    @property
    def succeeded(self):
        return bool(self)
        
        
    @property
    def selectors(self):
        return self.__selectors

        
    @property
    def children(self):
        return self.__children_results

        
    @property
    def leaves(self):
        result = []

        # If command result instance has no depth
        if not self.children:
            # Append current leaf
            result.append(self)
        else: 
            for current_child in self.children:
                result += current_child.leaves

        return result

        
    @property
    def empty(self):
        # TODO ? si pas de selecteur et children empty
        pass

        
    @property
    def ancestors(self):
        result = []
        
        if self.parent is not None:
            result.append(self.parent)
            result += self.parent.ancestors
        
        return result

        
    def append_child(self, child):
        self.__children_results.append(child)
        child.parent = self
        
        # If result value is OK and child is failed
        if (self.succeeded and not child.succeeded):
            # Update self result as well. This will lead to the whole 
            # ancestors list's results update
            self.result = child.result

        
    def get_leaf_selector(self, io_type, rank=-1):
        result = None
        leaves = self.leaves
        nb_result = len(leaves)
        
        if (rank < nb_result) and (rank >= -nb_result):
            result = leaves[rank].selectors.get(io_type, None)
            
        return result

        
    def get_leaf_result(self, rank=-1):
        result = None
        leaves = self.leaves
        nb_result = len(leaves)
        
        if (rank < nb_result) and (rank >= -nb_result):
            result = leaves[rank].result
            
        return result

        
    # TODO quid d'un get_item, qui retournerait resultat, ou selecteur, et qui prendrait un rank ou ou iotype ou un name
    # TODO qui de prendre en parametre de iologs.select un command_result ou un selecteur, et on renverrait en resultat un iobuffer merge

        
    # TODO ca sert ca ?
    @property
    def rank(self):
        result = 0
        
        if self.parent is not None:
            for i, current_child in enumerate(self.parent.children):
                if current_child is self:
                    result = i
                    break
            
        return result

        
    # TODO ca sert ca ?
    def set_selector(self, io_selector):
        self.__selectors[io_selector.io_type] = io_selector
        