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

from agglo_tk.exceptions import AtkLimitedAccessError

from .host_proxy import AtbHostProxy


__all__ = ["AtbConductorProxy"]

class AtbConductorProxy(AtbHostProxy):

    def __init__(self, conductor, **kwargs):
        # Init an host proxy with access to conductor's send method
        AtbHostProxy.__init__(self, conductor, **kwargs)
        try:
            self.allow_access("send")
        # TODO je pense que ce cas ne peut pas arriver
        # Case where send method was already allowed
        except AtkLimitedAccessError as exception:
            if exception.message == AtkLimitedAccessError.CONFLICT:
                pass

        self.add_attr("_default_dest", None)


    @property
    def default_dest(self):
      return self._default_dest


    @default_dest.setter
    def default_dest(self, default_dest):
      self._default_dest = default_dest
    
        
    # def send(self, data, target_interface=None):
    def send(self, data, dest=None):
        # If destination is not given
        if dest is None:
            # Use default destination
            dest = self.default_dest
        
        # Send data
        result = self.__subject__.send(data, None, dest)



    #     class AtbConductorProxy(AtkReferencer):

    # def __init__(self, target):
    #     AtkReferencer.__init__(self)
    #     self.__target = target


    # @property
    # # @friend(AtbTarget)
    # # def __skeleton(self):
    # def skeleton(self):
    #     return self.__conductor


    # @skeleton.setter
    # # @friend(AtbTarget)
    # # def __skeleton(self, conductor):
    # def skeleton(self, value):
    #     self.__conductor = value
        
        
    # def send(self, data, target_interface=None):
    #     result = self.conductor is not None
    #     test_target = None
        
    #     if result:
    #       # Destination must be either target or one of its interface
    #       if target_interface is None:
    #           test_target = self.__target
    #       elif target_interface in self.__target:
    #           test_target = target_interface
    #       result = (test_target is not None)
        
    #     if result:
    #         # Send data toward target
    #         result = self.__conductor.send(data, test_target=test_target)
        
    #     return result
    #     