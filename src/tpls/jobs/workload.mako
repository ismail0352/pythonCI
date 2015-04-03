## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

 <%inherit file="base.mako" />
 
<%def name="title()">${_("Viewpoint Workload")}</%def>

<%def name="head_tags()">

</%def>

<%def name="jquery_tags()">
	<script type="text/javascript">
		google.load("visualization", "1", {packages:["corechart"]});
	</script>

	<script type="text/javascript">
		$(document).ready(function(){			
			
			$('#dataGrid .preloader').show();
			
			var statusCode = $('#hiddenstatusCode').val();
			
            disableWorkloadContentOnPageLoad();

			$.ajax({
				url:'/workload_table/',
				type:'GET',
				data:{max:20, offset:1, status:statusCode},
				success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					if (statusCode != ""){
					$('#totalJobsCnt').text($('#hiddenTotalCnt').val() + ' Jobs');
					}

					disablePaginationContent();
					enableWorkloadContentAfterPageLoad();
				}

			});

			var status = getParameterByName('status');


			if (status != "")
			{$('#jobState').val(status);}
			statusCodeInitialise()


		});


	</script>

<link rel="stylesheet" type="text/css" href="/static/css/datepicker.css" />
<script src="../static/js/bootstrap-datetimepicker.js" type="text/javascript"></script>


</%def>

<%def name="main_content()">
	<div class="row">
		<div class="col-xs-8">
			%if messages:
				%if status == "200":
    				<div class="alert alert-success" id="myAlert">
    				<a href="#" class="close" data-dismiss="alert">&times;</a>
    					${ "<br />".join(str(messages).split(",")) | n,decode.utf8 }
    				</div>
        	    %else:
        	       <div class="alert alert-danger" id="myAlert">
                    <a href="#" class="close" data-dismiss="alert">&times;</a>
                        ${ "<br />".join(str(messages).split(",")) | n,decode.utf8 }
                    </div>
        	    %endif
			%endif
			<div class="col-xs-6 section-header padlt">
			<h1><b>${_("Workload")}</b>
					<span class="refresh" id="workloadRefresh" onClick="refreshContentForWorkloadFilters(this);"></span>
			</h1>

			</div>
			<div class="clearfix"></div>
				<!--<span class="right-icon-section">
					<button type="button" class="btn btn-primary" disabled>
						<span class="glyphicon glyphicon-plus"></span>&nbsp;&nbsp;&nbsp;${_("Create Reservation")}
					</button>
				</span>-->
				<!--<span class="icon-grid" ></span>
				<span class="icon-timeline" ></span>-->

			<div>
				<input type="text" id="hiddenstatusCode" style='display:none' value=${ statusCode  }></input>
				<div class= "alert alert-success" style= "display: none" id="statusMsg">

				</div>
				<div style="display:none;" id="loaderDiv">

				</div>
				<div id="dataGrid" class="dtGrid datagrid-container container panel panel-default">
					<div class="preloader"></div>
				<div class="endless_page_template">

				</div>
				</div>
			</div>
		</div>
		<div class="col-xs-4 search-filter-section padLeft">
			<h5><b>${_("Current Search")}: </b><strong><label id='totalJobsCnt'></label></strong></h5>
			<div id="searchValues">

			</div>
			<span>
				<!-- <input type="checkbox"> -->
				<select id="searchCat" class="form-control" onChange="$('#searchBox').focus()">
					<option value="select" id="opt0">- ${_("Select")} -</option>
					<option id="opt1" value="JobId">Job ID</option>
					<option id="opt2" value="SubmitterID">Submitter ID</option>
				</select>
			</span>
			<span>
				<input id="searchBox" type="text" onclick="clearValue(this)" class="form-control search" placeholder="${_("Narrow Search")}" onkeypress="addFilter(this,event)"/>
				<span id="searchBtn" class="glyphicon glyphicon-search" onclick="addFilter(this,event)"></span>
			</span>
			<h5 class="filter">${_("Filters")}</h5>
			<span>
				<!-- <input type="checkbox"> -->
				<select id="jobState" class="form-control">
					<option id ="opt0" value="null" >${_("Select Job State")}</option>
					%if workload_filter:
						% for i in workload_filter:
							<option value="${ i  }">${ i  }</option>
						% endfor
					%endif
				</select>
			</span>
			<div class="col-xs-12">
