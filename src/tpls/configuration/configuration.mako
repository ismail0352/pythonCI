## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />
<%namespace name="base" file="base.mako" />
<%def name="title()">${_("Viewpoint Configuration")}</%def>
<%def name="head_tags()"></%def>
<%def name="jquery_tags()">
<script type="text/JavaScript">
		$(document).ready(function(){
					 var h = document.getElementById("page-content").offsetHeight;
					 $("#side").height(h);

				createDirtyUnloadListener("input.form-control","${_("You have unsaved changes that will be lost.")}");
		});
 </script>
</%def>
<%def name="main_content()">
	<div class="row configuration">
	<%include file="leftpanel.mako"/>

		<div class="col-xs-8">
			<div class="col-xs-12 section-header search-filter-section">
				
				<h1><b>${_("MWS Configuration")}</b></h1>
				<div>										
						<div class="alert alert-danger" id="myAlert" style="display:none">				
						</div>
						<div class="alert alert-success" id="successAlert" style="display:none">                
                        </div>								
				</div>
				
			</div>
			<div class="clearfix"></div>

			<div class="col-xs-12 search-filter-section">
				<form id="contact-form" class="form-horizontal" action="/configuration/" method="POST">
					<span class="control-group">
						<label for="URL" class="col-xs-2 text-left">${_("Server")}</label>
						<div class="col-xs-8">
							<input type="text" class="form-control" id="URL" name="URL" value="${ fileData['URL']  }" required />
							<div id="testpreload" style="display:none;"></div>
							<span id="urlverify" class="glyphicon glyphicon-ok-circle valid" style="display:none;"></span>
							<span id="urlwrong" class="glyphicon glyphicon-remove" style="display:none;"></span>
							<span id="lblLegitimate style="display:none;"></span>
						</div>
						<div class="col-xs-2"></div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">
						<label for="Username" class="col-xs-2 text-left">${_("Username")}</label>
						<div class="col-xs-8">
							<input type="text" class="form-control" id="Username" name="Username" value="${ fileData['USERNAME']  }" required />
						</div>
						<div class="col-xs-2"></div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">
						<label for="Password" class="col-xs-2 text-left">${_("Password")}</label>
						<div class="col-xs-8">
							<input type="password" class="form-control" id="Password" name="Password" value="${ fileData['PASSWORD']  }" required/>
						</div>
						<div class="col-xs-2"></div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">
						<label for="Path" class="col-xs-2 text-left">${_("Path")}</label>
						<div class="col-xs-8">
							<input type="text" class="form-control" id="Path" name="Path" value="${ fileData['SUB_URL']  }" required/>
						</div>
						<div class="col-xs-2"></div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">
						<label for="ClientId" class="col-xs-2 text-left" title="This is required for OAuth.">${_("Client Id")}</label>
						<div class="col-xs-8">
							<input type="text" class="form-control col-xs-10 pull-left" id="ClientId" name="ClientId" title="${ fileData['CLIENTID']  }" value="${ fileData['CLIENTID']  }" required/>
						</div>
						<div class="col-xs-2"></div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">
						<label for="ClientSecret" class="col-xs-2 text-left" title="This is required for OAuth.">${_("Client Secret")}</label>
						<div class="col-xs-8">
							<input type="password" class="form-control" id="ClientSecret" name="ClientSecret" value="${ fileData['CLIENTSECRET']  }" required />
						</div>
						<div class="col-xs-2"></div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">

						<div class="col-xs-8">						
							% if fileData['GOOGLE_ANALYTICS'] == "1":
							<input type="checkbox" class="form-control" id="analytics" name="analytics" onclick="setAnalytics(this)" checked />
							%else:
							<input type="checkbox" class="form-control" id="analytics" name="analytics" onclick="setAnalytics(this)" />
							% endif
							<label for="analytics" class="col-xs-7 text-left required">${_("Use Google Analytics to help improve this product")} </label>
							<input type="hidden" id="analytics1" name="analytics1" value="" />
						</div>
					</span>
					<div class="clearfix"></div>
					<span class="control-group">
						<div class="col-xs-9 height">						
							<input type="checkbox" class="form-control" id="Permissions" name="Permissions" value="alert-danger" onclick="resetPermission(this)"/>
							<label for="Permissions" class="col-xs-7 text-left permission">${_("Reset Permissions")} </label>
							<input type="hidden" id="resetpermission" name="resetpermission" />
						<div class="alert alert-danger pull-left" style="display:none;" >${_("Warning : All permissions will be reset to default !")}</div>
						</div>
					</span>
					<div class="clearfix"></div>
					<div class="text-center">
						<div class="col-xs-2"></div>
						
						<div id="divSubmit" class="MWSConfiguration col-xs-2 text-left">
							<button type="button" class="btn btn-primary configprog" id="submit" onclick="testForm('save')">${_("Save")}</button>
						</div>
						<div  class="MWSConfiguration col-xs-2 text-center">
							<button type="button" class="btn btn-primary" onclick="testForm('test')" id="test">${_("Test")}</button>
						</div>
					</div>
				</form>
			</div>
		<div class="col-xs-12" style="margin-top:15px;"><div class="hrule"></div></div>
		<div class="col-xs-12">
			<h4>${_("Viewpoint Build Information")}</h4>
					<span class="control-group">
						<span class="col-xs-2 text-left">${_("Version")}:</span>
						<div class="col-xs-8">
							<span class="col-xs-10 pull-left">
								%if build_info["version"] is not None:
									${ build_info["version"]  }
								%else:
								   &nbsp;-&nbsp;
								%endif
							</span>
						</div>
						<div class="col-xs-2"></div>
					</span>

			<div class="clearfix"></div>
					<span class="control-group">
						<span class="col-xs-2 text-left">${_("Revision")}:</span>
						<div class="col-xs-8">
							<span class="col-xs-10 pull-left">
								%if build_info["changeset"] is not None:
									${ build_info["changeset"] }
								%else:
								   &nbsp;-&nbsp;
								%endif
							</span>
						</div>
						<div class="col-xs-2"></div>
					</span>

			<div class="clearfix"></div>
					<span class="control-group">
						<span class="col-xs-2 text-left">${_("Build Date")}:</span>
						<div class="col-xs-8">
							<span class="col-xs-10 pull-left">
								%if build_info["build_date"] is not None:
									${ build_info["build_date"]  }
								%else:
								   &nbsp;-&nbsp;
								%endif
							</span>
						</div>
						<div class="col-xs-2"></div>
					</span>

			<div class="clearfix"></div>
		</div>
		</div>
	</div>
