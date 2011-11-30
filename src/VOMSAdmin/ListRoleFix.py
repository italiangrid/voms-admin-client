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

from VOMSAdminService_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
import ZSI

class listRolesRequest:
    def __init__(self):
        self._in0 = None
        self._in1 = None
        return
listRolesRequest.typecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.admin","listRoles"), 
                                   ofwhat=[], 
                                   pyclass=listRolesRequest, 
                                   encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.admin")

class listRolesResponse:
    def __init__(self):
        self._listRolesReturn = None
        return
listRolesResponse.typecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.admin","listRolesResponse"), 
                                    ofwhat=[ns1.ArrayOf_soapenc_string_Def(pname="listRolesReturn", aname="_listRolesReturn", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                    pyclass=listRolesResponse, 
                                    encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.admin")
