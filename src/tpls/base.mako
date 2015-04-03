## Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.

<%! from django.utils.translation import ugettext as _ %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta http-equiv='pragma' content='no-cache'>
    <meta http-equiv='expires' content='0'>
    <meta http-equiv='cache-control' content='no-cache'>

    <title>${self.title()}</title>

    <!--[if !IE]><!--><script>
    if (/*@cc_on!@*/false) {
            document.documentElement.className+=' ie10';
    }
</script><!--<![endif]-->
    
    <!-- CSS -->
    <link rel="stylesheet" type="text/css" href="/static/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/style.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/css/number-polyfill.css" />
    
    <!-- JavaScripts -->
        <script src="/static/js/jquery-min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <!-- Latest compiled and minified JavaScript -->
        <script src="/static/bootstrap/js/bootstrap.min.js"></script>
        <script src="/static/js/require.js" type="text/javascript"></script>
        <script type="text/javascript" src="/static/js/main.js"></script>
        <script type="text/javascript" src="/static/js/number-polyfill.min.js"></script>
        <script type="text/javascript" src="/static/js/jsapi.js"></script>

    <script type="text/javascript">
        $(document).ready(function(){

            //inner pages if tab is in querystring
            var querytab = getParameterByName("tab");                                                    
            $('#mainNav li a').each(function(){                                                                           
            //alert(this.id);
            if(this.id.trim() == querytab.trim()){
                $(this).parent().addClass('active');
                return true;
            }else{
                $(this).parent().removeClass('active');                                                                                   
            }
        });

        var str = location.href.toLowerCase();
        
        $('#mainNav li a').each(function(){
            if(str.indexOf(this.href.toLowerCase()) > -1) {
                $('li.active').removeClass('active');
                $(this).parent().addClass('active');
            }
        });

    });

		initCsrfToken('${ csrftoken }');
    </script>


    
    ${self.head_tags()}

    ${self.jquery_tags()}
</head>

<body>
    <div class="container">
        <header>
		
		<div class="col-xs-8">
            <img src="../static/images/moab_logo.png" width="209" height="30" alt="Moab Logo" />
            
			</div>
			<div class="col-xs-4">
			<ul class="nav navbar-nav navbar-right">
                %if username:                    
                    <li id="welcome_user">${_("Welcome, {0}").format(username)  }</li>
                    <!--<li>${_("Welcome, {0}")}.format(${ username  })</li>-->
                    <li><a href="/logout/" title="Sign Out" id="signout">${_("Sign Out")}</a></li>
                %else:
                    <li><a href="/login/" title="Login">${_("Login")}</a></li>          
                %endif                
                <li>
                %if 'Configuration page' in session_permission_list:
                        <a href="/configuration/" id="settings"><span class="icon ico-settings"></span></a>
                    %endif
                    <a href="http://docs.adaptivecomputing.com/suite/8-0/enterprise/help.htm" target="_blank" id="help"><span class="icon ico-question"></span></a>
                </li>
            </ul>
			</div>
		
        </header>
        <nav id="mainNav">
            <ul>
                
                <li class="active"><a href="/dashboard/" id="dashboard" title="${_("Home")}">${_("Home")}</a></li>
                %if hasAccess('Workload'):
                    <li><a href="/workload/" id="workload" title="${_("Workload")}">${_("Workload")}</a></li>
                %endif
                %if hasAccess('Resources'):
                    <li><a href="/nodelist/" id="resources" title="${_("Nodes")}">${_("Nodes")}</a></li>
                %endif
                %if 'Configuration page' in session_permission_list:
                    <li><a href="/configuration/" id="configuration" title="${_("Configuration")}">${_("Configuration")}</a></li>
                %endif
            </ul>
        </nav>
        <div id="page-content">

            ${self.main_content()}

            <div class="separator">
                <div></div>
            </div>
            <footer>
                <div><img src="/static/images/adaptive_logo.jpg" width="159" height="103" alt="Adaptive Computing" /></div>
                <span class="copyright">
						<span>Copyright&nbsp;&copy;&nbsp;2001-<script type="text/javascript">document.write(new Date().getFullYear());</script>&nbsp;Adaptive&nbsp;Computing&nbsp;Enterprises,&nbsp;Inc.&nbsp;All&nbsp;rights&nbsp;reserved.</span>
                </span>
            </footer>
        </div>
    </div>
    % if google_analytics == "1":
    <script>        
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
        ga('create', 'UA-35839514-1', 'adaptivecomputing.com');
        ga('send', 'pageview');
    </script>
    %endif
    ${self.end_script()}
    <%def name="hasAccess(x)">
    %if x in session_permission_list:
         <% return True %>
    %endif
    </%def>
</body>
</html>
