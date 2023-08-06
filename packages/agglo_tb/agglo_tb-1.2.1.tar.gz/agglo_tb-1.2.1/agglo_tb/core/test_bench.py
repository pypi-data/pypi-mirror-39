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

from collections import OrderedDict

from agglo_tk.ro_referencer import AtkROReferencer
from agglo_tk.trace import trace
from agglo_tk.io import AtkIOConnectionLogs

from agglo_tk.exceptions import AtkLimitedAccessError
from ..exceptions import AtbError
from ..exceptions import AtbTestBenchError

from .node import AtbNode
from .conductor import AtbConductor
from .host_interface import AtbHostInterface
from .host import AtbHost


__all__ = ["AtbTestBench"]

# TODO deplacer dans  fonction atk.utils
def validate_kwargs(allowed_kwargs, **kwargs):
    for kwarg in kwargs:
        if kwarg not in allowed_kwargs:
            raise ValueError("Unexpected keyword argument")


#TODO definir un fichier testscript definissant une fixture d'instanciation de la plateforme, plus les methodes send, parceque sinon il faut faire testplatform.send(frame) alors qu'on devrait faire send(frame, dest) avec target en node, target ou itflocale, ou alors itflocale.send(frame)
class AtbTestBench(AtkROReferencer):
    
    DEFAULT_NODE_NAME = "Node"
    TARGETS_LIST_ID = AtkROReferencer.DEFAULT_LIST_ID
    NODES_LIST_ID = AtkROReferencer.DEFAULT_LIST_ID + 1

    def __init__(self):
        trace(trace_class="ATB", info="AtbTestBench::instantiate platform")
        AtkROReferencer.__init__(self)
        # ou utiliser reference ? Avantage : l'ajout de target avec le nom conductor ne passera jamais, meme si on change le nom conductor par defaut
        self.__conductor = AtbConductor(self)
        self._add_reference_list(AtbTestBench.NODES_LIST_ID)

        self.__io_logs = AtkIOConnectionLogs()


    # TODO UT
    def __contains__(self, test_item):
        result = (test_item in self.hosts) or (test_item in self.nodes)
        if not result:
            try:
                # Test if test_item is a platform's host interface
                result = (test_item.host in self) and (test_item in test_item.host)
            # Case where test_item is not an interface (might be an host or node not in platform)
            except AttributeError:
                pass

        return result


    @property
    def io_logs(self):   
        return self.__io_logs


    @property
    def conductor(self):   
        return self.__conductor


    @property
    def targets(self):   
        return list(self._referenced_items[AtbTestBench.TARGETS_LIST_ID].values())


    @property
    def hosts(self):
        def iter_hosts(platform):
            yield platform.conductor
            for host in platform.targets:
                yield host

        return [host for host in iter_hosts(self)]
    

    @property
    def nodes(self):   
        return list(self._referenced_items[AtbTestBench.NODES_LIST_ID].values())


    def is_connected(self, test_item1, test_item2):
        result = False

        trace(trace_class="ATB", info="AtbTestBench::is_connected " + test_item1.name + \
                                      " and " + test_item2.name + " ?")

        # Use in instead of is, since test items might be proxied
        if test_item1 in [test_item2]:
            raise AtbTestBenchError(AtbTestBenchError.SAME_ITEM)
        else:
            # If one of given items is a node
            # TODO 2 node peuvent-ils etre connected ?
            # TODO eviter de tester instance, unifier les cas Node contenant host/interface et host contenant interface
            if isinstance(test_item1, AtbNode) or isinstance(test_item2, AtbNode):
                # Check if the other item is connected to the node
                if isinstance(test_item1, AtbNode):
                    result = test_item2 in test_item1
                else:
                    result = test_item1 in test_item2
            else:
                try:
                    if test_item1 in test_item2:
                        raise AtbTestBenchError(AtbTestBenchError.HOST_INTERFACE)
                except TypeError:
                    pass
                try:
                    if test_item2 in test_item1:
                        raise AtbTestBenchError(AtbTestBenchError.HOST_INTERFACE)
                except TypeError:
                    pass

                # Check if there is a node to which both items are connected
                for node in self.nodes:
                    result = test_item1 in node and test_item2 in node
                    if result:
                        break

        trace(trace_class="ATB", info="AtbTestBench::is_connected returns " + str(result))

        return result


    def get_conductor_interfaces(self, test_item):
        trace(trace_class="ATB", info="AtbTestBench::get_conductor_interfaces " + test_item.name)
        
        # TODO revoir ca en fonction des nouveau contains et iter de node
        try:
            return [interface for interface in self.conductor \
                              if self.is_connected(interface, test_item)]
        # TODO ca marche ca?
        except AtbTestBenchError as exception:
            if str(exception) == AtbTestBenchError.SAME_ITEM:
                raise AtbTestBenchError(AtbTestBenchError.HOST_INTERFACE)
            elif str(exception) == AtbTestBenchError.HOST_INTERFACE:
                raise AtbTestBenchError(AtbTestBenchError.SAME_ITEM)
            else:
                raise


    def get_connected_interfaces(self, test_item):
        result = []

        trace(trace_class="ATB", info="AtbTestBench::get_connected_interfaces " + test_item.name)

        for host in self.hosts:
            for interface in host:
                try:
                    if self.is_connected(interface, test_item):
                        result.append(interface)
                except AtbTestBenchError:
                    pass

        return result
        # return [interface for host in self.hosts \
        #                      for interface in host \
        #                   if self.is_connected(interface, test_item)]
        # TODO revoir ca en fonction des nouveau contains et iter de node
        # return [interface for interface in self.nodes \
        #                   if self.is_connected(interface, test_item)]


    def get_connected_hosts(self, test_item):
        result = []

        trace(trace_class="ATB", info="AtbTestBench::get_connected_hosts " + test_item.name)

        # TODO revoir ca en fonction des nouveau contains et iter de node
        for host in self.hosts:
            try:
                if self.is_connected(host, test_item):
                    result.append(host)
            except AtbTestBenchError:
                pass

        return result
        # return [host for host in self.hosts \
                     # if self.is_connected(host, test_item)]

    
    def add_target(self, target):
        trace(trace_class="ATB", info="AtbTestBench::add target " + target.name)

        # No use to check this, since conductor has the same name than 
        # AtbTestBench.conductor property. Hence reference() will fail
        # if (target.name == self.conductor.name):
        #     raise AtbError(AtbError.DUPLICATED_NAME)

        # Reference target
        self.reference(target, target.name, AtbTestBench.TARGETS_LIST_ID)

        # Make test target reference conductor, it might be useful for target serialization
        target.reference_conductor(self.conductor)



    # TODO verifier que on peut pas connecter 2 node
    def connect(self, *args, **kwargs):
        node = None
        node_name = None
        # exception = None

        # TODO TU
        # Validate kwargs names
        validate_kwargs(["node", "node_name"], **kwargs)
        if (node in kwargs) and (node_name in kwargs):
            raise ValueError("Duplicated node|node_name argument")

        # Retrieve node name 
        node = kwargs.get("node", None)
        node_name = kwargs.get("node_name", None)
        # If node nor node name are specified
        if (node is None) and (node_name is None):
            # Generate a unique node name
            node_name = self.__generate_node_name()

        str_args = ", ".join([item.name for item in args])
        trace(trace_class="ATB", info="AtbTestBench::connect " + (node_name if node_name is not None else node.name) + \
                                      " with items " + str_args)

        # If node is given
        if node is not None:
            # Check that node belongs to the platform
            # TODO peut-on connecter un node inconnu (equivalent AddNode)?
            if node not in self.nodes:
                raise AtbError(AtbError.UNKNOWN)
            node_name = node.name
        # If node_name is given
        else:
            # Try to retrieve node
            try:
                node = self._referenced_items[AtbTestBench.NODES_LIST_ID][node_name]
            # If node doesn't exist
            except KeyError:
                # Instantiate a new node
                node = AtbNode(node_name)

        # Connect all provided test items to node
        try:
            node.connect(*args)
        finally:
            # For all targets connected to node
            for target in node.hosts:
                # If target doesn't belong to the platform yet (it has just been connected)
                if target not in self.hosts:
                    # Add target to platform
                    self.add_target(target.__subject__)

        try:
            # Reference node in the platform
            self.reference(node, node_name, AtbTestBench.NODES_LIST_ID)
        # Case where the node already belongs to the platform
        except AtkLimitedAccessError:
            pass
            
        return node

        
    def start(self):
        trace(trace_class="ATB", info="AtbTestBench::start platform")

        # # init reseau + cli, synchrone ou asynchrone
        # TODO ajouter une methode start aux target, ainsi le end user peut surcharger ce start, et faire ses inits de target
        # au cours du start AtbTestBench, et non seulement une fois fini le AtbTestBench.start()
        # for  atcTestTargetGroup in self.__atcTestTargetGroupList
            # bRes = atcTestTargetGroup.start() && bRes
        pass


    def __generate_node_name(self):
        result = None
        reserved_names = [node.name for node in self.nodes] + [host.name for host in self.hosts]
        i = len(reserved_names) + 1

        # Generate a new node name
        while result is None:
            new_name = AtbTestBench.DEFAULT_NODE_NAME + str(i)
            if new_name not in reserved_names:
                result = new_name
            i += 1

        return result
