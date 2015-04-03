# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.utils.translation import ugettext

from api.build_info import BuildInfo
from api.configuration.views import ConfigurationDataView, RoleModel, \
    RoleDataManagementView, PrincipalModel
from frontend_utils.view_base import ViewBase
from login.utils import APIError, InitAPI, Error500


class GetConfigurationView(ViewBase):
    """
    Configuration page rendering

    Attrubutes:
    template_name = string
                    Holds 'configuration.mako' and used in get and post method for
                    rendering configuration page

    """
    template_name = 'configuration.mako'
    def get(self, request, *args, **kwargs):
        """
         Renders a configuration page. It checks for user is back door or not.

         Args:
             request: represents a single HTTP request. Request objects also have
                      a few useful methods like GET,POST,DELETE etc.

             *args: Variable length argument list.

             **kwargs: Arbitrary keyword arguments.

         Returns:
                HttpResponse and render configuration page with configuration
                data.

         Raises:
             None

         """
        #Check the Session is set otherwise redirect to login
        backdoor = request.GET.get("backdoor")
        username = ""
        session_permission_list = []
        message = ''
        storage = get_messages(request)
        for message in storage:
            message = message

        if backdoor:
            APIError.debug_log("Yes am a backdoor entry user")
            InitAPI_obj = InitAPI()
            fileData = {}
            fileData['USERNAME'] = InitAPI_obj.USERNAME
            fileData['PASSWORD'] = InitAPI_obj.PASSWORD
            fileData['CLIENTID'] = InitAPI_obj.CLIENTID
            fileData['CLIENTSECRET'] = InitAPI_obj.CLIENTSECRET
            fileData['URL'] = InitAPI_obj.URL
            fileData['SUB_URL'] = InitAPI_obj.SUB_URL
            fileData['GOOGLE_ANALYTICS'] = InitAPI_obj.GOOGLE_ANALYTICS

            request.session['active_tab'] = "configuration"

        else:
            APIError.debug_log("No am not a back door entry user")
            # Getting status success to check sessions
            status = request.GET.get("status")
            configObj = ConfigurationDataView()
            fileData = configObj.get(request)

            if str(status) != 'success':
                if request.session.get('BackDoorUser', None) != 'BackDoorUser':
                    try:
                        request.session['access_token']
                    except:
                        request.session['path_previous'] = request.path
                        return self.redirect('/login/')

                    if 'Configuration page' in request.session['session_permission_list']:
                        username = request.session['username']
                        session_permission_list = request.session['session_permission_list']
                    else:
                        return self.redirect('/unauthorized/')
        try:
            build_info = BuildInfo()
            build_obj = build_info.load_build_info(request)
        except Exception as exc:
            return Error500(request, exc.message)

        return self.render_template(self.template_name,
                                       username=username,
                                       fileData=fileData,
                                       messages=message,
                                       build_info=build_obj,
                                       session_permission_list=session_permission_list,
                                       google_analytics=request.session['google_analytics'],)

    def post(self, request, *args, **kwargs):
        """
        Modifiy configuration details on click of save
        verify the provided information is valid on click of test

        Args:
         request: represents a single HTTP request. Request objects also have
                          a few useful methods like GET,POST,DELETE etc.

         *args: Variable length argument list.

         **kwargs: Arbitrary keyword arguments.

        Returns:
                On successful data modification returns success message else
                shows exception message.

        Raises:
         None

        """
        def _fixPath(path):
            path = path.strip("/")
            path = "/" + path + "/"
            return path

        initdata = InitAPI()
        filedata = {}
        configvars = [
            # filevar, postvar, fixfunc, default
            ('USERNAME', 'Username', None, initdata.USERNAME),
            ('PASSWORD', 'Password', None, initdata.PASSWORD),
            ('CLIENTID', 'ClientId', None, initdata.CLIENTID),
            ('CLIENTSECRET', 'ClientSecret', None, initdata.CLIENTSECRET),
            ('URL', 'URL', None, initdata.URL),
            ('SUB_URL', 'PATH', _fixPath, initdata.SUB_URL),
            ('GOOGLE_ANALYTICS', 'analytics1', None, initdata.GOOGLE_ANALYTICS),
            ('ACTION', 'Action', None, "save"),
            ('SERVER_TIMEZONE', 'SERVER_TIMEZONE', None,
             initdata.SERVER_TIMEZONE),
        ]
        for filevar, postvar, fixfunc, default in configvars:
            postval = request.POST.get(postvar)
            if postval is None:
                fileval = default
            else:
                fileval = postval
                if fixfunc:
                    fileval = fixfunc(fileval.strip())
            filedata[filevar] = fileval.strip()

        configObj = ConfigurationDataView()
        res = configObj.post(request, filedata)

        result = {}

        if res == "Success":
            success_message = ugettext("Successfully Modified. Please Login Again.")
            # Deleting all sessions other than google_analytics on success
            for sesskey in request.session.keys():
                if str(sesskey) != 'google_analytics':
                    del request.session[sesskey]
            # Providing success status on successfully saving in configuration
            return HttpResponse(success_message+","+"success")

        if res[0] == "Fail":
            error_message = ugettext("Please check inputs..")
            return HttpResponse(str(res[1])+","+"fail")

        if res[0] == "Exception":
            return HttpResponse(str(res[1])+","+"fail")
        
        if res == "TestSuccess":
            success_message = ugettext("Provided information is valid")
            return HttpResponse(success_message+","+"success")

