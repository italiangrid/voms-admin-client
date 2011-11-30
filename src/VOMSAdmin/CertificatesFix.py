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

from VOMSCertificatesService_services_types import *

import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
import ZSI

serviceNameSpace = "http://glite.org/wsdl/services/org.glite.security.voms.service.certificates"

_getCertificatesRequestTypecode = Struct(pname=(serviceNameSpace,"getCertificates"), 
                                         ofwhat=[ZSI.TC.String(pname="subject", aname="_subject", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True), ZSI.TC.String(pname="issuer", aname="_issuer", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                         pyclass=None, encoded=serviceNameSpace)
class getCertificatesRequest:
    typecode = _getCertificatesRequestTypecode
    __metaclass__ = pyclass_type
    def __init__(self):
        self._subject = None
        self._issuer = None
        return
getCertificatesRequest.typecode.pyclass = getCertificatesRequest

_getCertificatesResponseTypecode = Struct(pname=("http://glite.org/wsdl/services/org.glite.security.voms.service.certificates","getCertificatesResponse"), ofwhat=[ns0.ArrayOfX509Certificate_Def(pname="getCertificatesReturn", aname="_getCertificatesReturn", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.certificates")
class getCertificatesResponse:
    typecode = _getCertificatesResponseTypecode
    __metaclass__ = pyclass_type
    def __init__(self):
        self._getCertificatesReturn = None
        return
getCertificatesResponse.typecode.pyclass = getCertificatesResponse

_addCertificateRequestTypecode = Struct(pname=(serviceNameSpace,"addCertificate"), 
                                        ofwhat=[ZSI.TC.String(pname="registeredCertSubject", aname="_registeredCertSubject", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=False), 
                                                ZSI.TC.String(pname="registeredCertIssuer", aname="_registeredCertIssuer", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=False), 
                                                ns0.X509Certificate_Def(pname="cert", aname="_cert", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=True)], 
                                                pyclass=None, encoded=serviceNameSpace)
class addCertificateRequest:
    typecode = _addCertificateRequestTypecode
    __metaclass__ = pyclass_type
    def __init__(self):
        self._registeredCertSubject = None
        self._registeredCertIssuer = None
        self._cert = None
        return
addCertificateRequest.typecode.pyclass = addCertificateRequest

_addCertificateResponseTypecode = Struct(pname=(serviceNameSpace,"addCertificateResponse"), ofwhat=[], pyclass=None, encoded="http://glite.org/wsdl/services/org.glite.security.voms.service.certificates")
class addCertificateResponse:
    typecode = _addCertificateResponseTypecode
    __metaclass__ = pyclass_type
    def __init__(self):
        return
addCertificateResponse.typecode.pyclass = addCertificateResponse

_restoreCertificateRequestTypecode = Struct(pname=(serviceNameSpace,"restoreCertificate"), 
                                        ofwhat=[ns0.X509Certificate_Def(pname="cert", aname="_cert", typed=False, encoded=None, minOccurs=1, maxOccurs=1, nillable=False)], 
                                                pyclass=None, encoded=serviceNameSpace)

class restoreCertificateRequest:
    typecode = _restoreCertificateRequestTypecode
    __metaclass__ = pyclass_type
    def __init__(self):
        self._cert = None
        return
restoreCertificateRequest.typecode.pyclass = restoreCertificateRequest

_restoreCertificateResponseTypecode = Struct(pname=(serviceNameSpace,"restoreCertificateResponse"), ofwhat=[], pyclass=None, encoded=serviceNameSpace)

class restoreCertificateResponse:
    typecode = _restoreCertificateResponseTypecode
    __metaclass__ = pyclass_type
     
    def __init__(self):
        return

restoreCertificateResponse.typecode.pyclass = restoreCertificateResponse

     


    