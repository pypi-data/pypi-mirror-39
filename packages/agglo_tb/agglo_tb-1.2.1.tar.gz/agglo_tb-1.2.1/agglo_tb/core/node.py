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

from agglo_tk.ro_referencer import AtkROReferencer
from agglo_tk.trace import trace

from .._private.host_proxy import AtbHostProxy
from ..exceptions import AtbError


__all__ = ["AtbNode"]

class AtbNode(AtkROReferencer):
    """
        AtbNode links interfaces of hosts together. This allows test scripts 
        to send data by specifying destination rather than conductor emitting 
        interface, making test scripts more readable.
    """
    
    def __init__(self, name):
        trace(trace_class="ATB", info="AtbNode::instantiate node " + name)

        AtkROReferencer.__init__(self)
        self.__name = name
        # TODO posible de supprimer cette map, utiliser uniquement roreferencer ?
        self.__host_proxies = {}


    def __contains__(self, test_item):
        return (test_item in self.__host_proxies) or \
               (test_item in [interface for interface in self.interfaces])

        
    def __iter__(self):
        for interface in self.interfaces:
            yield interface

        
    @property
    def name(self):
        return self.__name


    @property
    def interfaces(self):
        return [interface for host_proxy in self.__host_proxies.values() \
                          for interface in host_proxy.interfaces]


    @property
    def hosts(self):
        return list(self.__host_proxies.values())

    
    # TODO private pour platform ? Sinon risque de modification de node sans 
    # passer par platform
    def connect(self, *args):
        exception = None

        str_args = ", ".join([item.name for item in args])
        trace(trace_class="ATB", info="AtbNode::connect on " + self.name + \
                                      " items: " + str_args)

        # TODO supprimer. Comme ca on peut faire plaform.connect(node_name="empty_node")
        # qui cree un node empty
        # If there is no item to connect
        if not args:
            exception = AtbError(AtbError.EMPTY)

        # Iterate on all item to connect
        for current_test_item in args:
            try:
                # Connect test item to node
                self.__connect(current_test_item)
            # In case of error
            except Exception as current_exception:
                # Register exception
                if exception is None:
                    exception = current_exception

        # Raise first exception only once all test_item have been connected
        if exception is not None:
            raise exception


    def __connect(self, test_item):
        trace(trace_class="ATB", info="AtbNode::__connect on " + self.name + \
                                      " single item " + test_item.name)

        # Get or instantiate an host proxy. It is called here to 
        # force creation of host proxy in the case of empty host
        host_proxy = self.__get_host_proxy(test_item)

        # Assume test_item is an host
        try:
            new_interfaces = [interface for interface in test_item.interfaces \
                                        if interface not in self]

            if new_interfaces:
                # Connect new interfaces of host
                self.connect(*new_interfaces)

        # Case where test_item is not an host
        except AttributeError:
            # Add interface to host proxy
            host_proxy.add_interface(test_item)


    def __get_host_proxy(self, test_item):
        host_proxy = None
        host = None
        
        trace(trace_class="ATB", info="AtbNode::__get_host_proxy: retrieve host proxy for item " + \
                                      test_item.name)

        # Retrieve host from test_item
        try:
            # Assume test_item is an interface
            host = test_item.host
        # Case where test_item is not an interfae
        except AttributeError:
            host = test_item

        if host is None:
            # TODO c'est bien ca? ou renommer en ORPHAN_INTERFACE
            raise AtbError(AtbError.UNKNOWN)
        else:
            host_proxy = self.__host_proxies.get(host, None)
            
            # If host is not referenced (none of its interfaces has been added yet)
            if host_proxy is None:
                # # Check that node isn't connected yet to another host with same name
                # if host.name in [current_host.name for current_host, current_host_proxy in self.__host_proxies.items()]:
                #     raise AtbError(AtbError.DUPLICATED_NAME)

                trace(trace_class="ATB", info="AtbNode::__get_host_proxy: no proxy found, instantiate new one")

                # Instantiate a new proxy and reference it in node.It will 
                # fail if an host with same name is already referenced
                host_proxy = AtbHostProxy(host)
                self.reference(host_proxy, host.name)
                self.__host_proxies[host] = host_proxy
                
        return host_proxy