</%def>
<%def name="end_script()">
	<script type="text/javascript">
		function setAnalytics(obj)
		{
			if(obj.checked){
				$("#analytics1").val(1)
			}
		}
		
		function resetPermission(obj)
		{
			$('.alert-danger.pull-left').toggle();
			if(obj.checked){				
				$("#resetpermission").val(1)
			}else{							
				$("#resetpermission").val(0)
			}
			
		}
	
		function testURLOnSubmit(){
			var urlPattern = /(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/;
			var txtfield = $("#URL").val();
			if (urlPattern.test(txtfield)){
				url = $("#URL").val();				
				$("#lblLegitimate").hide();
				$("#urlverify").hide();
				$("#urlwrong").hide();
				$("#testpreload").show();	
				$("#testpreload").addClass("configuration-preloader");
				$.ajax({
						
								url:'/configurationtest/?url='+url,
								type:'GET',
								cache:false,			
								success:function(result){
									if(result.toLowerCase() == "true")
									{
										$("#urlverify").show();
										$("#testpreload").hide();
										//$("#urlwrong").css();
										return true;
									}
									else if(result.toLowerCase()  == "false"){
		
										$("#urlwrong").show();
										$("#testpreload").hide();
										$("#urlverify").hide();
										
										return false;
										}
								},
								error: function(){
									
									$("#urlwrong").show();
									$("#testpreload").hide();
									$("#urlverify").hide();
									$("#lblLegitimate").show();
									$("#lblLegitimate").text("* not a valid URL pattern");
									return false;
								}			
						}); 
				}
				else{
					$("#lblLegitimate").show();
					$("#lblLegitimate").text("* not a valid URL pattern");
					$("#urlwrong").hide();
					$("#testpreload").hide();
					$("#urlverify").hide();
				}
		}
	
	
		function testURL()
		{
		
							//Code to validate the required fields, done on 8/14/14 - abhinavr
						if(!validateConfigurationForm('URL'))
							return false;
						if(!validateConfigurationForm('Username'))
							return false;
						if(!validateConfigurationForm('Password'))
							return false;
						if(!validateConfigurationForm('ClientId','${_('Client Id')}'))
							return false;
						if(!validateConfigurationForm('ClientSecret','${_('Client Secret')}'))
							return false;
					
						//Code to validate the required fields ends
						
						url ='&Username='+$('#Username').val() + '&Password='+$('#Password').val() + 
                            '&ClientId='+$('#ClientId').val() +'&ClientSecret='+$('#ClientSecret').val() +'&URL='+$('#URL').val() +'&Path='+$('#Path').val();
                            					
						$("#lblLegitimate").hide();
						//alert(url)
						$("#urlverify").hide();
						$("#urlwrong").hide();
						$("#testpreload").show();	
						$("#testpreload").addClass("configuration-preloader")
						$.ajax({
						
								url:'/configurationtest/?'+url,
								type:'GET',
								cache:false,			
								success:function(result){
									if(result.toLowerCase() == "true")
									{
										$("#urlverify").show();
										$("#testpreload").hide();
										$("#urlwrong").css();
										
                                        $('#myAlert').empty();
                                        $('#myAlert').html('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">&times;</a>');
                                        $('#myAlert').append("${_("Provided information is invalid")}");
                                        $('#myAlert').show();
                            
                            
										return true;
									}
									else if(result.toLowerCase()  == "false"){
		
										$("#urlwrong").show();
										$("#testpreload").hide();
										$("#urlverify").hide();

                                        $('#myAlert').empty();
                                        $('#myAlert').html('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">&times;</a>');
                                        $('#myAlert').append("${_("Provided information is invalid")}");
                                        $('#myAlert').show();
                                        
										return false;
										}
								},
								error: function(){
									
									$("#urlwrong").show();
									$("#testpreload").hide();
									$("#urlverify").hide();
									
                                    $('#myAlert').empty();
                                    $('#myAlert').html('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">&times;</a>');
                                    $('#myAlert').append("${_("Provided information is invalid")}");
                                    $('#myAlert').show();
                                        
                                        
									return false;
								}			
						}); 
				
		}
	
	</script>
	
<script type="text/javascript"> 

function testForm(action)
{
		//Code to validate the required fields, done on 7/4/14 - abhinavr
			if(!validateConfigurationForm('URL'))
				return false;
			if(!validateConfigurationForm('Username'))
				return false;
			if(!validateConfigurationForm('Password'))
				return false;
			if(!validateConfigurationForm('Path'))
				return false;
			if(!validateConfigurationForm('ClientId','${_('Client Id')}'))
				return false;
			if(!validateConfigurationForm('ClientSecret','${_('Client Secret')}'))
				return false;
		
		//Code to validate the required fields ends

			//Code to post the form fields asynchronously

            
				url = $("#URL").val();				
				$("#lblLegitimate").hide();
				$("#urlverify").hide();
				$("#urlwrong").hide();
				$("#testpreload").show();	
				$("#testpreload").addClass("configuration-preloader");

				//$('#divSubmitLoader').show();
				if(action != 'test'){
				    $('#submit').text("In progress..");
				}
				//disabling the buttons on post start
					$('.form-control').prop('readonly', 'true');   //disables all textbox
					$('#submit').prop('disabled', true);
					$('#test').prop('disabled', true);
				//disabling the buttons on post ends 
				
				//removing the links
					$("#dashboard").removeAttr("href");
					$('#workload').removeAttr("href");
					$('#resources').removeAttr("href");
					$('#configuration').removeAttr("href");
					$('#mwsconfiguration').removeAttr("href");
					$('#roles').removeAttr("href");
					$('#principals').removeAttr("href");
					$('#signout').removeAttr("href");
					$('#settings').removeAttr("href");
					$('#help').removeAttr("href");
					$('#mwsconfiguration').css("color","#fff");
					$('#roles').css("color","#fff");
					$('#principals').css("color","#fff")
				//removing the links ends
				
				
					var formData = 'Username='+$('#Username').val() + '&Password='+$('#Password').val() + '&Action='+ action +
					'&ClientId='+$('#ClientId').val() +'&ClientSecret='+$('#ClientSecret').val() +'&URL='+$('#URL').val() +'&Path='+$('#Path').val() +'&analytics1='+$('#analytics1').val()+'&resetpermission='+$('#resetpermission').val();
					
      
					$.post('/configuration/',formData,function(result){
						if(result != 'False'){

							//Showing the alert message on success
								var res = "";
								var resStatus = ""
								if(result.lastIndexOf(",") > 0){
									res = result.substring(0,result.lastIndexOf(",")).trim();
									resStatus = result.substring(result.lastIndexOf(",")+1).trim()
								}else {
									res = result;
								}

								$('#myAlert').hide();
								$('#successAlert').hide();
								if(resStatus=="success"){
								     if(action != 'test'){
								        $('#successAlert').empty();
                                        $('#successAlert').html('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">&times;</a>');
                                        $('#successAlert').append(res);
                                        $('#successAlert').show();
										 // for turning off dirty check on save
										 isDirtyPlaceholder = false;
                                     }
                                     $("#urlverify").show();
                                     $("#testpreload").hide();
								}
								else{
								     $('#myAlert').empty();
                                     $('#myAlert').html('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">&times;</a>');
                                     $('#myAlert').append(res);
                                     $('#myAlert').show();
                                     
                                     $("#urlwrong").show();
                                    $("#testpreload").hide();
                                    $("#urlverify").hide();
								}
								
								$('#submit').text("Save");
							//Showing the alert message on success ends

							//enabling the buttons on post
								$('#submit').prop('disabled', false);
								$('#test').prop('disabled', false);
								$('.form-control').removeAttr('readonly');
							//Enabling the buttons on post ends
							
							//Adding the links again
								$("#dashboard").attr("href","/dashboard/");
								$('#workload').attr("href","/workload/");
								$('#resources').attr("href","/nodelist/");
								$('#configuration').attr("href","/configuration/");
								$('#mwsconfiguration').attr("href","/configuration/");
								$('#roles').attr("href","/rolelist/?tab=configuration");
								$('#principals').attr("href","/principallist/?tab=configuration");
								$('#signout').attr("href","/logout/");
								$('#settings').attr("href","/configuration/");
								$('#help').attr("href","http://docs.adaptivecomputing.com/suite/8-0/enterprise/help.htm");
							//Adding the links again ends
						}
					});

				
				//return false;
			//Code to post the form fields asynchronously ends
}
function closeBtn(){

	$('#myAlert').hide();
	$('#successAlert').hide();
}
</script>
<script type="text/javascript">
<!--
// Form validation code will come here.
function validateConfigurationForm(ctrlName, ctrlValue)
{
   if( $('#' + ctrlName + '').val().trim() == "" )
   {
	 if(ctrlValue == undefined || ctrlValue == null || ctrlValue.trim() == ""){
		 ctrlValue = ctrlName
	 }
     alert( "Please provide valid value for " +  ctrlValue);
     $('#' + ctrlName + '').focus() ;
     return false;
   }
   
   if(!document.getElementById("URL").value.match(/^[\u0020-\u007e]+$/))            
    {
        $('#myAlert').empty();
        $('#myAlert').append('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">x</a>Invalid URL: Server url is invalid');
        $('#myAlert').show();
        return false;
    }
    
    if(!document.getElementById("Path").value.match(/^[\u0020-\u007e]+$/))          
    {
        $('#myAlert').empty();
        $('#myAlert').append('<a onclick="closeBtn()" class="close" id="crossBtn" href="#">x</a>Invalid URL: Server path is invalid');
        $('#myAlert').show();
        return false;
    }
   
   return true;
}
//-->
</script>
</%def>
