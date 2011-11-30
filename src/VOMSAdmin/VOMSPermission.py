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

import re

def parse_permissions(permString):
    p  = VOMSPermission()
    p.parse(permString)
    return p
    
class VOMSPermission:
    
    permissions = [
     'CONTAINER_READ', 
     'CONTAINER_WRITE', 
     'MEMBERSHIP_READ', 
     'MEMBERSHIP_WRITE', 
     'ACL_READ', 
     'ACL_WRITE', 
     'ACL_DEFAULT', 
     'REQUESTS_READ', 
     'REQUESTS_WRITE', 
     'ATTRIBUTES_READ', 
     'ATTRIBUTES_WRITE',
     'PERSONAL_INFO_READ',
     'PERSONAL_INFO_WRITE',
     'SUSPEND']
    
    all_permission_mask = 2**(len(permissions))-1
    
    def __init__(self, bitsIn=0):
        self.bits = bitsIn
    
    def __repr__(self):
        if self.bits == 0:
            return "NONE"
        
        if (self.test(VOMSPermission.all_permission_mask)):
            return "ALL"
        
        perm_list = []
        
        for index in range(len(VOMSPermission.permissions)):
            mask = 1 << index
            if self.test(mask):
                perm_list.append(VOMSPermission.permissions[index])
        
        return ",".join(perm_list)
            
        
    def set(self, perm):
        if perm < 0:
            raise RuntimeError,"permission must be a positive integer!"
        
        self.bits |= perm
    
    def unset(self,perm):
        if perm < 0:
            raise RuntimeError,"permission must be a positive integer!"
        self.bits &= ~perm
    
    def test(self, perm):
        if perm < 0:
            raise RuntimeError,"permission must be a positive integer!"
        return ((self.bits & perm) == perm)
            
    def parse(self, permText):
        perms = re.split(",", permText)
        
        for p in perms:
            p = p.strip()
            if len(p) == 0:
                continue 
            
            if p == "ALL":
                self.set(VOMSPermission.all_permission_mask)
                return
            
            try:
                index = VOMSPermission.permissions.index(p)
            except ValueError:
                raise ValueError, "%s is not a supported VOMSPermission" % p
            
            self.set(2**index)        