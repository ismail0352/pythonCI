## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />
<%namespace name="base" file="base.mako" />

<%def name="title()">${_("Viewpoint Job Details")}</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()"></%def>
    
<%def name="main_content()">
<div class="row">
% if status_code == 2000 :
    <form class="form-jobDetail" role="form" method="post" action='/jobdetails/' onsubmit="return validate_Form()">
    
        <div class="col-xs-12">
            <h1><b>${_("Job Details")}</b></h1>         
            %if messages:
                %if status == "200":
                    <div class="alert alert-success">
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
            <div class="col-xs-12"><span class="case" id="jDJobID">${_("Job Id")} :  <span class="marginl" id="jDJobIDVal">${entries[0]['name']  }</span></span><input type="label" hidden id="job_name" name="job_name" size="20" value=${entries[0]['name']  } /><input type="hidden" name="job_status" value=${entries[0]['state']  } /><span class="right"><span class="case" id="jDStatus">${_("Status")}:<span><b class=${entries[0]['state']  } id="jDStatusVal">${entries[0]['state']  }</b></span></span></div>
                <input type="hidden" id="job_name" name="job_name" size="20" value=${entries[0]['name']  } />
                <input type="hidden" name="job_status" value=${entries[0]['state']  } />
                <input type="hidden" name="job_id" value=${ job_id  } />
                <div class="clearfix"></div>
            <!--<div class="alert alert-danger">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                <strong>${_("ERROR : The Job Status is Complete but the resource is not idle")}.
            </div>-->
            
            <div class="section-title-common"><p>Time Frame</p></div>
                <table class="table-common">
                    <thead>
                        <tr>
                            <td id="jDStartTm">${_("Start Time")}</td>
                            <td id="jDDuration">${_("Duration")}</td>
                            <td id="jDCompletionTm">${_("Completion Time")}</td>
                            <td id="jDActualDuration">${_("Actual")} ${_("Duration")}</td>                        
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="width:170px;" id="jDStartDateTmVal">${entries[0]['start_datetime']  }</td>
                            <td style=" position: relative; " id="jDTime">
                                <input id="durInput" type="text" readonly name="duration" class="form_save_data" value=${ duration_format } onkeypress="checkObjection(this,event)"/>
                                <!--<span id="infoPopUp" class="glyphicon glyphicon-time close-popover-link" style="cursor: pointer" data-container="body" rel="popover" data-placement="bottom"></span>-->
                                <span id="infoPopUp" class="glyphicon glyphicon-time close-popover-link" style="cursor: pointer" onclick="jobDetailsDuration()"></span>
                                <div id="durationContent" style="display:none" class="popover bottom">
                                <div class="arrow"></div>
                                <div class="popover-content">
                                    <div>
                                        <!--<input type="number" id="dInput" value="00" min="0" max="31" class="text-center" onkeypress="checkObjection(this,event)"/>&nbsp;:&nbsp;
                                        <input type="number" id="hInput" value="00" min="0" max="23" size="3" maxlength="2" class="text-center" onkeypress="checkObjection(this,event)" />&nbsp;:&nbsp;
                                        <input type="number" id="hInput" value="00" min="0" max="59" class="text-center" onkeypress="checkObjection(this,event)" />&nbsp;: &nbsp;
                                        <input type="number" id="sInput" value="00" min="0" max="59" class="text-center" onkeypress="checkObjection(this,event)"/>-->
										
										<div class="durationBtn">
										<input type="text" name="dInput" id="dInput" value="0" onkeyup="durationDay('dInput',0)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onmousedown="mousedownfunc('dInput', incrementDay)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('dInput', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
										<div class="durationBtn">
										<input type="text" name="hInput" id="hInput" value="0" onkeyup="durationHour('hInput',0,23)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onmousedown="mousedownfunc('hInput', incrementHour)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('hInput', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
										<div class="durationBtn">
										<input type="text" name="mInput" id="mInput" value="0" onkeyup="durationMinutes('mInput',0,59)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onmousedown="mousedownfunc('mInput', incrementMinutes)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('mInput', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
										<div class="durationBtn">
										<input type="text" name="sInput" id="sInput" value="0" onkeyup="durationSeconds('sInput',0,59)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onmousedown="mousedownfunc('sInput', incrementSeconds)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('sInput', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
									</div>
									<div class="clearfix"></div>
                                    <div class="labels">
                                        <span>days</span>
                                        <span>hours</span>
                                        <span>min</span>
                                        <span>sec</span>
                                    </div>
                                    <div class="cta">
                                        <input type="button" id="btnCancel"  onclick="cancelpopover()" class="btn btn-default" value="${_("Cancel")}">
                                        <input type="button" id="btnClear"  class="btn btn-default" value="${_("Clear")}" onclick="clearpopover()">
                                        <input type="button" id="btnApply"  class="btn btn-default" onclick="durationContent()" value="${_("Apply")}">
                                    </div>
                                </div>
                                </div>
                            </td>
                            <td id="jDCompleteionTmVal">${entries[0]['completion_datetime']  }</td>
                            <td id="jDActualFormatVal">${ actualduration_format }</td>
                        </tr>
                    </tbody>
                </table>
            </div><!-- .col-xs-10 ends -->
            <div class="col-xs-6" style="padding-left: 20px;">
                <div class="row">
                    <div class="col-xs-6 left-sub-section">
                        <p><b>Credentials</b></p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDUser">${_("User")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDUserVal">${entries[0]['user_name']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDGroup">${_("Group")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDGroupVal">${entries[0]['group_name']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDAccount">${_("Account")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDAccountVal">${entries[0]['account_name']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDClass">${_("Class")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDClassNmVal">${entries[0]['class_name']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDQoS">${_("Quality of Service")}</div>
                    <div class="col-xs-6 right-sub-section">
                        %if base.hasAccess('Job Edit-admin'):
                            <input type="text" name="qos" class="form_save_data" value=${entries[0]['qos_name']} id="qos_txtBox" onkeypress="validate_QOS_OnKeyPress('qos_txtBox', this, event)" onblur="chkData('qos_txtBox')"/>
                        %else:
                            ${entries[0]['qos_name']  }
                        %endif
                    </div>
                </div>
                <div class="hrule"></div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section">
                        <p><b>${_("Job Priority")}</b></p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDPartitionAccess">Partition Access List</div>
                    <div class="col-xs-6 right-sub-section" id="jDPartitionAccessList">${entries[0]['partition_access_list']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDStartCount">${_("Start Count")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDStartCountVal">${entries[0]['start_count']  }</div>
                </div>
                <%doc>
                # Commenting code to remove priority columns --IRIS-455
                <div class="row">
                    <div class="col-xs-6 left-sub-section">${_("Start Priority")}</div>
                    <div class="col-xs-6 right-sub-section">${entries[0]['start_priority']  }</div>
                </div>
                </%doc>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDUserJobPr">${_("User Job Priority")}</div>
                    <div class="col-xs-6 right-sub-section"><input type="text" id='job_priority' name="job_priority" class="form_save_data" value=${entries[0]['run_priority']} onkeyup="validate_user_priority_OnKeyUp('job_priority',-1024,0)"  onkeypress="validate_user_priority_range('job_priority',this,event)" onblur="chkData('job_priority')"/></div>
                </div>
				
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDSysPr">${_("System Priority")}</div>
                    <div class="col-xs-6 right-sub-section">
                        %if base.hasAccess('Job Edit-admin'):
                            <input type="text" name="sys_priority" class="form_save_data" value=${entries[0]['system_priority']} onkeypress="checkObjection(this,event)" id="jobDetails_SysPriorityTxtbox" onblur="chkData('jobDetails_SysPriorityTxtbox')" />
                        %else:
                            ${entries[0]['system_priority']  }
                        %endif
                    </div>
                </div>
            </div><!-- .col-xs-6 ends -->
            <div class="col-xs-6" style="padding-right: 20px;">
                <div class="row">
                <%doc>
                ## Commenting for mini utilization charts IRIS-293 
                    <div class="col-xs-6 left-sub-section"><b>${_("Processor Statistics")}</b></div>
                    
                    <input type="hidden" name="job_id" value=${ job_id  } />
                    <div class="uChart-wrapper job-detail-chart" id= ${ job_id  }>
                        <img class="cc-spinner" id="spinner" src="/static/images/spinner.gif"/>
                        <div class="uChart-container"></div>
                    </div>
                </%doc>
                </div>

                <div class="row">
                    <div class="col-xs-6 left-sub-section"><p><b>${_("Resource")}</b></p></div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDRequriedNodeListPre">${_("Required Node List")}</div>
                    <div class="col-xs-6 right-sub-section">

                        <input type="hidden" class="form_save_data" name="nodeList" id="nodeList" value="" />
						%if not node_list or len(node_list) == 0:
							%if required_nodelist:
								%for i in required_nodelist:
									%if len(i) > 7:
										<span class="label label-primary" title="${ i  }">${ i[0:7]  }...</span>
									%else:
										<span class="label label-primary" title="${ i  }">${ i  }</span>
									%endif
								%endfor
							%else:
								<span> - </span>
							%endif
						%else:
							<div class="features job-details" id="nodeListContainer">
								%if required_nodelist:
									%for i in required_nodelist:
										<span class="label label-default" id="addnode_${ i }">
											<a id='node_${ i }'>${ i }</a>
											<span class="glyphicon glyphicon-remove" id="destroyNode_${ i }"
												  onclick="hideNodes('${ i }')"></span>
                                    </span>
									%endfor
								%else:
									<span>  </span>
								%endif

                            	<span class="add" data-toggle="modal" data-target="#myModal" id="jobDetails_addNodeList">+</span>
                        	</div>
						%endif

                            <!-- Node List Modal -->
                            <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                            <h4 class="modal-title" id="myModalLabel">${_("Select Nodes")}</h4>
                                        </div>
                                        <div class="modal-body node-list">
                                            <table class="table" width="100%" cellspacing="1" cellpadding="0" border="0">
                                                <tr>
                                                    <th>${_("Add")}</th>
                                                    <th>${_("Resource ID")}</th>
                                                </tr>
                                                %if node_list:
                                                    %if isinstance(node_list, list):
                                                        % for count,nodes in enumerate(node_list) :
                                                            <tr>
                                                            %if nodes in required_nodelist:
                                                                <td>
    
                                                                    <span class="add" id="reqNode_${ nodes }" onclick="toggleNodes(this,'${ nodes }',1)">-</span>
                                                                </td>
                                                            %else:
                                                                <td>
                                                                    <span class="add" id="reqNode_${ nodes }" onclick="toggleNodes(this,'${ nodes }',0)">+</span>
                                                                </td>
                                                            %endif
    
                                                            <td id="node_${ count }">${ nodes }</td>
                                                            </tr>
                                                        
                                                        %endfor
                                                    %else:
                                                        <tr><td colspan="4"><div class="alert alert-success">${ node_list  }</div></td></tr>
                                                    %endif
                                                %endif
                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button id="modalDone" type="button" class="btn btn-primary default" data-dismiss="modal" name="action" value="Done">${_("Done")}</button>
                                        </div>
                                    </div>
                                </div>
                            </div><!-- Node List Modal ends -->
                        
                        
                    </div>
                </div>
                 <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDAllocatedPart">${_("Allocated Partition")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDAllocatedPartVal">${entries[0]['allocated_partition']  }</div>
                </div>
                <div class="hrule"></div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section"><p><b>${_("Requirements")}</b></p></div>
                </div>
                 <input type="hidden" id="isMultiReqJob" name="isMultiReqJob" value="${ hasMultiReqs  }"/>
                %if hasMultiReqs:
                    <div class="row">
						<table class="table table-bordered mrlt">
						<thead>
						<tr>
						<th colspan="2">Required Features</th>
                        <th>${_("Processors per Task")}</th>
                        <th>${_("Operating System")}</th>
						<th>${_("Required Minimum Tasks")}</th>
						</tr>
						</thead>
						<tbody>
                        %for num , req in enumerate(job_requirements):
								<tr>
                                    <td colspan="2" width="45%">

                                        %if req['requested_features']:
                                            <div class="right-sub-section">
                                            %for i in req['requested_features'].split(","):
                                               <span class="label label-primary">${i.strip()  }</span>
                                            %endfor
                                            </div>
                                        %else:
                                            <span> - </span>
                                        %endif
                                    </td>
                                    <td>${req['processors_per_task'] }</td>
                                    <td><div style="word-wrap: break-word;width: 100px">${req['operating_system']  }</div></td>
                                    <td>${req['required_minimum_tasks']  }</td>
								</tr>
                        %endfor
                            </tbody>
						</table>
                     </div>
                %elif job_requirements:
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDRequriedFeatures">Required Features</div>
                    <div class="col-xs-6 right-sub-section">

                            %if requiredfeatures and isinstance(requiredfeatures, list) and len(requiredfeatures) > 0:
								<input type="hidden" class="form_save_data" name="featureList" id="featureList" value="" />
								
                        	<div class="features job-details" id="featuresContainer">
								%if featurelist:
                                	%for i in featurelist:
                                    	<span class="label label-default add_features" id="addfeature_${ i }">
											<a  id='feature_${ i }' title='${ i }'>${ i }</a>
                                        	<span class="glyphicon glyphicon-remove" id="destroyFeature_${ i }" onclick="hideFeatures('${ i }')"></span>
                                   		</span>
                               		 %endfor
                            	%else:
                                <span >  </span>
                            	%endif
								<span class="add fet" data-toggle="modal" data-target="#rfModal" id="jobDetails_addRequiredFeatures">+</span>
							</div>
							%else:
								   	%if featurelist:
								   		%for i in featurelist:
                                               <span class="label label-primary">${ i  }</span>
                                        %endfor
                                    %else:
                                            <span> - </span>
                                    %endif
                            %endif

                            <!-- Required Features Modal -->
                            <div class="modal fade" id="rfModal" tabindex="-1" role="dialog" aria-labelledby="rfModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                            <h4 class="modal-title" id="rfModalLabel">${_("Select Features")}</h4>
                                        </div>
                                        <div class="modal-body feature-list">
                                            <table class="table" width="100%" cellspacing="1" cellpadding="0" border="0">
                                                <tr>
                                                    <th>${_("Add")}</th>
                                                    <th>${_("Feature")}</th>
                                                    <th>${_("Available")}</th>
                                                    <th>${_("Description")}</th>
                                                </tr>
                                                %if requiredfeatures:
                                                    %if isinstance(requiredfeatures, list):
                                                        % for features in requiredfeatures:

                                                            <tr>
                                                            %if features['feature'] in featurelist:
                                                                <td>
                                                                    <span class="add" id="reqFeature_${ str(features['feature']) }" onclick="toggleFeatures(this,'${ str(features['feature']) }',1)">-</span>
                                                                </td>
                                                            %else:
                                                                <td>
                                                                    <span class="add" id="reqFeature_${ str(features['feature']) }" onclick="toggleFeatures(this,'${ str(features['feature']) }',0)">+</span>
                                                                </td>
                                                            %endif
                                                            %if len(features['feature']) > 5:
                                                                <td><span title="${ features['feature'] }" id="feature_${ str(features['feature']) }">${ features['feature'][0:5] }...</span></td>
                                                            %else:

                                                                <td><span title="${ features['feature'] }" id="feature_${ str(features['feature']) }">${ features['feature'] }</span></td>
                                                            %endif
                                                            <td>${ features['available']  }</td>
                                                            <td>${ features['description']  }</td>
                                                            </tr>
                                                        %endfor
                                                    %else:
                                                        <tr><td colspan="4"><div class="alert alert-success">${ requiredfeatures  }</div></td></tr>
                                                    %endif
                                                %endif

                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-primary default" data-dismiss="modal" name="action" value="Done" id="jDDoneBtn">Done</button>
                                        </div>
                                    </div>
                                </div>
                            </div><!-- Required Features Modal ends -->

                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDProcTask">${_("Processors per Task")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDProcTaskVal">${entries[0]['processors_per_task']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDOpSys">${_("Operating System")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDOpSysVal">${entries[0]['operating_system']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDRequriedMinTask">${_("Required Minimum Tasks")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDRequriedMinTaskVal">${entries[0]['required_minimum_tasks']  }</div>
                </div>
                %endif
                <%doc><div class="hrule"></div>
            
                <div class="row">
                    <div class="col-xs-6 left-sub-section"><b>${_("Add Generic Resource")}</b></div>
                    <div class="col-xs-6 right-sub-section">
                        <input type="hidden" name="resourceList" id="resourceList" value="" />
                        <div class="features job-details" id="resourceContainer">
                        
                            %if generic_resourceslist:
                                %for i in generic_resourceslist:
                                    <span class="label label-default" id="resource${i  }">
                                        <a>${ i  }</a>
                                        <span class="glyphicon glyphicon-remove" id="destroyResource" onclick="hideResources('${ i  }')"></span>
                                    </span>
                                %endfor
                            %else:
                                <span >  </span>
                            %endif
                            <span class="add genRes" data-toggle="modal" data-target="#grModal">+</span>
                        </div>  
                            <!-- Generic Resource Modal -->
                            <div class="modal fade" id="grModal" tabindex="-1" role="dialog" aria-labelledby="grModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                            <h4 class="modal-title" id="grModalLabel">Select Resources</h4>
                                        </div>
                                        <div class="modal-body res-list">
                                            <table class="table" width="100%" cellspacing="1" cellpadding="0" border="0">
                                                <tr>
                                                    <th>${_("Add")}</th>
                                                    <th>${_("ID")}</th>
                                                    <th>${_("Name")}</th>
                                                    <th>${_("Description")}</th>
                                                </tr>
                                                %if genericresoucres:
                                                    % for resources in genericresoucres :
                                                        
                                                        <tr>
                                                        %if resources['name'] in generic_resourceslist:
                                                            <td>
                                                                <span class="add" id="${ resources['name']  }" onclick="toggleResources(this,'${ resources['name']  }',1)">-</span>
                                                            </td>
                                                        %else:
                                                            <td>
                                                                <span class="add" id="${ resources['name']  }" onclick="toggleResources(this,'${ resources['name']  }',0)">+</span>
                                                            </td>
                                                        %endif                                                  
                                                        <td>${ resources['id']  }</td>
                                                        <td>${ resources['name']  }</td>
                                                        <td>${ resources['description']  }</td>
                                                        
                                                        </tr>
                                                    %endfor
                                                %endif
                                                
                                            </table>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-primary default" data-dismiss="modal" name="action" value="Done">Done</button>
                                        </div>
                                    </div>
                                </div>
                            </div><!-- Generic Resource Modal ends -->
                        
                    </div></%doc>
            
            </div><!-- .col-xs-6 ends -->
    </div><!-- .row ends -->
    
    <div class="row">
        <div class="col-xs-12">
            <div class="hrule"></div>
            <input type="hidden" name="prvpath" id="prvpath">
                <button type="submit" onclick="prepareData()" class="btn btn-primary default right" name="action" value="Apply" id="jDApplyBtn">${_("Apply")}</button>
                <button type="submit" onclick="prepareData()"  class="btn btn-primary default right" style="margin-right: 10px" name="action" value="Done" id="jDDoneBtn">${_("Done")}</button>
                <button type="button" id="cancel" class="btn btn-primary default right" style="margin-right: 10px" >${_("Cancel")}</button>
        </div>

    </form>
    </div>
% else:

    <div><h5>${ entries  } </h5></div>

%endif      
</%def>
<%def name="end_script()">
<%doc>
## Commenting for mini utilization charts IRIS-293 
    <script type="text/JavaScript">
                
                 if (typeof google === "object" && typeof google.visualization === "object") {
                    if($('#NoRecordsFound').length == 0)
                    {
                        drawUAreaChart();
                    }
                  } else {
                    google.load("visualization", "1", { packages:["corechart"] }); 
                    google.setOnLoadCallback(drawUAreaChart);
                  }
                function drawUAreaChart() {
                try{
                                $('.uChart-wrapper').each(function(){
                                var chartId = $(this).attr('id');
                                var lblUtilizationPercentage = $(this).find('.uChart-wrapper');
                                var imgSpinner = $(this).find('.uChart-wrapper>img');
                                imgSpinner.prop("id","spinner" + chartId);
                                //lblUtilizationPercentage.prop("id","lbl" + chartId); 

                                var utilizationPercentage ;
                                $.ajax({
                                    url:'/api/getutilization/',
                                    type:'GET',
                                    data:{jobId:chartId},
                                    success:function(result){
                                            var jsonData = result;
                                                if (jsonData[1] == undefined){
                                                    $('.uChart-wrapper').find('#spinner').hide();
                                                    $('.uChart-wrapper').find(".uChart-container").append('<span style="display:block;margin-top:11px">N/A</span>');
                                                
                                            }
                                            
                                            if(jsonData[1].length != undefined || jsonData[1].length != null)
                                            {
                                            
                                                    //pass the data array to google arrayToDataTable API.

                                                        
                                                    var data = google.visualization.arrayToDataTable(jsonData[1]);

                                                    var options = {
                                                        hAxis: {title: '',  titleTextStyle: {color: '#333'},minValue:1,maxValue:50,textPosition:'none',baselineColor:'#aaaaaa'},
                                                        vAxis: {minValue: 0,maxValue:50, gridlines:{count:1}, titleTextStyle:{color:'white'},textPosition:'none'},
                                                        legend: {position: 'none'},
                                                        colors:["#ccc5ae"],
                                                        areaOpacity:0.8,
                                                        isStacked: true,
                                                        animation:{
                                                            duration: 2000,
                                                            easing: 'out',
                                                        },
                                                        'tooltip' : {
                                                            trigger: 'none'
                                                        },
                                                        enableInteractivity : false,
                                                        height:70,
                                                        width:100
                                                    };
                                                    var chart = new google.visualization.AreaChart(document.getElementById(chartId));
                                                    chart.draw(data, options);
                                                    
                                                    //removing the spinner
                                                    if($('.uChart-wrapper').find('#spinner' + chartId) != null)
                                                    {
                                                        $('.uChart-wrapper').find('#spinner' + chartId).hide();
                                                    }
                                                    //removing the spinner ends
                                                    //Adding the Chart utilization % value starts
                                                    if($('.uChart-wrapper').find(chartId) != null)
                                                    {
                                                        $('.uChart-wrapper').find(chartId).text(jsonData[0]);
                                                    }
                                                    //Chart utilization % value ends

                                                }
                                                else
                                                {
                                                    //removing the spinner
                                                    if($('.uChart-wrapper').find('#spinner' + chartId) != null)
                                                    {
                                                        $('.uChart-wrapper').find('#spinner' + chartId).hide();
                                                    }
                                                    //removing the spinner ends

                                                    $('.uChart-wrapper').find(chartId).text("N/A");
                                                        
                                                        
                                                }
                                            }                                           
                                        });
                                    });// each() ends
                                }
                                catch(e)
                                {
                
                                }
                            }
    </script>
</%doc>
                
    <script type="text/javascript">
    $(document).ready(function(){
        
        prevpath = document.referrer
        path = getParameterByName('prvpath');
        if(prevpath.indexOf('workload') > -1 || path == "workload")
        {
            if(path == 'workload')
                $("#prvpath").val('workload');
            else
                $("#prvpath").val('workload');
                
            $("#cancel").click(function(){
                goto('workload');
            });
        }else if(prevpath.indexOf('dashboard') > -1 || path == "dashboard")
        {
            if(path == 'dashboard')
                $("#prvpath").val('dashboard');
            else
                $("#prvpath").val('dashboard');
                
            $("#cancel").click(function(){
                goto('dashboard');
            });
        }
		createDirtyUnloadListener(".form_save_data, #nodeListContainer, #featuresContainer","${_("You have unsaved changes that will be lost.")}");
    });
    </script>
    
    
    <script type="text/javascript">
        function addClicked(){
            $('.modal-body .preloader').hide();
            getNodeList();
    
            
            $('#modalDone').click(function(){
                $('.modal-body.node-list').html('<div class="preloader"></div>');
            });
        }
        function getNodeList(){
            var IDs = [];
            $("#nodeListContainer").find("span").each(function(){
                if(this.id != "destroyNode" && this.id != ""){
                    id = this.id.replace('node','');
                    $("#"+id).html("-");
                    $("#"+id).removeAttr('onclick');
                }
            });
        }
        
        
        function fetchPrepareData(id)
        {        
            nodelist = ""
            $(id).find("a").each(function(){
                        nodelist += "," + $(this).text();
            });
             
            nodelist=nodelist.replace(/^(,)*/,'');

            return nodelist;
        }
        
        
        function prepareData()
        {
			
			
			$("#nodeList").val(fetchPrepareData("#nodeListContainer"));
        	$("#featureList").val(fetchPrepareData("#featuresContainer"));
		
			
           /* nodelist = ""
            $("#nodeListContainer").find("span").each(function(){
                if(this.id != "destroyNode" && this.id != ""){
                    id = this.id.replace('node','');
                    if(nodelist == "")
                        nodelist = id;
                    else
                        nodelist +=  "," + id 
                }
            });
            $("#nodeList").val(nodelist);
            
            featurelist = ""
            $("#featuresContainer").find("span").each(function(){
                if(this.id != "destroyFeature" && this.id != ""){
                    id = this.id.replace('node','');
                    if(featurelist == "")
                        featurelist = id;
                    else
                        featurelist +=  "," + id;
                }
            });
                    
            $("#featureList").val(featurelist);
            
            resourcelist = ""
            $("#resourceContainer").find("span").each(function(){
                if(this.id != "destroyResource" && this.id != ""){
                    id = this.id.replace('node','');
                    if(resourcelist == "")
                        resourcelist = id;
                    else
                        resourcelist +=  "," + id;
                }
            });         
            $("#resourceList").val(resourcelist);

			isDirtyPlaceholder = false;
            return true;*/

			//Need this on so dirty check is disabled when saving
			isDirtyPlaceholder = false;

        }

    </script>
    
    <script type="text/javascript">
        $('span.fet').click(function(){
            $('#rfModal').on('shown.bs.modal', function(){
                //alert('Modal was shown');
                //$('.modal span.add').html("+");
                getFeatureList();
            });
                
        });
        
        function getFeatureList(){
            var fetIDs = [];
            $('#featuresContainer').find("span").each(function(){               
                if(this.id == "destroyFeature"){
                    //alert(this.id);
                    id = this.id.replace('node','');
                    //$("#"+id).html("-");
                    //$("#"+id).removeAttr('onclick');
                }else{
                    //alert(thid.id);
                    $('.modal-body .preloader').show();
                    //$("#"+id).html("+");
                    //$("#"+id).attr("onclick","toggleFeatures(this,'"+id+"',0)");                   
                    $('.modal-body .preloader').hide();
                }
            });
        }
    </script>
    
    <script type="text/javascript">
        $('span.add.genRes').click(function(){
            $('#grModal').on('shown.bs.modal', function(){
                //alert('Modal was shown');
                getResourceList();
            });
                
        });
        
        function getResourceList(){
            var resIDs = [];
            $('#resourceContainer').find("span").each(function(){
                if(this.id == "destroyResource"){
                    //alert(this.id.replace('resource',''));
                    id = this.id.replace('node','');
                    //alert($("#"+id).html());
                    //$("#"+id).html("+");
                } else {
                    //alert(thid.id);
                   // $("#"+id).html("+");
                   // $("#"+id).attr("onclick","toggleResources(this,'"+id+"',0)");
                }
            });
        }
        
    </script>
    
    <script type="text/javascript">
        function applyJobDetails() {
            nodes = [];
            
            $("#nodeListContainer").find("span").each(function(){
                alert($('span.label').html());
            });
            
            requiredFeatures = [];
            genResources = [];                      
        }
        
         function validate_Form() {
        
            if(chkData('qos_txtBox')==false)
                return false;
            else if(chkData('jobDetails_SysPriorityTxtbox')==false)
                return false;
            else if(chkData('job_priority')==false)
                return false;               
        }
    </script>
    <script type="text/javascript">
		function isNumberKey(evt) {
			var charCode = (evt.which) ? evt.which : event.keyCode;
			if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
				return false;
			} else {
				return true;
			}      
		}
</script>
</%def>
