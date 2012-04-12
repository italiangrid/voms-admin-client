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

from AttributesFix import *
from VOMSAttributesService_services import *
from VOMSAttributesService_services_types import *
from socket import error
import sys

class VOMSAttributes:
    def __init__(self, **kw):
        self.port = VOMSAttributesSoapBindingSOAP(**kw)
    
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
    
    def createAttributeClass(self,name, description, unique):
        method_name = self.port.createAttributeClass.__name__
        request = createAttributeClassRequest()
        
        request._name = name
        request._description = description
        request._unique = unique
        
        response = self._callRemoteMethod(method_name,request)
    
    def deleteAttributeClass(self, name):
        method_name = self.port.deleteAttributeClass.__name__
        request = deleteAttributeClassRequest()
        
        request._name = name
        
        response = self._callRemoteMethod(method_name,request)
    
    def listAttributeClasses(self):
        method_name = self.port.listAttributeClasses.__name__
        
        request = listAttributeClassesRequest()
        
        response = self._callRemoteMethod(method_name,request)
        return response._listAttributeClassesReturn
    
    
    def setUserAttribute(self,dn,ca,attrName,attrValue):
        method_name = self.port.setUserAttribute.__name__
        request = setUserAttributeRequest()
        
        user = ns0.User_Def(None)
        attr_val = ns1.AttributeValue_Def(None)
        
        user._DN = dn
        user._CA = ca
        
        attr_val._attributeClass = ns1.AttributeClass_Def(None)
        attr_val._attributeClass._name = attrName
        attr_val._attributeClass._uniquenessChecked = False
        attr_val._value = attrValue
        
        request._in0 = user
        request._in1 = attr_val
        response = self._callRemoteMethod(method_name,request)
        
    
    def deleteUserAttribute(self, dn,ca, attrName):
        method_name = self.port.deleteUserAttribute.__name__
        
        request = deleteUserAttributeRequest()
        
        user = ns0.User_Def(None)
        user._DN = dn
        user._CA = ca
                
        request._user = user
        request._attrName = attrName
        response = self._callRemoteMethod(method_name,request)
        
    def listUserAttributes(self,dn,ca):
        method_name = self.port.listUserAttributes.__name__
        
        request = listUserAttributesRequest()
        
        u = ns0.User_Def(None)
        u._DN = dn
        u._CA = ca
        
        request._in0 = u
        
        response = self._callRemoteMethod(method_name,request)
        return response._listUserAttributesReturn
        
    def setGroupAttribute(self,group,attrName,attrValue):
        method_name = self.port.setGroupAttribute.__name__
        request = setGroupAttributeRequest()
        
        attr_val = ns1.AttributeValue_Def(None)
        attr_val._attributeClass = ns1.AttributeClass_Def(None)
        attr_val._attributeClass._name = attrName
        attr_val._attributeClass._uniquenessChecked = False
        attr_val._value = attrValue
        
        request._in0 = group
        request._in1 = attr_val
        
        response = self._callRemoteMethod(method_name,request)
    
    def deleteGroupAttribute(self, group, attrName):
        method_name = self.port.deleteGroupAttribute.__name__
        
        
        attr_class = ns1.AttributeClass_Def(None)
        attr_class._name = attrName
        attr_class._uniquenessChecked = False
        
        request = deleteGroupAttributeRequest1()
        request._in0 = group
        request._in1 = ns1.AttributeValue_Def(None)
        request._in1._attributeClass = attr_class
        
        
        response = self._callRemoteMethod(method_name,request)
    
    def listGroupAttributes(self,group):
        method_name = self.port.listGroupAttributes.__name__
        
        request = listGroupAttributesRequest()
        
        request._in0 = group
        response = self._callRemoteMethod(method_name,request)
        
        return response._listGroupAttributesReturn
    
    def setRoleAttribute(self,group, role,attrName,attrValue):
        method_name = self.port.setRoleAttribute.__name__
        request = setRoleAttributeRequest()
        
        attr_val = ns1.AttributeValue_Def(None)
        attr_val._attributeClass = ns1.AttributeClass_Def(None)
        attr_val._attributeClass._name = attrName
        attr_val._attributeClass._uniquenessChecked = False
        attr_val._value = attrValue

        request._in0 = group
        request._in1 = role
        request._in2 = attr_val
        
        response = self._callRemoteMethod(method_name,request)
        
    def deleteRoleAttribute(self, group, role, attrName):
        method_name = self.port.deleteRoleAttribute.__name__
        
        attr_val = ns1.AttributeValue_Def(None)
        attr_val._attributeClass = ns1.AttributeClass_Def(None)
        attr_val._attributeClass._name = attrName
        attr_val._attributeClass._uniquenessChecked = False
        
        request = deleteRoleAttributeRequest1()
        request._in0 = group
        request._in1 = role
        request._in2 = attr_val
        
        response = self._callRemoteMethod(method_name,request)
        
        
    def listRoleAttributes(self, group, role):
        method_name = self.port.listRoleAttributes.__name__
        request = listRoleAttributesRequest()
        
        request._in0 = group
        request._in1 = role
        response = self._callRemoteMethod(method_name,request)
        
        return response._listRoleAttributesReturn