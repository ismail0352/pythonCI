## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>
<%inherit file="base.mako" />
<%namespace name="base" file="base.mako" />

<%def name="title()">${_("Viewpoint Dashboard")}</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()">

		<script type="text/javascript">
			google.load("visualization", "1", {packages:["corechart"]});
		</script>
%if base.hasAccess('Resources'):
		<script type="text/javascript">

		function formatDate(dateVal){
			var str = dateVal.replace(/-/g,'/');
			var dt = new Date(str);
			return dt.format("mmm dd, HH:ss");
		}
		//load right panel system utilization chart
			google.setOnLoadCallback(drawChart);
			function drawChart() {
				// get the utilization graph data from utilization.json(temp file) and parse it.
				var jsonData = JSON.parse($.ajax('/api/getsystemutilization/',{ async:false	}).responseText);
				// define and array and convert the json data into array format;
				var sampleArray = [];
				var processor_dedication_array= [];
				var memory_dedication_array= [];
				if(!jsonData.messages){
				if (jsonData == ''){
				$('#chart_div').append("<div class='noChData'>"+"${_("No Data Found")}"+"</div>");
				}
				else{

					var dataTable = new google.visualization.DataTable();
					dataTable.addColumn('string', 'Year');
					// A column for custom tooltip content
					dataTable.addColumn('number', 'Memory');
					dataTable.addColumn({type: 'string', role: 'tooltip'});
					dataTable.addColumn('number', 'CPU');

				for(var i in jsonData){
					/*if(i==0){
						var keys =['Time','Memory','Processor'];
						var count =0;
						for(j in jsonData[i])
							{
								keys[count] = j;
								count++;
							}
						sampleArray.push(keys);
					}*/
					var timestamp_datetime =jsonData[i].timestamp_datetime.slice(0,15);
					var time_format = formatDate(timestamp_datetime);
					var processor_dedication = Math.floor(Number(jsonData[i].processor_dedication_percentage));

					var memory_dedication = Math.floor(Number(jsonData[i].memory_dedication_percentage));
					processor_dedication_array.push(processor_dedication)

					memory_dedication_array.push(memory_dedication)


					//Changes for showing up the string on tooltip

					if (memory_dedication != 0) {
						dataTable.addRows([
							[time_format, memory_dedication, memory_dedication + '%', processor_dedication]
						]);
					}
					else {
						dataTable.addRows([
							[time_format, memory_dedication, '0%\n\n0 memory dedicated to jobs usually means that \n users are not requesting memory when they submit jobs.', processor_dedication]
						]);
					}
					//Changes for showing up the string on tooltip ends
				}

				//pass the data array to google arrayToDataTable API.

				var data = google.visualization.arrayToDataTable(sampleArray)

				var min = 0;
				var max = 0;

				if (Math.min.apply(null,memory_dedication_array)>Math.min.apply(null,processor_dedication_array))
				{

					min = Math.floor(Math.min.apply(null,processor_dedication_array));
				}
				else {
					min = Math.floor(Math.min.apply(null,memory_dedication_array));

				}

				if (Math.max.apply(null,memory_dedication_array)>Math.max.apply(null,processor_dedication_array))
				{
					max = Math.ceil(Math.max.apply(null,memory_dedication_array));
				}
				else {
					max = Math.ceil(Math.max.apply(null,processor_dedication_array));
				}


				var options = {
					hAxis: {title: '',"maxValue":200, "slantedText":true,"slantedTextAngle":90, textStyle:{color :'white'}},
					vAxis: {minValue: min,maxValue:100, gridlines:{count:3}, titleTextStyle:{color:'white'},textPosition:'in'},
					focusTarget: 'category',
					colors:["#ccc6ae","#00457e"],
					areaOpacity:0.9,
					pointShape: "circle",
					legend:"none",
					chartArea: {
						width: 310,
						height: 180,
						top:0
					}

				};
				var formatter = new google.visualization.NumberFormat({pattern:"###,##0'%'"});
				formatter.format(dataTable, 3);

				var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));

				chart.draw(dataTable, options);

				}
				} else{
					$('#chart_div').append("<div class='noChData'>"+jsonData.messages+"</div>");
				}
				}


	</script>
%endif
	<script type="text/javascript">
		$(document).ready(function(){
			$('#dataGrid .preloader').show();
			$.ajax({
				url:'/workload_table/',
				type:'GET',
				data:{max:10, offset:1},
				success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);

			disablePaginationContent();
			}
		});
	});
</script>
</%def>

