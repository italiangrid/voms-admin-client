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

from VOMSCertificatesService_services import *
from VOMSCertificatesService_services_types import ns0 
from socket import error
from CertificatesFix import *
import sys

class VOMSCertificate:
    def __init__(self, **kw):
        self.port = VOMSCertificatesSoapBindingSOAP(**kw)
        
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
    
    
    def getUserIdFromDn(self,dn,ca):
        method_name = self.port.getUserIdFromDn.__name__
        
        request = getUserIdFromDnRequest()
        request._subject = dn
        request._issuer = ca
        
        response = self._callRemoteMethod(method_name,request)
        return response._getUserIdFromDnReturn
    
    def getCertificates(self, dn, ca):
        method_name = self.port.getCertificates.__name__
        request = getCertificatesRequest()
        
        request._subject = dn
        request._issuer = ca
        response = self._callRemoteMethod(method_name,request)
        return response._getCertificatesReturn
    
    def addCertificate(self,regDn,regCa, certDn,certCa):
        method_name = self.port.addCertificate.__name__
        
        request = addCertificateRequest()
        request._registeredCertSubject =regDn
        request._registeredCertIssuer = regCa
        request._cert = ns0.X509Certificate_Def(None)
        request._cert._subject = certDn
        request._cert._issuer = certCa
        response = self._callRemoteMethod(method_name,request)
        return
    
    def removeCertificate(self, certDn, certCA):
        method_name = self.port.removeCertificate.__name__
        
        request = removeCertificateRequest()
        
        request._cert = ns0.X509Certificate_Def(None)
        request._cert._subject = certDn
        request._cert._issuer = certCA
        
        response = self._callRemoteMethod(method_name,request)
        return
    
    def suspendCertificate(self, certDn, certCa, reason):
        method_name = self.port.suspendCertificate.__name__
        request = suspendCertificateRequest()
        
        request._cert = ns0.X509Certificate_Def(None)
        request._cert._subject = certDn
        request._cert._issuer = certCa
        
        request._reason = reason
        
        response = self._callRemoteMethod(method_name, request)
        return
    
    def restoreCertificate(self, certDn, certCA):
        method_name = self.port.restoreCertificate.__name__
        
        request = restoreCertificateRequest()
        
        request._cert = ns0.X509Certificate_Def(None)
        request._cert._subject = certDn
        request._cert._issuer = certCA
        
        response = self._callRemoteMethod(method_name,request)
        return
    