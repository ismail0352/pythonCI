## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>

<%inherit file="base.mako" />
<%namespace name="base" file="base.mako" />

<%def name="title()">500</%def>

<%def name="head_tags()"></%def>

<%def name="jquery_tags()"></%def>
<%def name="main_content()">
<div class="container">
            <div style="font-size:18px;margin-left: 20px;margin-right: 20px;text-align:center; margin-top:40px;">
				<div class="alert alert-danger" id="error_500">${_("500......Internal Server error")}
					%if error_message:
						<br/><br/>${ error_message }
                    %endif
				</div>
                </div>
			</div>
                <div class="row">
                </div>
                <div class="row">
                </div>
                <div class="row">
                </div>
                <div class="row">
                </div>
                <div class="row">
                </div>
                <div class="row">
                </div>

</%def>
<%def name="end_script()"></%def>
