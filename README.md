<h3>Project for calculating SLA time</h3> <br>
<b>Requirements</b>: <br>
&nbsp; 1) Demo DB - ENV setting DOCKER_MODE, default True. <b>Installed and running Docker required!</b><br>
&nbsp; 2) Python 3.12 with insalled requirements<br>
<br>
Needed for authorization for get token (basic auth, defaults for demo: username: 'Bob', password: '123'. <br>
Token used in request header ('Token': 'taked token after auth'). <br>
Body of request - input data <br><br>

<b>Input data</b>: json format like <br> 

<code>{<br>
&nbsp;&nbsp;&nbsp;"date": <datetime, UTC format, default=datetime.now()>, <br> 
&nbsp;&nbsp;&nbsp;"operating_mode_from": <beginning_of_the_working_day, int or float value>, <br>
&nbsp;&nbsp;&nbsp;"operating_mode_to": <ending_of_the_working_day, int or float value>, <br>
&nbsp;&nbsp;&nbsp;"sla_time": <SLA_time, positive int or float value> <br>
}</code>


<b>Output data</b>: json format like <br> 

<code>{<br>
&nbsp;&nbsp;&nbsp;"deadline": "YYYY-MM-DD HH:mm:SS" <br>
}</code>

