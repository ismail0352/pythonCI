// Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

// JavaScript Document	
// Dashboard & workload Array representing the sorting states of grid
var sortingState = {
					'jobid':-1,
					'jobname':-1,
					'priority':-1,
					'jobstatus':-1,
					'rank':-1,
					'wallclock':-1,
					'job_start_datetime':-1
					};
var persistedSortingState = {
					'colname':null,
					'sortState': -1
};
var isDirtyPlaceholder = false;
var intervalId;
//Dashboard & workload function to get sorting target and perform sort
function onSort(colName){
	var colId = $(colName).attr('id');
	switch(colId){
		case 'job_name': sortingState.jobid = -(sortingState.jobid);
					  doSort(colId,sortingState.jobid);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.jobid
					  break;
		case 'user_name': sortingState.jobname = -(sortingState.jobname);
					  doSort(colId,sortingState.jobname);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.jobname
					  break;
		case 'priority': sortingState.priority = -(sortingState.priority);
					  doSort(colId,sortingState.priority);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.priority
					  break;
		case 'job_start_datetime': sortingState.job_start_datetime = -(sortingState.job_start_datetime);
					  doSort(colId,sortingState.job_start_datetime);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.job_start_datetime
					  break;			
		case 'job_state': sortingState.jobstatus = -(sortingState.jobstatus);
					  doSort(colId,sortingState.jobstatus);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.jobstatus
					  break;
		case 'rank': sortingState.rank = -(sortingState.rank);
					  doSort(colId,sortingState.rank);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.rank
					  break;
		case 'wallclock_seconds': sortingState.wallclock = -(sortingState.wallclock);
					  doSort(colId,sortingState.wallclock);
					  persistedSortingState.colname = colId;
					  persistedSortingState.sortState = sortingState.wallclock
					  break;			
		default:break;
	};
					
}


//Dashboard & workload function to do sorting on column with its ascending state
function doSort(colId,sortState){
	var pageNumber = $('#pageNumber').val();
	var viewPerPage = $('#viewPerPage').val();
	$('#dataGrid').append('<div class="preloader"></div>').show();
	
	var searchValue = null;
	var searchCat = null;
	if($('#searchBoxDashboard').is(':visible'))
	 searchValue= $('#searchBoxDashboard').val();
	
	if($('#searchCategory').is(':visible'))
	 searchCat= $('#searchCategory').val();
	
	
	//Created for sending data of narrow search- abhinavr - 4/29/14

	if(filterParam.jobState != 'null')
		{
				filterParam.jobState = $('#jobState').val();
		}
		if(filterParam.priorityFrom != '0')
		{
			filterParam.priorityFrom = $('#priorityFrom').val();
		}
		if(filterParam.priorityTo != '0')
		{
			filterParam.priorityTo = $('#priorityTo').val();
		}
		if(filterParam.rankFrom != '0')
		{
			filterParam.rankFrom = $('#rankFrom').val();
		}
		if(filterParam.rankTo != '0')
		{
			filterParam.rankTo = $('#rankTo').val();
		}
		if(filterParam.dateTimeRange != 'null')
		{
			filterParam.dateTimeRange = $('#dateTimeRange').val();
		}
		if(filterParam.startDate != 'null')
		{
			filterParam.startDate = $('#txtStartDate').val();
		}
		if(filterParam.endDate != 'null')
		{
			filterParam.endDate = $('#txtEndDate').val();
		}
		if(filterParam.wallclockStartDay != '0')
		{
			filterParam.wallclockStartDay = $('#wallclockStart #day').val();
		}
		if(filterParam.wallclockStartHr != '0')
		{
			filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
		}
		if(filterParam.wallclockStartMin != '0')
		{
			filterParam.wallclockStartMin = $('#wallclockStart #min').val();
		}
		if(filterParam.wallclockStartSec != '0')
		{
			filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
		}
		if(filterParam.wallclockEndDay != '0')
		{
			filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
		}
		if(filterParam.wallclockEndHr != '0')
		{
			filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
		}
		if(filterParam.wallclockEndMin != '0')
		{
			filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
		}
		if(filterParam.wallclockEndSec != '0')
		{
			filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
		}

	//Ends
	
	$.ajax({
		url:'/workload_table',
		type:'GET',
		data:{sort_parameter:colId,
			sortState:sortState,
			max:viewPerPage,
			offset:pageNumber,
			searchValue:searchValue,
			searchCategory:searchCat,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			jobId:searchParam.jobId,
			userName:searchParam.userName,
			resourceName:searchParam.resourceName,
			jobState:filterParam.jobState,
			priorityFrom:filterParam.priorityFrom,
			priorityTo:filterParam.priorityTo,
			rankFrom:filterParam.rankFrom,
			rankTo:filterParam.rankTo,
			dateTimeRange:filterParam.dateTimeRange,
			startDate:filterParam.startDate,
			endDate:filterParam.endDate,
			wallclockStartDay:filterParam.wallclockStartDay,
			wallclockStartHr:filterParam.wallclockStartHr,
			wallclockStartMin:filterParam.wallclockStartMin,
			wallclockStartSec:filterParam.wallclockStartSec,
			wallclockEndDay:filterParam.wallclockEndDay,
			wallclockEndHr:filterParam.wallclockEndHr,
			wallclockEndMin:filterParam.wallclockEndMin,
			wallclockEndSec:filterParam.wallclockEndSec,
			//ends
		},
		success:function(result){
			$('#dataGrid .preloader').hide();
			$('#dataGrid').html(result);
			$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
			//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
			$('#viewPerPage').val(viewPerPage);
			disablePaginationContent();
		}
	});
}//doSort ends



//Resource Summary status section
                //function to load resource summary section chart
function loadResSumChart(){
	$('#resSumSection .preloader').show();
	$.getJSON('/api/getresourcesummary/',function(jsondata){
		if(!jsondata.messages){
		$('#resSumSection .preloader').hide();
		var totalStateCnt = 0;
		var cntOfNodes = 0;
		for(var i in jsondata){
						totalStateCnt += Number(jsondata[i].count);
						cntOfNodes ++;
		}
		$('#countNodes').text(totalStateCnt +" Nodes");
		//Abhinavr code starts
		//1. Get the total count of all states - stored in totalStateCnt var
		
		//2. Calculation of % participation of each state / totalStateCnt
		var calculationParticipationPercentageArr = [];
		for(var i in jsondata){
						calculationParticipationPercentageArr[i] = (Number(jsondata[i].count)/totalStateCnt)+ "-" +jsondata[i].state+ "-" + jsondata[i].count ;
		}
		//3. Calculating the px , from the total width provided to the cylinder  % par * 266
		
		var pxRequiredArr = [];
		
		for(var i in calculationParticipationPercentageArr)
		{
						pxRequiredArr[i] =  (calculationParticipationPercentageArr[i].split('-')[0] * 266) +"-"+ (calculationParticipationPercentageArr[i].split('-')[1]) +"-"+ (calculationParticipationPercentageArr[i].split('-')[2]);
		}
						
		//4. Need to identify the states with state value less then 20 px
		var minStates = [];
		var deviatedValue = 0;
		var remainingStates = [];
		var totalRemainingStCount = 0;
		
		for(var i in pxRequiredArr)
		{
										if((pxRequiredArr[i].split('-')[0]) < 20)
										{
														minStates.push(pxRequiredArr[i]);
														//5. Get the deviated value
														deviatedValue += (20 - (pxRequiredArr[i].split('-')[0]));
										}
										else
										{
														remainingStates.push(pxRequiredArr[i]);
														//Identifying the count of states after deducting 20 px
														totalRemainingStCount += (pxRequiredArr[i].split('-')[0] - 20);
										}
		}
		
		//5. Get the deviation value and divide it by rest of the states > 20 px
		var restStateCnt = pxRequiredArr.length - minStates.length;
		
		var deviationPerState = deviatedValue/restStateCnt;
		

		
		
		for(var i in remainingStates)
		{
										var relativePercentageFromTotalStCount = (remainingStates[i].split('-')[0] - 20)/totalRemainingStCount;
										remainingStates[i] = (remainingStates[i].split('-')[0] - (deviatedValue * relativePercentageFromTotalStCount))+"-"+(remainingStates[i].split('-')[1])+"-"+(remainingStates[i].split('-')[2]);
		}

		for(var i in minStates)
		{
						minStates[i] = 20 +"-"+ minStates[i].split('-')[1] +"-"+ minStates[i].split('-')[2];
						remainingStates.push(minStates[i]);
		}
		
		
		var linkCnt = 0;
		for(var k in remainingStates) {
						stateVal = remainingStates[k].split('-')[1].toLowerCase();
						$('#resourceSummary').append("<a id='resSummaryLink"+linkCnt +"'href='/nodelist/?max=10&offset=1&status="+stateVal.toUpperCase()+"' title="+stateVal+"><div class='progress-bar-"+stateVal+"'>&nbsp;</div></a>");
						linkCnt++;
		}
		
		var resourceSummaryCnt =0;
		for(var j in remainingStates){
						if(Math.floor(remainingStates[j].split('-')[0]) >= 50){
						$('#resourceSummary>a>div').eq(j).css('width',Math.floor(remainingStates[j].split('-')[0])+'px')
						.append("<span id='resourceSummarySpan"+resourceSummaryCnt+"' class='node-status "+remainingStates[j].split('-')[1].toLowerCase()+"'><b>"+remainingStates[j].split('-')[2]+"</b><br/>"+remainingStates[j].split('-')[1].toLowerCase()+"</span>");
						}
						else
						{
						$('#resourceSummary>a>div').eq(j).css('width',Math.floor(remainingStates[j].split('-')[0])+'px')
						.append("<span id='resourceSummarySpan"+resourceSummaryCnt+"' class='node-status "+remainingStates[j].split('-')[1].toLowerCase()+"'><b>"+remainingStates[j].split('-')[2]+"</b></span>");
						}
						resourceSummaryCnt++;
		}
					
					
	}else{
		$("#resourcepanelbody").css('display','none');
		$('#resourcepanel').prepend("<div class='noChartData'>"+jsondata.messages+"</div>");
	}
					
	}).error(function(){
	});
}//loadResSumChart () ends

	
//Job Summary Status section
//function to load jobs summary chart
function loadJobSumChart(){
$('#jobSumSection .preloader').show();
$.getJSON('/api/getjobsummary/?format=json',function(jsondata){
	if(!jsondata.messages){
			var totalStateCnt = 0;
			var cntOfNodes = 0;
			for(var i in jsondata){
					//Changes done for IRIS-325 starts
						if(jsondata[i].state.toLowerCase() != 'completed'){
							totalStateCnt += Number(jsondata[i].count);
							cntOfNodes ++;
						}
					//Changes done for IRIS-325 starts ends
			}
			$('#countJobs').text(totalStateCnt +" Jobs");
			//Abhinavr code starts
			//1. Get the total count of all states - stored in totalStateCnt var
			
			//2. Calculation of % participation of each state / totalStateCnt
			var calculationParticipationPercentageArr = [];
			for(var i in jsondata){
				//Changes done for IRIS-325 starts
				if(jsondata[i].state.toLowerCase() != 'completed'){
							calculationParticipationPercentageArr[i] = (Number(jsondata[i].count)/totalStateCnt)+ "-" +jsondata[i].state+ "-" + jsondata[i].count ;
				}
				//Changes done for IRIS-325 starts ends
			}
			//3. Calculating the px , from the total width provided to the cylinder  % par * 266
			
			var pxRequiredArr = [];
			
			for(var i in calculationParticipationPercentageArr)
			{
							pxRequiredArr[i] =  (calculationParticipationPercentageArr[i].split('-')[0] * 266) +"-"+ (calculationParticipationPercentageArr[i].split('-')[1]) +"-"+ (calculationParticipationPercentageArr[i].split('-')[2]);
			}
			
			//4. Need to identify the states with state value less then 20 px
			var minStates = [];
			var deviatedValue = 0;
			var remainingStates = [];
			var totalRemainingStCount = 0;
			
			for(var i in pxRequiredArr)
			{
				if((pxRequiredArr[i].split('-')[0]) < 20)
				{
								minStates.push(pxRequiredArr[i]);
								//5. Get the deviated value
								deviatedValue += (20 - (pxRequiredArr[i].split('-')[0]));
				}
				else
				{
								remainingStates.push(pxRequiredArr[i]);
								//Identifying the count of states after deducting 20 px
								totalRemainingStCount += (pxRequiredArr[i].split('-')[0] - 20);
				}
			}
			//5. Get the deviation value and divide it by rest of the states > 20 px
			var restStateCnt = pxRequiredArr.length - minStates.length;
			
			var deviationPerState = deviatedValue/restStateCnt;
			//6. Identify how close the remaining states are from minimum clickable width i.e 20 px
			
			
			for(var i in remainingStates)
			{
				var relativePercentageFromTotalStCount = (remainingStates[i].split('-')[0] - 20)/totalRemainingStCount;
				remainingStates[i] = (remainingStates[i].split('-')[0] - (deviatedValue * relativePercentageFromTotalStCount))+"-"+(remainingStates[i].split('-')[1])+"-"+(remainingStates[i].split('-')[2]);
			}

			for(var i in minStates)
			{
				minStates[i] = 20 +"-"+ minStates[i].split('-')[1] +"-"+ minStates[i].split('-')[2];
				remainingStates.push(minStates[i]);
			}
			
			var jobSummaryCnt = 0;
			for(var k in remainingStates) {
				stateVal = remainingStates[k].split('-')[1].toLowerCase();
				$('#jobSummary').append("<a id='jobSummaryLink"+jobSummaryCnt +"'href='/workload/?max=10&offset=1&status="+stateVal.toUpperCase()+"' title="+stateVal+"><div class='progress-bar-"+stateVal+"'>&nbsp;</div></a>");
				jobSummaryCnt++;			
			}
			var jobSummaryCnt =0;
			for(var j in remainingStates){
				if(Math.floor(remainingStates[j].split('-')[0]) >= 50){
					$('#jobSummary>a>div').eq(j).css('width',Math.floor(remainingStates[j].split('-')[0])+'px')
					.append("<span id='jobSummarySpan"+jobSummaryCnt+"'class='node-status "+remainingStates[j].split('-')[1].toLowerCase()+"'><b>"+remainingStates[j].split('-')[2]+"</b><br/>"+remainingStates[j].split('-')[1].toLowerCase()+"</span>");
				}
				else
				{
					$('#jobSummary>a>div').eq(j).css('width',Math.floor(remainingStates[j].split('-')[0])+'px')
					.append("<span id='jobSummarySpan"+jobSummaryCnt+"'class='node-status "+remainingStates[j].split('-')[1].toLowerCase()+"'><b>"+remainingStates[j].split('-')[2]+"</b></span>");
				}
				jobSummaryCnt++;	
			}
					
			}
			else{
					$("#jobpanelbody").css('display','none');
					$('#jobpanel').prepend("<div class='noChartData'>"+jsondata.messages+"</div>");
			}
			
}).error(function(){
});

}//loadJobSumChart () ends

	//function to disable the pagination buttons
	function disablePaginationContent()
	{
		var pageNumber = $('#pageNumber').val();
		
		$('#goToLast').attr('disabled',false);
		$('#next').attr('disabled',false);
		
		$('#goToFirst').attr('disabled',false);
		$('#prev').attr('disabled',false);
		
		if(pageNumber == $('#totalPages').text())
		{
			$('#goToLast').attr('disabled',true);
			$('#next').attr('disabled',true);
		}
		if(pageNumber == '1')
		{
			$('#goToFirst').attr('disabled',true);
			$('#prev').attr('disabled',true);
			
		}
		if ($('#totalPages').text().trim() == '1')
		{
			$('#goToFirst').attr('disabled',true);
			$('#prev').attr('disabled',true);
			$('#goToLast').attr('disabled',true);
			$('#next').attr('disabled',true);
		}
	}
	
	//Datagrid for workload and dashboard Pagination Section
	//function to call pagination on changing the values from page number or records per page drop down
	function onPageChangePerPage(){
	
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		var searchValue = null;
		var searchCat = null;
		if($('#searchBoxDashboard').is(':visible'))
		 searchValue= $('#searchBoxDashboard').val();
		
		if($('#searchCategory').is(':visible'))
		 searchCat= $('#searchCategory').val();
		
		disablePaginationContent();
		
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		//Created for sending data of narrow search- abhinavr - 4/29/14

	if(filterParam.jobState != 'null')
		{
				filterParam.jobState = $('#jobState').val();
		}
		if(filterParam.priorityFrom != '0')
		{
			filterParam.priorityFrom = $('#priorityFrom').val();
		}
		if(filterParam.priorityTo != '0')
		{
			filterParam.priorityTo = $('#priorityTo').val();
		}
		if(filterParam.rankFrom != '0')
		{
			filterParam.rankFrom = $('#rankFrom').val();
		}
		if(filterParam.rankTo != '0')
		{
			filterParam.rankTo = $('#rankTo').val();
		}
		if(filterParam.dateTimeRange != 'null')
		{
			filterParam.dateTimeRange = $('#dateTimeRange').val();
		}
		if(filterParam.startDate != 'null')
		{
			filterParam.startDate = $('#txtStartDate').val();
		}
		if(filterParam.endDate != 'null')
		{
			filterParam.endDate = $('#txtEndDate').val();
		}
		if(filterParam.wallclockStartDay != '0')
		{
			filterParam.wallclockStartDay = $('#wallclockStart #day').val();
		}
		if(filterParam.wallclockStartHr != '0')
		{
			filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
		}
		if(filterParam.wallclockStartMin != '0')
		{
			filterParam.wallclockStartMin = $('#wallclockStart #min').val();
		}
		if(filterParam.wallclockStartSec != '0')
		{
			filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
		}
		if(filterParam.wallclockEndDay != '0')
		{
			filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
		}
		if(filterParam.wallclockEndHr != '0')
		{
			filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
		}
		if(filterParam.wallclockEndMin != '0')
		{
			filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
		}
		if(filterParam.wallclockEndSec != '0')
		{
			filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
		}

		//Ends
		
		$.ajax({
			url:'/workload_table/',
			type:'GET',
			
			data:{max:viewPerPage, offset:pageNumber,
			searchValue:searchValue,
			searchCategory:searchCat,
			sort_parameter:persistedSortingState.colname,
			sortState: persistedSortingState.sortState,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			jobId:searchParam.jobId,
			userName:searchParam.userName,
			resourceName:searchParam.resourceName,
			jobState:filterParam.jobState,
			priorityFrom:filterParam.priorityFrom,
			priorityTo:filterParam.priorityTo,
			rankFrom:filterParam.rankFrom,
			rankTo:filterParam.rankTo,
			dateTimeRange:filterParam.dateTimeRange,
			startDate:filterParam.startDate,
			endDate:filterParam.endDate,
			wallclockStartDay:filterParam.wallclockStartDay,
			wallclockStartHr:filterParam.wallclockStartHr,
			wallclockStartMin:filterParam.wallclockStartMin,
			wallclockStartSec:filterParam.wallclockStartSec,
			wallclockEndDay:filterParam.wallclockEndDay,
			wallclockEndHr:filterParam.wallclockEndHr,
			wallclockEndMin:filterParam.wallclockEndMin,
			wallclockEndSec:filterParam.wallclockEndSec
			//ends
			},
			success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
					
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
			}
		})
	}
	
