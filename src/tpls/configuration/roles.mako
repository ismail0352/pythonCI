## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />

<%def name="title()">${_("Viewpoint Roles")}</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()">
<script type="text/JavaScript">
		$(document).ready(function(){
					 var h = document.getElementById("page-content").offsetHeight;
					 $("#side").height(h);
					 });
 </script>
</%def>
<%def name="main_content()">
<div class="row configuration">
		<%include file="leftpanel.mako"/>
		<div class="row rolesmanagement">
			
			<div class="col-xs-7 pull-left">
		<h2>${_("Roles")}</h2>
	</div>
	<div class="col-xs-8 padle15">	
	%if messages:
	   %if status == "success":	      
            <div class="alert alert-success" id="alertrole">
            <a href="#" class="close" data-dismiss="alert" id="alert_success_closeBtn">&times;</a>
                ${ messages  }
            </div>
       %else:
            <div class="alert alert-danger" id="alertrole">
            <a href="#" class="close" data-dismiss="alert" id="alert_danger_closeBtn">&times;</a>
                ${ messages  }
            </div>
       %endif
    %endif
	
		<form id="roles" class="management" method="post" action="/createrole/" name="roleform" onsubmit="return validateForm()">
			<span class="control-group">
				<label for="RoleName" class="col-xs-3">${_("Enter Role Name")}</label>
					<div class="col-xs-5">
					%if role['id']:
						<div class="col-xs-12" id="roleNameContainer">
						<input type="hidden" id="RoleName" name="RoleName" value="${ role['name']  }"  />
						${ role['name']  }  </div>
					%else:					
						<div class="col-xs-12"><input type="text" class="form-control" id="RoleName" name="RoleName"/></div>
					%endif
					</div>
				<div class="col-xs-3">
					<!--<div class="text-left">
							<button type="submit" class="btn btn-primary">${_("Create Role")}</button>
					</div> -->  
				</div>
			</span>
			<div class="clearfix"></div>
			<span class="control-group">
				<label for="Description" class="col-xs-3">${_("Description")}</label>
					<div class="col-xs-5">
						<textarea class="form-control resize" id="Description" name="Description" maxlength="100">${ role['description']  }</textarea>
					</div>
			</span>
			<div class="clearfix"></div>
            %if isinstance(data, dict):
                <div class="col-xs-5 text-left">
                    <b>${_("Viewpoint Permissions")} :</b>
                    
                    <div class="clearfix"></div>
					   <table class="table borderless" cellpadding="0" cellspacing="0" style="margin-bottom:0px;">
							<tr>
								<td width="11%">
								<input type="checkbox" id="selectallvp"/>
								</td>
								<td>${_("Select All")}</td>
							</tr>
						</table>
                        <div class="col-xs-12 padding ">
                            <table class="table" cellpadding="0" cellspacing="0">
                                %if data['permissions']:
                                    %for count, perm in enumerate(data['permissions']):
                                        %for p in perm:
                                            <tr>
                                                <td>
                                                    
                                                    % if p in rolepermission:
                                                        <input type="checkbox" name="permissions" id="${ ''.join(perm[p]['label'].split(' '))  }CB" class="checked" value="${ p  }" checked />
                                                    % else:
                                                        <input type="checkbox" name="permissions" id="${ ''.join(perm[p]['label'].split(' '))  }CB" class="checked" value="${ p  }" />
                                                    % endif
                                                </td>	
                                                <td>										
                                                    <label for="permissions" id="${ ''.join(perm[p]['label'].split(' '))  }" class="col-xs-11">${ perm[p]['label']  }</label>
                                                </td>
                                            </tr>
                                        %endfor	
                                    %endfor	
                                %else:
                                    <br/>
                                    ${_("No view point permissions found!!")}                                    
                                %endif

                        </table>
                    </div>
                </div>
                <div class="col-xs-5 text-left">
                    <b> ${_("Domain Permissions")} :</b>
					 <div class="clearfix"></div>
                    <table class="table borderless" cellpadding="0" cellspacing="0" style="margin-bottom:0px;">
						<tr>
							<td width="11%">
								<input type="checkbox" id="selectall"/>
							</td>
							<td>${_("Select All")}</td>
						</tr>
					</table>
							
                   
                        <div class="col-xs-12 padding scroll">
                            <table class="table borderless" cellpadding="0" cellspacing="0">
							
							
                                %if data['domainpermissions']:
                                    %for count, perm in enumerate(data['domainpermissions']):
                                        %for p in perm:
                                        
                                            <tr>
                                            
                                                <td>
                                                    
                                                    % if p in rolepermission:
                                                        <input type="checkbox" name="permissions" id="${ ''.join(perm[p]['label'].split(' '))  }CB" class="page1" value="${ p  }" checked />
                                                    % else:
                                                        <input type="checkbox" name="permissions" id="${ ''.join(perm[p]['label'].split(' '))  }CB" class="page1" value="${ p  }" />
                                                    % endif
                                                </td>									
                                                <td>
                                                    <label for="permissions" id="${ ''.join(perm[p]['label'].split(' '))  }" class="col-xs-12">${ perm[p]['label']  }</label>
                                                </td>
                                            </tr>
											
                                        %endfor	
                                    %endfor		
                                %else:
                                <br/>
                                ${_("No Domain permissions found!!")}                                    
                                %endif
								
                        </table>
                    </div>
                </div>
            %else:
                <div class="alert alert-success">${ data  }</div>
            %endif
            
		<div class="col-xs-12">			
			<div class="col-xs-2">
			<input type="hidden" id="roleid" name="roleid" value="${ role['id']  }">
				<div class="text-left">
					<button type="button" class="btn btn-primary" onclick="goto('rolelist')" id="roleCancelBtn">
					${_("Cancel")}
					</button>
				</div> 
			</div>
			<div class="col-xs-2">
				<div class="text-left">
					<button type="submit" name="submit" id="submitDone" class="btn btn-primary" value="Done">
					${_("Done")}
					</button>
				</div> 
			</div>
			<div class="col-xs-2">
				<div class="text-left">
					<button type="submit" name="submit" id="submit" class="btn btn-primary" value="Apply">
					${_("Apply")}
					</button>
				</div> 
			</div>
			
		</div>
		</form>
		</div>
  </div>
