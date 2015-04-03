## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>
<%inherit file="base.mako" />
<%def name="title()">${_("Node List")}</%def>
<%def name="head_tags()">
    <style type="text/css">

</style>

</%def>
<%def name="jquery_tags()">
    <script type="text/javascript">
        google.load("visualization", "1", {packages:["corechart"]});
    </script>
    <script type="text/javascript">
        $(document).ready(function(){
            $('#dataGrid .preloader').show();

            var statusCode = $('#hiddenstatusCode').val();
            disableResourcelistContentOnPageLoad();
            //alert(statusCode);
            $.ajax({
                url:'/node_table/',
                type:'GET',
                data:{max:20, offset:1, status:statusCode},
                success:function(result){
                    $('#dataGrid .preloader').hide();
                    $('#dataGrid').html(result);
                    
                    if (statusCode != ""){
                    $('#totalResourcesCnt').text($('#hiddenTotalCnt').val() + ' Jobs');
                    
                    }
                    disablePaginationContent();
                 enableResourcelistContentOnPageLoad();
                }
        
                });
            
            var status = getParameterByName('status');
            //status = status.slice(0,1).toUpperCase() + status.slice(1);   
            if (status != ""){
                $('#resourceState').val(status);
                statusCodeInitialiseRes()
            }
        });
    </script>
    <link rel="stylesheet" type="text/css" href="/static/css/datepicker.css" />
    <script src="/static/js/bootstrap-datetimepicker.js" type="text/javascript"></script>   

</%def>

