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

import commands, re, os.path

class X509Helper:
    def __init__(self,filename, openssl_cmd=None):    
        self.filename= filename
        
        ## Check that the filename passed as argument actually exists
        if not os.path.exists(filename):
            raise RuntimeError("Certificate path '%s' passed as argument does not exist!" % (filename))
        
        self.openssl_cmd = openssl_cmd
        self.parse()
    
    def parse(self):        
        if self.openssl_cmd:
            openssl = self.openssl_cmd
        else:
            openssl = 'openssl'
        
        base_cmd = openssl+' x509 -in %s -noout ' % self.filename
        
        status,subject = commands.getstatusoutput(base_cmd+'-subject')
        if status:
            raise RuntimeError, "Error invoking openssl: "+ subject
        
        status,issuer = commands.getstatusoutput(base_cmd+'-issuer')
        if status:
            raise RuntimeError, "Error invoking openssl: "+ issuer
        
        
        status,email = commands.getstatusoutput(base_cmd+'-email')
        if status:
            raise RuntimeError, "Error invoking openssl: "+ email
        
        self.subject = re.sub(r'^subject= ','',subject.strip())
        self.issuer = re.sub(r'^issuer= ','',issuer.strip())
        self.subject = re.sub(r'/(E|e|((E|e|)(mail|mailAddress|mailaddress|MAIL|MAILADDRESS)))=','/Email=',self.subject)
        
        # Handle also UID
        self.subject = re.sub(r'/(UserId|USERID|userId|userid|uid|Uid)=','/UID=',self.subject)
        
        # Strip white spaces from emails
        self.email = email.strip()
        
        # Check that only first email address is taken from the certificate, the openssl -email command
        # returns one address per line
        emails = email.splitlines(False)
        
        if len(emails) > 0:
            self.email = emails[0]
        else:
            self.email = None
    
    def __repr__(self):
        return 'Subject:%s\nIssuer:%s\nEmail:%s' % (self.subject, self.issuer, self.email)