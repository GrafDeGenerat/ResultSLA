<h3>Project for calculating SLA time. Minimalistic version</h3> <br>
<b>Requirements</b>: <br>
&nbsp; 1) .env file in root dir
&nbsp; 2) Requirements from requirements.txt

<b>Input data</b>: json format like <br> 
<code>
{<br>
&nbsp;&nbsp;&nbsp;"date": <datetime, UTC format, default=datetime.now()>, <br> 
&nbsp;&nbsp;&nbsp;"operating_mode_from": <beginning_of_the_working_day, int or float value>, <br>
&nbsp;&nbsp;&nbsp;"operating_mode_to": <ending_of_the_working_day, int or float value>, <br>
&nbsp;&nbsp;&nbsp;"sla_time": <SLA_time, positive int or float value> <br>
}
</code>
