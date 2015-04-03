## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />

<%def name="title()">${_("Viewpoint Principals")}</%def>

<%def name="head_tags()">

</%def>

<%def name="jquery_tags()">
<script type="text/JavaScript">
		$(document).ready(function(){
		var autoheight = document.getElementById("page-content").offsetHeight;
		$("#side").height(autoheight);

		createDirtyUnloadListener("input.form-control, textarea.form-control, input[name=roleslist], select[name=groupusertype]", "${_("You have unsaved changes that will be lost.")}");
	});
 </script>
<script type="text/javaScript">

	function addrow_ldap(){
		
		var rowCount = $('#grouptable tr').length;	
		typecolumn = "<select id='groupusertype"+rowCount+"' name='groupusertype'>";		
		typecolumn += "<option value='LDAPGROUP'>LDAPGROUP</option>";
		typecolumn += "<option value='LDAPOU'>LDAPOU</option>";
		typecolumn += "<option value='LDAP'>LDAP</option>";
		typecolumn += "</select>";
		
		row = "<tr id='"+rowCount+"'>";
		row += "<td><input type='text' class='form-control' id='groupuser"+rowCount+"' name='groupuser'></td>";
		row += "<td>"+typecolumn+"</td>";
		row += "<td>";
		//row += "<a href='#'><span class='glyphicon glyphicon-check'></span></a>";

		row += "<a href='JavaScript:deleteRow("+rowCount+")' class='link' ><span class='glyphicon glyphicon-remove' id='removeuser"+rowCount+"'></span></a>";

		row += "</td>";
		row += "</tr>";		
		$("#grouptable").append(row);
		$("#grouptable input.form-control").first().trigger("change");
	}
	
	
	
	function addrow_pam(){
		
		var rowCount = $('#grouptable tr').length;		
		typecolumn = "<select id='groupusertype"+rowCount+"' name='groupusertype'>";
		typecolumn += "<option value='PAMGROUP'>PAMGROUP</option>";
		typecolumn += "<option value='PAM'>PAM</option>";
		typecolumn += "</select>";
		
		row = "<tr id='"+rowCount+"'>";
		row += "<td><input type='text' class='form-control' id='groupuser"+rowCount+"' name='groupuser'></td>";
		row += "<td>"+typecolumn+"</td>";
		row += "<td>";
		//row += "<a href='#'><span class='glyphicon glyphicon-check'></span></a>";
		row += "<a href='JavaScript:deleteRow("+rowCount+")' class='link' ><span class='glyphicon glyphicon-remove' id='removeuser"+rowCount+"'></span></a>";\
		row += "</td>";
		row += "</tr>";
		$("#grouptable").append(row);
		$("#grouptable input.form-control").first().trigger("change");
	}
	
	function deleteRow(id){
		$("#" + id + " input.form-control").trigger("change");
		$("#"+id).remove();
	}
	
</script>