<%def name="main_content()">
	<div class="row">
		<div class="col-xs-8 padlt">
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
			<div class="search-section">
				<div class="input-group">

					<input id="searchBoxDashboard" type="text" class="form-control search-input" placeholder="${_("Search")}" onkeypress="search	(this,event)">
					<select id="searchCategory" class="form-control search-select">
						<option value="job_name">Job ID</option>

					</select>

					<div class="input-group-btn">
						<!-- Button and dropdown menu -->
						<button id="search_btn" type="button" class="btn btn-primary search-btn" onClick="search(this,event)">
							<span class="glyphicon glyphicon-search"></span>
						</button>
					</div>
				</div>
			</div>
			<h1><b>${_("Workload")}</b>
				<span class="refresh" id="workloadRefreshDashboard" onClick="refreshSearch();"></span>
			</h1>
				<div class="export pull-right">
					<span>${_("Export to")}</span>
					<a href="/generateReports/?format=csv"><span class="ico-csv"></span></a>
					<a href="/generateReports/?format=xml" target= "_blank"><span class="ico-xml"></span></a>
				</div>
				<div class= "alert alert-success" style= "display: none" id="statusMsg">

				</div>
				<div style="display:none;" id="loaderDiv">

				</div>
				<div id="dataGrid" class="dtGrid datagrid-container container panel panel-default">
					<div class="preloader"></div>
				<div class="endless_page_template">

				</div>
				</div>
				<!-- <h2><b>${_("Understanding Rank")}</b><a href="#" class="link" title="Scheduling with control over a priority-weighting hierarchy where each priority and customer credentials are calculated.Scheduling with control over a priority-weighting hierarchy where each priority and customer credentials are calculated."><span class="icon ico-info"></span></a></h2>
			<div class="row">
				<div class="col-xs-6">
				<button type="button" class="btn btn-primary">CREDENTIALS &amp; PRIORITY<span class="glyphicon glyphicon-play"></span></button>
					<p>
						${_("Scheduling with control over a priority-weighting hierarchy where each priority and customer credentials are calculated")}.
					</p>
				</div>
				<div class="col-xs-6">
					<button type="button" class="btn btn-primary">Policies<span class="glyphicon glyphicon-play"></span></button>
					<p>
						${_("Further scheduling management with reservations, Fairshare, backfill, job access, resource access, and customer access")}.						
					</p>
				</div> 
			</div>
		</div>-->
			</div>
		<div class="col-xs-4 padLeft">
		%if base.hasAccess('Resources'):
			<h3 class="first-title"><b>${_("Dedicated System Resources")}</b></h3>
			<div class="panel panel-default">
				<div class="chart-legend">
					<span class="legend legend-grey">CPU</span>
					<span class="legend legend-blue pull-right">${_("MEMORY")}</span>
				</div>
				<div class="su_chart_wrapper">
					<div id="chart_div" class="su_chart_container"></div>
				</div>
				<div class="chart-legend">
					<span class="legend small">24h...</span>
					<span class="legend pull-right small">current</span>
				</div>
			</div>
		%endif
			%if base.hasAccess('Resources'):
			<h3><b>${_("Node Summary")}</b></h3>
			<div class="panel panel-default" id="resourcepanel">
				<h4 id="countNodes"></h4>
				<div class="panel-body" id="resourcepanelbody">
				
					<section id="resSumSection" class="chart-section">
						
						<div id="resourceSummary" class="progress">

						</div>
						
					</section>
					
				</div>
				<a href="/nodelist/"  class="btn btn-primary" id="view_nodes_btn">${_("View All Nodes")}<span class="glyphicon glyphicon-play"></span>
						</a>
			</div>
			%endif
			<h3><b>${_("Workload Summary")}</b></h3>
			<div class="panel panel-default" id="jobpanel">
				<h4 id="countJobs"></h4>
				<div class="panel-body" id="jobpanelbody">
					<!-- Job Summary Section -->
					<section id="jobSumSection" class="chart-section">
						
						<div id="jobSummary" class="progress progress-striped active">

						</div>
							
					</section>
					
				</div>
				<a href="/workload/" class="btn btn-primary" id="view_workload_btn">${_("View All Workload")}<span class="glyphicon glyphicon-play"></span>
						</a>
			</div>
		</div>

	</div>

</%def>

<%def name="end_script()">
%if base.hasAccess('Resources'):
	<script type="text/javascript">
		$(document).ready(function(){

			loadResSumChart();

		});
	</script>
%endif
	<script type="text/javascript">
		$(document).ready(function(){


			loadJobSumChart();
		});
	</script>
</%def>