class RoleManagementCreate(ViewBase):
    """
    Creation of new Role

    Attrubutes:
    template_name = string
                Holds 'roles.mako' and used in get and post method for
                rendering role management page

    """

    template_name = 'roles.mako'
    def get(self, request, *args, **kwargs):
        """
        Rendering page for creation of Role

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
               If roleid is exists it render page having role details.
               else it create role and returns HttpResponse
               Redirect to login page if access token not found

        Raises:
            Redirect to rolelist page if any exception during above process.

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        message = ''
        storage = get_messages(request)
        for message in storage:
            message = message
        status = request.GET.get("status")
        try:
            success = request.GET.get("success")
            roleid = request.GET.get("roleid")

            if roleid:
                """
                get role id details
                """
                roleObj = RoleModel()
                roledata = roleObj.getRole(request)
                errormessage = {}
                errormessage['message'] = ""
                role = {}
                role['description'] = roledata['description']
                if roledata['description'] == None:
                    role['description'] = ""
                role['name'] = roledata['name']
                role['id'] = roledata['id']
                rolepermission = []

                for perm in roledata['permissions']:
                    rolepermission.append(perm['id'])

                """
                get permission list
                """

                roleObj = RoleDataManagementView()
                data = roleObj.get(request)

                return self.render_template(self.template_name, username=request.session['username'],
                                               data=data,
                                               errormessage=errormessage,
                                               role=role,
                                               rolepermission=rolepermission,
                                               messages=message,
                                               status=status,
                                               session_permission_list=request.session['session_permission_list'],
                                               google_analytics=request.session['google_analytics'],)
            elif success:

                roleObj = RoleDataManagementView()
                data = roleObj.get(request)

                role = request.session['role']
                role['id'] = ""
                rolepermission = request.session['rolepermission']
                del request.session['role'], request.session['rolepermission']
                errormessage = {}
                errormessage['message'] = ""

                return self.render_template(self.template_name, username=request.session['username'],
                                               data=data,
                                               errormessage=errormessage,
                                               role=role,
                                               rolepermission=rolepermission,
                                               messages=message,
                                               status=status,
                                               session_permission_list=request.session['session_permission_list'],
                                               google_analytics=request.session['google_analytics'],)

            else:

                roleObj = RoleDataManagementView()
                data = roleObj.get(request)
                role = {}
                role['description'] = ""
                role['name'] = ""
                role['id'] = ""
                rolepermission = []
                errormessage = {}
                errormessage['message'] = ""
                return self.render_template(self.template_name, username=request.session['username'],
                                               data=data,
                                               errormessage=errormessage,
                                               role=role,
                                               rolepermission=rolepermission,
                                               messages=message,
                                               status=status,
                                               session_permission_list=request.session['session_permission_list'],
                                               google_analytics=request.session['google_analytics'],)

        except Exception as eX:
            return self.redirect('/rolelist/'+'&status='+str(status))

    def post(self, request, *args, **kwargs):
        """
        Submit role details

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
               Collects role related data and return HttpResponse and render create role page.
               Redirect rolelist apge if submitvalue is 'Done' or 'Apply' or any
               exception occures.
               Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')
        try:
            roleObj = RoleModel()
            submitValue = request.POST.get("submit")

            roleName = request.POST.get("RoleName")
            description = request.POST.get("Description")
            permissions = request.POST.getlist("permissions")
            permissionlist = []
            for id in permissions:
                permissionlist.append({"id":id})

            roledict = {"name": roleName.strip(),
                        "description": description.strip(),
                        "scope": "GLOBAL",
                        "permissions": permissionlist}

            roleid = "".join(request.POST.getlist("roleid"))
            
            request.session['active_tab'] = 'configuration'
            
            response_message, Onsuccessid, status = roleObj.createRole(request, roleid, roledict)

            messages.success(request, response_message)

            if submitValue == "Done":
                return self.redirect('/rolelist/?status='+str(status))

            elif submitValue == "Apply":

                if Onsuccessid:
                    return self.redirect("/createrole/?roleid="+str(Onsuccessid)+"&tab="+str(request.session['active_tab'])+"&status="+str(status))
                else:
                    request.session['role'] = roledict
                    request.session['rolepermission'] = permissions

                    return self.redirect("/createrole/?success=not-saved"+"&status="+str(status))

                name = request.POST.get("RoleName")
                roleObj = RoleModel()
                data = roleObj.getRoleByName(request, name)
                id = data['id']
                return self.redirect('/createrole/?roleid='+id+'&status='+str(status))
            else:
                return self.redirect('/rolelist/'+'&status='+str(status))
        except:
            return self.redirect('/rolelist/'+'&status='+str(status))

