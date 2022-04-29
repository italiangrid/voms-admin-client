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

commands_def = """<?xml version="1.0" encoding="UTF-8"?>
<voms-commands>
  <command-group
    name="User management commands"
    shortname="user">
    <command
      name="list-users">
      <description>list-users</description>
      <help-string
        xml:space="preserve">
        Lists the VO users.</help-string>
    </command>

    <command
      name="list-suspended-users">
      <description>list-suspended-users</description>
      <help-string
        xml:space="preserve">
        Lists the VO users that are currently suspended. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>

    <command
      name="list-expired-users">
      <description>list-expired-users</description>
      <help-string
        xml:space="preserve">
        Lists the VO users that are currently expired. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>

    <command
      name="count-expired-users">
      <description>count-expired-users</description>
      <help-string
        xml:space="preserve">
        Prints how many VO users are currently expired. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>

    <command
      name="count-suspended-users">
      <description>count-suspended-users</description>
      <help-string
        xml:space="preserve">
        Counts how many VO users are currently suspended. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>

    <command
      name="count-users">
      <description>count-users</description>
      <help-string
        xml:space="preserve">
        Counts how many users are in the VO. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>

    <command
      name="list-user-stats">
      <description>list-user-stats</description>
      <help-string
        xml:space="preserve">
        List users statistics for this VO. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>
    <command
        name="get-user-info">
        <description>get-user-info</description>
        <help-string
          xml:space="preserve">
          List user VO membership information. (Requires VOMS Admin server >= 3.4.0)</help-string>
        <arg type="UserV2"/>
    </command>
    <command
      name="create-user">
      <description>[options] create-user CERTIFICATE.PEM</description>
      <help-string
        xml:space="preserve">
        Registers a new user in VOMS.

        Personal information can be specified with the following options:
        name, surname, address, institution, phone-number.
        (Personal info submission requires VOMS Admin server >= 2.7.0)

        All these options must be provided when registering a new user,
        or no option regarding personal information should be set.

        Besides the personal information, information about user certificate
        can be provided specifying a certificate file parameter.

        When using the --nousercert  option, then four parameters are
        required (DN CA CN MAIL) to create the user.

        Examples:

        voms-admin --vo test --name Andrea --surname Ceccanti --institution IGI \\
                   --phoneNumber 243 --address "My Address" \\
                   create-user .globus/usercert.pem

        voms-admin --vo test_vo create-user .globus/usercert.pem

        voms-admin --nousercert --vo test_vo create-user \
        'My DN' 'My CA' 'My CN' 'My Email'</help-string>
      <arg
        type="X509v2" />
    </command>

    <command
      name="suspend-user">
      <description>suspend-user USER REASON</description>
      <help-string
        xml:space="preserve">
        Supends a VOMS user.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.

        (Requires VOMS Admin server >= 2.7.0)
      </help-string>
      <arg type="User"/>
      <arg type="String"/>
    </command>

    <command
      name="restore-user">
      <description>restore-user USER</description>
      <help-string
        xml:space="preserve">
        Restores a VOMS user.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.

        (Requires VOMS Admin server >= 2.7.0)
      </help-string>
      <arg type="User"/>
    </command>

    <command
      name="restore-all-suspended-users">
      <description>restore-all-suspended-users</description>
      <help-string
        xml:space="preserve">
        Restores all the users currently suspended in the VOMS database. (Requires VOMS Admin server >= 2.7.0)</help-string>
    </command>

    <command
      name="delete-user">
      <description>delete-user USER</description>
      <help-string
        xml:space="preserve">
        Deletes a user from VOMS, including all their attributes
        and membership information.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.

        Examples:

        voms-admin --vo test_vo delete-user .globus/usercert.pem

        voms-admin --nousercert --vo test_vo delete-user \
        'My DN' 'MY CA'</help-string>
      <arg
        type="User" />
    </command>
  </command-group>
  <command-group
    name="Role management commands"
    shortname="role">
    <command
      name="list-roles">
      <description>list-roles</description>
      <help-string
        xml:space="preserve">
        Lists the roles defined in the VO.</help-string>
    </command>
    <command
      name="create-role">
      <description>create-role ROLENAME</description>
      <help-string
        xml:space="preserve">
        Creates a new role</help-string>
      <arg
        type="Role" />
    </command>
    <command
      name="delete-role">
      <description>delete-role ROLENAME</description>
      <help-string
        xml:space="preserve">
        Deletes a role.</help-string>
      <arg
        type="Role" />
    </command>
  </command-group>
  <command-group
    name="Group management commands"
    shortname="group">
    <command
      name="list-groups">
      <description>list-groups</description>
      <help-string
        xml:space="preserve">
        Lists all the groups defined in the VO.</help-string>
    </command>
    <command
      name="list-sub-groups">
      <description>list-sub-groups GROUPNAME</description>
      <help-string
        xml:space="preserve">
        List the subgroups of GROUPNAME.</help-string>
      <arg
        type="Group" />
    </command>
    <command
      name="create-group">
      <description>[options] create-group GROUPNAME</description>
      <help-string xml:space="preserve">
        Creates a new group named GROUPNAME.

        If the --description option is given, a description is registered
        for the group in the VOMS database (requires VOMS Admin server >= 2.7.0).

        Note that the vo root group part of the fully qualified group name
        can be omitted, i.e., if the group to be created is called /vo/ciccio,
        where /vo is the vo root group, this command accepts both the "ciccio"
        and "/vo/ciccio" syntaxes.</help-string>
      <arg
        type="NewGroup" />
    </command>
    <command
      name="delete-group">
      <description>delete-group GROUPNAME</description>
      <help-string
        xml:space="preserve">
        Deletes a group.</help-string>
      <arg
        type="Group" />
    </command>
    <command
      name="list-user-groups">
      <description>list-user-groups USER</description>
      <help-string xml:space="preserve">
        Lists the groups that USER is a member of. USER is either
        an X509 certificate file in PEM format, or a DN, CA couple when the
        --nousercert option is set.</help-string>
      <arg
        type="User" />
    </command>
  </command-group>
  <command-group
    name="Group membership management commands"
    shortname="membership">
    <command
      name="add-member">
      <description>add-member GROUPNAME USER</description>
      <help-string xml:space="preserve">
        Adds USER to the GROUPNAME group.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.</help-string>
      <arg
        type="Group" />
      <arg
        type="User" />
    </command>
    <command
      name="remove-member">
      <description>remove-member GROUPNAME USER</description>
      <help-string xml:space="preserve">
        Removes USER from the GROUPNAME group.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.</help-string>
      <arg
        type="Group" />
      <arg
        type="User" />
    </command>
    <command
      name="list-members">
      <description>list-members GROUPNAME</description>
      <help-string
        xml:space="preserve">
        Lists all members of a group.</help-string>
      <arg
        type="Group" />
    </command>
  </command-group>
  <command-group
    name="Role assignment commands"
    shortname="role-assign">
    <command
      name="assign-role">
      <description>assign-role GROUPNAME ROLENAME USER</description>
      <help-string xml:space="preserve">
        Assigns role ROLENAME to user USER in group GROUPNAME.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.</help-string>
      <arg
        type="Group" />
      <arg
        type="Role" />
      <arg
        type="User" />
    </command>
    <command
      name="dismiss-role">
      <description>dismiss-role GROUPNAME ROLENAME USER
      </description>
      <help-string xml:space="preserve">
        Dismiss role ROLENAME from user USER in group GROUPNAME.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.</help-string>
      <arg
        type="Group" />
      <arg
        type="Role" />
      <arg
        type="User" />
    </command>
    <command
      name="list-users-with-role">
      <description>list-users-with-role GROUPNAME ROLENAME
      </description>
      <help-string xml:space="preserve">
        Lists all users with ROLENAME in GROUPNAME.</help-string>
      <arg
        type="Group" />
      <arg
        type="Role" />
    </command>
    <command
      name="list-user-roles">
      <description>list-user-roles USER</description>
      <help-string xml:space="preserve">
        Lists the roles that USER is assigned.

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.</help-string>
      <arg
        type="User" />
    </command>
  </command-group>
  <command-group
    name="Attribute class management commands"
    shortname="attr-class">
    <command
      name="create-attribute-class">
      <description> create-attribute-class CLASSNAME DESCRIPTION UNIQUE
      </description>
      <help-string xml:space="preserve">
        Creates a new generic attribute class named CLASSNAME, with
        description DESCRIPTION.

        UNIQUE is a boolean argument. If UNIQUE is true,
        attribute values assigned to users for this class are checked for
        uniqueness. Otherwise no checks are performed on user attribute values.
      </help-string>
      <arg
        type="String" />
      <arg
        type="String"
        nillable="true" />
      <arg
        type="Boolean"
        nillable="true" />
    </command>
    <command
      name="delete-attribute-class">
      <description>delete-attribute-class CLASSNAME
      </description>
      <help-string xml:space="preserve">
        Removes the generic attribute class CLASSNAME. All the
        user, group and role attribute mappings will be deleted as well.
      </help-string>
      <arg
        type="String" />
    </command>
    <command
      name="list-attribute-classes">
      <description>list-attribute-classes</description>
      <help-string xml:space="preserve">
        Lists the attribute classes defined for the VO.</help-string>
    </command>
  </command-group>
  <command-group
    name="Generic attribute assignment commands"
    shortname="attrs">
    <command
      name="set-user-attribute">
      <description> set-user-attribute USER ATTRIBUTE ATTRIBUTE_VALUE
      </description>
      <help-string xml:space="preserve">
        Sets the generic attribute ATTRIBUTE value to
        ATTRIBUTE_VALUE for user USER. USER is either an X509 certificate file
        in PEM format, or a DN, CA couple when the --nousercert option is set.
      </help-string>
      <arg
        type="User" />
      <arg
        type="String" />
      <arg
        type="String" />
    </command>
    <command
      name="delete-user-attribute">
      <description>delete-user-attribute USER ATTRIBUTE
      </description>
      <help-string xml:space="preserve">
        Deletes the generic attribute ATTRIBUTE value from user
        USER. USER is either an X509 certificate file in PEM format, or a DN,
        CA couple when the --nousercert option is set.</help-string>
      <arg
        type="User" />
      <arg
        type="String" />
    </command>
    <command
      name="list-user-attributes">
      <description>list-user-attributes USER</description>
      <help-string xml:space="preserve">
        Lists the generic attributes defined for user USER. USER is
        either an X509 certificate file in PEM format, or a DN, CA couple when
        the --nousercert option is set.</help-string>
      <arg
        type="User" />
    </command>
    <command
      name="set-group-attribute">
      <description> set-group-attribute GROUP ATTRIBUTE ATTRIBUTE_VALUE
      </description>
      <help-string xml:space="preserve">
        Sets the generic attribute ATTRIBUTE value to
        ATTRIBUTE_VALUE for group GROUP.</help-string>
      <arg
        type="Group" />
      <arg
        type="String" />
      <arg
        type="String" />
    </command>
    <command
      name="set-role-attribute">
      <description> set-role-attribute GROUP ROLE ATTRIBUTE ATTRIBUTE_VALUE
      </description>
      <help-string xml:space="preserve">
        Sets the generic attribute ATTRIBUTE value to
        ATTRIBUTE_VALUE for role ROLE in group GROUP.</help-string>
      <arg
        type="Group" />
      <arg
        type="Role" />
      <arg
        type="String" />
      <arg
        type="String" />
    </command>
    <command
      name="delete-group-attribute">
      <description>delete-group-attribute GROUP ATTRIBUTE
      </description>
      <help-string xml:space="preserve">
        Deletes the generic attribute ATTRIBUTE value from group
        GROUP.</help-string>
      <arg
        type="Group" />
      <arg
        type="String" />
    </command>
    <command
      name="list-group-attributes">
      <description>list-group-attributes GROUP
      </description>
      <help-string xml:space="preserve">
         Lists the generic attributes defined for group GROUP.</help-string>
      <arg
        type="Group" />
    </command>
    <command
      name="list-role-attributes">
      <description>list-role-attributes GROUP ROLE
      </description>
      <help-string xml:space="preserve">
        Lists the generic attributes defined for role ROLE in group
        GROUP.</help-string>
      <arg
        type="Group" />
      <arg
        type="Role" />
    </command>
    <command
      name="delete-role-attribute">
      <description> delete-role-attribute GROUP ROLE ATTRIBUTE</description>
      <help-string xml:space="preserve">
        Deletes the generic attribute ATTRIBUTE value from role
        ROLE in group GROUP.</help-string>
      <arg
        type="Group" />
      <arg
        type="Role" />
      <arg
        type="String" />
    </command>
  </command-group>
  <command-group
    name="ACL management commands"
    shortname="acl">
    <command
      name="get-ACL">
      <description>get-ACL CONTEXT</description>
      <help-string xml:space="preserve">
        Gets the ACL defined for voms context CONTEXT. CONTEXT may
        be either a group (e.g. /groupname ) or a qualified role
        (e.g./groupname/Role=VO-Admin).</help-string>
      <arg
        type="String" />
    </command>
    <command
      name="get-default-ACL">
      <description>get-default-ACL GROUP</description>
      <help-string xml:space="preserve">
        Gets the default ACL defined for group GROUP.</help-string>
      <arg
        type="Group" />
    </command>
    <command
      name="add-ACL-entry">
      <description> add-ACL-entry CONTEXT USER PERMISSION PROPAGATE
      </description>
      <help-string xml:space="preserve">
        Adds an entry to the ACL for CONTEXT assigning PERMISSION
        to user/admin USER. If PROPAGATE is true, the entry is
        propagated to children contexts.

        CONTEXT may be either a group (e.g. /groupname ) or
        a qualified role (e.g./groupname/Role=VO-Admin).

        USER is either an X509 certificate file in PEM format,
        or a DN, CA couple when the --nousercert option is set.

        PERMISSION is a VOMS permission expressed using the
        VOMS-Admin 2.x format. Allowed permission values are:

        ALL
        CONTAINER_READ CONTAINER_WRITE
        MEMBERSHIP_READ MEMBERSHIP_WRITE
        ATTRIBUTES_READ ATTRIBUTES_WRITE
        ACL_READ ACL_WRITE ACL_DEFAULT
        REQUESTS_READ REQUESTS_WRITE
        PERSONAL_INFO_READ PERSONAL_INFO_WRITE
        SUSPEND

        Multiple permissions can be assigned by combining them
        in a comma separated list, e.g.:
        "CONTAINER_READ,MEMBERSHIP_READ"

        Special meaning DN,CA couples (to be used with
        the --nousercert option set) are listed hereafter:

        If DN is ANYONE and CA is VOMS_CA, an entry will be created
        that assigns the specified PERMISSION to to any
        authenticated user (i.e., any client that authenticates
        with a certificates signed by a trusted CA).

        if CA is GROUP_CA, DN is interpreted as a group and entry
        will be assigned to members of such group.

        if CA is ROLE_CA, DN is interpreted as a qualified role
        (i.e., /test_vo/Role=TestRole), the entry will be assigned
        to VO members that have the given role in the given group.


        Examples:

        voms-admin --vo test_vo add-ACL-entry /test_vo \\
        .globus/usercert.pem ALL true

        (The above command grants full rights to the user identified by
        '.globus/usercert.pem' on the whole VO, since PROPAGATE is true)

        voms-admin --nousercert --vo test_vo add-ACL-entry /test_vo \\
        'ANYONE' 'VOMS_CA' 'CONTAINER_READ,MEMBERSHIP_READ' true

        (The above command grants READ rights on VO structure and membership
        to any authenticated user on the whole VO, since PROPAGATE is true)

        To get more detailed information about Voms admin AuthZ
        framework, either consult the voms-admin user's guide
        or type:

        voms-admin --help-acl</help-string>
      <arg
        type="String" />
      <arg
        type="User" />
      <arg
        type="Permission" />
      <arg
        type="Boolean" />
    </command>
    <command
      name="add-default-ACL-entry">
      <description> add-default-ACL-entry GROUP USER PERMISSION</description>
      <help-string xml:space="preserve">
        Adds an entry to the default ACL for GROUP assigning
        PERMISSION to user/admin USER.

        USER is either an X509 certificate file
        in PEM format, or a DN, CA couple when the --nousercert option is set.

        PERMISSION is a VOMS permission expressed using the VOMS-Admin 2.x
        format.

        Allowed permission values are:
        ALL
        CONTAINER_READ CONTAINER_WRITE
        MEMBERSHIP_READ MEMBERSHIP_WRITE
        ATTRIBUTES_READ ATTRIBUTES_WRITE
        ACL_READ ACL_WRITE ACL_DEFAULT
        REQUESTS_READ REQUESTS_WRITE
        PERSONAL_INFO_READ PERSONAL_INFO_WRITE
        SUSPEND

        Multiple permissions can be assigned by combining them
        in a comma separated list, e.g.:
        "CONTAINER_READ,MEMBERSHIP_READ"

        Special meaning DN,CA couples are listed hereafter:

        If DN is ANYONE and CA is VOMS_CA, an entry will be created that
        assigns the specified PERMISSION to to any authenticated user (i.e.,
        any client that authenticates with a certificates signed by
        a trusted CA).

        if CA is GROUP_CA, DN is interpreted as a group and entry will be
        assigned to members of such group.

        if CA is ROLE_CA, DN is interpreted as a qualified role
        (i.e., /test_vo/Role=TestRole), the entry will be assigned to VO
        members that have the given role in the given group.

        To get more detailed information about Voms admin AuthZ framework,
        either consult the voms-admin user's guide or type:

        voms-admin --help-acl</help-string>
      <arg
        type="Group" />
      <arg
        type="User" />
      <arg
        type="Permission" />
    </command>
    <command
      name="remove-ACL-entry">
      <description>remove-ACL-entry CONTEXT USER PROPAGATE
      </description>
      <help-string xml:space="preserve">
        Removes the entry from the ACL for CONTEXT for user/admin USER.

        If PROPAGATE is true, the entry is removed also from children
        contexts.

        CONTEXT may be either a group (e.g. /groupname ) or a
        qualified role (e.g./groupname/Role=VO-Admin).

        USER is either an X509 certificate file
        in PEM format, or a DN, CA couple when the --nousercert option is set.

        Special meaning DN,CA couples are listed hereafter:

        If DN is ANYONE and CA is VOMS_CA, an entry will be created that
        assigns the specified PERMISSION to to any authenticated user (i.e.,
        any client that authenticates with a certificates signed by
        a trusted CA).

        if CA is GROUP_CA, DN is interpreted as a group and entry will be
        assigned to members of such group.

        if CA is ROLE_CA, DN is interpreted as a qualified role
        (i.e., /test_vo/Role=TestRole), the entry will be assigned to VO
        members that have the given role in the given group.

        Examples:

        voms-admin --nousercert --vo test_vo remove-ACL-entry \\
        /test_vo 'ANYONE' 'VOMS_CA' true

        (The above command removes any right on the VO from any authenticated
        user)

        To get more detailed information about Voms admin AuthZ framework,
        either consult the voms-admin user's guide or type:

        voms-admin --help-acl</help-string>
      <arg
        type="String" />
      <arg
        type="User" />
      <arg
        type="Boolean" />
    </command>
    <command
      name="remove-default-ACL-entry">
      <description>remove-default-ACL-entry GROUP USER
      </description>
      <help-string xml:space="preserve">
        Removes the entry for user/admin USER from the default ACL
        for GROUP.

        USER is either an X509 certificate file in PEM format, or a DN,
        CA couple when the --nousercert option is set.

        Special meaning DN,CA couples are listed hereafter:

        If DN is ANYONE and CA is VOMS_CA, an entry will be created that
        assigns the specified PERMISSION to to any authenticated user (i.e.,
        any client that authenticates with a certificates signed by
        a trusted CA).

        if CA is GROUP_CA, DN is interpreted as a group and entry will be
        assigned to members of such group.

        if CA is ROLE_CA, DN is interpreted as a qualified role
        (i.e., /test_vo/Role=TestRole), the entry will be assigned to VO
        members that have the given role in the given group.

        To get more detailed information about Voms admin AuthZ framework,
        either consult the voms-admin user's guide or type:

        voms-admin --help-acl</help-string>
      <arg
        type="Group" />
      <arg
        type="User" />
    </command>
  </command-group>
  <command-group
    name="Other commands"
    shortname="other">
    <command
      name="get-vo-name">
      <description>get-vo-name</description>
      <help-string xml:space="preserve">
        This command returns the name of the contacted vo.</help-string>
    </command>
    <command
      name="list-cas">
      <description>list-cas</description>
      <help-string xml:space="preserve">
        Lists the certificate authorities accepted by the VO.</help-string>
    </command>
  </command-group>
  <command-group
      name="Certificate management commands"
      shortname="Certificate"
      >
      <command
          name="add-certificate">
              <description>add-certificate USER CERT</description>
              <help-string xml:space="preserve">
                  Binds a certificate to an existing VO user.
                  This operation may take either two pem certficate files as argument, or,
                  if the --nousercert option is set, two DN CA couples.

                  Example:
                  voms-admin --vo infngrid add-certificate my-cert.pem my-other-cert.pem

                  voms-admin --vo infngrid --nousercert add-certificate \\
                    '/C=IT/O=INFN/OU=Personal Certificate/L=CNAF/CN=Andrea Ceccanti' '/C=IT/O=INFN/CN=INFN CA' \\
                    '/C=IT/ST=Test/CN=user0/Email=andrea.ceccanti@cnaf.infn.it' '/C=IT/ST=Test/L=Bologna/O=Voms-Admin/OU=Voms-Admin testing/CN=Test CA'
            </help-string>
            <arg type="User"/>
            <arg type="User"/>
      </command>
      <command
          name="remove-certificate">
              <description>remove-certificate USER</description>
              <help-string xml:space="preserve">
                  Unbinds a certificate from an existing VO user.
                  This operation takes either a pem certificate as argument, or,
                  if the --nousercert option is set, a DN CA couple.

                  Example:

                  voms-admin --vo infngrid remove-certificate my-cert.pem

                  voms-admin --vo infngrid --nousercert remove-certificate \\
                    '/C=IT/O=INFN/OU=Personal Certificate/L=CNAF/CN=Andrea Ceccanti' '/C=IT/O=INFN/CN=INFN CA'
            </help-string>
            <arg type="User"/>
      </command>
      <command
          name="suspend-certificate">
              <description>suspend-certificate USER REASON</description>
              <help-string xml:space="preserve">
                  Suspends a user certificate, and specifies a reason for the suspension.
                  This operation takes, for the first argument, either a pem certificate as argument, or,
                  if the --nousercert option is set, a DN CA couple.

                  Example:
                  voms-admin --vo infngrid suspend-certificate usercert.pem 'Security incident!'

                  voms-admin --vo infngrid --nousercert suspend-certificate \\
                      '/C=IT/O=INFN/OU=Personal Certificate/L=CNAF/CN=Andrea Ceccanti' '/C=IT/O=INFN/CN=INFN CA' \\
                      'Security incident!'
            </help-string>
            <arg type="User"/>
            <arg type="String"/>
      </command>
      <command
          name="restore-certificate">
              <description>restore-certificate USER</description>
              <help-string xml:space="preserve">
                  Restores a user certificate.
                  This operation takes, for the first argument, either a pem certificate as argument, or,
                  if the --nousercert option is set, a DN CA couple.

                  Example:
                  voms-admin --vo infngrid restore-certificate usercert.pem

                  voms-admin --vo infngrid --nousercert restore-certificate \\
                      '/C=IT/O=INFN/OU=Personal Certificate/L=CNAF/CN=Andrea Ceccanti' '/C=IT/O=INFN/CN=INFN CA'
            </help-string>
            <arg type="User"/>
      </command>
      <command
          name="get-certificates">
          <description>get-certificates USER</description>
          <help-string xml:space="preserve">
            Lists the certificates associated to a user.
            This operation takes either a pem certificate as argument, or, if the --nousercert option is set, a DN CA couple.

            Example:
            voms-admin --vo infngrid get-certificates usercert.pem

            voms-admin --vo infngrid --nousercert get-certificates \\
                '/C=IT/O=INFN/OU=Personal Certificate/L=CNAF/CN=Andrea Ceccanti' '/C=IT/O=INFN/CN=INFN CA'
        </help-string>
        <arg
            type="User"/>
      </command>

  </command-group>
</voms-commands>"""