<%def name="main_content()">
            
    <div class="row">
        <div class="col-xs-8">
            %if messages:
                %if status == "success":
                    <div class="alert alert-success" id="myAlert">
                        <a href="#" class="close" data-dismiss="alert">&times;</a>
                        ${ messages | n,decode.utf8}
                    </div>
                %else:
                    <div class="alert alert-danger" id="myAlert">
                        <a href="#" class="close" data-dismiss="alert">&times;</a>
                        ${ messages | n,decode.utf8}
                    </div>
                %endif
            %endif
            <div class="col-xs-6 section-header padlt">
                <h1><b>${_("Nodes")}</b>
                        <span class="refresh" id="resourceListRefresh" onClick="refreshResourceListContent(this);"></span>
                </h1>
                
            </div>
            <div class="clearfix"></div>
            <!--<span class="right-icon-section">
                <button type="button" class="btn btn-primary" disabled>
                    <span class="glyphicon glyphicon-plus"></span>&nbsp;&nbsp;&nbsp;${_("Create Reservation")}
                </button>
            </span>-->
            <!--<span class="icon-grid"></span>-->
            <!--<span class="icon-timeline"></span>-->
            <div>
            <input type="text" id="hiddenstatusCode" style='display:none' value=${ jobStatus  }></input>
                <div id="dataGrid" class="dtGrid datagrid-container container panel panel-default">
                    <div class="preloader"></div>
                    <div class="endless_page_template">

                    </div>
                </div>
            </div>
        </div>
        <!--This is Filter section-->
        <div class="col-xs-4 search-filter-section padLeft">
            <h5><b>${_("Current Search")}: </b><strong><label id='totalResourcesCnt'></label></strong></h5>
            <div id="searchValues">
                
            </div>
            <span>
                <!-- <input type="checkbox"> -->
                <select id="searchCat" class="form-control" onChange="$('#searchBox').focus()">
                    <option  id="opt0" value="select">- ${_("Select")} -</option>
                    <option id="opt1" value="NodeID">Node ID</option>
                    <option id="opt2" value="Class">Class</option>
                    <option id="opt3" value="Features">Features</option>
                </select>
            </span>
            <span>
                <input id="searchBox" type="text" class="form-control search" onclick="clearValue(this)" placeholder="${_("Narrow Search")}" onkeypress="addResourceListFilter(this,event)"/>
                <span id="searchBtn" class="glyphicon glyphicon-search" onclick="addResourceListFilter(this,event)"></span>
            </span>
            <h5 class="filter">${_("Filters")}</h5>
            <span>
                <!-- <input type="checkbox"> -->
                    <select id="resourceState" class="form-control">
                        <option id="opt0" value="null">${_("Select Status")}</option>
                        %if resource_filter:
                            % for i in resource_filter:
                                <option value="${ i  }">${ i  }</option>
                            % endfor
                        %endif
                </select>
            </span>
            
            <div class="col-xs-12">
        <div class="col-xs-6 padLR">
            <div class="form-group">
                <label class="labelfilter">${_("Processors")}</label>
                    <input type="text" name="From" id="procsFrom" value="0" class="form-control number-input"  onkeypress="checkObjection(this,event)">
                <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('procsFrom', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('procsFrom', decrement)" onmouseup="mouseupfunc()"></div></div>
            </div>
        </div>
        <div class="col-xs-6 padLR">
            <div class="form-group">
                <label class="labelfilter1">${_("To")}</label>
                    <input type="text" name="From" id="procsTo" value="0" class="form-control number-input"  onkeypress="checkObjection(this,event)">
                    <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('procsTo', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('procsTo', decrement)" onmouseup="mouseupfunc()"></div></div>
                </div>
            </div>
        </div>
        <div class="clearfix"></div>
    <div class="col-xs-12">
        <div class="col-xs-6 padLR">
            <div class="form-group">
                <label for="From" class="labelfilter">${_("Jobs")}</label>
                    <input type="text" name="From" id="jobsFrom" value="0" class="form-control number-input"  onkeypress="checkObjection(this,event)">
                    <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('jobsFrom', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('jobsFrom', decrement)" onmouseup="mouseupfunc()"></div></div>
            </div>
        </div>
        <div class="col-xs-6 padLR">
            <div class="form-group">
                <label class="labelfilter1">${_("To")}</label>
                <input type="text" name="From" id="jobsTo" value="0" class="form-control number-input"  onkeypress="checkObjection(this,event)">
                <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('jobsTo', increment)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('jobsTo', decrement)" onmouseup="mouseupfunc()"></div></div>
            </div>
        </div>
    </div>
    <div class="clearfix"></div>
    <div class="col-xs-12">
        <div class="col-xs-6 padLR">
            <div class="form-group">
                <label class="labelfilter">${_("CPU Utilization")}</label>
                <input type="text" name="From" id="proc_utilFrom" value="0" class="form-control number-input" onkeyup="checkMax('proc_utilFrom',0,100)" onkeypress="checkObjection(this,event)">
                <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('proc_utilFrom', incrementMax)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('proc_utilFrom', decrement)" onmouseup="mouseupfunc()"></div></div>
            </div>
        </div>
        <div class="col-xs-6 padLR">
            <div class="form-group">
                <label class="labelfilter1">${_("To")}</label>
                <input type="text" name="From" id="proc_utilTo" value="0" class="form-control number-input" onkeyup="checkMax('proc_utilTo',0,100)" onkeypress="checkObjection(this,event)">
                <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('proc_utilTo', incrementMax)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('proc_utilTo', decrement)" onmouseup="mouseupfunc()"></div></div>
            </div>
        </div>

        <div class="col-xs-12">
            <div class="col-xs-6 padLR">
                <div class="form-group">
                    <label class="labelfilter">${_("Memory Utilization")}</label>
                    <input type="text" name="From" id="memory_utilFrom" value="0" class="form-control number-input"  onkeyup="checkMaxMemory('memory_utilFrom',0,100)" onkeypress="checkObjection(this,event)">
                    <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('memory_utilFrom', incrementMaxM)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('memory_utilFrom', decrement)" onmouseup="mouseupfunc()"></div></div>
                </div>
            </div>
            <div class="col-xs-6 padLR">
                <div class="form-group">
                    <label class="labelfilter1">${_("To")}</label>
                        <input type="text" name="From" id="memory_utilTo" value="0" class="form-control number-input" onkeyup="checkMaxMemory('memory_utilTo',0,100)" onkeypress="checkObjection(this,event)">
                        <div class="buttonbig"><div class="incbutton" onmousedown="mousedownfunc('memory_utilTo', incrementMaxM)" onmouseup="mouseupfunc()"></div><div class="decbutton" onmousedown="mousedownfunc('memory_utilTo', decrement)" onmouseup="mouseupfunc()"></div></div>
                </div>
            </div>
        </div>
        <div class="clearfix"></div>
    </div> 
            
            <button type="button" class="btn btn-primary right filter" onclick="doResourceListFiltering()" id="nodeList_filterBtn">${_("Filter")}</button>
        </div>
    </div>
<!--Filter section ends-->
</%def>
<%def name="end_script()">
</%def>
