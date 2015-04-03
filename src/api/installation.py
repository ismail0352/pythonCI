# coding=utf-8
"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
import json

from django.conf import settings
import requests

from login.utils import APIError


class Installation_settings():
    def __init__(self, api_obj, params):
        try:
            with open(settings.PERMISSIONS_PATH, "r") as permi_data:
                permissions_json = permi_data.read()
                data = json.loads(permissions_json)
                self.iris_per_data = data
                self.api_obj = api_obj
                self.params = params

        except Exception as eX:
            APIError.error_log(eX)
            error_message = "Internal Server Error Please check logs"
            return "Exception", error_message

    def IRISPermissions(self):
        try:
            # Reset of all roles, Api will recreate the roles and re-attach the domain permissions.
            resetRoles_url = self.api_obj.baseUrl_resetRoles + self.api_obj.api_version
            APIError.debug_log("resetRoles_url " + resetRoles_url)
            response = requests.post(resetRoles_url, headers=self.params)

            if response.status_code == 200:
                user_permissions = []
                admin_permissions = []

                # This api call gets all the permissions list using requests.get and same url is used for creating new iris permissions with requests.post
                permission_url = self.api_obj.baseUrl_permission + self.api_obj.api_version

                permission_data = requests.get(permission_url, headers=self.params)
                if permission_data.status_code == 200:
                    existing_iris_permissions = []
                    for permi in permission_data.json()['results']:
                        if permi['label'] in settings.PERMISSIONS_LIST:
                            if permi['label'] not in ('read-insight-user', 'read-insight-privileged'):
                                existing_iris_permissions.append(permi['label'])

                                admin_permissions.append({"id": permi['id']})
                                if permi['label'] in ("Workload", "Job Details", "Job Edit-user"):
                                    user_permissions.append({"id": permi['id']})

                    perdict = self.iris_per_data["IRIS_permissions"]

                    for iris_permission in perdict:
                        if iris_permission['label'] not in existing_iris_permissions:
                            # Post api call for permissions creation
                            params = dict(self.params.items() + self.api_obj.headers.items())
                            APIError.debug_log("permission_url " + permission_url)
                            response = requests.post(permission_url, data=json.dumps(iris_permission), headers=params)

                            # not getting response 200 from api
                            if response.status_code == 201:
                                permissionid = response.json()["id"]
                                label = response.json()["label"]
                                admin_permissions.append({"id": permissionid})
                                if label in ("Workload", "Job Details", "Job Edit-user"):
                                    user_permissions.append({"id": permissionid})

                            else:
                                APIError.debug_log("permissions response status " + str(response.status_code))
                                APIError.debug_log("permissions response data " + str(response.json()))
                                APIError.debug_log("status code 200 not found")
                                error_message = "".join(str(response.json()['messages'][0]))
                                return "Fail", error_message

                    # Resetting Roles and reattach IRIS Permissions to HPCAdmin and HPCUser
                    role_status = self.Roles(admin_permissions, user_permissions)
                    if role_status == "Success":
                        return "Success"
                    else:
                        error_message = "Unable to create/edit Roles"
                        return "Exception", error_message
                else:
                    APIError.debug_log("status code 200 not found")
                    error_message = "".join(str(response.json()['messages'][0]))
                    return "Fail", error_message

            else:
                APIError.debug_log("status code 200 not found")
                error_message = "".join(str(response.json()['messages'][0]))
                return "Fail", error_message

        except Exception as eX:
            APIError.error_log(eX)
            error_message = "Unable to create/edit permissions"
            return "Exception", error_message


    def Roles(self, admin_permissions, user_permissions):
        try:

            update_role = self.api_obj.baseUrl_role
            # UPDATE THE ROLES FOR PERMISSION (HPCAdmin) IF USER ALREADY EXISTS After the call, all you should have to do is attach the page permissions to the roles
            roleurl = update_role + "/HPCAdmin" + self.api_obj.api_version + self.api_obj.changemodeadd
            roleurl = roleurl.strip()

            adminper = {
            "permissions": admin_permissions
            }
            params = dict(self.params.items() + self.api_obj.headers.items())
            APIError.debug_log("roleurl update HPCAdmin " + roleurl)
            response = requests.put(roleurl, data=json.dumps(adminper), headers=params)

            #UPDATE THE ROLES FOR PERMISSION (HPCUser) IF USER ALREADY EXISTS
            roleurl = update_role + "/HPCUser" + self.api_obj.api_version + self.api_obj.changemodeadd
            roleurl = roleurl.strip()
            userper = {
            "permissions": user_permissions
            }
            APIError.debug_log("roleurl update HPCUser " + roleurl)
            response = requests.put(roleurl, data=json.dumps(userper), headers=params)

            return "Success"

        except Exception as eX:
            return "Exception"