<%doc>
# Commenting code to remove priority columns --IRIS-455
<div class="col-xs-6">
<div class="form-group">
<label class="labelfilter">Priority</label>
        <input type="text" name="From" id="priorityFrom" value="0" class="form-control number-input"   onkeypress="checkObjection(this,event)">
        <div class="buttonbig"><div class="incbutton" onclick="increment('priorityFrom')"></div><div class="decbutton" onclick="decrement('priorityFrom')"></div></div>
        </div>
        </div>
        <div class="col-xs-6">
<div class="form-group">
<label class="labelfilter1">To</label>
        <input type="text" name="From" id="priorityTo" value="0" class="form-control number-input"   onkeypress="checkObjection(this,event)">
        <div class="buttonbig"><div class="incbutton" onclick="increment('priorityTo')"></div><div class="decbutton" onclick="decrement('priorityTo')"></div></div>
        </div>
        </div>
</%doc>
        </div>

        <div class="clearfix"></div>
<%doc>
# Commenting code to remove rank columns --IRIS-309
		 <div class="col-xs-12">
<div class="col-xs-6">

<div class="form-group">
<label class="labelfilter">Rank</label>
        <input type="text" name="From" id="rankFrom" value="0" class="form-control number-input"  onkeypress="checkObjection(this,event)">
        <div class="buttonbig"><div class="incbutton" onclick="increment('rankFrom')"></div><div class="decbutton" onclick="decrement('rankFrom')"></div></div>
        </div>
        </div>
        <div class="col-xs-6">

<div class="form-group">
<label class="labelfilter1">To</label>
        <input type="text" name="From" id="rankTo" value="0" class="form-control number-input" onkeypress="checkObjection(this,event)">
        <div class="buttonbig"><div class="incbutton" onclick="increment('rankTo')"></div><div class="decbutton" onclick="decrement('rankTo')"></div></div>
        </div>
        </div>
        </div>
