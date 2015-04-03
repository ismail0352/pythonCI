## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>
<%inherit file="base.mako" />

<%def name="title()">${_("Viewpoint Node Details")}</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()">
<script type="text/javascript">
	$(document).ready(function(){
		$('span.glyphicon-remove').click(function(){
			$(this).parent().fadeOut().remove();
			if ($('.features span.label').length == 0) {
				setMsg();	
				//$('.features').append('<span id="dmsg">${_("No Features added")}</span>')
				//$('.features').append(${_("No Features added")});
			}
			
		});
		//Need this on so dirty check is turned on for passed in fields
		createDirtyUnloadListener("#conFeaturesContainer","${_("You have unsaved changes that will be lost.")}");
	});
	
	function setMsg(){
		$('.features').append('<span id="dmsg">${_("No Features added")}</span>')
	}
</script>
</%def>

<%def name="main_content()">
	<div class="row">
	% if status_code == 2000 : 
		<form class="form-nodeDetail" role="form" method="post" action='/nodedetails/'>
				%if messages:
				    %if status == "success":				    
        				<div class="alert alert-success" >
        					<a href="#" class="close" data-dismiss="alert">&times;</a>
        					${ messages | n,decode.utf8}
        				</div>
        			%else:
        			     <div class="alert alert-danger">
                            <a href="#" class="close" data-dismiss="alert">&times;</a>
                            ${ messages | n,decode.utf8}
                        </div>
        			%endif
			%endif
				
				<div class="col-xs-6">
					<h1><b>${_("Node Details")}</b></h1>
					<div class="row">
						<input type="hidden" name="node_name" value=${entries[0]['name']  } />
						<div class="col-xs-5 node-left-sub-section">${_("Name")}</div>
						<div id="node_details_name_value" class="col-xs-7 node-right-sub-section">${entries[0]['name']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("State")}</div>
						<div id="node_details_state_value" class="col-xs-7 node-right-sub-section">${entries[0]['state']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Power")}</div>
						<div id="node_details_power_value" class="col-xs-7 node-right-sub-section"><span class="ico_on"></span>${entries[0]['power_actual_state']  }</div>
					</div>
					<%doc><div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Tenant")}</div>
						<div id="node_details_tenant_value" class="col-xs-7 node-right-sub-section"> - </div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Datacenter")}</div>
						<div id="node_details_datacenter_value" class="col-xs-7 node-right-sub-section"> - </div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Hypervisor type")}</div>
						<div id="node_details_hv_type_value" class="col-xs-7 node-right-sub-section"> - </div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Virtual Machines")}</div>
						<div id="node_details_vm_value" class="col-xs-7 node-right-sub-section"> - </div>
					</div></%doc>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("IP Address")}</div>
						<div id="node_details_ip_value" class="col-xs-7 node-right-sub-section">${entries[0]['ip_address']}</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Image")}</div>
						<div id="node_details_image_value" class="col-xs-7 node-right-sub-section">${entries[0]['image']}</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Resource Managers")}</div>
						<div id="node_details_rm_value" class="col-xs-7 node-right-sub-section">
						%if torquelist:
						
							%for i in torquelist:
								${i  }<br />
							%endfor
						%endif
						</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Jobs")}</div>
						<div id="node_details_jobs_value" class="col-xs-7 node-right-sub-section">${entries[0]['jobs']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Reservations")}</div>
						<div id="node_details_reservations_value" class="col-xs-7 node-right-sub-section">${entries[0]['reservations']  }</div>
					</div>
				</div><!-- .col-xs-6 ends -->
				<div class="col-xs-6">
					<h1><b>${_("Resources")}</b></h1>
					<!--<div class="row">
						<div class="col-xs-6 left-sub-section">Node List</div>
						<div class="col-xs-6 right-sub-section">
							<span class="label label-primary"><a href="#">x86-090</a></span>
							<span class="label label-primary"><a href="#">x86-089</a></span>
							<span class="label label-primary"><a href="#">x86-088</a></span>
							<span class="label label-primary"><a href="#">x86-087</a></span>
							<span class="label label-primary"><a href="#">x86-086</a></span>
						</div>
					</div>-->
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Real processors")}</div>
						<div id="node_details_real_procs_value" class="col-xs-7 node-right-sub-section">${entries[0]['real_processors']  }</div>
					</div>
					<%doc><div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Processor overcommit limit")}</div>
						<div id="node_details_proc_overcommit_value" class="col-xs-7 node-right-sub-section">${entries[0]['processor_overcommit_limit']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Memory (MB) overcommit limit")}</div>
						<div id="node_details_mem_overcommit_value" class="col-xs-7 node-right-sub-section">${entries[0]['memory_overcommit_limit']  }</div>
					</div></%doc>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Available processors")}</div>
						<div id="node_details_available_procs_value" class="col-xs-7 node-right-sub-section">${entries[0]['available_processors']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Real memory")}</div>
						<div id="node_details_real_mem_value" class="col-xs-7 node-right-sub-section">${entries[0]['real_memory_mb']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">${_("Available memory")} (MB)</div>
						<div id="node_details_available_mem_value" class="col-xs-7 node-right-sub-section">${entries[0]['available_memory_mb']  }</div>
					</div>
					<div class="row">
						<div class="col-xs-5 node-left-sub-section">CPU ${_("Utilization")}</div>
						<div id="node_details_cpu_utilization_value" class="col-xs-7 node-right-sub-section">${entries[0]['cpu_utilization']  }%</div>
					</div>
					<div class="row">
					<div>
					<div class="dtGrid datagrid-container container panel panel-default mrlt" style="margin-left:0 !important;width:60%;">
						<table class="table table-bordered">
						<thead>
						<tr>
						<th width="80%">Generic Resource </th>
						<th>Count </th>
						</tr>
						</thead>
						<tbody>
						%if generic_resources:
							%for cnt,i in enumerate(generic_resources):
								<tr>
								<td><div id="genericResource${cnt  }" style="word-wrap: break-word;">${i['generic_resource']  }</div></td>
								<td id="count${cnt  }">${i['count']  }</td>
								</tr>
							%endfor
						%else:
							<tr>
								<td colspan=2 align="center" id="genericResource" >No Generic Resources present for this node</td>
							</tr>	
						%endif 
						</tbody>
						</table>
					</div>
					</div>
						
					</div>
				</div><!-- .col-xs-6 ends -->
			</div><!-- .row ends -->
			<div class="row">
				<div class="col-xs-12">
					<div class="hrule"></div>
				</div>
			
				<div class="row">
					<div class="col-xs-12">
						<h1><b>${_("Features")}</b></h1>
					</div>
					<div class="col-xs-2 node-left-sub-section">${_("Reported features")}</div>
					<div class="col-xs-4 paddTop10" id="reported_features_container">
					%if featurelist:
						%for count,i in enumerate(featurelist):
							<span class="label label-default"><a id="reportedFeature${ count  }">${i  }</a></span>
						%endfor
					%else :
						<span id="reportedFeature">${ featurelist  }</span>
					%endif
					</div>
					<div class="col-xs-6">&nbsp;</div>
				</div>
				<div class="row">
					<div class="col-xs-2 node-left-sub-section">${_("Configurable features")}</div>
					<input type="hidden" name="cfList" id="cfList" value="" />
					<div id="conFeaturesContainer" class="col-xs-4 features job-details" style="width: 30%;">
						%if config_features:
							%for i in config_features:
								<span class="label label-default" >
									<a class="a" id="conFeature_${ i }">${ i }</a>
									<span class="glyphicon glyphicon-remove" id="destroyConFeature_${ i }" onclick="hideConFeatures($(this).parent(),'${ i }')"></span>
								</span>
							%endfor
						%else:
							<span id="dmsg">No Features added</span>
						%endif
						<span class="add configFeat" data-toggle="modal" data-target="#cfModal">+</span>
					</div>
					
					<!-- Configurable features Modal -->
					<div class="modal fade" id="cfModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
						<div class="modal-dialog">
							<div class="modal-content">
								<div class="modal-header">
									<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
									<h4 class="modal-title" id="myModalLabel">${_("Configurable features")}</h4>
								</div>
								<div class="modal-body">
									<div class="modal-body res-list" style="padding-top:0;">
                                         <div id="newCustomFeatureContainer" style="margin-bottom: 20px;">
                                                <span style="font-weight: bold;">Add New Feature:</span>
                                                <input type="text" id="newCustomFeature" placeholder="New Feature" style="width:80%; margin-right:10px;padding:5px;">
                                                <button type="button" class="btn btn-primary default" id="addNewfeature"  onclick="addConFeatures($('#newCustomFeature'))" value="Add">Add</button>
                                            </div>
										<table class="table" width="100%" cellspacing="1" cellpadding="0" border="0" id="grouptable">
											<tr>
												<th>${_("Add")}</th>
												<th>${_("Feature")}</th>
												<th>${_("Available")}</th>
												<th>${_("Description")}</th>
											</tr>
											%if config_features_list:
												%for conf_features in config_features_list:
													
													<tr>
													%if conf_features['feature'] in config_features:
														<td>
															<span class="add config_features_hide"  style="cursor:pointer;" id="addconfeature_${ conf_features['feature'] }">-</span>
														</td>
													%else:
														<td>
															<span class="add config_features_add" style="cursor:pointer;" id="addconfeature_${ conf_features['feature'] }">+</span>
														</td>
													%endif
														<td id="feature_value_${ conf_features['feature'] }">${ conf_features['feature'] }</td>
														<td>${ conf_features['available'] }</td>
														<td>${ conf_features['description'] }</td>
													</tr>
												%endfor
											%endif
										</table> 
									</div>
									
								</div>
								<div class="modal-footer">
									<button type="button" class="btn btn-primary default" data-dismiss="modal" name="action" value="Done">&nbsp; ${_("Done")} &nbsp;</button>
								</div>
							</div>
						</div>
					</div>
					<!-- Configurable features Modal ends -->
				</div>
				<div class="col-xs-6 paddTop10">&nbsp;</div>
				<div class="col-xs-6 paddTop10">
					<div style="float:right;clear:both">
					<button type="button" id="node_details_cancel_button" class="btn btn-primary default" style="margin-right: 10px" onClick=goto('nodelist')>${_("Cancel")}</button>
					<button type="submit" id="node_details_done_button" onclick="prepareNodeData()" class="btn btn-primary default" style="margin-right: 10px" name="action" value="Done">${_("Done")}</button>
					<button type="submit" id="node_details_apply_button" onclick="prepareNodeData()" class="btn btn-primary default" style="margin-right: 10px" name="action" value="Apply">${_("Apply")}</button>
				</div>
			</div>
		</form>
% else:
	
	<div><h5>${ entries  } </h5></div>

%endif
	</div><!-- main .row ends -->
</%def>
<%def name="end_script()">
		<script type="text/javascript">

            $('#cfModal table').on("click", "span.add", function (event) {
                var feature =  $(this).attr('id').substring(14);
				var status = 0;
                if ($(this).html().trim() == "-") {
                	status = 1;
                }
				toggleConFeature($(this), feature, status)
            });
            $('#newCustomFeature').bind('keypress', function (event) {
                var k = String.fromCharCode(event.which);
                var regex = /^([A-Za-z0-9]|\_|\-)$/;
                if (event.which != 8 && event.which != 0 && !regex.test(k)) {
                    event.preventDefault();
                }
                //enter pressed in textbox so adding
                if(event.which == 13){
                  $("#addNewfeature").trigger("click");
                }
            }).bind('paste', function (event) {
                var regex = /^([A-Za-z0-9]|\_|\-)+$/;
                var pastedText = event.originalEvent.clipboardData.getData('Text')
                if (!regex.test(pastedText)) {
                    event.preventDefault()
                }
            });
            function prepareNodeData() {
               var cflist = ""
                $("#conFeaturesContainer").find("span.label a").each(function () {
                    cflist+=","+$(this).text()
                });
                cflist=cflist.replace(/^(,)*/,'');
               
                $("#cfList").val(cflist);

			 	//Need this on so dirty check is disabled when saving
			    isDirtyPlaceholder = false;
            }
		</script>
</%def>
