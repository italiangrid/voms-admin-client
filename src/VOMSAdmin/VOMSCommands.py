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
#     Andrea Ceccanti (INFN)
#

import xml.dom.minidom, re, sys, os.path, urllib2, httplib
import simplejson as json

from VOMSAdminService import VOMSAdmin
from VOMSAttributesService import VOMSAttributes
from VOMSACLService import VOMSACL
from VOMSCertificateService import VOMSCertificate
from X509Helper import X509Helper
from VOMSCommandsDef import commands_def
from VOMSPermission import parse_permissions
from VOMSAdmin import __version__, __commands__
from xml.parsers.expat import ExpatError
from urllib2 import HTTPError, URLError
import simplejson

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):

    def __init__(self, key, cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert
    
    def https_open(self, req):
        return self.do_open(self.getConnection, req)

    def getConnection(self, host):
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)



def command_argument_factory(type):
    
    if type == "X509":
        return X509Argument()
    elif type == "User":
        return UserArgument()
    elif type == "Group":
        return GroupArgument()
    elif type == "Role":
        return RoleArgument()
    elif type == "String":
        return StringArgument()
    elif type == "Boolean":
        return BooleanArgument()
    elif type == "Permission":
        return PermissionArgument()
    else:
        raise RuntimeError, "Argument type unknown!"
 
class CommandArgument:
    def __init__(self):
        self.value = None
        self.missing_arg_msg = "Missing argument!"
        self.nillable = False
        
    def parse(self, cmd, args, options):
        
        self.check_length(cmd, args, 1)
        val = args.pop(0)
        return [val]
    
    def check_length(self, cmd, args, min_length):
                   
        if len(args) < min_length:
            raise RuntimeError, self.missing_arg_msg
        
        for i in args[:min_length]:
            if unicode(i,'utf-8') in supported_commands.keys():
                raise RuntimeError, "Found command '%s' while parsing arguments for command '%s'!" % (i,cmd.name)
        

class StringArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing string argument!"

class BooleanArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing boolean argument!"
    
    def parse(self, cmd, args, options):
        self.check_length(cmd, args, 1)
        bool = args.pop(0)
        ret_val = False
        if bool == '0' or bool == 'false' or bool == 'False' or bool == 'FALSE':
            ret_val = False
        elif bool == '1' or bool == 'true' or bool == 'True' or bool == 'TRUE':
            ret_val = True
        
        return [ret_val]
        

class X509Argument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing X509 cert argument!"
    
    def parse(self, cmd, args, options):
        
        if options.has_key("nousercert"):
            self.check_length(cmd, args, 4)
            dn = args.pop(0)
            ca = args.pop(0)
            cn = args.pop(0)
            mail = args.pop(0)
        
            return [dn,ca,cn,mail]
        else:
            
            self.check_length(cmd=cmd, args=args, min_length=1)
            cert = X509Helper(args.pop(0))
            
            return [cert.subject,cert.issuer,None,cert.email]
        
    
class UserArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing user argument!"
        
    def parse(self, cmd, args, options):
        
        if options.has_key("nousercert"):
            self.missing_arg_msg = "Please specify DN and CA for the user!"
            self.check_length(cmd, args, 2)
            dn = args.pop(0)
            ca = args.pop(0)
            return [dn,ca]
        else:
            self.check_length(cmd=cmd, args=args, min_length=1)
            cert = X509Helper(args.pop(0))
            return [cert.subject,cert.issuer]
      

class GroupArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing group argument!"
    
    def parse(self,cmd,args, options):
        self.check_length(cmd, args, 1)
        group = args.pop(0)
        if group.strip() == "VO":
            return ["/"+options['vo']]
        else:
            return [group]
    
class RoleArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing role argument!"
    
    def parse(self, cmd, args, options):
        self.check_length(cmd, args, 1)
        role = args.pop(0)
        if not role.strip().startswith("Role="):
            return ["Role="+role]
        else:
            return [role]

