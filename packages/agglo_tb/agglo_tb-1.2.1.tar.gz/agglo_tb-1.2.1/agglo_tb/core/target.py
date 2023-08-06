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

from agglo_tk.serializable import AtkSerializable
from agglo_tk.friend import friend
from agglo_tk.friend import has_friends
from agglo_tk.ro_referencer import AtkROReferencer

from .host import AtbHost
from .conductor import AtbConductor
from .test_bench import AtbTestBench
from .._private.conductor_proxy import AtbConductorProxy


__all__ = ["AtbTarget"]

@has_friends
class AtbTarget(AtbHost, AtkSerializable):

    CLI_CLIENTS_LIST_ID = AtkROReferencer.DEFAULT_LIST_ID + 1
            
    def __init__(self, name):
        AtbHost.__init__(self, name)
        AtkSerializable.__init__(self)
        self.__conductor_proxy = None
        self._add_reference_list(AtbConductor.CLI_CLIENTS_LIST_ID)


    # TODO utiliser plutot une reference pour que self.conductor failed
    @property
    def conductor(self):
        return self.__conductor_proxy
    
    
    # TODO privee ou public ?
    @friend("AtbConductor")
    def __reference_cli_client(self, cli_client, cli_client_name):
        # TODO faire un proxy sur le client
        self.reference(cli_client, cli_client_name, AtbTarget.CLI_CLIENTS_LIST_ID)
        # TODO ou bien le client est reference dans un proxy conductor ?
        # self.conductor.reference(cli_client, name, AtbConductor.CLI_CLIENTS_LIST_ID)

        
    # TODO privee ou public ?
    @friend("AtbTestBench")
    def __reference_conductor(self, conductor):
        # Create a proxy on conductor which by default send datas to self
        # TODO ou reference pour avoir plusieurs conductor (probleme : la liste des rfeerences d'un host sert a generer la liste des interfaces)
        self.__conductor_proxy = AtbConductorProxy(conductor)
        self.__conductor_proxy.default_dest = self



# class AtbTarget(AtbHost, AtkSerializable):
            
#     def __init__(self, name):
#         AtbHost.__init__(self, name)
#         AtkSerializable.__init__(self)
#         self.__conductor_proxy = AtbConductorProxy(self)

        
#     @property
#     def conductor(self):
#         return self.__conductor_proxy
    
    
#     @friend(AtbConductor)
#     def __reference_cli_client(self, cli_client, cli_client_name):
#         # Pas de proxy ? est-ce qu'on ne va pas faire target.client.close?
#         # setattr(self, cli_client_name, cli_client)
#         self.conductor.reference(cli_client, cli_client_name)

        
#     @friend(AtbTestBench)
#     def __reference_conductor(self, conductor):
#         self.__conductor_proxy.skeleton = conductor

            
#     class AtbConductorProxy(AtkReferencer):

#         def __init__(self, target):
#             AtkReferencer.__init__(self)
#             self.__target = target


#         @property
#         # @friend(AtbTarget)
#         # def __skeleton(self):
#         def skeleton(self):
#             return self.__conductor


#         @skeleton.setter
#         # @friend(AtbTarget)
#         # def __skeleton(self, conductor):
#         def skeleton(self, value):
#             self.__conductor = value
            
            
#         def send(self, data, target_interface=None):
#             result = self.conductor is not None
#             test_target = None
            
#             if result:
#               # Destination must be either target or one of its interface
#               if target_interface is None:
#                   test_target = self.__target
#               elif target_interface in self.__target:
#                   test_target = target_interface
#               result = (test_target is not None)
            
#             if result:
#                 # Send data toward target
#                 result = self.__conductor.send(data, test_target=test_target)
            
#             return result
#         