//Datagrid for workload and dashboard Pagination Section
	//function to call pagination on changing the values from page number or records per page drop down
	function onPageChange(){
	
		
		var viewPerPage = $('#viewPerPage').val();
		var searchValue = null;
		var searchCat = null;
		if($('#searchBoxDashboard').is(':visible'))
		 searchValue= $('#searchBoxDashboard').val();
		
		if($('#searchCategory').is(':visible'))
		 searchCat= $('#searchCategory').val();
		
		disablePaginationContent();
		
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		//Created for sending data of narrow search- abhinavr - 4/29/14

		if(filterParam.jobState != 'null')
		{
				filterParam.jobState = $('#jobState').val();
		}
		if(filterParam.priorityFrom != '0')
		{
			filterParam.priorityFrom = $('#priorityFrom').val();
		}
		if(filterParam.priorityTo != '0')
		{
			filterParam.priorityTo = $('#priorityTo').val();
		}
		if(filterParam.rankFrom != '0')
		{
			filterParam.rankFrom = $('#rankFrom').val();
		}
		if(filterParam.rankTo != '0')
		{
			filterParam.rankTo = $('#rankTo').val();
		}
		if(filterParam.dateTimeRange != 'null')
		{
			filterParam.dateTimeRange = $('#dateTimeRange').val();
		}
		if(filterParam.startDate != 'null')
		{
			filterParam.startDate = $('#txtStartDate').val();
		}
		if(filterParam.endDate != 'null')
		{
			filterParam.endDate = $('#txtEndDate').val();
		}
		if(filterParam.wallclockStartDay != '0')
		{
			filterParam.wallclockStartDay = $('#wallclockStart #day').val();
		}
		if(filterParam.wallclockStartHr != '0')
		{
			filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
		}
		if(filterParam.wallclockStartMin != '0')
		{
			filterParam.wallclockStartMin = $('#wallclockStart #min').val();
		}
		if(filterParam.wallclockStartSec != '0')
		{
			filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
		}
		if(filterParam.wallclockEndDay != '0')
		{
			filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
		}
		if(filterParam.wallclockEndHr != '0')
		{
			filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
		}
		if(filterParam.wallclockEndMin != '0')
		{
			filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
		}
		if(filterParam.wallclockEndSec != '0')
		{
			filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
		}
		//Ends
		
		$.ajax({
			url:'/workload_table/',
			type:'GET',
			
			data:{max:viewPerPage, offset:1,
			searchValue:searchValue,
			searchCategory:searchCat,
			sort_parameter:persistedSortingState.colname,
			sortState: persistedSortingState.sortState,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			jobId:searchParam.jobId,
			userName:searchParam.userName,
			resourceName:searchParam.resourceName,
			jobState:filterParam.jobState,
			priorityFrom:filterParam.priorityFrom,
			priorityTo:filterParam.priorityTo,
			rankFrom:filterParam.rankFrom,
			rankTo:filterParam.rankTo,
			dateTimeRange:filterParam.dateTimeRange,
			startDate:filterParam.startDate,
			endDate:filterParam.endDate,
			wallclockStartDay:filterParam.wallclockStartDay,
			wallclockStartHr:filterParam.wallclockStartHr,
			wallclockStartMin:filterParam.wallclockStartMin,
			wallclockStartSec:filterParam.wallclockStartSec,
			wallclockEndDay:filterParam.wallclockEndDay,
			wallclockEndHr:filterParam.wallclockEndHr,
			wallclockEndMin:filterParam.wallclockEndMin,
			wallclockEndSec:filterParam.wallclockEndSec
			//ends
			},
			success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					//$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
					//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
			}
		})
	}
	//function to call pagination on controls' click event
	function onControlClick(caller){
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		if(!$('#filterInputJobId').is(':visible'))
		searchParam.jobId = null;
		
		//if(!$('#filterInputUserName').is(':visible'))
		if(!$('#filterInputSubmitterID').is(':visible'))
		searchParam.userName = null;
	
		var clickedButton = $(caller).attr('id');
		var lastPageNumber= $('#pageNumber').find('option:last').val();
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		
		var searchValue = null;
		var searchCat = null;
		if($('#searchBoxDashboard').is(':visible'))
		 searchValue= $('#searchBoxDashboard').val();
		
		if($('#searchCategory').is(':visible'))
		 searchCat= $('#searchCategory').val();
		
		//Created for sending data of narrow search- abhinavr - 4/29/14

		if(filterParam.jobState != 'null')
		{
				filterParam.jobState = $('#jobState').val();
		}
		if(filterParam.priorityFrom != '0')
		{
			filterParam.priorityFrom = $('#priorityFrom').val();
		}
		if(filterParam.priorityTo != '0')
		{
			filterParam.priorityTo = $('#priorityTo').val();
		}
		if(filterParam.rankFrom != '0')
		{
			filterParam.rankFrom = $('#rankFrom').val();
		}
		if(filterParam.rankTo != '0')
		{
			filterParam.rankTo = $('#rankTo').val();
		}
		if(filterParam.dateTimeRange != 'null')
		{
			filterParam.dateTimeRange = $('#dateTimeRange').val();
		}
		if(filterParam.startDate != 'null')
		{
			filterParam.startDate = $('#txtStartDate').val();
		}
		if(filterParam.endDate != 'null')
		{
			filterParam.endDate = $('#txtEndDate').val();
		}
		if(filterParam.wallclockStartDay != '0')
		{
			filterParam.wallclockStartDay = $('#wallclockStart #day').val();
		}
		if(filterParam.wallclockStartHr != '0')
		{
			filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
		}
		if(filterParam.wallclockStartMin != '0')
		{
			filterParam.wallclockStartMin = $('#wallclockStart #min').val();
		}
		if(filterParam.wallclockStartSec != '0')
		{
			filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
		}
		if(filterParam.wallclockEndDay != '0')
		{
			filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
		}
		if(filterParam.wallclockEndHr != '0')
		{
			filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
		}
		if(filterParam.wallclockEndMin != '0')
		{
			filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
		}
		if(filterParam.wallclockEndSec != '0')
		{
			filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
		}

		//Ends
		$.ajax({
			url:'/workload_table',
			type:'GET',
			data:{max:viewPerPage,
			offset:pageNumber,
			searchValue:searchValue,
			searchCategory:searchCat,
			sort_parameter:persistedSortingState.colname,
			sortState: persistedSortingState.sortState,
			control:clickedButton,
			lastOffset:lastPageNumber,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			jobId:searchParam.jobId,
			userName:searchParam.userName,
			resourceName:searchParam.resourceName,
			jobState:filterParam.jobState,
			priorityFrom:filterParam.priorityFrom,
			priorityTo:filterParam.priorityTo,
			rankFrom:filterParam.rankFrom,
			rankTo:filterParam.rankTo,
			dateTimeRange:filterParam.dateTimeRange,
			startDate:filterParam.startDate,
			endDate:filterParam.endDate,
			wallclockStartDay:filterParam.wallclockStartDay,
			wallclockStartHr:filterParam.wallclockStartHr,
			wallclockStartMin:filterParam.wallclockStartMin,
			wallclockStartSec:filterParam.wallclockStartSec,
			wallclockEndDay:filterParam.wallclockEndDay,
			wallclockEndHr:filterParam.wallclockEndHr,
			wallclockEndMin:filterParam.wallclockEndMin,
			wallclockEndSec:filterParam.wallclockEndSec
			//ends
			},
			success:function(result){
					//$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					
					switch(clickedButton){
							case 'goToFirst': $('#pageNumber').children('option:first').attr('selected',true);
											  break;
							case 'goToLast':  $('#pageNumber').children('option:last').attr('selected',true);
											  break;
							case 'prev': if(!($('#pageNumber').children('option').is(':first')))
												$('#pageNumber').children('option').eq(pageNumber-2).attr('selected',true);
											break;
							case 'next':if(!($('#pageNumber').children('option').is(':last')))
												$('#pageNumber').children('option').eq(pageNumber).attr('selected',true);
							default:break;				
						};
						$('#viewPerPage').val(viewPerPage);
					//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);	
						disablePaginationContent();
			}
		})
	}

	
	function refreshSearch(){
			
			//Changes done for IRIS - 434 starts
			var searchStr = $('#searchBoxDashboard').val();
			searchStr = searchStr.replace(/"/g,'\\"');
			searchStr = searchStr.replace(/\\/g,'\\');
			var searchValue = escape(searchStr);
			//Changes done for IRIS - 434 starts ends
			var searchCat = $('#searchCategory').val();
			var pageNumber = $('#pageNumber').val();
			var viewPerPage = $('#viewPerPage').val();
			$('#dataGrid').append('<div class="preloader"></div>').show();
			$('#workloadRefreshDashboard').hide();
			$.ajax({
				url:'/workload_table',
				type:'GET',
				data:{searchValue:searchValue,
				searchCategory:searchCat,
				max:viewPerPage},
				success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
					$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
					
					disablePaginationContent();
					$('#viewPerPage').val(viewPerPage);
					$('#workloadRefreshDashboard').show();
					}
			});	
	}
	

	