class PermissionArgument(CommandArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing permission argument!"
        
    def parse(self, cmd, args, options):
        self.check_length(cmd, args, 1)
        perm_str  = args.pop(0)
        permission = parse_permissions(perm_str)
        
        return [permission.bits]        
        
        
class Command:
    def __init__(self, name, desc=None, help_str=None):
        self.name = name
        self.desc = desc
        self.arg_types = []
        self.help_str = help_str
        self.group_name=None
        self.group_short_name=None

    def add_arg(self,arg):
        self.arg_types.append(arg)
    
    def num_args(self):
        return len(self.arg_types)
    
    def __repr__(self):

        return "%s(%s)" % (self.name,
                              ",".join([e.__class__.__name__ for e in self.arg_types]))
                          

class UserCommand(Command):
    def __init__(self,cmd, arg_list=[]):
        Command.__init__(self, cmd.name, cmd.desc, cmd.help_str)
        self.arg_types = cmd.arg_types
        self.arg_list = arg_list

    def parse_args(self,cmd_line, options=None):
        
        for i in self.arg_types:
            self.arg_list= self.arg_list + i.parse(cmd=self,args=cmd_line,options=options)
        
    def help(self):
        return "Usage:\n%s\n\t%s\n" % (self.desc, self.help_str)

def _parse_commands():
    
    def get_text(nodelist):
        text = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                text = text + node.data
        return text
    
    command_hash = {}
    grouped_commands_hash = {}
    
    doc = xml.dom.minidom.parseString(commands_def)
    
    for c in doc.getElementsByTagName("command"):
                    
        cmd_name = c.getAttribute("name")     
        cmd = Command(name=cmd_name)
               
        for child in c.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                if child.nodeName == "description":
                    cmd.desc = get_text(child.childNodes).strip()
                elif child.nodeName == "help-string":
                    cmd.help_str = get_text(child.childNodes)
                elif child.nodeName == "arg":
                    _arg = command_argument_factory(child.getAttribute("type"))
                    cmd.add_arg(_arg)

        ## Get command group from parent node
        if not (c.parentNode is None):
            cmd.group_name = c.parentNode.getAttribute("name")
                        
            if grouped_commands_hash.has_key(cmd.group_name):
                grouped_commands_hash[cmd.group_name].append(cmd)
            else:
                grouped_commands_hash[cmd.group_name] = [cmd]
        
        command_hash[cmd.name]= cmd
        
        
    
    return command_hash, grouped_commands_hash

supported_commands, grouped_commands = _parse_commands()

def print_version():  
    print "voms-admin v.", __version__

def print_supported_commands():
    print "Supported commands list:"
    print
    for group in grouped_commands.keys():
        
        print group.upper()+":\n\n", "\n".join(["  "+c.name for c in grouped_commands[group]])
        print
    
def print_supported_commands_help():
    print "Supported commands and usage info:"
    print
#    for v in supported_commands.values():
#        print v.desc
#        print "\t", v.help_str
    for group in grouped_commands.keys():
        print group.upper(),":\n\n"
        for c in grouped_commands[group]:
            print c.desc
            print c.help_str
            print
        print "\n\n"
        

def unknown_command(cmd):
    print "Unknown command: %s" % cmd
    print "To get a list of supported commands, type:\n\n\tvoms-admin --list-commands"
    sys.exit(1)
    
    
def print_command_help(cmd):
    if not supported_commands.has_key(cmd):
            unknown_command(cmd)
    
    c = supported_commands[cmd]
    print
    print c.desc
    print "\t", c.help_str
    print

def parse_commands(args, options):
    commands = []
   
    while len(args)>0:
        
        cmd = args.pop(0).strip()
        if not supported_commands.has_key(cmd):
            unknown_command(cmd)
                            
        usr_cmd = UserCommand(supported_commands[cmd])
        usr_cmd.parse_args(args, options)
        
        commands.append(usr_cmd)
    
    return commands

class VOMSAdminProxy:
    def __init__(self,*args, **kw):
        self.base_url = "https://%s:%s/voms/%s/services" % (kw['host'],
                                                            kw['port'],
                                                            kw['vo'])
        
        self.rest_base_url = "https://%s:%s/voms/%s/ajax" % (kw['host'],
                                                            kw['port'],
                                                            kw['vo'])
                
        self.url_opener = urllib2.build_opener(HTTPSClientAuthHandler(key=kw['user_key'], cert=kw['user_cert']))
        
        transdict = {
                     "cert_file":kw['user_cert'], 
                     "key_file":kw['user_key']
                     }
        
        
        self.services = { 
                         "admin": VOMSAdmin(url=self.base_url+"/VOMSAdmin", transdict=transdict),
                         "attributes": VOMSAttributes(url=self.base_url+"/VOMSAttributes", transdict=transdict),
                         "acl": VOMSACL(url=self.base_url+"/VOMSACL", transdict=transdict),
                         "certificates": VOMSCertificate(url=self.base_url+"/VOMSCertificates", transdict=transdict)
                         }
        
        
        for s in self.services.values():
            s.port.binding.AddHeader("X-VOMS-CSRF-GUARD", "")
            
        
    
    def transname(self, method_name):
        def f(m):
            return m.group(2).upper()
        
        return re.sub("(-(.))",f,method_name)
    
    
    def call_method(self, method_name, *args, **kw):
        mn = self.transname(method_name)
        
        if self.__class__.__dict__.has_key(mn):
            return self.__class__.__dict__[mn](self,*args,**kw)
        
        else:
            for service in self.services.values():
                if service.__class__.__dict__.has_key(mn):
                    return service.__class__.__dict__[mn](service, *args, **kw)
            
            raise RuntimeError, "Unkown method '%s'!" %mn
    
        
    def listUsers(self):
        users = self.services["admin"].listUsers()
        if users is None:
            return "No users found in vo!"
        
        return users
    
    def listMembers(self,group):
        members = self.services["admin"].listMembers(group)
        if members is None:
            return "No members found in group %s" % group
        else:
            return members
    
    def getDefaultACL(self,group):
        defaultACL = self.services["acl"].getDefaultACL(group)
        if defaultACL is None:
            return "Default ACL not defined for group %s" % group
        else:
            return defaultACL
    
    def __httpGet(self, action):
        url = "%s/%s" % (self.rest_base_url, action)
        
        try:
            f = self.url_opener.open(url)
        except HTTPError, e:
            raise RuntimeError, "The server could not answer the request for %s. %s" % (url,e)
        except URLError, e:
            raise RuntimeError, "Error contacting remote server: %s. Error: %s" % (url, e)
        
        return simplejson.load(f) 
    
    def __getUserStats(self):
        return self.__httpGet('user-stats.action')
    
    def __getSuspendedUsers(self):
        return self.__httpGet('suspended-users.action')
    
    def __getExpiredUsers(self):
        return self.__httpGet('expired-users.action')
    
    def __printUserList(self, user_list):
        for u in user_list:
            
            name = "%s %s" %(u['name'],u['surname'])
                
            if len(u['name']) == 0 and len(u['surname']) == 0:
                ## Use certificate subject if name is not defined for this
                ## user
                name = u['certificates'][0]['subjectString']
            
            if u['suspended']:
                status = "Suspended.  Reason: %s" % u['suspensionReason']
            else:
                status = "Active."
                
            print "%s (%d) - %s" % (name, u['id'],status)
        
    def countUsers(self):
        res = self.__getUserStats()
        print "User count: %d" % res['usersCount']        
    
    def countSuspendedUsers(self):
        res = self.__getUserStats()
        print "Suspended user count: %d" % res['suspendedUsersCount']
    
    def countExpiredUsers(self):
        res = self.__getUserStats()
        print "Expired user count: %d" % res['expiredUsersCount']
        
    def listSuspendedUsers(self):
        res = self.__getSuspendedUsers()
        if len(res['suspendedUsers']) == 0:
            print "No suspended users found."
        else:
            self.__printUserList(res['suspendedUsers'])
    
    def listExpiredUsers(self):
        res = self.__getExpiredUsers()
        
        if len(res['expiredUsers']) == 0:
            print "No expired users found."
        else:
            self.__printUserList(res['expiredUsers'])
    
    def listUserStats(self):
        res = self.__getUserStats()
        for k in res.keys():
            print "%s = %s " % (k,res[k])
        
        