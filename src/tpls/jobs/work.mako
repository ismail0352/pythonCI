## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<table class="table">
  <thead>
  <tr>
		<th id="job_name" width="120" onclick="onSort(this)" class="sort">${_("Job ID")}</th>
		<th id="user_name" width="120" onclick="onSort(this)" class="sort">${_("Submitter ID")}</th>
		<%doc>
		# Commenting code to remove priority columns --IRIS-455
		<th id="priority" width="60" class="text-center sort" onclick="onSort(this)">${_("Priority")}</th>
		</%doc>
		<th id="job_start_datetime" width="120" class="text-center sort" onclick="onSort(this)">${_("Start Datetime")}</th>
		<th id="job_state" width="90" class="text-center sort" onclick="onSort(this)">${_("Job Status")}</th>
		<%doc>
		# Commenting code to remove rank columns --IRIS-309
		<th id="rank" width="70" class="text-center sort" onclick="onSort(this)">${_("Rank")}</th>
		</%doc>
		<th width="90" class="text-center" id="workload_CoresColumn">${_("Cores")}</th>
		<th width="90" class="text-center" id="workload_NodesColumn">${_("Nodes")}</th>
		<th id="wallclock_seconds" width="90" class="text-right sort" onclick="onSort(this)">${_("Wall Clock")}</th>
		<%doc><th>${_("Utilization")}</th></%doc>
  </tr>
  </thead>
  
  <tbody>
% if status_code == 2000 :
	% if entries :
		% for count,entry in enumerate(entries):
				<tr>
					<td width="120">
					
					%if hasAccessforjobdetails('Job Details'):
						<a href="/jobdetails/?job_name=${entry['job_id']  }&job_status=${entry['job_state']  }&job_id=${entry['uChartjobId']  }&tab=${ active  }" id="jobName${ count  }">${entry['job_id']  }</a>
					%else:
						<a id="jobName${ count  }">${entry['job_id']  }</a>
					%endif
					%if hasAccessforjobdetails('Job Edit-admin'):
						% if entry['job_state'] in ('RUNNING','SUSPENDED','DEFERRED','BATCHHOLD','BLOCKED','NOTQUEUED','STAGING','STARTING'):
							<button id="infoPopUp" type="button" class="popmenu close-popover-link" rel="popover" data-placement="right" data-content="" data-trigger="hover"></button>
							
							<div id="popoverContent" style="display:none">
								<a href="#" id= "cancel" title="${entry['job_id']  }" onclick="JavaScript:onStatusClick('cancel','${entry['job_id']  }')" >Cancel</a>
							</div>
						% elif entry['job_state'] in ('IDLE','UNKNOWN'):
							
							<button id="infoPopUp" type="button" class="popmenu close-popover-link" rel="popover" data-placement="right" data-content="" data-trigger="hover"></button>
							
							<div id="popoverContent" style="display:none">
								<a href="#" id= "hold" title="${entry['job_id']  }" onclick="JavaScript:onStatusClick('hold','${entry['job_id']  }')">Hold</a>
								<a href="#" id= "cancel" title="${entry['job_id']  }" onclick="JavaScript:onStatusClick('cancel','${entry['job_id']  }')" >Cancel</a>
							</div>
						% elif entry['job_state'] in ('HOLD','SYSTEMHOLD','USERHOLD'):
							
							<button id="infoPopUp" type="button" class="popmenu close-popover-link" rel="popover" data-placement="right" data-content="" data-trigger="hover"></button>
							
							<div id="popoverContent" style="display:none">
								<a href="#" id= "release" title="${entry['job_id']  }" onclick="JavaScript:onStatusClick('release','${entry['job_id']  }')">Release</a>
								<a href="#" id= "cancel" title="${entry['job_id']  }" onclick="JavaScript:onStatusClick('cancel','${entry['job_id']  }')" >Cancel</a>
							</div>
						%else:
							&nbsp;
						% endif
						
					%endif
					
					</td>

				<td width="120" id="userName${ count  }">${entry['user_name']  }</td>
				<%doc>
				# Commenting code to remove priority columns --IRIS-455
				<td width="60" class="text-center"><p class="ellipsistxt"  title="${entry['priority']  }">${entry['priority']  }</p></td>
				</%doc>
				<td width="120" class="text-center" id="startDatetime${ count  }">${entry['job_start_datetime']  }</td>
				<td width="90" class="text-center" id="jobStatus${ count  }">${entry['job_state']  }</td>
				<%doc>
				# Commenting code to remove rank columns --IRIS-309
				<td width="70" class="text-center">${entry['rank']  }</td>
				</%doc>

				<td width="90" id="cores${ count  }" class="text-center">${entry['processor_count']  }</td>
				<td width="90" id="nodes${ count  }" class="text-center">${entry['node_count']  }</td>
				<td width="90" id="wallClock${ count  }" class="text-right"><div title='${entry['elapsed_time']  }'>${entry['wallclock_seconds']  }</div></td>

				<td id="chartColumn" width="80" style="display:none">

					<%doc><img class="cc-spinner" id="spinner" src="/static/images/spinner.gif" />
					<label></label></%doc>
					<div class="uChart-wrapper">
						<div id= ${entry['uChartjobId']  } class="uChart-container"></div>
					</div>
				</td>
				</tr>
		% endfor
	% else :
		<tr id="NoRecordsFound">
		<td colspan="6"><h5>No Records Found </h5></td>
		</tr>
	% endif 