//Search section
		//function to perform narrow search according to the combination of parameters
		function search(caller,event){
			
		var keycode = event.keyCode? event.keyCode : event.charCode;
		var btnid = $(caller).attr('id');
		if(keycode == 13 || btnid == 'search_btn') {
		
			//Changes done for IRIS - 434 starts
			var searchStr = $('#searchBoxDashboard').val();
			searchStr = searchStr.replace(/"/g,'\\"');
			searchStr = searchStr.replace(/\\/g,'\\');
			var searchValue = searchStr;
			
			//Changes done for IRIS - 434 starts ends
			var searchCat = $('#searchCategory').val();
			var pageNumber = $('#pageNumber').val();
			var viewPerPage = $('#viewPerPage').val();
			filterParam.jobState = $('#jobState').val();
			filterParam.priorityFrom = $('#priorityFrom').val();
			filterParam.priorityTo = $('#priorityTo').val();
			filterParam.rankFrom = $('#rankFrom').val();
			filterParam.rankTo = $('#rankTo').val();
			filterParam.dateTimeRange = $('#dateTimeRange').val();
			filterParam.startDate = $('#txtStartDate').val();
			filterParam.endDate = $('#txtEndDate').val();
			filterParam.wallclockStartDay = $('#wallclockStart #day').val();
			filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
			filterParam.wallclockStartMin = $('#wallclockStart #min').val();
			filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
			filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
			filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
			filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
			filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
			$('#dataGrid').append('<div class="preloader"></div>').show();
			$.ajax({
				url:'/workload_table',
				type:'GET',
				data:{searchValue:searchValue,
				searchCategory:searchCat,
				max:viewPerPage,
				//offset:pageNumber,
				jobState:filterParam.jobState,
					priorityFrom:filterParam.priorityFrom,
					priorityTo:filterParam.priorityTo,
					rankFrom:filterParam.rankFrom,
					rankTo:filterParam.rankTo,
					dateTimeRange:filterParam.dateTimeRange,
					startDate:filterParam.startDate,
					endDate:filterParam.endDate,
					wallclockStartDay:filterParam.wallclockStartDay,
					wallclockStartHr:filterParam.wallclockStartHr,
					wallclockStartMin:filterParam.wallclockStartMin,
					wallclockStartSec:filterParam.wallclockStartSec,
					wallclockEndDay:filterParam.wallclockEndDay,
					wallclockEndHr:filterParam.wallclockEndHr,
					wallclockEndMin:filterParam.wallclockEndMin,
					wallclockEndSec:filterParam.wallclockEndSec},
				success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
					$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
					
					}
					
					
			});
			}
		}

// Filter Control Section

//global object to store values of jobid, username and resourcename
var searchParam ={
					jobId : 'null',
					userName:'null',
					resourceName:'null'
					}

					
function refreshContentForWorkloadFilters(caller){
var btnid = $(caller).attr('id');
	$('#statusMsg').hide();
	$('#myAlert').hide();
	
	//Changes for IRIS-345
	if(btnid == 'workloadRefresh'){
		doFiltering();
	}
	//Changes for IRIS-345 ends
}
					
//Refresh button implementation for Workload View- by Abhinavr on 4/23/2014
function refreshContent(caller){
	var btnid = $(caller).attr('id');
	$('#statusMsg').hide();
	$('#myAlert').hide();

	//Get back the narrow search to its default state - Abhinavr on 4/24/2014
	
		if($('#filterInputJobId').length > 0)
		{
			$('#opt1').show();
			$('#opt1').removeAttr('disabled');
			$('#opt1').removeClass("optiondisabled");
			//$('#filterInputJobId').hide();
			$('#filterInputJobId').remove();
			$('#destroyFilterJobId').remove();
			//$('#destroyFilterJobId').hide();
			searchParam.jobId = null;

		}
		if($('#filterInputSubmitterID').length > 0)
		{
			$('#opt2').show();
			$('#opt2').removeAttr('disabled');
			$('#opt2').removeClass("optiondisabled");
			$('#filterInputSubmitterID').remove();
			$('#destroyFilterSubmitterID').remove();
			//$('#filterInputUserName').hide();
			//$('#filterInputUserName').empty();
			//$('#destroyFilterUserName').hide();
			searchParam.userName = null;
		}
		//if($('#jobState').!=null)
		
	
		$('#jobState').val($('#jobState').find('#opt0').val());
		$('#searchCat').val($('#searchCat').find('#opt0').val());
		$('#searchBox').val($('#searchBox').find().val());
		$('#searchBoxDashboard').val($('#searchBoxDashboard').find('#opt0').val());
		
		$('#priorityFrom').val('0');
		$('#priorityTo').val('0');
		$('#rankFrom').val('0');
		$('#rankTo').val('0');
		
		$('#dateTimeRange').val($('#dateTimeRange').find('#opt0').val());
		
		if($('.start-date').is(':visible'))
		$('.start-date').hide();
		if($('.wall-clock').is(':visible'))
		$('.wall-clock').hide();
		
		$('#txtStartDate').val('');
		$('#txtEndDate').val('');
		
		$('#wallclockStart #day').val('0');
		$('#wallclockStart #hr').val('0');
		$('#wallclockStart #min').val('0');
		$('#wallclockStart #sec').val('0');
		$('#wallclockEnd #today').val('0');
		$('#wallclockEnd #tohr').val('0');
		$('#wallclockEnd #tomin').val('0');
		$('#wallclockEnd #tosec').val('0');
		var viewPerPage = $('#viewPerPage').val();
	//Get back the narrow search to its default state ends
	
	$('#workloadRefresh').hide();
	
	
	if(btnid == 'workloadRefresh'){
		$('#dataGrid').empty();
		$('#dataGrid').html('<div class="preloader"></div>');
		//$('#totalJobsCnt').text('');
		$.ajax({
			url:'/workload_table/',
			type:'GET',
			
			data:{max:viewPerPage, offset:1},
			success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					$('#totalJobsCnt').text('');
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
					$('#workloadRefresh').show();
				}
		});
		
		
	}

}

function checkMax(ctrl,min,max){
	var input=parseInt(document.getElementById(ctrl).value);
	if(input<min || input>max){
		alert("CPU Utilization:Value should be between 0 - 100");
		//alert(msg);
		clearInterval(intervalId);
		document.getElementById(ctrl).value = 100;
				return false;
		}
	return true;
}

function checkMaxMemory(ctrl,min,max){	
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<min || input>max){
			alert("Memory Utilization:Value should be between 0 - 100");
			//alert(msg);
			clearInterval(intervalId);
			document.getElementById(ctrl).value = 100;
					return false;
			}
		return true;
}  				
					
//method to object the characters and special notations - by Abhinavr on 4/23/2014

function checkObjection(caller, event){

	var btnid = $(caller).attr('id');
	var keycode = event.keyCode? event.keyCode : event.charCode;
	if((event.keyCode == 8) || (event.keyCode ==46) || (event.keyCode ==9))
	{
	
	}
	else if (!(keycode >= 48 && keycode <= 57)){
		event.preventDefault();
	}
}

	function validate_user_priority(ctrl,event)
{		
	var keycode = event.keyCode? event.keyCode : event.charCode;
	if((keycode == 8) || (keycode ==46) || (keycode ==9) || (keycode == 45))
	{
	
	}
	else if (!(keycode >= 48 && keycode <= 57)){
		event.preventDefault();
	}
}

	function chkData(ctrl) {
		
		  var x = document.getElementById(ctrl).value;
		
		  if(ctrl=="qos_txtBox")
		  {
		  	var reg=/^[A-Za-z0-9]+$/;
		  	msg= "Quality Of Service should have alphanumeric characters only";
		  }
		  else
		  {
		  	var reg=/^[\-]?[0-9]+$/;
		  	if(ctrl=="job_priority")
		  		msg="User Job Priority should have numeric characters only";
		  	else
		  		msg="System Priority should have numeric characters only";
		  }
		
		  if (!x.match(reg) && x!= "")
		  {
		  	alert(msg);
		  	return false;
		  }
		  	
		 return true;
		 }

		function validate_QOS_OnKeyPress(Id, obj, KeyEvent) {

			var input=document.getElementById(Id).value;
			
			evt = KeyEvent || window.event;
			
			var keycode = evt.which || evt.keyCode;

			if((keycode == 8) || (keycode ==46) || (keycode ==9))
			{
				
			}
			else if (!(keycode >= 48 && keycode <= 57) && !(keycode >= 65 && keycode <= 90) && !(keycode >= 97 && keycode <= 122) )
			{
					evt.preventDefault();
			}

		
		 }
	
	
	
function validate_user_priority_OnKeyUp(ctrl,max,min)
{
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<max || input>min){
			alert("Job User Priority:Value should be between -1024 to 0");			
			document.getElementById(ctrl).value = 0;
			return false;
		}
		return true;
}
function validate_user_priority_range(ctrl, caller, e)
{	
	var input=document.getElementById(ctrl).value;
	
	var btnid = $(caller).attr('id');

	evt = e || window.event;
	
	var keycode = evt.which || evt.keyCode;

	if((keycode == 8) || (keycode ==46) || (keycode ==9))
	{
		
	}
	else if(keycode == 45){
		if(input.indexOf('-') >= 0){
			evt.preventDefault();
		}
	}
	else if (!(keycode >= 48 && keycode <= 57)){
			evt.preventDefault();
	}
}



function padWithLeadingZeros(string) {	
    return new Array(5 - string.length).join("0") + string;
}

function unicodeCharEscape(charCode) {
    return "\\u" + padWithLeadingZeros(charCode.toString(16));
}

