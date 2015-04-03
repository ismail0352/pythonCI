## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />

<%def name="title()">${_("Viewpoint Role management")}</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()">

<script type="text/javascript">
	function editRole(id)
	{
		window.location.href = "/createrole/?roleid="+id+"&tab=configuration";
	}
	function deleteRole(id,name)
	{						
		// Disable default filtering for confirmation alert java script localization
		data = confirm("${_("Are you sure you want to delete role '{0}'?") | n,decode.utf8 }".replace("{0}", name ));
		if(data){			
			
			$('#loaderDiv').show();
			$('#loaderDiv').html('<div id="err preloader" class="preloader"></div>');			
			$.ajax({
				url:'/deleterole/?id='+id,
				type:'GET',
				cache:false,			
				success:function(result){
				
				$('#error').html('<a href="#" id="crossBtn" class="close" onClick="closeBtn()">&times;</a><div id="errpreloader" class="preloader"></div>');			
					if(result == "True"){
						$('#loaderDiv').hide();
						$('#myAlert').hide();
						$('#error').show();
						$('#error').addClass("alert alert-success");
						$('#error').append("${_("Role Identify by '{0}' deleted successfully")}".replace("{0}", name));											
						$('#errpreloader').hide();			
						refreshContentRole('rolelistrefresh')
					}									
					else{		
						$('#loaderDiv').hide();
						$('#myAlert').hide();
						$('#error').show();
						$('#error').addClass("alert alert-success");
						$('#error').show();
						$('#errpreloader').hide();						
						$('#error').append(result);
					}

				},
				error: function(jqXHR, textStatus, errorThrown){					
					$('#error').addClass("alert alert-success");
					$('#error.preloader').hide();
					$('#error').show();
					$('#error').text("Error! " + textStatus + "" + errorThrown);				
				}			
			});
		}				
	}	
	
</script>

<script type="text/javascript">
		$(document).ready(function(){
			$('#rolelistcontainer.preloader').show();
			$.ajax({
				url:'/rolelist_grid/',
				type:'GET',
				data:{},
				success:function(result){
					$('#rolelistcontainer.preloader').hide();
					$('#rolelistcontainer').html(result);
					disablePaginationContent();
					 var h = document.getElementById("page-content").offsetHeight;
					 $("#side").height(h);	
			}
			
		});
	});
</script>

</%def>
<%def name="main_content()">

		<div class="row rolesmanagement">
		<%include file="leftpanel.mako"/>
			<div class="col-xs-8 pull-left padle15">

			
				<h2>${_("Role Management")}</h2>
					<form id="rolemanagement">
						%if messages:
						  %if status == "success":						  
    							<div class="alert alert-success" id="myAlert">
    							 <a href="#" class="close" data-dismiss="alert">&times;</a>
    							${ messages  }				
    							</div>
    					   %else:
    					       <div class="alert alert-danger" id="myAlert">
                                 <a href="#" class="close" data-dismiss="alert">&times;</a>
                                ${ messages  }               
                                </div>
    					   %endif				
						%endif
						<div style="display:none;" id="error" name="error">

						</div>
						
						<div style="display:none;" id="loaderDiv">

						</div>
				
						<div class="col-xs-3">
						</div>
						<div class="clearfix"></div>
						<div class="text-left col-xs-3">

							<button type="button" class="btn btn-primary" onclick="createRole()" id="create_role">${_("Create")}</button>							

						</div> 
						<div class="text-left col-xs-3">
							<span class="refresh"  id="rolelistrefresh"  onClick="refreshRoleListPage('rolelistrefresh');"></span>
						</div> 
						<div class="col-xs-12">
							<div class="clearfix"></div>
								<div class="col-xs-12">
									<div id="rolelistcontainer">
									<div class="preloader"></div>
									</div>
		</div>
	</div>
	</form>							
	</div>	
</div>

  </%def>
<%def name="end_script()">
<script type="text/javascript">
function closeBtn(){

	$('#error').hide();
}


</script> 
</%def>