class RoleManagementDelete(ViewBase):
    """
    Delete role functionality

    Attrubutes:
    template_name = string
                Holds 'rolelist.mako' and used in get  method for
                rendering role rolelist page

    """
    template_name = 'rolelist.mako'
    def get(self, request, *args, **kwargs):
        """
        Delete role

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
                If role id is found it deletes role and returns success message
                otherwise showing message 'Role id is missing'.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        id = request.GET.get("id")
        if id:
            roleObj = RoleModel()
            data = roleObj.deleteRole(request)
            errormessage = {}
            try:
                if data['messages']:
                    return HttpResponse(data['messages'])
            except:
                return HttpResponse(True)
        else:
            return HttpResponse("RoleId Missing")

class RoleListView(ViewBase):
    """
    Role list related funtionality.

    Attrubutes:
    template_name = string
                Holds 'rolelist.mako' and used in get  method for
                rendering  rolelist page

    """
    template_name = 'rolelist.mako'
    def get(self, request):
        """
        Role list related funtionality.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse with username,password,permission list etc.
                Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        message = ''
        storage = get_messages(request)
        for message in storage:
            message = message

        status = request.GET.get("status")
        return self.render_template(self.template_name, username=request.session['username'],
                                       messages=message,
                                       status=status,
                                       session_permission_list=request.session['session_permission_list'],
                                       google_analytics=request.session['google_analytics'],)