</%doc>
        <div class="clearfix"></div>
			<!--<span>
				<label class="rPadding15">${_("Priority")}</label>
				<input id="priorityFrom" type="number" class="form-control number-input" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
				${_("To")} <input id="priorityTo" type="number" class="form-control number-input"  min="0" value="0" onkeypress="checkObjection(this,event)"/>
			</span>
			<span class="clearfix">
				<label class="rPadding15">${_("Rank")}</label>
				<input id="rankFrom" type="number" class="form-control number-input"  min="0"  value="0" onkeypress="checkObjection(this,event)"/>
				${_("To")} <input id="rankTo" type="number" class="form-control number-input" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
			</span> -->
			<span>
				<!-- <input type="checkbox"> -->
				<select id="dateTimeRange" class="form-control" onChange="selectRange(this)">
							<option id="opt0" value="null">${_("Select")}</option>
							<option value="startdate">Start Date</option>
							<option value="wallclock">Wall Clock</option>
						</select>
						<div class="start-date">
							<label>${_("Start Date")}</label>
							<div id="startDate" class="input-append date">
								<input id="txtStartDate" data-format="yyyy-MM-dd hh:mm:ss" class="form-control" type="text"/>
								<span class="add-on icon">
									<i data-time-icon="glyphicon glyphicon-time" data-date-icon="glyphicon glyphicon-calendar" class="glyphicon glyphicon-calendar" id="workload_startDate">
									</i>
								</span>
							</div>
							<label>${_("To")}</label>
							<div id="endDate" class="input-append date">
								<input id="txtEndDate" data-format="yyyy-MM-dd hh:mm:ss" class="form-control" type="text"/>
								<span class="add-on icon">
									<i data-time-icon="glyphicon glyphicon-time" data-date-icon="glyphicon glyphicon-calendar" class="glyphicon glyphicon-calendar" id="workload_toDate">
									</i>
								</span>
							</div>
						</div><!-- //.start-date ends -->
						<div class="wall-clock">
							<span id="wallclockStart">
							
							
							<div class="col-xs-12">
								<span>From</span>
								<div class="col-xs-6">
									<div class="clearfix"></div>
									<div class="form-group">
										<label class="labelfilter">Day</label>
											<input type="text" class="form-control number-input" min="0"  value="0" onkeypress="checkObjection(this,event)" id="day">
										<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('day', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('day', decrement)" onmouseup="mouseupfunc()"></div></div>
									</div>
								</div>
								<div class="col-xs-6">
									<div class="form-group">
										<label class="labelfilter1">Hr</label>
											<input type="text"	class="form-control number-input" id="hr" min="0"  value="0" onkeypress="checkObjection(this,event)"> 
											<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('hr', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('hr', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
									</div>
								</div>
								<div class="clearfix"></div>
								
							<div class="col-xs-12">
								<div class="col-xs-6">
									<div class="form-group">
									
										<label class="labelfilter">Min</label>
											<input type="text" class="form-control number-input"id="min" min="0"  value="0" onkeypress="checkObjection(this,event)">
										<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('min', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('min', decrement)" onmouseup="mouseupfunc()"></div></div>
									</div>
								</div>
								<div class="col-xs-6">
									<div class="form-group">
										<label class="labelfilter1">Sec</label>
											<input type="text"	class="form-control number-input" id="sec" min="0"  value="0" onkeypress="checkObjection(this,event)"> 
											<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('sec', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('sec', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
									</div>
								</div>
								<div class="clearfix"></div>
								<!-- <span>From</span>
								<span>
									<label>Day:</label><input type="number" id="day" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
									<label>Hr:</label><input type="number" id="hr" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
								</span>
								<span>
									<label>Min:</label><input type="number" id="min" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
									<label>Sec:</label><input type="number" id="sec" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
								</span> -->
							</span>
							<span id="wallclockEnd">
							
							<div class="col-xs-12">
								<span>To</span>
								<div class="col-xs-6">
									<div class="clearfix"></div>
									<div class="form-group">
										<label class="labelfilter">Day</label>
											<input type="text" class="form-control number-input" min="0"  value="0" onkeypress="checkObjection(this,event)" id="today"/>
										<div class="buttonbig"><div class="incbutton"onmousedown="mousedownfunc('today', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('today', decrement)" onmouseup="mouseupfunc()"></div></div>
									</div>
								</div>
								<div class="col-xs-6">
									<div class="form-group">
										<label class="labelfilter1">Hr </label>
											<input type="text"	class="form-control number-input"  min="0"  value="0" onkeypress="checkObjection(this,event)" id="tohr"/>
											<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('tohr', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('tohr', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
									</div>
								</div>
								<div class="clearfix"></div>
								
							<div class="col-xs-12">
								<div class="col-xs-6">
									<div class="form-group">
									
										<label class="labelfilter">Min</label>
											<input type="text" class="form-control number-input" min="0"  value="0" onkeypress="checkObjection(this,event)" id="tomin"/>
										<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('tomin', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('tomin', decrement)" onmouseup="mouseupfunc()"></div></div>
									</div>
								</div>
								<div class="col-xs-6">
									<div class="form-group">
										<label class="labelfilter1">Sec</label>
											<input type="text"	class="form-control number-input" min="0"  value="0" onkeypress="checkObjection(this,event)" id="tosec" />
											<div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('tosec', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('tosec', decrement)" onmouseup="mouseupfunc()"></div></div>
										</div>
									</div>
								</div>
								<div class="clearfix"></div>

<!--<div class="wall-clock">
							<span id="wallclockStart">
								<span>${_("From")}</span>
								<span>
									<label>Day:</label><input type="number" id="day" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
									<label>Hr:</label><input type="number" id="hr" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
								</span>
								<span>
									<label>Min:</label><input type="number" id="min" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
									<label>Sec:</label><input type="number" id="sec" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
								</span>
							</span>
							<span id="wallclockEnd">
								<span>${_("To")}</span>
								<span>
									<label>Day:</label><input type="number" id="day" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
									<label>Hr:</label><input type="number" id="hr" min="0" value="0" onkeypress="checkObjection(this,event)"/>
								</span>
								<span>
									<label>Min:</label><input type="number" id="min" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
									<label>Sec:</label><input type="number" id="sec" min="0"  value="0" onkeypress="checkObjection(this,event)"/>
								</span>
							</span> -->
						</div> 
					</span>
					<button type="button" class="btn btn-primary right filter" onclick="doFiltering()" id="workload_filterBtn">${_("Filter")}</button>
				</div>
			</span>
			
	</div>
</%def>

<%def name="end_script()">
	
</%def>
