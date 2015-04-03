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
        <form class="form-jobDetail" role="form" method="post" action='/jobdetails/'>
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
            <div class="col-xs-12"><span class="case" id="jDJobID">${_("Job Id")} : <span class="marginl" id="jDJobIDVal">${entries[0]['name']  }</span></span><span class="right"><span class="case" id="jDStatus">${_("Status")}:<span><b class="free" id="jDStatusVal">${entries[0]['state'] }</b></span></span></div>
                <input type="hidden" id="job_name" name="job_name" size="20" value=${entries[0]['name'] } />
                <input type="hidden" name="job_status" value=${entries[0]['state'] } />
                <input type="hidden" name="job_id" value=${ job_id  } />
                <div class="clearfix"></div>
            <div class="alert alert-success" style="display: none">
                <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                <strong>${_("ERROR : The Job Status is Complete but the resource is not idle")}.</strong>
            </div>
            <!--<div class="section-title-common">
                How Priority is defined
                <script type="text/javascript">
                    $(document).ready(function(){
                        $('#infoPopUp').tooltip();
                    });
                </script>
                <button id="infoPopUp" type="button" class="btn btn-default" data-toggle="tooltip" data-placement="right" title="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.">?</button>
            </div>-->
            <!--<table class="table-common">
                <thead>
                    <tr>
                        <td>Fareshare, User</td>
                        <td>Fareshare, Account</td>
                        <td>Service, Queue Time</td>
                        <td>Credential, Quality of Src</td>
                        <td>Usage, Consumed</td>
                        <td>Usage, Remaining</td>
                        <td>Component, Subcomponent</td>
                        <td>Component, Subcomponent</td>
                        <td>Priority</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>1000</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1000</td>
                        <td>1</td>
                        <td>1</td>
                        <td>1000000</td>
                    </tr>
                </tbody>
            </table>-->
            <div class="section-title-common"><p>${_("Time Frame")}</p></div>
                <table class="table-common">
                    <thead>
                        <tr>
                            <td id="jDStartTm">${_("Start Time")}</td>
                            <td id="jDDuration">${_("Duration")}</td>
                            <td id="jDCompletionTm">${_("Completion Time")}</td>
                            <td id="jDActualDuration">${_("Actual Duration")}</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="width:170px;" id="jDStartDateTmVal">${entries[0]['start_datetime']  }</td>
                            % if job_status in ("COMPLETED","FAILED","REMOVED","VACATED"):
                                <td id="jDTime">${ duration_format  }</td>
                            % else:
                            <td style=" position: relative; ">
                                <input id="durInput" type="text" readonly name="duration" class="form_save_data" value=${ duration_format  } onkeypress="checkObjection(this,event)"/>
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
										<div class="buttonbig popbuttonbig"><div class="incbutton" onclick="incrementDay('dInput')"></div><div class="decbutton" onclick="decrement('dInput')"></div></div>
										</div>
										<div class="durationBtn">
										<input type="text" name="hInput" id="hInput" value="0" onkeyup="durationHour('hInput',0,23)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onclick="incrementHour('hInput')"></div><div class="decbutton" onclick="decrement('hInput')"></div></div>
										</div>
										<div class="durationBtn">
										<input type="text" name="mInput" id="mInput" value="0" onkeyup="durationMinutes('mInput',0,59)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onclick="incrementMinutes('mInput')"></div><div class="decbutton" onclick="decrement('mInput')"></div></div>
										</div>
										<div class="durationBtn">
										<input type="text" name="sInput" id="sInput" value="0" onkeyup="durationSeconds('sInput',0,59)" class="pull-left"onkeypress="checkObjection(this,event)">
										<div class="buttonbig popbuttonbig"><div class="incbutton" onclick="incrementSeconds('sInput')"></div><div class="decbutton" onclick="decrement('sInput')"></div></div>
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
                            % endif
                            <td id="jDCompleteionTmVal">${entries[0]['completion_datetime']  }</td>
                            <td id="jDActualFormatVal">${ actualduration_format  }</td>
                        </tr>
                    </tbody>
                </table>
            </div><!-- .col-xs-10 ends -->
            <div class="col-xs-6" style="padding-left: 20px;">
                <div class="row">
                    <div class="col-xs-6 left-sub-section">
                        <p><b>${_("Credentials")}</b></p>
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
                    <div class="col-xs-6 right-sub-section" id="jDQoSNmVal">${entries[0]['qos_name'] }</div>
                </div>
                <div class="hrule"></div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section">
                        <p><b>${_("Job Priority")}</b></p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDPartitionAccess">Partition Access List</div>
                    <div class="col-xs-6 right-sub-section" id="jDPartitionAccessList">${entries[0]['partition_access_list'] }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDStartCount">${_("Start Count")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDStartCountVal">${entries[0]['start_count'] }</div>
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
                    <div class="col-xs-6 right-sub-section" id="jDUserJobPrVal">${entries[0]['run_priority']  }</div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDSysPr">${_("System Priority")}</div>
                    <div class="col-xs-6 right-sub-section">
                    %if base.hasAccess('Job Edit-admin'):
                        % if job_status in ("COMPLETED","FAILED","REMOVED","VACATED") :
                            <input type="hidden" name="sys_priority" class="" value=${entries[0]['system_priority']  } onkeypress="checkObjection(this,event)" />
                            ${entries[0]['system_priority']  }
                        % else :
                            <input type="text" name="sys_priority" class="form_save_data" value=${entries[0]['system_priority']  } onkeypress="checkObjection(this,event)" id="jobDetails_SysPriorityTxtbox"/>
                        % endif
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
                        
                        <div class="uChart-wrapper job-detail-chart" id=${ job_id  }>
                            <img class="cc-spinner" id="spinner" src="/static/images/spinner.gif" />
                            <div class="uChart-container"></div>
                    </div>
                    </%doc>
                </div>

                <div class="row">
                    <div class="col-xs-6 left-sub-section"><p><b>${_("Resource")}</b></p></div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDAllocatedNode">${_("Allocated Node List")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDAllocatedNodeValueList">
                    
                        <%doc><span class="label label-primary">${ entries[0]['allocated_node_list']  }</span></%doc>
                        
                        %if nodelist_allocated:
                            %for count,i in enumerate(nodelist_allocated):
                                %if len(i) > 7:
                                    <span class="label label-primary" title="${ i  }" id="allcatednode${ count  }">${ i[0:7]  }...</span>
                                %else:
                                    <span class="label label-primary" title="${ i  }" id="allocatednode${ count  }">${ i  }</span>
                                %endif
                            %endfor
                        %else:
                            <span > - </span>
                        %endif
                        
                    </div>
                </div>
                <div class="row">
                    <div class="col-xs-6 left-sub-section" id="jDAllocatedPart">${_("Allocated Partition")}</div>
                    <div class="col-xs-6 right-sub-section" id="jDAllocatedPartVal">${entries[0]['allocated_partition']  } bit</div>
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
                                    <td>${req['processors_per_task']  }</td>
                                    <td><div style="word-wrap: break-word;width: 100px">${req['operating_system']  }</div></td>
                                    <td>${req['required_minimum_tasks']  }</td>
								</tr>
                        %endfor
                            </tbody>
						</table>
                     </div>
                %elif job_requirements:
                    <div class="row">
                        <div class="col-xs-6 left-sub-section" id="jDRequriedFeatures">${_("Required Features")}</div>
                        <div class="col-xs-6 right-sub-section" id="jDReqdFeaturesValue">
                            %if featurelist:
                                %for count,i in enumerate(featurelist):
                                    <span class="label label-primary" id="requiredfeature${ count  }">${ i  }</span>
                                %endfor
                            %else:
                                <span> - </span>
                            %endif
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
            </div><!-- .col-xs-6 ends -->
        </div><!-- .row ends -->
        <div class="row">
            <div class="col-xs-12">
                <div class="hrule"></div>
                <input type="hidden" name="prvpath" id="prvpath">
                % if job_status in ("COMPLETED","FAILED","REMOVED","VACATED") :
                        <button type="button" id="cancel"  class="btn btn-primary default right" style="margin-right: 10px" >${_("Cancel")}</button>
                % else:
                    <%doc>%if base.hasAccess('Job Edit-admin'):</%doc>
                        <button type="submit" onclick="prepareData()" class="btn btn-primary default right" name="action" value="Apply" id="jDApplyBtn">${_("Apply")}</button>
                        <button type="submit" onclick="prepareData()"  class="btn btn-primary default right" style="margin-right: 10px" name="action" value="Done" id="jDDoneBtn">${_("Done")}</button>
                    <%doc>%endif</%doc>
                        <button type="button" id="cancel" class="btn btn-primary default right" style="margin-right: 10px">${_("Cancel")}</button>
                % endif
            </div>
        </div>
    </form>
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
        //Code Below written for redirection of cancel button
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
		createDirtyUnloadListener(".form_save_data","${_("You have unsaved changes that will be lost.")}");
    });
    function prepareData(){
			isDirtyPlaceholder = false;
            return true;
	}
    </script>
</%def>