class RoleListGridView(ViewBase):
    """
    Role list related funtionality.

    Attrubutes:
    template_name = string
                Holds 'rolelistcontainer.html' and used in get  method for
                rendering  rolelist page

    """
    template_name = 'rolelistcontainer.html'
    def get(self, request):
        """
        Role list related funtionality.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse with username,password,permission list etc.
                Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        roleObj = RoleModel()
        rolelist, status_code = roleObj.getRoles(request)
        message = ''
        status = request.GET.get("status")
        return self.render_template(self.template_name, status_code=status_code,
                                       username=request.session['username'],
                                       rolelist=rolelist,
                                       mesaages=message,
                                       status=status,
                                       session_permission_list=request.session['session_permission_list'],)

class PrincipalListView(ViewBase):
    """
    Principal list related funtionality.

    Attrubutes:
    template_name = string
                Holds 'principallist.mako' and used in get  method for
                rendering  principallist page

    """
    template_name = 'principallist.mako'
    def get(self, request):
        """
        Principal list related funtionality.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse and renders principallist with username,password,permission list etc.
                Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')
        status = request.GET.get("status")
        message = ''
        storage = get_messages(request)
        for message in storage:
            message = message

        return self.render_template(self.template_name, username=request.session['username'],
                                       messages=message,
                                       status=status,
                                       session_permission_list=request.session['session_permission_list'],
                                       google_analytics=request.session['google_analytics'],)

