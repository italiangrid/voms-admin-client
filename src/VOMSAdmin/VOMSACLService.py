#
# Copyright (c) Members of the EGEE Collaboration. 2006-2009.
# See http://www.eu-egee.org/partners/ for details on the copyright holders.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# 	Andrea Ceccanti (INFN)
#

from VOMSACLService_services import *
from socket import error
import sys

anyone_aliases = ['ANYONE','ANYUSER','ANY_AUTHENTICATED_USER','EVERYONE', 'ANY']
unauthenticated_aliases = [ 'UNAUTHENTICATED', 'UNAUTH']
vomsca_aliases = ['VOMS_CA','VOMSCA', 'VOMS']
groupca_aliases = ['GROUPCA', 'GROUP_CA', 'GROUP']
roleca_aliases = ['ROLECA','ROLE_CA','ROLE']
        
class VOMSACL:
    def __init__(self, **kw):
        self.port = VOMSACLSoapBindingSOAP(**kw)
        
    
    def _callRemoteMethod(self, method_name, *args, **kw):
        
        try:
            res = self.port.__class__.__dict__[method_name](self.port, *args, **kw)
            return res
        
        except TypeError, e:
            print "Error deserializing SOAP response:", e
            print "This is very probably caused by the VO being inactive..."
            sys.exit(3)
        
        except error, e:
            print "Socket error: ", e
            sys.exit(2)        
        
        except Exception, ex:
            print ex
            sys.exit(1)
    
    
    def _parse_admin(self, dn,ca):    
        
        if dn in unauthenticated_aliases and ca in vomsca_aliases:
            dn = "/O=VOMS/O=System/CN=Unauthenticated Client"
            ca = "/O=VOMS/O=System/CN=Dummy Certificate Authority"

        if dn in anyone_aliases and ca in vomsca_aliases:
            dn = "/O=VOMS/O=System/CN=Any Authenticated User"
            ca = "/O=VOMS/O=System/CN=Dummy Certificate Authority"
            
        elif ca in groupca_aliases:
            ca = "/O=VOMS/O=System/CN=VOMS Group"
        
        elif ca in roleca_aliases:
            ca = "/O=VOMS/O=System/CN=VOMS Role"
        
        return (dn,ca)

    def getACL(self, container):
        method_name = self.port.getACL.__name__

        request = getACLRequest()
        request._in0 = container
        
        ## Insert arguments here, if any...

        response = self._callRemoteMethod(method_name, request)
        return response._getACLReturn
    
    def getDefaultACL(self,group):
        method_name = self.port.getDefaultACL.__name__

        request = getDefaultACLRequest()

        ## Insert arguments here, if any...
        request._in0 = group


        response = self._callRemoteMethod(method_name, request)
        return response._getDefaultACLReturn
    
    def addACLEntry(self,container,dn,ca,perm_bits,propagate):
        method_name = self.port.addACLEntry.__name__

        request = addACLEntryRequest()

        dn,ca = self._parse_admin(dn, ca)
                
        entry = ns2.ACLEntry_Def(None)
        entry._adminSubject = dn
        entry._adminIssuer = ca
        entry._vomsPermissionBits = perm_bits
                
        ## Insert arguments here, if any...
        request._in0 = container
        request._in1 = entry
        request._in2 = propagate

        response = self._callRemoteMethod(method_name, request)
        return
    
    def addDefaultACLEntry(self,container,dn,ca,perm_bits):
        method_name = self.port.addDefaultACLEntry.__name__

        request = addDefaultACLEntryRequest()
        
        dn,ca = self._parse_admin(dn, ca)
        
        entry = ns2.ACLEntry_Def(None)
        entry._adminSubject = dn
        entry._adminIssuer = ca
        entry._vomsPermissionBits = perm_bits
        
		## Insert arguments here, if any...
        request._in0 = container
        request._in1 = entry

        response = self._callRemoteMethod(method_name, request)
        return
    
    def removeACLEntry(self,container, dn,ca, propagate):
        method_name = self.port.removeACLEntry.__name__

        request = removeACLEntryRequest()
        
        dn,ca = self._parse_admin(dn, ca)
        
        entry = ns2.ACLEntry_Def(None)
        entry._adminSubject = dn
        entry._adminIssuer = ca
        entry._vomsPermissionBits = 0
        
        ## Insert arguments here, if any...
        request._in0 = container
        request._in1 = entry
        request._in2 = propagate

        response = self._callRemoteMethod(method_name, request)
        return
    
    def removeDefaultACLEntry(self, group, dn, ca):
        method_name = self.port.removeDefaultACLEntry.__name__

        request = removeDefaultACLEntryRequest()
        
        dn,ca = self._parse_admin(dn, ca)
        
        entry = ns2.ACLEntry_Def(None)
        entry._adminSubject = dn
        entry._adminIssuer = ca
        entry._vomsPermissionBits = 0
        
        ## Insert arguments here, if any...
        request._in0 = group
        request._in1 = entry

        response = self._callRemoteMethod(method_name, request)
        return        
        







    
    
    
    



        
