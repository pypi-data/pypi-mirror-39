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

__all__ = ["AtbHostInterfaceProxy"]

class AccScriptRecorder():

    def __init__(self, asFilePath):
        self.__sFilePath = asFilePath
        self.__bIsOpen = False
        self.__bPauseRecording = False

        
    def start(self, abAppendFile = False):
        bRes = (not self.__bIsOpen) and ("" != self.__sFilePath)

        if (bRes):
            with open(self.__sFilePath, 'a') as pyFile:
                self.__bIsOpen = True
            
            bRes = self.__bIsOpen
            
        if (bRes and not abAppendFile):
            # Erase file
            open(self.__sFilePath, 'w').close()

        return (bRes)


    def pause(self, abPause):
        self.__bPauseRecording = abPause


    def stop(self):
        bRes = self.__bIsOpen

        if (bRes):
            self.__bIsOpen = False
            self.__bPauseRecording = False
        
        return (bRes)


    def record(self, asOutput):
        bRes = (self.__isRecording()) and ("" != asOutput)

        if (bRes):
            with open(self.__sFilePath, 'a') as pyFile:
                pyFile.write(asOutput)

        return (bRes)


    def addTrace(self, asTrace):
        #TODO ajouter les TU
        with open(self.__sFilePath, 'a') as pyFile:
            pyFile.write(asTrace)

        
    def __isRecording(self):
        return (self.__bIsOpen and not self.__bPauseRecording)