% else:
	<tr id="NoRecordsFound">
		<td colspan="6"><h5>${ entries  } </h5></td>
	</tr>
% endif
  </tbody>  
  
</table>
<div class="grid-pagination">
	<div class="page-views">
		${_("View")}   
		<select id="viewPerPage" class="form-control page-views-select" onchange="onPageChange()">
			
			% if active == "dashboard":
				<option value="10">10</option>
			% endif
			<option value="20">20</option>
			<option value="50">50</option>
			<option value="100">100</option>
			<option value="500">500</option>
			<option value="1000">1000</option>
		
		</select>
		${_("Per Page")}
	</div>
	<div class="page-count pull-right">
		<button type="button" class="btn btn-primary page-count-btn" id="goToFirst" onclick="onControlClick(this)">
			<span class="glyphicon glyphicon-backward prev"></span>
		</button>
		<button type="button" class="btn btn-primary page-count-btn" id="prev" onclick="onControlClick(this)">
			<span class="glyphicon glyphicon-play prev"></span>
		</button>
		${_("Page")}
		<select class="form-control page-views-select" id="pageNumber" onchange="onPageChangePerPage()">
		% for no in page_nums:
			
			<option value=${no  }>${ no  }</option>
		% endfor
		</select>&nbsp;
		${_("of")} <label id="totalPages">${ total_pages  }</label>
		<input type="text" id="hiddenTotalCnt" style='display:none' value=${ total_count  }></input>
				<button type="button" class="btn btn-primary page-count-btn" id="next" onclick="onControlClick(this)">
			<span class="glyphicon glyphicon-play"></span>
		</button>
		<button type="button" class="btn btn-primary page-count-btn" id="goToLast" onclick="onControlClick(this)">
			<span class="glyphicon glyphicon-forward"></span>
		</button>
	</div>