class PrincipalGridView(ViewBase):
    """
    Principal list related funtionality.

    Attrubutes:
    template_name = string
                Holds 'principallistcontainer.html' and used in get  method for
                rendering  principallist page

    """
    template_name = 'principallistcontainer.html'
    def get(self, request):
        """
        Principal list related funtionality.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse and renders principallist with username,password,permission list etc.
                Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')       
        principalObj = PrincipalModel()
        principallist_data, totalcount, status_code = principalObj.getPrincipalListing(request)
        message = ''
        return self.render_template(self.template_name, status_code=status_code,
                                       username=request.session['username'],
                                       principallist_data=principallist_data,
                                       messages=message,                                       
                                       session_permission_list=request.session['session_permission_list'],)

class GetPrincipalCreateEditView(ViewBase):
    """
    This view is used to create new principal and edit existing principal

    Attrubutes:
    template_name = string
                            Holds 'principal.mako' and used in get  method for
                            rendering  principallist page

    """
    template_name = 'principal.mako'
    def get(self, request):
        """
        Principal list related funtionality.

        Args:
                request: represents a single HTTP request. Request objects also have
                                 a few useful methods like GET,POST,DELETE etc.

                *args: Variable length argument list.

                **kwargs: Arbitrary keyword arguments.

        Returns:
                        If it get principal id it edit principal and render principal list page
                        else it create new principal and then render principal list page
                        Redirect to login page if access token not found.

        Raises:
                None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        message = ''

        principalid = request.GET.get("principalId")
        success = request.GET.get("success")
        status = request.GET.get("status")
        #Creating object of principal model
        peditObj = PrincipalModel()

        if principalid:
            #principal id edit section
            response_status, principal_data = peditObj.getPrincipal(request, principalid)
            if response_status == "Fail":
                id, name, description = '', '', ''
                LDAP_Entity, PAM_Entity = peditObj.getPrincipalEntity(request)
                existing_roles, groups = [], []
            else:
                id = principal_data['id']
                name = principal_data['name']
                # Converting description to string to handle None type objects in description that gets handled in mako
                description = principal_data['description']
                if principal_data['description'] == None:
                    description = ""
                existing_roles = []
                #Getting LDAP PAM connection status
                LDAP_Entity, PAM_Entity = peditObj.getPrincipalEntity(request)

                for data in principal_data['attachedRoles']:
                    existing_roles.append(data['id'])

                groups = principal_data['groups'] + principal_data['users']

        elif success:
            #principal create section in case principal is not successfully created

            id = ''
            name = request.session['name']
            description = request.session['description']
            existing_roles = request.session['existing_roles']
            groups = request.session['groups']
            #Getting LDAP PAM connection status
            LDAP_Entity, PAM_Entity = peditObj.getPrincipalEntity(request)

            del request.session['name'], request.session['description'], request.session['existing_roles'], request.session['groups']
        else:
            #principal create section
            id, name, description = '', '', ''
            #Getting LDAP PAM connection status
            LDAP_Entity, PAM_Entity = peditObj.getPrincipalEntity(request)

            existing_roles, groups = [], []

        roleObj = RoleModel()
        roledata, status_code_roles = roleObj.getRoles(request)

        storage = get_messages(request)
        for message in storage:
                message = message

        return self.render_template(self.template_name, username=request.session['username'],
                                       principalId=id,
                                       name=name,
                                       description=description,
                                       existing_roles_list=existing_roles,
                                       groupslist=groups,
                                       rolelist=roledata,
                                       status_code_roles=status_code_roles,
                                       LDAP_Entity=LDAP_Entity,
                                       PAM_Entity=PAM_Entity,
                                       messages=message,
                                       status=status,
                                       session_permission_list=request.session['session_permission_list'],
                                       google_analytics=request.session['google_analytics'],)


    def post(self, request):
        """
        Principal list related funtionality.

        Args:
                request: represents a single HTTP request. Request objects also have
                                 a few useful methods like GET,POST,DELETE etc.

                *args: Variable length argument list.

                **kwargs: Arbitrary keyword arguments.

        Returns:
                        Edit principal and redirect to principal list page
                        Redirect to login page if access token not found.

        Raises:
                None
        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')

        request.session['active_tab'] = 'configuration'

        principalId = request.POST.get("principalId")
        principalName = request.POST.get("name")
        description = request.POST.get("description")

        attachedRoles = request.POST.getlist("roleslist")
        groupuser = request.POST.getlist("groupuser")
        groupusertype = request.POST.getlist("groupusertype")

        principal_data = {}
        #Need "principalname" principal name while to set principal edit api
        principalname = principalName.strip()
        principal_data["name"] = principalname

        principal_data["description"] = description.strip()

        roles_list = []
        for roles in attachedRoles:
            roles_list.append({"name" : str(roles)})

        principal_data['attachedRoles'] = roles_list

        group_list = []
        user_list = []

        for name, type in zip(groupuser, groupusertype):
            if type == u"LDAP" or type == u"PAM":
                user_list.append({"name" : name.strip(), "type" : str(type)})
            else:
                group_list.append({"name" : name.strip(), "type" : str(type)})
               
        principal_data["groups"] = group_list
        principal_data["users"] = user_list

        #Adding two list groups and user this is used in redirection for create.
        group_user_list = group_list + user_list

        peditObj = PrincipalModel()
        response_message, Onsuccessid, status = peditObj.post(request, principalId, principalname, principal_data)

        messages.success(request, response_message)
                
        action = request.POST.get("action")
        if action == "Apply":
            if Onsuccessid or principalId:

                return self.redirect("/principal/?principalId="+str(Onsuccessid)+"&tab="+str(request.session['active_tab']+"&status="+str(status)))
            else:
                request.session['name'] = principalname
                request.session['description'] = description
                request.session['description'] = description
                request.session['existing_roles'] = roles_list
                request.session['groups'] = group_user_list
                return self.redirect("/principal/?success=not-saved&status="+str(status))
        else:
            # IF action id Done redirect to workload without display of a message
            return self.redirect("/principallist/?status="+str(status))

class GetPrincipalDeleteView(ViewBase):
    """
    This view is used to delete principal

    Attrubutes:
            None
    """
    def get(self, request):
        """
        Principal delete related funtionality.

        Args:
            request: represents a single HTTP request. Request objects also have
                     a few useful methods like GET,POST,DELETE etc.

            *args: Variable length argument list.

            **kwargs: Arbitrary keyword arguments.

        Returns:
                HttpResponse with success message after deletion of principal using principal id
                Redirect to login page if access token not found.

        Raises:
            None

        """
        try:
            request.session['access_token']
        except:
            request.session['path_previous'] = request.path
            return self.redirect('/login/')
        principalid = request.GET.get("principalId")
        principalname = request.GET.get("name")

        peditObj = PrincipalModel()
        response = peditObj.deletePrincipal(request, principalid, principalname)
        
        if isinstance(response, str):
            return HttpResponse(True)
        else:
            return HttpResponse(response[1])