</%def>
<%def name="main_content()">
	<div class="row configuration">
	<%include file="leftpanel.mako"/>
		<div class="row principle">
			<div class="col-xs-8 pull-left">
				<div class="text-left col-xs-12">
					<h2>${_("Principals")}</h2>
					${_("A principal's resources and access is based on the role(s) they are granted.  Each role has a list of permissions that can be configured in the Roles tab")}.
				</div>
				<div class="col-xs-12">				
					%if messages:						   
						%if status == "success":						  
                             <div class="alert alert-success" id="alertp">
                            <a class="close" data-dismiss="alert">&times;</a>
                                ${ messages }
                            </div>                                                       
                        %else:
                               <div class="alert alert-danger" id="alertp">
                                <a class="close" data-dismiss="alert">&times;</a>
                                ${ messages  }
                                </div>
                        %endif    
						
					%endif
					
					<form id="principal" class="management" method="post" action="/principal/" onsubmit="return validateForm()" name="principalform">

				
					<input type="hidden" id="principalId" name="principalId" value="${ principalId  }">

						<div class="col-xs-4">
							<span class="control-group">
								<label for="Name" class="col-xs-11 role">${_("Name")}:</label>
									<div class="clearfix">
									</div>
								<div class="col-xs-12">														
								%if principalId:
									  <div class="col-xs-12" id="principalNameContainer">
									  <input type="hidden" class="form-control" id="name" name="name" value="${ name  }" />
									  ${ name  }									  
									  </div>
								%else:
									<input type="text" class="form-control" id="name" name="name" value="${ name  }" />
								%endif
								

								</div>
							</span>
						</div>
						<div class="col-xs-6">
							<span class="control-group">
								<label for="Description" class="col-xs-11 role">${_("Description")}:</label>
									<div class="clearfix">
									</div>
									<div class="col-xs-9">
										<textarea id="Description" name="description" class="form-control resize" maxlength="100">${ description }</textarea>
									</div>
							</span>
						</div>
						<div class="clearfix"></div>
						<div class="col-xs-12">
							${_("Roles")}
								<table class="table table-bordered">
									<tbody>
										%if status_code_roles == 2000:
											%for count,roles in enumerate(rolelist) :
												%for id in roles:										
												<tr>
													<td><label id="${ ''.join(roles[id]['name'].split(' '))  }">${ roles[id]['name']  }</label></td>
													%if roles[id]['id'] in existing_roles_list:
														<td><input type="checkbox" id="${ ''.join(roles[id]['name'].split(' '))  }CB" name="roleslist" value = "${ roles[id]['name']  }"  checked  /></td>
													% else:
														<td><input type="checkbox" name="roleslist" id="${ ''.join(roles[id]['name'].split(' '))  }CB" class="page1" value="${ roles[id]['name']  }"  /></td>
													% endif
												</tr>
												%endfor
											%endfor
										%else:
											<div class="alert alert-success">${ rolelist  }</div>
										%endif
									</tbody>
								</table>
							</div>
					
   <div class="clearfix"></div>
   
   <table class="table table-bordered width pull-left" id="grouptable">
				<thead>
					<tr id="0">
						<th class="bg">${_("Principal Entity")}</th>
            <th class="bg" colspan="2">Type</th>

          </tr>
        </thead>
        <tbody>
		
		%for num , group in enumerate(groupslist):
          <tr id ="${ num + 1 }">
		  
              <td><input type="text" class="form-control" id="groupuser${ num + 1  }" name="groupuser" value= "${ group['name']  }" /></td>
              <td>
			  <select id="groupusertype${ num + 1  }" name="groupusertype">
				%if LDAP_Entity == "true" and PAM_Entity == "false":
					<option value="LDAPGROUP" ${'selected' if group['type'] == "LDAPGROUP"  else ''  }>LDAPGROUP</option>
					<option value="LDAPOU" ${'selected' if group['type'] == "LDAPOU" else ''  }>LDAPOU</option>
					<option value="LDAP" ${'selected' if group['type'] == "LDAP" else ''  }>LDAP</option>
				%elif PAM_Entity == "true" and LDAP_Entity == "false":
					<option value="PAMGROUP" ${'selected' if group['type'] == "PAMGROUP" else ''  }>PAMGROUP</option>
					<option value="PAM" ${'selected' if group['type'] == "PAM" else ''  }>PAM</option>
				%else:
					<option value="LDAPGROUP" ${'selected' if group['type'] == "LDAPGROUP"  else ''  }>LDAPGROUP</option>
					<option value="LDAPOU" ${'selected' if group['type'] == "LDAPOU" else ''  }>LDAPOU</option>
					<option value="LDAP" ${'selected' if group['type'] == "LDAP" else ''  }>LDAP</option>		  
				%endif
			  </select>
			  </td>
              <td><a href="JavaScript:deleteRow('${ num + 1  }')" class="link" title="Delete"><span class="glyphicon glyphicon-remove" id="removeuser${ num + 1  }"></span></a></td>
          </tr>
		%endfor
	
		</tbody>
      </table>
		<div class="col-xs-4">
			<div class="addbut col-xs-7" id="principalPlusIcon">
				%if LDAP_Entity == "true" and PAM_Entity == "false":
					<span class="glyphicon glyphicon-plus pull-left" id="icon1" onclick="addrow_ldap()" style="cursor:pointer;" title="Add"></span>					
				%elif PAM_Entity == "true" and LDAP_Entity == "false":
					<span class="glyphicon glyphicon-plus pull-left" id="icon2" onclick="addrow_pam()" style="cursor:pointer;" title="Add"></span>					
				%else:
					<span class="glyphicon glyphicon-plus pull-left" id="icon3" onclick="addrow_ldap()" style="cursor:pointer;" title="Add"></span>					
				%endif
				</div>
			</div>
		</div>
		<div class="col-xs-12">
			<div class="row">
				<div class="col-xs-2">
				</div>
				<div class="col-xs-2">         
					<button type="button" class="btn btn-primary" style="margin-right: 10px" onclick="goto('principallist')" id="principalCancelBtn">${_("Cancel")}</button>
				</div>	
				<div class="col-xs-2"> 		
					<button type="submit" class="btn btn-primary" style="margin-right: 10px" name="action" value="Done" id="principalDoneBtn">${_("Done")}</button>
				</div>	
				<div class="col-xs-2">
					<button type="submit" class="btn btn-primary" name="action" value="Apply" id="principalApplyBtn">${_("Apply")}</button>
				</div>
			</div>
		</div>
   </form>
</div>
</div>
</div>
</%def>
  <%def name="end_script()">
  <script type="text/javascript">
$(function(){
   $(".close").click(function(){
      $("#alertp").alert();
   });
});  
</script>

	<script type="text/javascript">
function validateForm()
{
var x=document.forms["principalform"]["name"].value;
if (x==null || x=="")
  {
  alert("${_("Please enter principal name")}.");
  document.principalform.name.focus() ;
  return false;
  }
	isDirtyPlaceholder = false;
}

</script>
  <script type="text/javascript">
	$("#name").on("keydown", function (e) {
		return e.which !== 32;
	});  
   </script>
  </%def>
