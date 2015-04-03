## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />

<%def name="title()">${_("Viewpoint Principal management")}</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()">
<script type="text/javascript">
		$(document).ready(function(){
			$('#principallistcontainer.preloader').show();
			$.ajax({
				url:'/principallist_grid/',
				type:'GET',
				data:{max:10, offset:1},
				success:function(result){
					$('#principallistcontainer.preloader').hide();
					$('#principallistcontainer').html(result);
					 var autoheight = document.getElementById("page-content").offsetHeight;
					 $("#side").height(autoheight);
			}
		});
	});
</script>
<script type="text/javascript">
	function editPrincipal(id)
	{
		window.location.href = "/principal/?principalId="+id+"&tab=configuration";
	}
	
	function deletePrincipal(id,name)
	{
		// Disable default filtering for confirmation alert java script localization
		data = confirm("${_("Are you sure you want to delete principal '{0}'?") | n,decode.utf8 }".replace("{0}", name));
		if(data){			
			
			$('#loaderDiv').show();
			$('#loaderDiv').html('<div id="err preloader" class="preloader"></div>');
				
			$.ajax({
				url:'/deleteprincipal/',
				type:'GET',
				data:{principalId:id, name:name},
				cache:false,			
				success:function(result){
				$('#error').html('<a href="#" id="crossBtn" class="close" onClick="closeBtn()">&times;</a><div id="errpreloader" class="preloader"></div>');			
					if(result == "True"){
						$('#loaderDiv').hide();
						$('#myAlert').hide();
						$('#alertp').hide();
						$('#error').show();
						$('#error').addClass("alert alert-success");
						$('#error').append("${_("Principal Identify by '{0}' deleted successfully")}".replace("{0}", name));											
						$('#errpreloader').hide();			
						refreshContentPrincipal('principallistrefresh')
											
					}else{		
						$('#loaderDiv').hide();
						$('#myAlert').hide();
						$('#alertp').hide();
						$('#error').show();
						$('#error').addClass("alert alert-success");
						$('#error').show();
						$('#errpreloader').hide();						
						$('#error').append(result);
					}
						
				},
				error: function(jqXHR, textStatus, errorThrown){
					alert("false");
					$('#error').addClass("alert alert-success");
					$('#error .preloader').hide();
					$('#error').show();
					$('#error').text("Error! " + textStatus + "" + errorThrown);		
				}			
			});
		}				
	}	
</script>
</%def>
<%def name="main_content()">
<div class="row configuration">
<%include file="leftpanel.mako"/>
	<div id="mainContent" class="row rolesmanagement">
			<div class="col-xs-8 pull-left padle15">
			
			<h2>${_("Principal Management")}</h2>
				<form id="rolemanagement">
				%if messages:				    
					%if status == "success":                          
                             <div class="alert alert-success" id="alertp">
                            <a class="close" data-dismiss="alert">&times;</a>
                                ${ messages  }
                            </div>                                                       
                     %else:
                               <div class="alert alert-danger" id="alertp">
                                <a class="close" data-dismiss="alert">&times;</a>
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
						<button type="button" class="btn btn-primary" onclick="createPrincipal()" id="create_principal">${_("Create")}</button>
					</div> 
					<div class="text-left col-xs-3">
						<span class="refresh" id="principallistrefresh"  onClick="refreshPrincipalList('principallistrefresh');"></span>
					</div> 
					<div class="col-xs-12">
					<div class="clearfix"></div>
					<div class="col-xs-12">
						<div id="principallistcontainer" style="overflow:auto;">  
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
$(function(){
   $(".close").click(function(){
      $("#myAlert").alert();
   });
});  
</script>
<script type="text/javascript">
function closeBtn(){
	$('#error').hide();
}
</script> 
</%def>