function unicodeEscape(string) {
    return string.split("").map(function (char)
    		     {
                     var charCode = char.charCodeAt(0);
                     return charCode > 127 ? unicodeCharEscape(charCode) : char;
                 })
                 .join("");
}

	
function addFilter(caller,event){
	var keycode = event.keyCode? event.keyCode : event.charCode;
	var btnid = $(caller).attr('id');
	
	
	
	
	if(keycode == 13 || btnid == 'searchBtn') {
		
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		var searchBoxVal = $('#searchCat').val()+':'+$.trim($('#searchBox').val());
		var searchCat = $('#searchCat').val();
		if(searchCat == "select")
		return;
		//$('#totalJobsCnt').text('');
		var searchVal = $.trim($('#searchBox').val());
		searchVal = searchVal.replace(/"/g,'\\"');
		searchVal = searchVal.replace(/\\/g,'\\');		
		//Changes done for IRIS - 434 starts ends
		
		
		
		

		if(searchVal == "")
		return;
		filterParam.jobState = $('#jobState').val();
		filterParam.priorityFrom = $('#priorityFrom').val();
		filterParam.priorityTo = $('#priorityTo').val();
		filterParam.rankFrom = $('#rankFrom').val();
		filterParam.rankTo = $('#rankTo').val();
		filterParam.dateTimeRange = $('#dateTimeRange').val();
		filterParam.startDate = $('#txtStartDate').val();
		filterParam.endDate = $('#txtEndDate').val();
		filterParam.wallclockStartDay = $('#wallclockStart #day').val();
		filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
		filterParam.wallclockStartMin = $('#wallclockStart #min').val();
		filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
		filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
		filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
		filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
		filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
		// Removing value tag
		var valuePan = '<span class="search-values" ><input type="text" id="filterInput" class="form-control"  disabled><span class="glyphicon glyphicon-remove" id="destroyFilter" onclick="removeSearchVal(this)"></span></span>'
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		$('.form-control').prop('readonly', true);
		$('.filter').prop('disabled', true);
		$('#searchCat').prop('disabled', true);
		$('#jobState').prop('disabled', true);
		$('#dateTimeRange').prop('disabled', true);
		$('#searchBtn').prop('readonly', true);
		
		switch(searchCat){
			case 'JobId':	searchParam.jobId = searchVal;
						
								$('#opt1').attr('disabled','disabled')
								$('#opt1').addClass("optiondisabled");
							$('#searchCat').val($('#searchCat').find('#opt0').val());
							break;
			case 'SubmitterID':	searchParam.userName = searchVal;
						
								$('#opt2').attr('disabled','disabled')
								$('#opt2').addClass("optiondisabled");
								$('#searchCat').val($('#searchCat').find('#opt0').val());
								break;
			case 'ResourceName':searchParam.resourceName = searchVal;
								break;
		};
		$('#searchValues').append(valuePan);
		// Adding code for setting value for filterInput box.
		$('#filterInput').val(searchBoxVal);
		
		$('#filterInput').prop("id","filterInput" + searchBoxVal.split(':')[0]);
		$('#destroyFilter').prop("id","destroyFilter" + searchBoxVal.split(':')[0]);
		$('#searchBox').val('');
		
			$.ajax({
						url:'/workload_table',
						type:'GET',
						data:{
								jobId:searchParam.jobId,
								userName:searchParam.userName,
								resourceName:searchParam.resourceName,
								max:viewPerPage,
								//offset:pageNumber,
								jobState:filterParam.jobState,
								priorityFrom:filterParam.priorityFrom,
								priorityTo:filterParam.priorityTo,
								rankFrom:filterParam.rankFrom,
								rankTo:filterParam.rankTo,
								dateTimeRange:filterParam.dateTimeRange,
								startDate:filterParam.startDate,
								endDate:filterParam.endDate,
								wallclockStartDay:filterParam.wallclockStartDay,
								wallclockStartHr:filterParam.wallclockStartHr,
								wallclockStartMin:filterParam.wallclockStartMin,
								wallclockStartSec:filterParam.wallclockStartSec,
								wallclockEndDay:filterParam.wallclockEndDay,
								wallclockEndHr:filterParam.wallclockEndHr,
								wallclockEndMin:filterParam.wallclockEndMin,
								wallclockEndSec:filterParam.wallclockEndSec
							},
							
						success:function(result){
							$('#dataGrid').children('.preloader').hide();
							$('#dataGrid').html(result);
							$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
							//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
							$('#viewPerPage').val(viewPerPage)
							$('#totalJobsCnt').text($('#hiddenTotalCnt').val() + ' Jobs');
							disablePaginationContent();
		$('.form-control').removeAttr('readonly');
				$('.filter').prop('disabled', false);
				$('#searchCat').prop('disabled', false);
				$('#jobState').prop('disabled', false);
				$('#dateTimeRange').prop('disabled', false);
				$('#searchBtn').removeAttr('readonly');
								},
						error:function(){
							
						}
					});
	}
}		
//remove search parameter
function removeSearchVal(caller){
	var searchValue = $(caller).prev('input[type="text"]').val();
	var searchString = searchValue.split(':');
	switch(searchString[0]){
			case 'JobId':	searchParam.jobId = 'null';
							//$('#opt1').show();
							$('#opt1').removeAttr('disabled');
							$('#opt1').removeClass("optiondisabled");
							
							break;
			case 'SubmitterID':	searchParam.userName = 'null';
								//$('#opt2').show();
								$('#opt2').removeAttr('disabled');
								$('#opt2').removeClass("optiondisabled");
								break;
			case 'ResourceName':searchParam.resourceName = 'null';
								break;
		};
	$(caller).parent().remove();
	doFiltering();
}
//select duration according to start date or wallclock
function selectRange(caller){
	switch($(caller).val()){
		case 'startdate':	$('#startDate').datetimepicker({ language: 'pt-BR'	});
							$('#endDate').datetimepicker({ language: 'pt-BR' });
							if($('.wall-clock').is(':visible'))
								$('.wall-clock').hide();
							$('.start-date').show();
							$('#wallclockStart #day').val('0');
							$('#wallclockStart #hr').val('0');
							$('#wallclockStart #min').val('0');
							$('#wallclockStart #sec').val('0');
							$('#wallclockEnd #today').val('0');
							$('#wallclockEnd #tohr').val('0');
							$('#wallclockEnd #tomin').val('0');
							$('#wallclockEnd #tosec').val('0');
							break;
		case 'wallclock':	if($('.start-date').is(':visible'))
								$('.start-date').hide();
							$('.wall-clock').show();	
							$('#txtStartDate').val('');
							$('#txtEndDate').val('');							
							break;
							
		default:	if($('.start-date').is(':visible'))
						$('.start-date').hide();
						if($('.wall-clock').is(':visible'))
						$('.wall-clock').hide();
						
						$('#txtStartDate').val('');
						$('#txtEndDate').val('');
						
						$('#wallclockStart #day').val('0');
						$('#wallclockStart #hr').val('0');
						$('#wallclockStart #min').val('0');
						$('#wallclockStart #sec').val('0');
						$('#wallclockEnd #today').val('0');
						$('#wallclockEnd #tohr').val('0');
						$('#wallclockEnd #tomin').val('0');
						$('#wallclockEnd #tosec').val('0');
							break;
	}
}

//Global Object to store filter values
filterParam = {
				'jobState':'null',
				'priorityFrom':0,
				'priorityTo':0,
				'rankFrom':0,
				'rankTo':0,
				'dateTimeRange':'null',
				'startDate':'null',
				'endDate':'null',
				'wallclockStartDay':0,
				'wallclockStartHr':0,
				'wallclockStartMin':0,
				'wallclockStartSec':0,
				'wallclockEndDay':0,
				'wallclockEndHr':0,
				'wallclockEndMin':0,
				'wallclockEndSec':0
			}


function disableWorkloadContentOnPageLoad(){

        $('.form-control').prop('readonly', 'true');
        $('.filter').prop('disabled', true);
        $('#searchCat').prop('disabled', true);
        $('#jobState').prop('disabled', true);
        $('#dateTimeRange').prop('disabled', true);
        $('#searchBtn').prop('readonly', 'true');
        $('#workloadRefresh').prop('readonly', 'true');
}

function enableWorkloadContentAfterPageLoad(){

        $('.form-control').removeAttr('readonly');
        $('.filter').prop('disabled', false);
        $('#searchCat').prop('disabled', false);
        $('#jobState').prop('disabled', false);
        $('#dateTimeRange').prop('disabled', false);
        $('#searchBtn').removeAttr('readonly');
        $('#workloadRefresh').prop('disable',false);
}




//Do filtering
function doFiltering(){
	
	
	if(checkFilterData()){
	$('#dataGrid').append('<div class="preloader"></div>').show();
//$('#totalJobsCnt').hide('');
	
	//disable
	$('.form-control').prop('readonly', 'true');
	$('.filter').prop('disabled', true);
	$('#searchCat').prop('disabled', true);
	$('#jobState').prop('disabled', true);
	$('#dateTimeRange').prop('disabled', true);
	$('#searchBtn').prop('readonly', 'true');
	
	
	
	
	var pageNumber = $('#pageNumber').val();
	var viewPerPage = $('#viewPerPage').val();
	
	if(!$('#filterInputJobId').is(':visible'))
	searchParam.jobId = null;
	
	//if(!$('#filterInputUserName').is(':visible'))
	if(!$('#filterInputSubmitterID').is(':visible'))
	searchParam.submitterID = null;
	
	filterParam.jobState = $('#jobState').val();
	filterParam.priorityFrom = $('#priorityFrom').val();
	if (filterParam.priorityFrom == "") {
		$('#priorityFrom').val(0);
		filterParam.priorityFrom = 0;
	}
	filterParam.priorityTo = $('#priorityTo').val();
	if (filterParam.priorityTo == "") {
		$('#priorityTo').val(0);
		filterParam.priorityTo = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.rankFrom = $('#rankFrom').val();
	if (filterParam.rankFrom == "") {
		$('#rankFrom').val(0);
		filterParam.rankFrom = 0;
	}
	filterParam.rankTo = $('#rankTo').val();
	if (filterParam.rankTo == "") {
		$('#rankTo').val(0);
		filterParam.rankTo = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();	
			return false;
		}
	}
	filterParam.dateTimeRange = $('#dateTimeRange').val();
	filterParam.startDate = $('#txtStartDate').val();
	filterParam.endDate = $('#txtEndDate').val();
	filterParam.wallclockStartDay = $('#wallclockStart #day').val();
	if (filterParam.wallclockStartDay == "") {
		$('#wallclockStart #day').val(0);
		filterParam.wallclockStartDay = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockStartHr = $('#wallclockStart #hr').val();
	if (filterParam.wallclockStartHr == "") {
		$('#wallclockStart #hr').val(0);
		filterParam.wallclockStartHr = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockStartMin = $('#wallclockStart #min').val();
	if (filterParam.wallclockStartMin == "") {
		$('#wallclockStart #min').val(0);
		filterParam.wallclockStartMin = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockStartSec = $('#wallclockStart #sec').val();
	if (filterParam.wallclockStartSec == "") {
		$('#wallclockStart #sec').val(0);
		filterParam.wallclockStartSec = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockEndDay = $('#wallclockEnd #today').val();
	if (filterParam.wallclockEndDay == "") {
		$('#wallclockEnd #today').val(0);
		filterParam.wallclockEndDay = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockEndHr = $('#wallclockEnd #tohr').val();
	if (filterParam.wallclockEndHr == "") {
		$('#wallclockEnd #tohr').val(0);
		filterParam.wallclockEndHr = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockEndMin = $('#wallclockEnd #tomin').val();
	if (filterParam.wallclockEndMin == "") {
		$('#wallclockEnd #tomin').val(0);
		filterParam.wallclockEndMin = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterParam.wallclockEndSec = $('#wallclockEnd #tosec').val();
	if (filterParam.wallclockEndSec == "") {
		$('#wallclockEnd #tosec').val(0);
		filterParam.wallclockEndSec = 0;
		if (!checkFilterData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	$('#workloadRefresh').hide();
	$.ajax({
			url:'/workload_table',
			type:'GET',
			data:{
					jobId:searchParam.jobId,
					userName:searchParam.userName,
					jobState:filterParam.jobState,
					priorityFrom:filterParam.priorityFrom,
					priorityTo:filterParam.priorityTo,
					rankFrom:filterParam.rankFrom,
					rankTo:filterParam.rankTo,
					dateTimeRange:filterParam.dateTimeRange,
					startDate:filterParam.startDate,
					endDate:filterParam.endDate,
					wallclockStartDay:filterParam.wallclockStartDay,
					wallclockStartHr:filterParam.wallclockStartHr,
					wallclockStartMin:filterParam.wallclockStartMin,
					wallclockStartSec:filterParam.wallclockStartSec,
					wallclockEndDay:filterParam.wallclockEndDay,
					wallclockEndHr:filterParam.wallclockEndHr,
					wallclockEndMin:filterParam.wallclockEndMin,
					wallclockEndSec:filterParam.wallclockEndSec,
					max:viewPerPage,
					//offset:pageNumber
				},
				
			success:function(result){
				$('#dataGrid .preloader').hide();
				$('#dataGrid').html(result);
				$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
				$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
				$('#totalJobsCnt').text($('#hiddenTotalCnt').val() + ' Jobs');
				$('#viewPerPage').val(viewPerPage);
				disablePaginationContent();
				$('.form-control').removeAttr('readonly');
				$('.filter').prop('disabled', false);
				$('#searchCat').prop('disabled', false);
				$('#jobState').prop('disabled', false);
				$('#dateTimeRange').prop('disabled', false);
				$('#searchBtn').removeAttr('readonly');
				$('#workloadRefresh').show();
				}
				
			
			});
		} else {
		}
	
}

///////ABHINAVR RULES//////////////

//Resource List Section starts

//global object to store values of jobid, username and resourcename
var searchResourceListParam ={
					resourceId : 'null',
					resourceClass:'null',
					features:'null'
					}

					
					//Global Object to store filter values
filterResourceListParam = {
				'resourceState':'null',
				'processorFrom':0,
				'processorTo':0,
				'jobsFrom':0,
				'jobsTo':0,
				'cpuUtilizationFrom':0,
				'cpuUtilizationTo':0,
				'memoryUtilizationFrom':0,
				'memoryUtilizationTo':0
			}
			
	function disableResourcelistContentOnPageLoad (){
		$('#searchCat').prop('disabled', true);
		$('.form-control').prop('readonly', 'true');
		$('#resourceState').prop('disabled', true);
		$('.filter').prop('disabled', true);	
	}

	function enableResourcelistContentOnPageLoad(){
		$('#searchCat').prop('disabled', false);
		$('.form-control').removeAttr('readonly');
		$('#resourceState').prop('disabled', false);
		$('.filter').prop('disabled', false);
	}

//Do filtering on Filter button click
function doResourceListFiltering(){

	$('#searchCat').prop('disabled', true);
	$('.form-control').prop('readonly', 'true');
	$('#resourceState').prop('disabled', true);
	$('.filter').prop('disabled', true);

	$('#totalResourcesCnt').text('');
	if(checkData()){
	$('#dataGrid').append('<div class="preloader"></div>').show();
	var pageNumber = $('#pageNumber').val();
	var viewPerPage = $('#viewPerPage').val();
	
	if(!$('#filterInputResourceID').is(':visible'))
	searchResourceListParam.resourceId = null;
			
	if(!$('#filterInputClass').is(':visible'))
	searchResourceListParam.resourceClass = null;
			
	if(!$('#filterInputFeatures').is(':visible'))
	searchResourceListParam.features = null;

	filterResourceListParam.resourceState = $('#resourceState').val();
	filterResourceListParam.processorFrom = $('#procsFrom').val();
	if (filterResourceListParam.processorFrom == "") {
		$('#procsFrom').val(0);
		filterResourceListParam.processorFrom = 0;
	}
	filterResourceListParam.processorTo = $('#procsTo').val();
	if (filterResourceListParam.processorTo == "") {
		$('#procsTo').val(0);
		filterResourceListParam.processorTo = 0;
			if (!checkData()){
				$('#dataGrid .preloader').hide();
				return false;
		}
	}
	filterResourceListParam.jobsFrom = $('#jobsFrom').val();
	if (filterResourceListParam.jobsFrom == "") {
		$('#jobsFrom').val(0);
		filterResourceListParam.jobsFrom = 0;
	}
	filterResourceListParam.jobsTo = $('#jobsTo').val();
	if (filterResourceListParam.jobsTo == "") {
		$('#jobsTo').val(0);
		filterResourceListParam.jobsTo = 0;
		if (!checkData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterResourceListParam.cpuUtilizationFrom = $('#proc_utilFrom').val();
	if (filterResourceListParam.cpuUtilizationFrom == "") {
		$('#proc_utilFrom').val(0);
		filterResourceListParam.cpuUtilizationFrom = 0;
	}
	filterResourceListParam.cpuUtilizationTo = $('#proc_utilTo').val();
	if (filterResourceListParam.cpuUtilizationTo == "") {
		$('#proc_utilTo').val(0);
		filterResourceListParam.cpuUtilizationTo = 0;
		if (!checkData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	filterResourceListParam.memoryUtilizationFrom = $('#memory_utilFrom').val();
	if (filterResourceListParam.memoryUtilizationFrom == "") {
		$('#memory_utilFrom').val(0);
		filterResourceListParam.memoryUtilizationFrom = 0;
	}
	filterResourceListParam.memoryUtilizationTo = $('#memory_utilTo').val();
	if (filterResourceListParam.memoryUtilizationTo == "") {
		$('#memory_utilTo').val(0);
		filterResourceListParam.memoryUtilizationTo = 0;
		if (!checkData()){
			$('#dataGrid .preloader').hide();
			return false;
		}
	}
	$('#resourceListRefresh').hide();
	
	$.ajax({
			url:'/node_table',
			type:'GET',
			data:{
					name:searchResourceListParam.resourceId,
					classes:searchResourceListParam.resourceClass,
					features:searchResourceListParam.features,
					state:filterResourceListParam.resourceState,
					procsFrom:filterResourceListParam.processorFrom,
					procsTo:filterResourceListParam.processorTo,
					jobsFrom:filterResourceListParam.jobsFrom,
					jobsTo:filterResourceListParam.jobsTo,
					proc_utilFrom:filterResourceListParam.cpuUtilizationFrom,
					proc_utilTo:filterResourceListParam.cpuUtilizationTo,
					memory_utilFrom:filterResourceListParam.memoryUtilizationFrom,
					memory_utilTo:filterResourceListParam.memoryUtilizationTo,
					max:viewPerPage,
					//offset:pageNumber
				},
				
			success:function(result){
				$('#dataGrid .preloader').hide();
				$('#dataGrid').html(result);
				$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
				//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
				$('#viewPerPage').val(viewPerPage);
				$('#totalResourcesCnt').text($('#hiddenTotalCnt').val() + ' Jobs');
				disablePaginationContent();

				$('#searchCat').prop('disabled', false);
				$('.form-control').removeAttr('readonly');
				$('#resourceState').prop('disabled', false);
				$('.filter').prop('disabled', false);
				$('#resourceListRefresh').show();
				}
				
			
			});
		
		} else {
		//$('#searchCat').prop('disabled', true);
		//$('.form-control').prop('readonly', 'true');
		//$('#resourceState').prop('disabled', true);
		//$('.filter').prop('disabled', true);
		$('#searchCat').prop('disabled', false);
				$('.form-control').removeAttr('readonly');
				$('#resourceState').prop('disabled', false);
				$('.filter').prop('disabled', false);

		}
	
}



//Do filtering on keyword button click or key press
function addResourceListFilter(caller,event){
	var keycode = event.keyCode? event.keyCode : event.charCode;
	var btnid = $(caller).attr('id');
	$('#totalResourcesCnt').text('');
	if(keycode == 13 || btnid == 'searchBtn') {
		
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		

		var searchBoxVal = $('#searchCat').val()+':'+$.trim($('#searchBox').val());
		/*var searchBoxVal = $('#searchCat').val()+':'+$('#searchBox').val();*/
		var searchCat = $('#searchCat').val();
		
		if(searchCat == "select")
		return;
		$('#totalResourcesCnt').text('');
		
		if(searchCat === 'NodeID'){
		
			searchCat = 'ResourceID';
		}
		
		//Changes done for IRIS - 434 starts
		var searchVal = $('#searchBox').val();
		searchVal = searchVal.replace(/"/g,'\\"');
		searchVal = searchVal.replace(/\\/g,'\\');		
		//Changes done for IRIS - 434 starts ends
		

		if(searchVal == "")
		return;
		
		filterResourceListParam.resourceState = $('#resourceState').val();
		filterResourceListParam.processorFrom = $('#procsFrom').val();
		filterResourceListParam.processorTo = $('#procsTo').val();
		filterResourceListParam.jobsFrom = $('#jobsFrom').val();
		filterResourceListParam.jobsTo = $('#jobsTo').val();
		filterResourceListParam.cpuUtilizationFrom = $('#proc_utilFrom').val();
		filterResourceListParam.cpuUtilizationTo = $('#proc_utilTo').val();
		filterResourceListParam.memoryUtilizationFrom = $('#memory_utilFrom').val();
		filterResourceListParam.memoryUtilizationTo = $('#memory_utilTo').val();

		
		
		var valuePan = '<span class="search-values" ><input type="text" id="filterInput" class="form-control" disabled><span class="glyphicon glyphicon-remove" id="destroyFilter" onclick="removeSearchValRes(this)"></span></span>'
		$('#dataGrid').append('<div class="preloader"></div>').show();
				
				$('#resourceState').prop('disabled', true);
				$('.form-control').prop('readonly', true);
				$('.filter').prop('disabled', true);
				
				$('#searchCat').prop('disabled', true);
				
		switch(searchCat){
			case 'ResourceID':	searchResourceListParam.resourceId = searchVal;
								$('#opt1').attr('disabled','disabled')
								$('#opt1').addClass("optiondisabled");
							$('#searchCat').val($('#searchCat').find('#opt0').val());
							break;
			case 'Class':	searchResourceListParam.resourceClass = searchVal;
								$('#opt2').attr('disabled','disabled')
								$('#opt2').addClass("optiondisabled");
								$('#searchCat').val($('#searchCat').find('#opt0').val());
								break;
			case 'Features':searchResourceListParam.features = searchVal;
								$('#opt3').attr('disabled','disabled')
								$('#opt3').addClass("optiondisabled");
								//$('#opt3').hide();
								$('#searchCat').val($('#searchCat').find('#opt0').val());
								break;
		};
		$('#searchValues').append(valuePan);
		var splitVal = searchBoxVal.split(':')[0]
		
		if(splitVal === 'NodeID'){
			splitVal = 'ResourceID';
		}
		// Adding code for setting value for filterInput box.
		$('#filterInput').val(searchBoxVal);
		
		$('#filterInput').prop("id","filterInput" + splitVal);
		$('#destroyFilter').prop("id","destroyFilter" + splitVal);
		$('#searchBox').val('');

			$.ajax({
						url:'/node_table',
						type:'GET',
						data:{
								name:searchResourceListParam.resourceId,
								classes:searchResourceListParam.resourceClass,
								features:searchResourceListParam.features,
								state:filterResourceListParam.resourceState,
								procsFrom:filterResourceListParam.processorFrom,
								procsTo:filterResourceListParam.processorTo,
								jobsFrom:filterResourceListParam.jobsFrom,
								jobsTo:filterResourceListParam.jobsTo,
								proc_utilFrom:filterResourceListParam.cpuUtilizationFrom,
								proc_utilTo:filterResourceListParam.cpuUtilizationTo,
								memory_utilFrom:filterResourceListParam.memoryUtilizationFrom,
								memory_utilTo:filterResourceListParam.memoryUtilizationTo,
								max:viewPerPage,
								//offset:pageNumber
							},
							
						success:function(result){
							$('#dataGrid').children('.preloader').hide();
							$('#dataGrid').html(result);
							$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
							//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
							$('#viewPerPage').val(viewPerPage);
							$('#totalResourcesCnt').text($('#hiddenTotalCnt').val() + ' Jobs');							
							disablePaginationContent();
							$('#searchCat').prop('disabled', false);
							$('.form-control').removeAttr('readonly');
							$('#resourceState').prop('disabled', false);
							$('.filter').prop('disabled', false);
							
								},
						error:function(){
							$('#dataGrid').html('No Records Found');
							$('#dataGrid').find('.preloader').hide();
						}
					});
	}
}	



function removeSearchValRes(caller){
	var searchValue = $(caller).prev('input[type="text"]').val();
	var searchString = searchValue.split(':');
	var switchVal = searchString[0];
	if(switchVal === 'NodeID'){
		switchVal = 'ResourceID';
	}
	switch(switchVal){
			case 'ResourceID':	searchParam.ResourceID = 'null';
							
							$('#opt1').removeAttr('disabled');
							$('#opt1').removeClass("optiondisabled");
							break;
			case 'Class':	searchParam.Class = 'null';
							
							$('#opt2').removeAttr('disabled');
							$('#opt2').removeClass("optiondisabled");
							break;
			case 'Features':searchParam.Features = 'null';
							
							$('#opt3').removeAttr('disabled');
							$('#opt3').removeClass("optiondisabled");
							break;
		};
	$(caller).parent().remove();
	
	//Add code for fix IRIS-509- Abhinavr - 8/21/2014
		doResourceListFiltering();
	//Add code for IRIS-509 ends
	
	if(!$('#filterInputResourceID').is(':visible'))
	searchResourceListParam.resourceId = ""
	
	if(!$('#filterInputClass').is(':visible'))
	searchResourceListParam.resourceClass = ""
	
	if(!$('#filterInputFeatures').is(':visible'))
	searchResourceListParam.features = ""

	

}
					
function refreshResourceListContent(caller){
	var btnid = $(caller).attr('id');

		$('#myAlert').hide();
		
		$('#totalJobsCnt').text('');
	
		if(btnid == 'resourceListRefresh'){
			
			doResourceListFiltering();
		}
}

//function to call pagination on controls' click event
	function onControlClickRes(caller){
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		var clickedButton = $(caller).attr('id');
		var lastPageNumber= $('#pageNumber').find('option:last').val();
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		if(!$('#filterInputResourceID').is(':visible'))
		searchResourceListParam.resourceId = null;
		
		if(!$('#filterInputClass').is(':visible'))
		searchResourceListParam.resourceClass = null;
		
		if(!$('#filterInputFeatures').is(':visible'))
		searchResourceListParam.features = null;
		//Created for sending data of narrow search- abhinavr - 4/29/14

		if(filterResourceListParam.resourceState != 'null')
		{
			filterResourceListParam.resourceState = $('#resourceState').val();
		}
		if(filterResourceListParam.processorFrom != '0')
		{
			filterResourceListParam.processorFrom = $('#procsFrom').val();
		}
		if(filterResourceListParam.processorTo != '0')
		{
			filterResourceListParam.processorTo = $('#procsTo').val();
		}
		if(filterResourceListParam.jobsFrom != '0')
		{
			filterResourceListParam.jobsFrom = $('#jobsFrom').val();
		}
		if(filterResourceListParam.jobsTo != '0')
		{
			filterResourceListParam.jobsTo = $('#jobsTo').val();
		}
		if(filterResourceListParam.cpuUtilizationFrom != '0')
		{
			filterResourceListParam.cpuUtilizationFrom = $('#proc_utilFrom').val();
		}
		if(filterResourceListParam.cpuUtilizationTo != '0')
		{
			filterResourceListParam.cpuUtilizationTo = $('#proc_utilTo').val();
		}
		if(filterResourceListParam.memoryUtilizationFrom != '0')
		{
			filterResourceListParam.memoryUtilizationFrom = $('#memory_utilFrom').val();
		}
		if(filterResourceListParam.memoryUtilizationTo != '0')
		{
			filterResourceListParam.memoryUtilizationTo = $('#memory_utilTo').val();
		}
		//Ends

		$.ajax({
			url:'/node_table/',
			type:'GET',
			data:{max:viewPerPage,
			offset:pageNumber,
			sort_parameter:persistedResSortingState.colname,
			sortState:persistedResSortingState.sortState,
			control:clickedButton,
			lastOffset:lastPageNumber,
			
			name:searchResourceListParam.resourceId,
			classes:searchResourceListParam.resourceClass,
			features:searchResourceListParam.features,
			state:filterResourceListParam.resourceState,
			procsFrom:filterResourceListParam.processorFrom,
			procsTo:filterResourceListParam.processorTo,
			jobsFrom:filterResourceListParam.jobsFrom,
			jobsTo:filterResourceListParam.jobsTo,
			proc_utilFrom:filterResourceListParam.cpuUtilizationFrom,
			proc_utilTo:filterResourceListParam.cpuUtilizationTo,
			memory_utilFrom:filterResourceListParam.memoryUtilizationFrom,
			memory_utilTo:filterResourceListParam.memoryUtilizationTo,

		
			},
			success:function(result){
					
					$('#dataGrid').html(result);
					
					switch(clickedButton){
							case 'goToFirst': $('#pageNumber').children('option:first').attr('selected',true);
											  break;
							case 'goToLast':  $('#pageNumber').children('option:last').attr('selected',true);
											  break;
							case 'prev': if(!($('#pageNumber').children('option').is(':first')))
												$('#pageNumber').children('option').eq(pageNumber-2).attr('selected',true);
											break;
							case 'next':if(!($('#pageNumber').children('option').is(':last')))
												$('#pageNumber').children('option').eq(pageNumber).attr('selected',true);
							default:break;				
						};
						$('#viewPerPage').val(viewPerPage);
					
						disablePaginationContent();
			}
		})
	}
//Datagrid for Resource List Pagination Section
	//function to call pagination on changing the values from page number or records per page drop down
	function onPageChangePerPageRes(){
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		
		disablePaginationContent();
		
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		if(!$('#filterInputResourceID').is(':visible'))
		searchResourceListParam.resourceId = null;
		
		if(!$('#filterInputClass').is(':visible'))
		searchResourceListParam.resourceClass = null;
		
		if(!$('#filterInputFeatures').is(':visible'))
		searchResourceListParam.features = null;
		
		//Created for sending data of narrow search- abhinavr - 4/29/14

		if(filterResourceListParam.resourceState != 'null')
		{
			filterResourceListParam.resourceState = $('#resourceState').val();
		}
		//filterResourceListParam.resourceState = $('#resourceState').val();
		if(filterResourceListParam.processorFrom != '0')
		{
			filterResourceListParam.processorFrom = $('#procsFrom').val();
		}
		if(filterResourceListParam.processorTo != '0')
		{
			filterResourceListParam.processorTo = $('#procsTo').val();
		}
		if(filterResourceListParam.jobsFrom != '0')
		{
			filterResourceListParam.jobsFrom = $('#jobsFrom').val();
		}
		if(filterResourceListParam.jobsTo != '0')
		{
			filterResourceListParam.jobsTo = $('#jobsTo').val();
		}
		if(filterResourceListParam.cpuUtilizationFrom != '0')
		{
			filterResourceListParam.cpuUtilizationFrom = $('#proc_utilFrom').val();
		}
		if(filterResourceListParam.cpuUtilizationTo != '0')
		{
			filterResourceListParam.cpuUtilizationTo = $('#proc_utilTo').val();
		}
		if(filterResourceListParam.memoryUtilizationFrom != '0')
		{
			filterResourceListParam.memoryUtilizationFrom = $('#memory_utilFrom').val();
		}
		if(filterResourceListParam.memoryUtilizationTo != '0')
		{
			filterResourceListParam.memoryUtilizationTo = $('#memory_utilTo').val();
		}

		//Ends
		
		$.ajax({
			url:'/node_table/',
			type:'GET',
			data:{max:viewPerPage, offset:pageNumber,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			sort_parameter:persistedResSortingState.colname,
			sortState:persistedResSortingState.sortState,
			name:searchResourceListParam.resourceId,
			classes:searchResourceListParam.resourceClass,
			features:searchResourceListParam.features,
			state:filterResourceListParam.resourceState,
			procsFrom:filterResourceListParam.processorFrom,
			procsTo:filterResourceListParam.processorTo,
			jobsFrom:filterResourceListParam.jobsFrom,
			jobsTo:filterResourceListParam.jobsTo,
			proc_utilFrom:filterResourceListParam.cpuUtilizationFrom,
			proc_utilTo:filterResourceListParam.cpuUtilizationTo,
			memory_utilFrom:filterResourceListParam.memoryUtilizationFrom,
			memory_utilTo:filterResourceListParam.memoryUtilizationTo,
			//ends
			},
			success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
					
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
			}
		})
	}
	
//Datagrid for Resource List Pagination Section
	//function to call pagination on changing the values from page number or records per page drop down
	function onPageChangeRes(){
		var viewPerPage = $('#viewPerPage').val();
		
		disablePaginationContent();
		
		$('#dataGrid').append('<div class="preloader"></div>').show();
		
		if(!$('#filterInputResourceID').is(':visible'))
		searchResourceListParam.resourceId = null;
		
		if(!$('#filterInputClass').is(':visible'))
		searchResourceListParam.resourceClass = null;
		
		if(!$('#filterInputFeatures').is(':visible'))
		searchResourceListParam.features = null;
		
		//Created for sending data of narrow search- abhinavr - 4/29/14
		if(filterResourceListParam.resourceState != 'null')
		{
			filterResourceListParam.resourceState = $('#resourceState').val();
		}
		//filterResourceListParam.resourceState = $('#resourceState').val();
		if(filterResourceListParam.processorFrom != '0')
		{
			filterResourceListParam.processorFrom = $('#procsFrom').val();
		}
		if(filterResourceListParam.processorTo != '0')
		{
			filterResourceListParam.processorTo = $('#procsTo').val();
		}
		if(filterResourceListParam.jobsFrom != '0')
		{
			filterResourceListParam.jobsFrom = $('#jobsFrom').val();
		}
		if(filterResourceListParam.jobsTo != '0')
		{
			filterResourceListParam.jobsTo = $('#jobsTo').val();
		}
		if(filterResourceListParam.cpuUtilizationFrom != '0')
		{
			filterResourceListParam.cpuUtilizationFrom = $('#proc_utilFrom').val();
		}
		if(filterResourceListParam.cpuUtilizationTo != '0')
		{
			filterResourceListParam.cpuUtilizationTo = $('#proc_utilTo').val();
		}
		if(filterResourceListParam.memoryUtilizationFrom != '0')
		{
			filterResourceListParam.memoryUtilizationFrom = $('#memory_utilFrom').val();
		}
		if(filterResourceListParam.memoryUtilizationTo != '0')
		{
			filterResourceListParam.memoryUtilizationTo = $('#memory_utilTo').val();
		}
		//Ends
		
		$.ajax({
			url:'/node_table/',
			type:'GET',
			data:{max:viewPerPage, offset:1,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			sort_parameter:persistedResSortingState.colname,
			sortState:persistedResSortingState.sortState,
			name:searchResourceListParam.resourceId,
			classes:searchResourceListParam.resourceClass,
			features:searchResourceListParam.features,
			state:filterResourceListParam.resourceState,
			procsFrom:filterResourceListParam.processorFrom,
			procsTo:filterResourceListParam.processorTo,
			jobsFrom:filterResourceListParam.jobsFrom,
			jobsTo:filterResourceListParam.jobsTo,
			proc_utilFrom:filterResourceListParam.cpuUtilizationFrom,
			proc_utilTo:filterResourceListParam.cpuUtilizationTo,
			memory_utilFrom:filterResourceListParam.memoryUtilizationFrom,
			memory_utilTo:filterResourceListParam.memoryUtilizationTo,
			//ends
			},
			success:function(result){
					$('#dataGrid .preloader').hide();
					$('#dataGrid').html(result);
					
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
			}
		})
	}
	
	


// Resource List Array representing the sorting states of grid	
var sortingStateRes = {
					'resourceid':-1,
					'resourcestatus':-1,
					'procs':-1,
					'jobs':-1,
					'cpuutilization':-1,
					'memoryutilization':-1
					};
var persistedResSortingState = {
					'colname':null,
					'sortState': -1
};				
//Resource List function to get sorting target and perform sort
function onSortRes(colName){
	var colId = $(colName).attr('id');

	switch(colId){
		case 'name': sortingStateRes.resourceid = -(sortingStateRes.resourceid);
					  doSortRes(colId,sortingStateRes.resourceid);
					  persistedResSortingState.colname = colId;
					  persistedResSortingState.sortState = sortingStateRes.resourceid
					  break;
		case 'state': sortingStateRes.resourcestatus = -(sortingStateRes.resourcestatus);
					  doSortRes(colId,sortingStateRes.resourcestatus);
					  persistedResSortingState.colname = colId;
					  persistedResSortingState.sortState = sortingStateRes.resourcestatus
					  break;
		case 'processors': sortingStateRes.procs = -(sortingStateRes.procs);
					  doSortRes(colId,sortingStateRes.procs);
					  persistedResSortingState.colname = colId;
					  persistedResSortingState.sortState = sortingStateRes.procs
					  break;
		case 'jobs': sortingStateRes.jobs = -(sortingStateRes.jobs);
					  doSortRes(colId,sortingStateRes.jobs);
					  persistedResSortingState.colname = colId;
					  persistedResSortingState.sortState = sortingStateRes.jobs
					  break;
		case 'processor_utilization_percentage': sortingStateRes.cpuutilization = -(sortingStateRes.cpuutilization);
					  doSortRes(colId,sortingStateRes.cpuutilization);
					  persistedResSortingState.colname = colId;
					  persistedResSortingState.sortState = sortingStateRes.cpuutilization
					  break;
		case 'memory_utilization_percentage': sortingStateRes.memoryutilization = -(sortingStateRes.memoryutilization);
					  doSortRes(colId,sortingStateRes.memoryutilization);
					  persistedResSortingState.colname = colId;
					  persistedResSortingState.sortState = sortingStateRes.memoryutilization
					  break;			
		default:break;
	};
					
}

//Resource List function to do sorting on column with its ascending state
function doSortRes(colId,sortState){
	
	var pageNumber = $('#pageNumber').val();
	var viewPerPage = $('#viewPerPage').val();
	$('#dataGrid').append('<div class="preloader"></div>').show();
	
	//Created for sending data of narrow search- abhinavr - 4/29/14
		if(filterResourceListParam.resourceState != 'null')
		{
			filterResourceListParam.resourceState = $('#resourceState').val();
		}
		//filterResourceListParam.resourceState = $('#resourceState').val();
		if(filterResourceListParam.processorFrom != '0')
		{
			filterResourceListParam.processorFrom = $('#procsFrom').val();
		}
		if(filterResourceListParam.processorTo != '0')
		{
			filterResourceListParam.processorTo = $('#procsTo').val();
		}
		if(filterResourceListParam.jobsFrom != '0')
		{
			filterResourceListParam.jobsFrom = $('#jobsFrom').val();
		}
		if(filterResourceListParam.jobsTo != '0')
		{
			filterResourceListParam.jobsTo = $('#jobsTo').val();
		}
		if(filterResourceListParam.cpuUtilizationFrom != '0')
		{
			filterResourceListParam.cpuUtilizationFrom = $('#proc_utilFrom').val();
		}
		if(filterResourceListParam.cpuUtilizationTo != '0')
		{
			filterResourceListParam.cpuUtilizationTo = $('#proc_utilTo').val();
		}
		if(filterResourceListParam.memoryUtilizationFrom != '0')
		{
			filterResourceListParam.memoryUtilizationFrom = $('#memory_utilFrom').val();
		}
		if(filterResourceListParam.memoryUtilizationTo != '0')
		{
			filterResourceListParam.memoryUtilizationTo = $('#memory_utilTo').val();
		}
	
	//Ends

	
	$.ajax({
		url:'/node_table/',
		type:'GET',
		data:{sort_parameter:colId,
			sortState:sortState,
			max:viewPerPage,
			offset:pageNumber,
			//Created for sending data of narrow search- abhinavr - 4/29/14
			name:searchResourceListParam.resourceId,
			classes:searchResourceListParam.resourceClass,
			features:searchResourceListParam.features,
			state:filterResourceListParam.resourceState,
			procsFrom:filterResourceListParam.processorFrom,
			procsTo:filterResourceListParam.processorTo,
			jobsFrom:filterResourceListParam.jobsFrom,
			jobsTo:filterResourceListParam.jobsTo,
			proc_utilFrom:filterResourceListParam.cpuUtilizationFrom,
			proc_utilTo:filterResourceListParam.cpuUtilizationTo,
			memory_utilFrom:filterResourceListParam.memoryUtilizationFrom,
			memory_utilTo:filterResourceListParam.memoryUtilizationTo,
			//ends
		},
		success:function(result){
			$('#dataGrid .preloader').hide();
			$('#dataGrid').html(result);
			$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
			//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
			$('#viewPerPage').val(viewPerPage);
			disablePaginationContent();
		}
	});
}//doSort ends

//Resource List Section Ends


//used to display the filter data on click on the bar chart - VJ
function getParameterByName(name) {
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
	var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
	results = regex.exec(location.search);
	return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

//close bootstrap popover when clicked outside of it
$(document).click(function (e) {
	$('.close-popover-link').each(function () {
		if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
			return;
		}
	});
});
//End//

//Duration popup data collection
function durationContent(){
	var mainInput = $('#durInput');
		
	var days = parseInt($('.popover #dInput').val());
	var hrs = parseInt($('.popover #hInput').val());
	var min = parseInt($('.popover #mInput').val());
	var sec = parseInt($('.popover #sInput').val());
	if(days < 10){
		days = "0" + days;
	} else if (isNaN(days)) {
		days = "00";
	}
	if(hrs < 10){
		hrs = "0" + hrs;
	}
	else if (isNaN(hrs)) {
		hrs = "00";
	}
	if(min < 10){
		min = "0" + min;
	}
	else if (isNaN(min)) {
		min = "00";
	}
	if(sec < 10){
		sec = "0" + sec;
	}
	else if (isNaN(sec)) {
		sec = "00";
	}
	mainInput.val(days+":"+hrs+":"+min+":"+sec);
	mainInput.trigger("change");
	//popover should close after apply click
	//$('#infoPopUp').popover('toggle');
	document.getElementById('durationContent').style.display='none';
} //durationContent ends
//Job Details Duration Function Call
function jobDetailsDuration() {
			var divDuration = document.getElementById('durationContent');
			if (divDuration.style.display !== 'none') {
				divDuration.style.display = 'none';
			}
			else {
				divDuration.style.display = 'block';
				divDuration.style.top = '23px';
				divDuration.style.left = '14px';
				var durationTxtBox = document.getElementById('durInput').value;
				var newArry= new Array();
				newArry=durationTxtBox.split(':');
				document.getElementById('dInput').value=newArry[0];
				document.getElementById('hInput').value=newArry[1];
				document.getElementById('mInput').value=newArry[2];
				document.getElementById('sInput').value=newArry[3];
			}
};
function cancelpopover ()
{
		var divDuration = document.getElementById('durationContent');
		divDuration.style.display='none';
}
function clearpopover ()
{
	document.getElementById('dInput').value='00';
	document.getElementById('hInput').value='00';
	document.getElementById('mInput').value='00';
	document.getElementById('sInput').value='00';
}
function toggleNodes(obj,str,status)
{
	
	if(status == 1){
        hideNodes(str)
	}
	else {
		str = escape(str);
		$('#nodeListContainer').append("<span class='label label-default' id='addnode_"+str+"'><a id='node_"+str+"'>"+str+"</a><span class='glyphicon glyphicon-remove' id='destroyNode_"+str+"' onclick='hideNodes(\""+str+"\")'></span></span>");
        var parentobj = $(obj).parent();
        $(obj).remove();
        parentobj.append($("<span/>").attr("id","reqNode_"+str).html("-").addClass("add").attr("onclick","hideNodes(\""+str+"\")"));
        $('#nodeListContainer').trigger("change");
	}
}
function putEllipses(strVal){
var length = strVal.length;

	if(length > 10)
	{
		strVal = strVal.substring(0, 10);
		strVal += ' ...';
	}
	
	return strVal;
}

function toggleFeatures(obj,str,status)
{
	if(status == 1){
        hideFeatures(str)
	}
	else {
		var strText = putEllipses(str);
        $('#featuresContainer').append("<span class='label label-default add_features' id='addfeature_"+str+"'><a  id='feature_"+str+"' title='"+str+"'>"+str+"</a><span class='glyphicon glyphicon-remove' id='destroyFeature_"+str+"' onclick='hideFeatures(\""+str+"\")'></span></span>");
		var parentobj = $(obj).parent();
          $(obj).remove();
        parentobj.append($("<span/>").attr("id","reqFeature_"+str).html("-").addClass("add").attr("onclick","hideFeatures(\""+str+"\")"));
	    $('#featuresContainer').trigger("change");
	}
}
function toggleResources(obj,str,status)
{
	if(status == 1){
		//alert("existis = " + str);
	}
	else {
	  //alert(str)
	  $('#resourceContainer').append("<span class='label label-default' id='node"+str+"'><a>"+str+"</a><span class='glyphicon glyphicon-remove' id='destroyResource' onclick=hideResources(\'"+str+"\')></span></span>");
		
		parentobj = obj.parentNode;
		obj.parentNode.innerHTML = "";
		span = document.createElement("span");
		span.className = "add";
		span.innerHTML = "-";
		span.id = str;
		span.onclick = function(str){}

		parentobj.appendChild(span);
	}
}

// script for node details Configurable features
function toggleConFeature(obj,str,status)
{
	
	if(status == 1){
		hideConFeatures(findElementByText($('#conFeaturesContainer span.label a'),str).parent() ,str);
	}
	else {
	  $("#dmsg").remove();
	  $('#conFeaturesContainer').append("<span class='label label-default'><a id='conFeature_"+str+"'>"+str+"</a><span class='glyphicon glyphicon-remove' id='destroyConFeature_"+str+"' onclick='hideConFeatures($(this).parent(),\"" + str + "\")'></span></span>");
		obj.html("-");
      $("#conFeaturesContainer").trigger("change");
	}
}
// end script for node details Configurable features


// Hide features
idlist = ""
function hideNodes(nodename)
{
	$("#addnode_"+nodename).remove();
    var parentObj =  $("#reqNode_"+nodename).parent();
    $("#reqNode_"+nodename).remove();
    parentObj.append($("<span/>").attr("id","reqNode_"+nodename).html("+").addClass("add").attr("onclick","toggleNodes(this,'"+nodename+"',0)"))
     $("#nodeListContainer").trigger("change");
}
// End Hide features

function hideFeatures(resourcename){
	$("#addfeature_"+resourcename).remove();
    var parentObj =  $("#reqFeature_"+resourcename).parent()
    $("#reqFeature_"+resourcename).remove()
    parentObj.append($("<span/>").attr("id","reqFeature_"+resourcename).html("+").addClass("add").attr("onclick","toggleFeatures(this,'"+resourcename+"',0)"))
     $("#featuresContainer").trigger("change");
}

function replaceQuote(str){
	alert("till thisss");
	str = str.replace(/\"/g,'\\"');
	return str;
}

function hideResources(node){
    id = node.trim();
	$("#node"+id).remove();
    $("#"+id).html("+");
    $("#"+id).attr("onclick","toggleResources(this,'"+id+"',0)");
}

//MATT

function hideConFeatures(obj, node){
	if( obj != undefined && obj != null){
       obj.remove();
    }
	$('#cfModal td#feature_value_'+node).parent().find("span.add").html("+");
	if ($('.features span.label').length == 0) {
		setMsg();
	}
    $("#conFeaturesContainer").trigger("change");
}

function addConFeatures(featureField) {
    var feature = featureField.val();
    if (feature == undefined || feature.trim() == "") {
        return;
    }
   var length =$('#grouptable tr').length;

    var featureDom = findElementByText($('#conFeaturesContainer span.label a'), feature);
	
	
    if (featureDom == undefined || featureDom.length == 0) {
        var tableFeatures = $('#cfModal td#feature_value_'+feature);
        if (tableFeatures == undefined || tableFeatures.length == 0) {
            var reportedFeatures = findElementByText($('#reported_features_container span.label a'), feature)
            if (reportedFeatures != undefined && reportedFeatures.length > 0) {
                alert("'" + feature + "' is a reported feature and can not be added again.");
                return;
            }

            var cfRow = $("<tr/>");
            var span = $("<span/>").addClass("add").css("cursor", "pointer").attr("id", "addconfeature_"+feature).html("+");
            cfRow.append($("<td>").append(span));
            cfRow.append($("<td>").attr("id", "feature_value_"+feature).html(feature));
            cfRow.append($("<td>").html("1"))
            cfRow.append($("<td>").html("New"))
            $('#cfModal table').append(cfRow);
            span.trigger("click");
        }else {
            tableFeatures.parent().find("span.add").trigger("click");
        }
    }
    featureField.val("")
}
function findElementByText(searchField,searchStr, caseSensitive){
    if(caseSensitive == undefined || caseSensitive == null){
        caseSensitive = false;
    }
   return searchField.filter(function() {
        if(caseSensitive){
          return $(this).text().trim().toLowerCase() == searchStr.trim().toLowerCase();
        }else {
          return $(this).text().trim() == searchStr.trim();
        }
   })
}

// *******************************Nathi's JS****************************** //
//########################Role List JS Begins here ##########################//

//Pagination on Grid . Functionality on Page change
function onPageChangeRole(){
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		
		disablePaginationContent();
		
		$('#rolelistcontainer').append('<div class="preloader"></div>').show();
		
		$.ajax({
			url:'/rolelist_grid/',
			type:'GET',
			data:{max:viewPerPage, offset:pageNumber,
			},
			success:function(result){
					$('#rolelistcontainer .preloader').hide();
					$('#rolelistcontainer').html(result);
					$('#pageNumber').children('option').eq(pageNumber-1).attr('selected',true);
					//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);
					$('#viewPerPage').val(viewPerPage);
					disablePaginationContent();
			}
		})
	}
	
//function to call pagination on controls' click event
	function onControlClickRole(caller){
		var pageNumber = $('#pageNumber').val();
		var viewPerPage = $('#viewPerPage').val();
		var clickedButton = $(caller).attr('id');
		var lastPageNumber= $('#pageNumber').find('option:last').val();
		$('#rolelistcontainer').append('<div class="preloader"></div>').show();
		
		$.ajax({
			url:'/rolelist_grid/',
			type:'GET',
			data:{max:viewPerPage,
			offset:pageNumber,
			control:clickedButton,
			lastOffset:lastPageNumber,
			},
			success:function(result){
					//$('#dataGrid .preloader').hide();
					$('#rolelistcontainer').html(result);
					
					switch(clickedButton){
							case 'goToFirst': $('#pageNumber').children('option:first').attr('selected',true);
											  break;
							case 'goToLast':  $('#pageNumber').children('option:last').attr('selected',true);
											  break;
							case 'prev': if(!($('#pageNumber').children('option').is(':first')))
												$('#pageNumber').children('option').eq(pageNumber-2).attr('selected',true);
											break;
							case 'next':if(!($('#pageNumber').children('option').is(':last')))
												$('#pageNumber').children('option').eq(pageNumber).attr('selected',true);
							default:break;				
						};
						$('#viewPerPage').val(viewPerPage);
					//$('#viewPerPage').children('option').eq(viewPerPage-1).attr('selected',true);	
						disablePaginationContent();
			}
		})
	}

	function refreshRoleListPage(btnid){
	$('#myAlert').hide();
	$('#error').hide();
	refreshContentRole(btnid);
	}
	
	
	function refreshPrincipalList(btnid){
		$('#alertp').hide();
		$('#error').hide();
		refreshContentPrincipal(btnid);
	}
	
//functionality for refreshhing the grid

function refreshContentRole(btnid){
	//var btnid = $(caller).attr('id');

	if(btnid == 'rolelistrefresh'){
		$('#rolelistcontainer').empty();
		$('#rolelistcontainer').html('<div class="preloader"></div>');
		$.ajax({
			url:'/rolelist_grid/',
			type:'GET',
			data:{max:10, offset:0},
			success:function(result){
					$('#rolelistcontainer .preloader').hide();
					$('#rolelistcontainer').html(result);
					
					disablePaginationContent();
				}
		});
		
		
	}

}

//function for creating roles in role list page
function createRole()
{
	window.location.href = "/createrole/?tab=configuration";
}

function goto(url){
	window.location.href = "/"+url+"/";
}

function checkData() {
	var processorFrom = 0;
	processorFrom = parseInt($('#procsFrom').val());
	var processorTo = 0;
	processorTo = parseInt($('#procsTo').val());

    // Adding code to remove rank columns --IRIS-333
	if (processorFrom != 0 && processorFrom > processorTo && processorTo != 0) {
		alert("Processors: Please enter correct Range");
		return false;
	}
	var jobsFrom = 0;
	jobsFrom = parseInt($('#jobsFrom').val());
	var jobsTo = 0;
	jobsTo = parseInt($('#jobsTo').val());

    // Adding code to remove rank columns --IRIS-333
	if (jobsFrom != 0 && jobsFrom > jobsTo && jobsTo != 0) {
		alert("Jobs: Please enter correct Range");
		return false;
	}
	var cpuUtilizationFrom = 0;
	cpuUtilizationFrom = parseInt($('#proc_utilFrom').val());
	var cpuUtilizationTo = 0;
	cpuUtilizationTo = parseInt($('#proc_utilTo').val());

    // Adding code to remove rank columns --IRIS-333
	if (cpuUtilizationFrom != 0 && cpuUtilizationFrom > cpuUtilizationTo && cpuUtilizationTo != 0) {
		alert("CPU Utilization: Please enter correct Range");
		return false;
	}
	var memoryUtilizationFrom = 0;
	memoryUtilizationFrom = parseInt($('#memory_utilFrom').val());
	var memoryUtilizationTo = 0;
	memoryUtilizationTo = parseInt($('#memory_utilTo').val());
    // Adding code to remove rank columns --IRIS-333
	if (memoryUtilizationFrom != 0 && memoryUtilizationFrom > memoryUtilizationTo && memoryUtilizationTo != 0) {
		alert("Memory Utilization: Please enter correct Range");
		return false;
	}
	
	
	else {
	$('.form-control').prop('readonly', 'true');
		$('#resourceState').prop('disabled', true);
		$('.filter').prop('disabled', true);
		$('#searchCat').prop('disabled', true);
		//$('#jobState').prop('disabled', true);
		//$('#dateTimeRange').prop('disabled', true);
		$('#searchBtn').prop('readonly', 'true');
		//alert("correct!");
		return true;
	}
}


function checkFilterData() {
	var priorityFrom = 0;
	priorityFrom = parseInt($('#priorityFrom').val());
	var priorityTo = 0;
	priorityTo = parseInt($('#priorityTo').val());
	if (priorityFrom != 0 && priorityFrom > priorityTo && priorityTo != 0) {
		alert("Priority: Please enter correct Range");
		return false;
	}

	var rankFrom = 0;
	rankFrom = parseInt($('#rankFrom').val());
	var rankTo = 0;
	rankTo = parseInt($('#rankTo').val());
	
	if (rankFrom != 0 && rankFrom > rankTo && rankTo != 0) {
		alert("Rank: Please enter correct Range");
		return false;
	}
	
	var StartDate = $('#txtStartDate').val();
	var EndDate = $('#txtEndDate').val();
	var re = /-/gi;
	StartDate = StartDate.replace(re, "/");
	EndDate = EndDate.replace(re, "/");
	//alert(StartDate+','+EndDate);
	var eDate = new Date(EndDate);
	var sDate = new Date(StartDate);
	//alert(sDate.getTime()+','+eDate.getTime());
	
	
	if(StartDate!= '' && EndDate!= '' && sDate>eDate)
		{
			alert("Please ensure that the End Date is greater than or equal to the Start Date.");
		return false;
		}
		//alert(wallclockStart);
		var wallclockStart = 0;
		var wallclockStartDay = 0;
		wallclockStartDay = parseInt($('#wallclockStart #day').val());
		var wallclockStartHr = 0 ;
		wallclockStartHr = parseInt($('#wallclockStart #hr').val());
		var wallclockStartMin = 0 ;
		wallclockStartMin = parseInt($('#wallclockStart #min').val());
		var wallclockStartSec = 0 ;
		wallclockStartSec = parseInt($('#wallclockStart #sec').val());
		//alert(wallclockend);
		var wallclockEnd = 0;
		var wallclockEndDay = 0 ;
		wallclockEndDay = parseInt($('#wallclockEnd #today').val());
		var wallclockEndHr = 0 ;
		wallclockEndHr = parseInt($('#wallclockEnd #tohr').val());
		var wallclockEndMin = 0 ;
		wallclockEndMin = parseInt($('#wallclockEnd #tomin').val());
		var wallclockEndSec = 0 ;
		wallclockEndSec = parseInt($('#wallclockEnd #tosec').val());
		
		//var wallclockStart = wallclockStartDay + wallclockStartHr + wallclockStartMin + wallclockStartSec;
		//var wallclockEnd = wallclockEndDay + wallclockEndHr + wallclockEndMin + wallclockEndSec;
		
		
        var wallclockStart = parseInt(wallclockStartDay) * 86400 + (parseInt(wallclockStartHr)*3600) + (parseInt(wallclockStartMin)*60) + (parseInt(wallclockStartSec));

        var wallclockEnd = parseInt(wallclockEndDay) * 86400 + (parseInt(wallclockEndHr)*3600) + (parseInt(wallclockEndMin)*60) + (parseInt(wallclockEndSec));

		if (wallclockStart != 0 && wallclockStart > wallclockEnd && wallclockEnd != 0) {
		alert("Please enter valid wallclock parameter: 'From' value must be equal to or less than the 'To' value.");
		return false;
	}
		else {
			//alert("correct!");
			$('.form-control').prop('readonly', 'true');
		$('.filter').prop('disabled', true);
		$('#searchCat').prop('disabled', true);
		$('#jobState').prop('disabled', true);
		$('#dateTimeRange').prop('disabled', true);
		$('#searchBtn').prop('readonly', 'true');
			return true;
		}
}

// For Principal List Page and its functionalities
function createPrincipal()
{
	window.location.href = "/principal/?tab=configuration";
}

function refreshContentPrincipal(btnid){
		//var btnid = $(caller).attr('id');

	if(btnid == 'principallistrefresh'){
		$('#principallistcontainer').empty();
		$('#principallistcontainer').html('<div class="preloader"></div>');
		$.ajax({
			url:'/principallist_grid/',
			type:'GET',
			data:{max:10, offset:0},
			success:function(result){
					$('#principallistcontainer .preloader').hide();
					$('#principallistcontainer').html(result);
				}
		});
		
		
	}
}

function goto(url)
{
	window.location.href = "/"+url+"/";
}


function clearValue(obj)
{
	obj.value = "";
}

function mousedownfunc(divid,fname) {
    intervalId = setInterval(fname, 80, divid);
}

function mouseupfunc() {
    clearInterval(intervalId);
}

function increment(id)
{
     var value = parseInt($("#"+id).val());	
	 if(isNaN(value))
		$("#"+id).val(0);
	 else
		$("#"+id).val(value+1);  	
}

function incrementMax(id)
{
	if(checkMax(id,0,99) == true)
	{
		 var value = parseInt($("#"+id).val());	
		 if(isNaN(value))
			$("#"+id).val(0);
		 else
			$("#"+id).val(value+1);
	}
}
function incrementMaxM(id)
{
	if(checkMaxMemory(id,0,99) == true)
	{
		 var value = parseInt($("#"+id).val());	
		 if(isNaN(value))
			$("#"+id).val(0);
		 else
			$("#"+id).val(value+1);
	}
}
//job details popover functions //
function incrementDay(id)
{
	if(durationDay(id,0) == true)
	{
		 var value = parseInt($("#"+id).val());	
		 if(isNaN(value))
			$("#"+id).val(0);
		 else
			$("#"+id).val(value+1);
	}
}
function durationDay(ctrl,min,max){	
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<min || input>max){
			//alert("Duration days:Value should be between 0 - 31");
			//alert(msg);
			clearInterval(intervalId);
			document.getElementById(ctrl).value = min;
					return false;
			}
		return true;
}
function incrementHour(id)
{
	if(durationHour(id,0,22) == true)
	{
		 var value = parseInt($("#"+id).val());	
		 if(isNaN(value))
			$("#"+id).val(0);
		 else
			$("#"+id).val(value+1);
	}
}
function durationHour(ctrl,min,max){	
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<min || input>max){
			alert("Duration hour's:Value should be between 0 - 23");
			//alert(msg);
			clearInterval(intervalId);
			document.getElementById(ctrl).value = min;
					return false;
			}
		return true;
}
function incrementMinutes(id)
{
	if(durationMinutes(id,0,58) == true)
	{
		 var value = parseInt($("#"+id).val());	
		 if(isNaN(value))
			$("#"+id).val(0);
		 else
			$("#"+id).val(value+1);
	}
}
function durationMinutes(ctrl,min,max){	
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<min || input>max){
			alert("Duration minutes:Value should be between 0 - 59");
			//alert(msg);
			clearInterval(intervalId);
			document.getElementById(ctrl).value = min;
					return false;
			}
		return true;
}
function incrementSeconds(id)
{
	if(durationSeconds(id,0,58) == true)
	{
		 var value = parseInt($("#"+id).val());	
		 if(isNaN(value))
			$("#"+id).val(0);
		 else
			$("#"+id).val(value+1);
	}
}
function durationSeconds(ctrl,min,max){	
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<min || input>max){
			alert("Duration seconds:Value should be between 0 - 59");
			//alert(msg);
			clearInterval(intervalId);
			document.getElementById(ctrl).value = min;
					return false;
			}
		return true;
}
 function jobPriority(ctrl,min,max){	
		var input=parseInt(document.getElementById(ctrl).value);
		if(input<min || input>max){
			alert("Job priority:Value should be between -1024 to 0");
			//alert(msg);
			document.getElementById(ctrl).value = min;
					return false;
			}
		return true;
}

//job details popover functions end //
function decrement(id)
{
	var value = parseInt($("#"+id).val());	
	if(value > 0)
		$("#"+id).val(value-1);
	else
		$("#"+id).val(0);
}

function statusCodeInitialiseRes()
{

filterResourceListParam.resourceState = $('#resourceState').val();

}

function statusCodeInitialise()
{
filterParam.jobState = $('#jobState').val();
}

function createDirtyUnloadListener(fieldObjects,message) {
    $("body").on("change",fieldObjects, function () {
        isDirtyPlaceholder = true
    });
    $(window).on('beforeunload', function() {
		     if(isDirtyPlaceholder){
                 if(message == undefined){
                     message = ""
                 }
				 return message
			 }
	});
}

//inject csrf token on form submit and ajax calls
function initCsrfToken(token) {

    $(document).on("submit", "form", function (e) {
        $(this).append('<input type="hidden" name="csrfmiddlewaretoken" value="' + token + '"/>');
    });

    $(document).ajaxSend(function (event, jqxhr, settings) {
        //only modify header if POST, PUT, or DELETE
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))) {
            jqxhr.setRequestHeader("X-CSRFToken", token)
        }
    });
}
//Date Formatter added on 06-27-2014 - Abhinav


var dateFormat = function () {
    var token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
        timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
        timezoneClip = /[^-+\dA-Z]/g,
        pad = function (val, len) {
            val = String(val);
            len = len || 2;
            while (val.length < len) val = "0" + val;
            return val;
        };

    // Regexes and supporting functions are cached through closure
    return function (date, mask, utc) {
        var dF = dateFormat;

        // You can't provide utc if you skip other args (use the "UTC:" mask prefix)
        if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
            mask = date;
            date = undefined;
        }

        // Passing date through Date applies Date.parse, if necessary
        date = date ? new Date(date) : new Date;
        if (isNaN(date)) throw SyntaxError("invalid date");

        mask = String(dF.masks[mask] || mask || dF.masks["default"]);

        // Allow setting the utc argument via the mask
        if (mask.slice(0, 4) == "UTC:") {
            mask = mask.slice(4);
            utc = true;
        }

        var _ = utc ? "getUTC" : "get",
            d = date[_ + "Date"](),
            D = date[_ + "Day"](),
            m = date[_ + "Month"](),
            y = date[_ + "FullYear"](),
            H = date[_ + "Hours"](),
            M = date[_ + "Minutes"](),
            s = date[_ + "Seconds"](),
            L = date[_ + "Milliseconds"](),
            o = utc ? 0 : date.getTimezoneOffset(),
            flags = {
                d:    d,
                dd:   pad(d),
                ddd:  dF.i18n.dayNames[D],
                dddd: dF.i18n.dayNames[D + 7],
                m:    m + 1,
                mm:   pad(m + 1),
                mmm:  dF.i18n.monthNames[m],
                mmmm: dF.i18n.monthNames[m + 12],
                yy:   String(y).slice(2),
                yyyy: y,
                h:    H % 12 || 12,
                hh:   pad(H % 12 || 12),
                H:    H,
                HH:   pad(H),
                M:    M,
                MM:   pad(M),
                s:    s,
                ss:   pad(s),
                l:    pad(L, 3),
                L:    pad(L > 99 ? Math.round(L / 10) : L),
                t:    H < 12 ? "a"  : "p",
                tt:   H < 12 ? "am" : "pm",
                T:    H < 12 ? "A"  : "P",
                TT:   H < 12 ? "AM" : "PM",
                Z:    utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
                o:    (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
                S:    ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
            };

        return mask.replace(token, function ($0) {
            return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
        });
    };
}();

// Some common format strings
dateFormat.masks = {
    "default":      "ddd mmm dd yyyy HH:MM:ss",
    shortDate:      "m/d/yy",
    mediumDate:     "mmm d, yyyy",
    longDate:       "mmmm d, yyyy",
    fullDate:       "dddd, mmmm d, yyyy",
    shortTime:      "h:MM TT",
    mediumTime:     "h:MM:ss TT",
    longTime:       "h:MM:ss TT Z",
    isoDate:        "yyyy-mm-dd",
    isoTime:        "HH:MM:ss",
    isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",
    isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
};

// Internationalization strings
dateFormat.i18n = {
    dayNames: [
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ],
    monthNames: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ]
};

// For convenience...
Date.prototype.format = function (mask, utc) {
    return dateFormat(this, mask, utc);
};


//Date Formatter ends
