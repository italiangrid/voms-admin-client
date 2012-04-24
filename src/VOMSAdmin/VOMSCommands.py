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

import xml.dom.minidom, re, sys, urllib2, httplib

from VOMSAdminService import VOMSAdmin
from VOMSAttributesService import VOMSAttributes
from VOMSACLService import VOMSACL
from VOMSCertificateService import VOMSCertificate
from X509Helper import X509Helper
from VOMSCommandsDef import commands_def
from VOMSPermission import parse_permissions
from VOMSAdmin import __version__
from urllib2 import HTTPError, URLError
import simplejson


personal_info_arguments = ["name",
                           "surname",
                           "address",
                           "institution",
                           "phoneNumber"]

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):

    def __init__(self, key, cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert
    
    def https_open(self, req):
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=None):
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
    elif type == "X509v2":
        return X509ArgumentV2()
    elif type == "NewGroup":
        return NewGroupArgument()
    elif type == "UserV2":
        return UserArgumentV2()
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

class X509ArgumentV2(X509Argument):
    def __init__(self):
        self.missing_arg_msg = "Missing user argument!"
    
    def has_personal_info_options(self, options):
        
        has_all_args = True
        has_some_args = False
        
        for a in personal_info_arguments:
            if not options.has_key(a):
                has_all_args = False
            elif not has_some_args:
                has_some_args = True    
        
        if has_some_args and not has_all_args:
            raise RuntimeError, "Please specify *all* the following options when creating a user: %s" % ",".join(personal_info_arguments)
        
        return has_all_args
        
    
    def create_user_from_personal_info(self, options):
        usr = {}
        for a in personal_info_arguments:
            usr[a] = options[a]
            
        return usr 
    
    def parse(self, cmd, args, options):
        
        cert_args = X509Argument.parse(self, cmd, args, options)
        user = None
        result = []
        
        if self.has_personal_info_options(options):
            user = self.create_user_from_personal_info(options)
        
        result.append(user)
        result.extend(cert_args)
         
        return result


    
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

class UserArgumentV2(UserArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing user argument!"
        
    def parse(self, cmd, args, options):
        
        if options.has_key("id"):
            return [options["id"], None, None]
        else:
            return [None, UserArgument.parse(self, cmd, args, options)]

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

class NewGroupArgument(GroupArgument):
    def __init__(self):
        self.missing_arg_msg = "Missing user argument!"
    
    def parse(self, cmd, args, options):
        group_name = GroupArgument.parse(self, cmd, args, options)
        group_desc = None
        
        result = []
        
        if options.has_key('description'):
            group_desc = options['description']
        
        result.append(group_desc)
        result.extend(group_name)
        
        return result
        
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
        
        self.rest_base_url = "https://%s:%s/voms/%s/apiv2" % (kw['host'],
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
        
    def __httpRequest(self, action, data=None):
        url = "%s/%s" % (self.rest_base_url, action)
        
        req = urllib2.Request(url)
        
        req.add_header('X-VOMS-CSRF-GUARD','')
        
        if data != None:
            req.add_header('Content-Type', 'application/json')
            req.add_data(simplejson.dumps(data))
        
        return req
        
    
    def __httpCall(self, action, data=None):
        
        req = self.__httpRequest(action, data)
        
        try:
            f = self.url_opener.open(req)
        except HTTPError, e:
            raise RuntimeError, "The server could not answer the request for %s. %s" % (req.get_full_url(),e)
        except URLError, e:
            raise RuntimeError, "Error contacting remote server: %s. Error: %s" % (req.get_host(), e)
        
        result = simplejson.load(f)
        
        return result 
    
    def __restCall(self, action, data=None):
        res = self.__httpCall(action, data)
        self.__handleCallReturnValue(res)
        return res

    def __suspendUser(self, dn, ca, reason):
        return self.__restCall('suspend-user.action', {"certificateSubject": dn, 
                                                       "caSubject": ca, 
                                                       "suspensionReason": reason})
    
    def __restoreAllSuspendedUsers(self):
        return self.__restCall('restore-all-suspended-users.action')
        
    def __restoreUser(self, dn, ca):
        return self.__restCall('restore-user.action', {"certificateSubject": dn, "caSubject": ca})

    def __createUser(self,user,dn,ca):
        return self.__restCall('create-user.action', {'user':user, "certificateSubject": dn, "caSubject": ca})
    
    def __createGroup(self, name, description):
        return self.__restCall('create-group.action', {'groupName': name, 'groupDescription': description}) 
    
    def __getUserStats(self):
        return self.__httpCall('user-stats.action')
    
    def __getSuspendedUsers(self):
        return self.__httpCall('suspended-users.action')
    
    def __getExpiredUsers(self):
        return self.__httpCall('expired-users.action')
    
    def __printUserList(self, user_list):
        for u in user_list:
            
            cert = "%s,%s" %(u['certificates'][0]['subjectString'],u['certificates'][0]['issuerString'])
            
            if u['suspended']:
                status = "Suspended: %s" % u['suspensionReason']
            else:
                status = "Active"
            
            if u['name'] != None and u['surname'] != None:
                name = "%s %s (%d)" % (u['name'], u['surname'], u['id'])
            else:
                name = ""
            
            print "%s,%s,%s" % (cert, status, name)
    
    def __handleCallReturnValue(self, ret_val):        
        if ret_val is None:
            sys.exit(0)
            return
        
        exit_status = 0
        
        if ret_val.has_key('exceptionClass'):
            exit_status = 1
            print >>sys.stderr, "%s : %s" % (ret_val['exceptionClass'], ret_val['exceptionMessage'])
            
        if ret_val.has_key('actionErrors'):
            exit_status = 1
            for i in ret_val['actionErrors']:
                print >> sys.stderr, "Error: %s" % i 
        
        if ret_val.has_key('fieldErrors'):
            exit_status = 1
            for i in ret_val['fieldErrors'].values():
                
                print >> sys.stderr, "%s" % i[0]
        
        if ret_val.has_key('actionMessages'):
            for i in ret_val['actionMessages']:
                print i 
        
        if exit_status != 0:
            sys.exit(exit_status)
        
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
    
    def createUser(self,user,dn,ca,cn,email):
        if user is None:
            self.services['admin'].createUser(dn,ca,cn,email)
        else:
            if email is None or "" == email.strip():
                raise RuntimeError, "Please provide an email for the user!"
            user["emailAddress"] = email
            self.__createUser(user, dn, ca)
    
    def createGroup(self,description,groupName):
        if description is None:
            self.services['admin'].createGroup(groupName)
        else:
            self.__createGroup(groupName, description)
        
        
    def suspendUser(self, dn, ca, reason):
        self.__suspendUser(dn, ca, reason)
    
    def restoreUser(self, dn, ca):
        self.__restoreUser(dn,ca)
    
    def restoreAllSuspendedUsers(self):
        res = self.__restoreAllSuspendedUsers()
        if len(res['restoredUsers']) == 0:
            print "No users were restored."
        else:
            print "The following user's membership has been restored:"
            self.__printUserList(res['restoredUsers'])
        
        