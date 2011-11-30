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

from VOMSAttributesService_services import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
import ZSI


_createAttributeClassRequestTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","createAttributeClass"), 
                                              ofwhat=[ZSI.TC.String(pname="name", aname="_name", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=False),
                                                      ZSI.TC.String(pname="description", aname="_description", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True),
                                                      ZSI.TC.Boolean(pname="unique", aname="_unique", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)
                                                      ], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class createAttributeClassRequest:
    typecode = _createAttributeClassRequestTypecode
    def __init__(self):
        self._name = None
        self._description = None
        self._unique = None
        return

createAttributeClassRequest.typecode.pyclass = createAttributeClassRequest

_createAttributeClassResponseTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","createAttributeClassResponse"), ofwhat=[], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")

class createAttributeClassResponse:
    typecode = _createAttributeClassResponseTypecode
    def __init__(self):
        return
createAttributeClassResponse.typecode.pyclass = createAttributeClassResponse

_deleteAttributeClassRequestTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteAttributeClass"), 
                                              ofwhat=[ZSI.TC.String(pname="name", aname="_name", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=False)], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteAttributeClassRequest:
    typecode = _deleteAttributeClassRequestTypecode

    def __init__(self):
        self._name = None
        return
deleteAttributeClassRequest.typecode.pyclass = deleteAttributeClassRequest

_deleteAttributeClassResponseTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteAttributeClassResponse"), ofwhat=[], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteAttributeClassResponse:
    typecode = _deleteAttributeClassResponseTypecode

    def __init__(self):
        return
deleteAttributeClassResponse.typecode.pyclass = deleteAttributeClassResponse

_deleteUserAttributeRequestTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteUserAttribute"), 
                                              ofwhat=[ns0.User_Def(pname="user", aname="_user", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), 
                                                      ZSI.TC.String(pname="attrName", aname="_attrName", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                              pyclass=None, 
                                              encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteUserAttributeRequest:
    typecode = _deleteUserAttributeRequestTypecode

    def __init__(self):
        self._user = None
        self._attrName = None
        return
deleteUserAttributeRequest.typecode.pyclass = deleteUserAttributeRequest

_deleteUserAttributeResponseTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteUserAttributeResponse"), ofwhat=[], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteUserAttributeResponse:
    typecode = _deleteUserAttributeResponseTypecode

    def __init__(self):
        return
deleteUserAttributeResponse.typecode.pyclass = deleteUserAttributeResponse

_deleteGroupAttributeRequestTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteGroupAttribute"), 
                                              ofwhat=[ZSI.TC.String(pname="group", aname="_group", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), 
                                                      ZSI.TC.String(pname="attrName", aname="_attrName", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                              pyclass=None, 
                                              encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteGroupAttributeRequest:
    typecode = _deleteGroupAttributeRequestTypecode

    def __init__(self):
        self._group = None
        self._attrName = None
        return
deleteGroupAttributeRequest.typecode.pyclass = deleteGroupAttributeRequest

_deleteGroupAttributeResponseTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteGroupAttributeResponse"), 
                                               ofwhat=[], 
                                               pyclass=None, 
                                               encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteGroupAttributeResponse:
    typecode = _deleteGroupAttributeResponseTypecode

    def __init__(self):
        return
deleteGroupAttributeResponse.typecode.pyclass = deleteGroupAttributeResponse

_deleteRoleAttributeRequestTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteRoleAttribute"), 
                                             ofwhat=[ZSI.TC.String(pname="group", aname="_group", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), 
                                                     ZSI.TC.String(pname="role", aname="_role", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), 
                                                     ZSI.TC.String(pname="attrName", aname="_attrName", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                             pyclass=None, 
                                             encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteRoleAttributeRequest:
    typecode = _deleteRoleAttributeRequestTypecode

    def __init__(self):
        self._group = None
        self._role = None
        self._attrName = None
        return

deleteRoleAttributeRequest.typecode.pyclass = deleteRoleAttributeRequest

_deleteRoleAttributeResponseTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.attributes","deleteRoleAttributeResponse"), 
                                              ofwhat=[], 
                                              pyclass=None, 
                                              encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.attributes")
class deleteRoleAttributeResponse:
    typecode = _deleteRoleAttributeResponseTypecode

    def __init__(self):
        return
deleteRoleAttributeResponse.typecode.pyclass = deleteRoleAttributeResponse

