VOMS-ADMIN(1)
=============
:doctype: manpage

== NAME

voms-admin - The VOMS Administration service command line tool

== SYNOPSIS

*voms-admin* --vo=`<NAME>` [OPTIONS] COMMAND PARAM...

== OVERVIEW

The Virtual Organization Membership Service is a Grid attribute authority which
serves as central repository for VO user authorization information, providing
support for sorting users into group hierarchies, keeping track of their roles
and other attributes in order to issue trusted attribute certificates and
assertions used in the Grid environment for authorization purposes.

The VOMS Admin service is a web application providing tools for administering
the VOMS VO structure. It provides an intuitive web user interface for daily
administration tasks

The *voms-admin* command line tool provides access to the most common VOMS Admin
service administrative operations.

== OPTIONS

=== General options

*--help*::
	Prints a short help message.

*--list-commands*::
	Prints a list of available commands.

*--help-command* CMD::
	Prints help about command CMD.

*--help-commands*::
	Prints help for all available commands.

*--version*::
	Prints the voms-admin version string.

*--verbose*::
	Prints more messages.

=== Service access
*--vo* NAME::
	Connect to the NAME Virtual Organization.
	
*--host* HOSTNAME::
	Connect to the VOMS Admin service running on HOSTNAME.
	(Default: localhost)

*--port* PORT::
	Set non standard VOMS Admin service port number.
	(Default: 8443)

== CLIENT AUTHENTICATION

*voms-admin* uses the UNIX effective user ID to choose which X.509 credential it
must use to connect to a (possibly remote) VOMS Admin instance. 

When ran as root, voms-admin uses the host credentials found in
/etc/gridsecurity. 

When running as a normal user, voms-admin does the following: 

* if the *X509_USER_PROXY* environment variable is set, voms-admin uses the
  credentials pointed by such environment variable

* otherwise If a proxy exists in /tmp, the proxy is used

* otherwise if the *X509_USER_CERT* environment variable is set, voms-admin uses
  the credentials pointed by *X509_USER_CERT* and *X509_USER_KEY* environment
  variables

* otherwise the usercert.pem and userkey.pem credentials from the $HOME/.globus
  directory are used.

Use the *--verbose* option to see which credential is used by voms-admin.

== ONLINE HELP

*voms-admin* provides access to a large number of administrative operation on
the VOMS database. In order to see the list of supported operations, you can
use:

[source,bash]
----
voms-admin --list-commands
----

Detailed help about individual commands can be obtained issuing the following command: 

[source,bash]
----
voms-admin --help-command <COMMAND_NAME>
----

The help message contains examples for typical use cases.

== Examples

Get list of all commands:

[source,bash]
----
voms-admin --list-commands
----

Get help on create-user command:

[source,bash]
----
voms-admin --help-command create-user
----

List all the users of VO +atlas+:

[source,bash]
----
voms-admin --vo atlas --host voms.cern.ch list-users
----

Get list of all commands:
[source,bash]
----
voms-admin --list-commands
----


== VOMS Admin authorization framework

This section introduces the VOMS Admin authorization framework. The *voms-admin*
tool provides online help for commands that work on VOMS Admin Access Control
Lists.
For instance, try typing the following command:

[source,bash]
----
voms-admin --help-command add-ACL-entry
----

In VOMS-Admin, each operation that access the VOMS database is authorized via
the VOMS-Admin Authorization framework.  For instance, only authorized admins
have the rights to add users or create groups for a specific VO.  More
specifically, Access Control Lists (ACLs) are linked to VOMS contexts to enforce
authorization decisions on such contexts.  In this framework, a Context is
either a VOMS group, or a VOMS role within a group. 
Each Context as an ACL, which is a set of access control  entries, i.e., (*VOMS
Administrator*, *VOMSPermission*) couples.

A *VOMS Administrator* may be:

* A VO administrator registered in the VO VOMS database

* A VO user certificate

* A VOMS FQAN (i.e., all members in a specific group or that have a certain role
  in a group)

* Any authenticated user (i.e., any user who presents a  certificate issued by a
  trusted CA)

A *VOMS Permission* is a fixed-length sequence of permission flags that describe
the set of permissions a *VOMS Administrator* has in a specific context.

The following list explains in detail the name and meaning of these permission
flags:

* +CONTAINER_READ,CONTAINER_WRITE+: These flags are used to control access to
 the operations that list/alter the VO internal structure (groups and roles
 list/creations/deletions, user creations/deletions).

* +MEMBERSHIP_READ,MEMBERSHIP_WRITE+: These flags are used to control access to
  operations that manage/list membership in group and roles.

* +ATTRIBUTES_READ,ATTRIBUTES_WRITE+: These flags are used to control access to
  operations that manage generic attributes (at the user, group, or role level).

* +ACL_READ,ACL_WRITE,ACL_DEFAULT+: These flags are used to control access to
  operations that manage VO ACLs and default ACLs.

* +REQUESTS_READ, REQUESTS_WRITE+: These flags are used to control access to
 operations that manage subscription requests regarding the VO, group
 membership, role assignment etc...

* +PERSONAL_INFO_READ, PERSONAL_INFO_WRITE+: The flags are used to control
  access to user personal information stored in the database. 

* +SUSPEND+: This flag controls who can suspend other users.

Each operation on the VOMS database is authorized according to the above set of
permissions, i.e., whenever an administrator tries to execute such operation,
its permissions are matched with the operation's set of required permission in
order to authorize the operation execution. 

=== ACL inheritance and default ACLs

Children groups, at creation time, inherit parent's group ACL.  However, VOMS
Admin implements an override mechanims for this behaviour via Default ACLs.
When the Default ACL is defined for a group, children groups inherit the Default
ACL defined at the parent level instead of the parent's group ACL. So, Default
ACLs are useful only if an administrator wants the ACL of children groups to be
different from the one of the parent's group. 


== Resources

1. EMI VOMS documentation: https://twiki.cern.ch/twiki/bin/view/EMI/EMIVomsDocumentation 
2. GGUS support portal: https://ggus.eu
