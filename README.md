<h3>Project for calculating SLA time</h3> <br>
<b>Requirements</b>: <br>
&nbsp; 1) BD - postgres, for auth users. <br>
&nbsp; 2  Demo DB - ENV setting DOCKER_MODE for enabling, default True. <b>Installed and running Docker required!</b><br>
&nbsp; 3) .env file in root dir (example - .env_demo)

<b>Input data</b>: json format like <br> 
<code>
{<br>
&nbsp;&nbsp;&nbsp;"date": <datetime, UTC format, default=datetime.now()>, <br> 
&nbsp;&nbsp;&nbsp;"operating_mode_from": <beginning_of_the_working_day, int or float value>, <br>
&nbsp;&nbsp;&nbsp;"operating_mode_to": <ending_of_the_working_day, int or float value>, <br>
&nbsp;&nbsp;&nbsp;"sla_time": <SLA_time, positive int or float value> <br>
}
</code>
