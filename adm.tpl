<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>WebSocket Connection Testing</title>
    
    <style>
        li { list-style: none; }
    </style>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
    <script>
   $(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
                }
            }
            ws = new WebSocket('ws://192.168.43.29:8080/ws_adm');
            ws.onopen = function(evt) {
                $('#messages').append('<li>Connected to server</li>');
                $('#btn').hide()
            }
            var c1=0;var n1=0;var n2=0;var str="";var i=0;
            ws.onmessage = function(evt) {
            str=evt.data;
            for(i=0;i<str.length;i++){
            if(str.charAt(i)==':'){
            c1=i;break;}}
            n1=parseInt(str.substring(3,c1));
            n2=parseInt(str.substring(c1+1,str.length));
            $('#count1').text(n1.toString());
            $('#count2').text(n2.toString());
            $('#count3').text((n1-n2).toString());
            google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var data = google.visualization.arrayToDataTable([
  ['Users', 'Status'],
  ['Total', n1],
  ['Online', n2],
  ['Offline', n1-n2]
]);
var options = {'title':'User Status', 'width':550, 'height':400};
  var chart = new google.visualization.PieChart(document.getElementById('piechart'));
  chart.draw(data, options);
}
            }
            $('#btn').click(function(){
            ws.send("Send");
            });
            setInterval(function(){$('#btn').trigger("click")},5000);
            ws.onclose = function()
            {
            $('#messages').append('<li>' + "Connection is closed..." + '</li>'); 
            }

        });
</script>
</head>
<body>
<h2>WebSocket Connection Testing</h2>
<br/><br/>
<button id="btn">Refresh</button>
<p>Total Users : <span id="count1"></span></p><br/>
<p>Online Users : <span id="count2"></span></p><br/>
<p>Offline Users : <span id="count3"></span></p><br/><br/>
<div id="piechart"></div><br/>
</body>
</html>