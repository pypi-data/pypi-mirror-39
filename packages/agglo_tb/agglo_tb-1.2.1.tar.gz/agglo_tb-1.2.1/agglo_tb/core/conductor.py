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

from agglo_tk.io.io_hub import AtkIOHub
from agglo_tk.ro_referencer import AtkROReferencer
from agglo_tk.trace import trace

from ..exceptions import AtbError
from ..exceptions import AtbConductorError
from .host import AtbHost


__all__ = ["AtbConductor"]

class AtbConductor(AtbHost):

    CONDUCTOR_NAME = "conductor"
    CLI_CLIENTS_LIST_ID = AtbHost.INTERFACES_LIST_ID + 1

    def __init__(self, platform=None):
        """
            Instantiate a test conductor.
            @param platform: test platform which can be used to resolve automatically which 
                             interface to use for test conductor output. Useless if this ATB 
                             feature is not used
        """
        AtbHost.__init__(self, AtbConductor.CONDUCTOR_NAME)
        self._add_reference_list(AtbConductor.CLI_CLIENTS_LIST_ID)
        self.__platform = platform
        self.__connections = set()

    
    # def __del__(self):
    #     try:
    #         self.close()
    #     except AtkIODeviceError:
    #         pass


    # TODO a quoi ca sert ? les connections sont ajoutees de l'exterieur. Une liste ne permet
    # pas de savoir a quoi correspond le iolog...
    @property
    def io_logs(self):
        return [connection.io_logs for connection in self.__connections]


    # TODO est-ce utile ? que ce soit au moins une map
    @property
    def cli_clients(self):
        return list(self._referenced_items[AtbConductor.CLI_CLIENTS_LIST_ID].values())


    def add_interface(self, connection):
        trace(trace_class="ATB", info="AtbConductor::add physical connection " + connection.name)

        # Add interface in host
        AtbHost.add_interface(self, connection)
        
        self.__connections.add(connection)


    def add_cli_client(self, cli_client, **kwargs):
        test_target = kwargs.get("test_target", None)
        cli_client_name = kwargs["client_name"] if "client_name" in kwargs else cli_client.name

        # If client has not been added yet
        if cli_client not in self.cli_clients:
            trace(trace_class="ATB", info="AtbConductor::add cli client " + cli_client_name)

            # Reference client in test conductor and in the target
            # It will fail if cli_client_name is already used
            self.reference(cli_client, cli_client_name, AtbConductor.CLI_CLIENTS_LIST_ID)

            # If target related to cli client is given
            if test_target is not None:
                # Make test target reference cli_client, it will be useful for target 
                # serialization. It will fail if cli_client_name is already used
                test_target.reference_cli_client(cli_client, cli_client_name)

            self.__connections.add(cli_client)
        else:
            # If cli client has been added with another name
            if self.get_reference_name(cli_client) != cli_client_name:
                raise AtbConductorError(AtbConductorError.CONFLICT)


    
    # TODO pour utiliser Atb pour faire de la conf telnet/ssh des targets
    def add_telnet_client(self, client_name, handler=None, ssh_enabled=True, test_target=None):
        pass


    def open(self, *args):
        if not args:
            trace(trace_class="ATB", info="AtbConductor::open all interfaces and cli clients")

            # Open all conductors'interfaces and cli clients
            self.open(*self.__connections)
        else:
            exception = None
            
            # Iterate on all connections (interfaces or cli clients)
            for current_connection in args:
                try:
                    trace(trace_class="ATB", info="AtbConductor::open " + current_connection.name + \
                                                  " on io hub " +str(id(current_connection.io_hub)))

                    if current_connection in self.__connections:
                        current_connection.open()
                    else:
                        raise AtbError(AtbError.UNKNOWN)
                        
                except Exception as _exception:
                    trace(trace_class="ATB", info="AtbConductor::open fail for " + current_connection.name)

                    # Register exception for later raise
                    exception = _exception

            if exception is not None:
                raise exception
        
        
    def close(self, *args):
        trace(trace_class="ATB", info="AtbConductor::close all interfaces and cli clients")
        
        # TODO gerer la fermeture d'une seule connection/io_hub
        for current_connection in self.__connections:
            current_connection.close()


    # TODO reflechir a la notion de route : ex je veux envoyer une trame sur l'itf de A mais en passant soit par C.Itf1->A, 
    # soit par C.Itf2->B->A.itf). 2 solutions : declarer une node physique(A.itf_clair, C.Itf1) et une node virtuelle(A.itfchiffre, C.itf2).
    # ou bien ajouter une notion de route dans le send, ou dans les interfaces
    def send(self, data, local_interface=None, test_target=None):
        # If no interface is provided
        if local_interface is None:
            # If conductor has only one interface
            if (len(self.interfaces) == 1):
                local_interface  = self.interfaces[0]
            else:
                # Retrieve from platform the interfaces connected to target
                local_interfaces = self.__platform.get_conductor_interfaces(test_target)

                # Check that only one connected interface has been found
                if (1 == len(local_interfaces)):
                    local_interface = local_interfaces[0]
                elif local_interfaces:
                    raise AtbConductorError(AtbConductorError.UNDECIDED_INTERFACE)
                else:
                    raise AtbConductorError(AtbConductorError.NO_INTERFACE)

        elif local_interface not in self:
            raise AtbError(AtbError.UNKNOWN)
        
        local_interface.send(data)

        
    # def __is_opened(self):
    #     result = False
        
    #     for io_hub in self.__io_hubs.values():
    #         result = io_hub.opened
    #         if result:
    #             break
        
    #     if not result:
    #         for cli_client in self.cli_clients:
    #             result = cli_client.opened
    #             if result:
    #                 break
                
    #     return result
