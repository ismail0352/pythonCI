## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>
	<script type="text/javascript">
			$(document).ready(function(){
				var str = location.href.toLowerCase();
				$('#leftnav li a').each(function(){
					if(str.indexOf('role') > -1) {						
						$('li.active1').removeClass('active1');
						$("#roles").parent().addClass('active1');
					}else if(str.indexOf('principal') > -1) {						
						$('li.active1').removeClass('active1');
						$("#principals").parent().addClass('active1');
					}
					
				});
			});
	</script>
	<div class="col-xs-4 search-filter-section leftnavBg" id="side">
		<div class="col-xs-12">
			<ul id="leftnav" class="nav nav-pills nav-stacked">
				<li class="active1">
				%if hasAccessforleftpanel('Configuration page'):
					<a href="/configuration/" id="mwsconfiguration">${_("MWS Configuration")}</a>				
				%endif
				</li>
				%if hasAccessforleftpanel('Principal and Roles Pages'):
				<li>
					<a href="/rolelist/?tab=configuration" id="roles" >${_("Roles")}</a>
				</li> 
				<li><a href="/principallist/?tab=configuration" id="principals">${_("Principals")}</a>
				</li>
				%endif
			</ul>	
		</div>
	</div>
	<%def name="hasAccessforleftpanel(x)">
		%if x in session_permission_list:
		<%return True%>
		%endif
	</%def>
