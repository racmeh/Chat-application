<html>
<head>
<title>Login/Register</title>
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
            ws = new WebSocket('ws://192.168.43.29:8080/ws_signlog');
            ws.onopen = function(evt) {
                $('#messages').append('<li>Connected to server</li>');
           }
           ws.onmessage = function(evt) {
           $('#messages').append('<li>' + evt.data + '</li>');
           if(evt.data=="Login successfull, redirecting..."||evt.data=="Signup successfull, redirecting...")
           $('#redirect').trigger('click');
           }
           $('#btn').click(function(){
            ws.send($('#usrnm').val());
            ws.send($('#usrid').val());
            ws.send($('#pwd').val());
            ws.send($('#stat').val());
            });
           $('#btn1').click(function(){
            ws.send($('#usrnm1').val());
            ws.send($('#usrid1').val());
            ws.send($('#pwd1').val());
            ws.send($('#stat1').val());
            });
           ws.onclose = function()
            {
            $('#messages').append('<li>' + "Connection is closed..." + '</li>'); 
            }
            });
</script>
</head>
<body>
<h2><b>Signup</b></h2><br/>
<input id="usrnm" type="text" placeholder="Username" name="usrnm"><br/><br/>
<input id="usrid" type="text" placeholder="User ID" name="usrid"><br/><br/>
<input id="pwd" type="text" placeholder="Password" name="pwd"><br/><br/>
<input id="stat" type="text" placeholder="Signup" name="stat"><br/><br/>
<button id="btn">Signup</button><br/><br/>
<b>OR</b><br/>
<h2><b>Login</b></h2><br/>
<input id="usrnm1" type="text" placeholder="Username" name="usrnm1"><br/><br/>
<input id="usrid1" type="text" placeholder="User ID" name="usrid1"><br/><br/>
<input id="pwd1" type="text" placeholder="Password" name="pwd1"><br/><br/>
<input id="stat1" type="text" placeholder="Login" name="stat1"><br/><br/>
<button id="btn1">Login</button><br/><br/>
<input id="redirect" type="button" onclick="location.href='http://192.168.43.29:8080/user';" value="Redirect" />
<div id="messages"></div>
</body>
</html>