</div>
	<%def name="hasAccessforjobdetails(x)">
	%if x in session_permission_list:
		 <%return True%>
	%endif
	</%def>

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
								
								var i =0;
								$('.table>tbody>tr').each(function(){
								
								
								var	chartId = $(this).find('td:last>div>div').attr('id');
								var lblUtilizationPercentage = $(this).find('td:last>label');
								
								var divPopOverContent = $(this).find('#popoverContent');
								divPopOverContent.prop("id","popoverContent-" + i); 

								var btnInfoPopUp = $(this).find('#infoPopUp');
								btnInfoPopUp.prop("id","infoPopUp-" + i); 
								btnInfoPopUp.css("visibility","hidden");
								<%doc>
								// Commenting code for Utilization Charts --IRIS-293
								
								var imgSpinner = $(this).find('td:last>img');
								imgSpinner.prop("id","spinner" + chartId);
								lblUtilizationPercentage.prop("id","lbl" + chartId); 
								
								var utilizationPercentage ;
								$.ajax({
									url:'/api/getutilization/',
									type:'GET',
									data:{jobId:chartId},
									success:function(result){
											var jsonData = result;

											
											if (jsonData[1] == undefined){
												$('.table>tbody>tr').find('#spinner' + chartId).hide();
												//removing the spinner ends
												$('.table>tbody>tr').find('#lbl' + chartId).text("N/A");
												return;
											}
											
											if(jsonData[1].length != undefined || jsonData[1].length != null)
											{
												

													//pass the data array to google arrayToDataTable API.
													var data = google.visualization.arrayToDataTable(jsonData[1]);

													var options = {
														hAxis: {title: '',  titleTextStyle: {color: '#333'},minValue:1,maxValue:100,textPosition:'none',baselineColor:'#aaaaaa'},
														vAxis: {minValue: 0,maxValue:100, gridlines:{count:1}, titleTextStyle:{color:'white'},textPosition:'none'},
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
													if($('.table>tbody>tr').find('#spinner' + chartId) != null)
													{
														
														$('.table>tbody>tr').find('#spinner' + chartId).hide();
													}
													//removing the spinner ends
													//Adding the Chart utilization % value starts
													if($('.table>tbody>tr').find('#lbl' + chartId) != null)
													{
														
														$('.table>tbody>tr').find('#lbl' + chartId).text(jsonData[0]);
													}
													//Chart utilization % value ends

												}
												else
												{
													
													//removing the spinner
													if($('.table>tbody>tr').find('#spinner' + chartId) != null)
													{
														$('.table>tbody>tr').find('#spinner' + chartId).hide();
													}
													//removing the spinner ends

													$('.table>tbody>tr').find('#lbl' + chartId).text("N/A");
														
														
												}
											}											
										}); </%doc>
									
									i++;
									});// each() ends
									
								}
								catch(e)
								{
									
								}
							} 
</script>


<script type="text/JavaScript">
				
					$(document).ready(function() {
						$(function(){
							$('[rel = popover]').popover({
								html:true,
								trigger: "click",
								content: function(){

									var arr = $(this).attr('id').split('-');
									return $('#popoverContent-'+arr[1]).html();

								}
							});
						});
					});
</script>

<script>
$( "button").click(function() {
  var arr = $(this).attr('id').split('-');
  if(arr[0] == 'infoPopUp')
  {
		$('#infoPopUp-'+arr[1]).popover();
  }
});
$("#dataGrid .table tbody tr").on({
	mouseenter:function() {
		$(this).find("button[rel = popover]").css("visibility","visible")
	},
	mouseleave: function() {
		$(this).find("button[rel = popover]").popover("hide");
		$(this).find("button[rel = popover]").css("visibility","hidden")
	}
});
</script>


<script type="text/javascript">
	function onStatusClick(status, jobId) {
		var changeStatus = status;
		$('#loaderDiv').show();
		$('#loaderDiv').html('<div id="err preloader" class="preloader"></div>');
		$.ajax({
			url: '/modifyjob/',
			type: 'GET',
			data: {jobId: jobId, changeStatus: changeStatus },
			success: function (result) {
				$('#errorMsg').hide();
				$('#statusMsg').hide();
				var lastIndex = result.lastIndexOf(",");
				if (lastIndex == -1) {
					lastIndex = result.length;
				}
				var message = result.substring(0, lastIndex).trim();
				var statusMsg = result.substring(lastIndex + 1).trim();
				if (statusMsg == "success") {
					$('#statusMsg').html('<a href="#" id="crossBtn" class="close" onClick="tryMe()">&times;</a>');
					$('#loaderDiv').hide();
					$('#statusMsg').show();
					$('#statusMsg').append(message);
				}
				else {
					$('#statusMsg').html('<a href="#" id="crossBtn" class="close" onClick="tryMe()">&times;</a>');
					$('#statusMsg').css('background-color', '#f2dede');
					$('#statusMsg').css('color', '#a94442');
					$('#loaderDiv').hide();
					$('#statusMsg').show();
					$('#statusMsg').append(message);
				}
			}
		});
	}
</script>

<script type="text/javascript">
	function tryMe(){
		$('#statusMsg').hide();
	};
	function tryMeforerror(){
        $('#errorMsg').hide();
    }
</script> 



