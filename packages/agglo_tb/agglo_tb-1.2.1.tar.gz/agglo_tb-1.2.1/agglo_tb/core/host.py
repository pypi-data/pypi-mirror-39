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

from ..exceptions import AtbHostError
from .._private.host_interface_proxy import AtbHostInterfaceProxy 


__all__ = ["AtbHost"]

class AtbHost(AtkROReferencer):
    
    INTERFACES_LIST_ID = AtkROReferencer.DEFAULT_LIST_ID

    def __init__(self, name):
        trace(trace_class="ATB", info="AtbHost::instantiate host " + name)
        
        AtkROReferencer.__init__(self)
        self.__name = name

        
    @property
    def name(self):
        return self.__name

    
    # TODO ou retourner une map ?
    @property
    def interfaces(self):
        return list(self._referenced_items[AtbHost.INTERFACES_LIST_ID].values())

        
    def __iter__(self):
        for _interface in self.interfaces:
            yield _interface
        
        
    def __contains__(self, interface):
        return interface in self.interfaces


    def add_interface(self, interface):
        trace(trace_class="ATB", info="AtbHost::add_interface " + interface.name + \
                                      " to host " + self.name)

        # If interface already belongs to an host     
        if interface.host is not None:
            if interface.host is not self:
                raise AtbHostError(AtbHostError.CONFLICT)
        else:
            # Reference new interface. It will fail if an interface 
            # with same name is already referenced
            interface_proxy = AtbHostInterfaceProxy(interface)
            self.reference(interface_proxy, interface.name, AtbHost.INTERFACES_LIST_ID)

            # Attach interface to host
            interface.set_host(self)