</%def>
<%def name="end_script()">
 <script type="text/javascript">
$(function(){
   $(".close").click(function(){
      $("#alertrole").alert();
   });
});  
</script>

	<script type="text/javascript">
function validateForm()
{
var x=document.forms["roleform"]["RoleName"].value;
if (x==null || x=="")
  {
  alert("Please enter role name.");
  document.roleform.RoleName.focus() ;
  return false;
  }
	isDirtyPlaceholder = false;
}

</script>
 <script type="text/javaScript">
	$(document).ready(function() {
    $('#selectall').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.page1').each(function() { //loop through each checkbox
                this.checked = true;                 
            });
        }else{
            $('.page1').each(function() { //loop through each checkbox
                this.checked = false;                        
            });         
        }
    });
    createDirtyUnloadListener("input.form-control, textarea.form-control, input[name=permissions], #selectall, #selectallvp","${_("You have unsaved changes that will be lost.")}");
});
</script>
 <script type="text/javaScript">
	$(document).ready(function() {
    $('#selectallvp').click(function(event) {  //on click 
        if(this.checked) { // check select status
            $('.checked').each(function() { //loop through each checkbox
                this.checked = true;                 
            });
        }else{
            $('.checked').each(function() { //loop through each checkbox
                this.checked = false;                        
            });         
        }
    });
    
});
</script>
  <script type="text/javascript">
	$("#RoleName").on("keydown", function (e) {
		return e.which !== 32;
	});  
   </script>
</%def>
