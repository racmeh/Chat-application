<!doctype html>
<head>
<title>Login/Register</title>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
<script>
$(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {	//Checking if websocket is supported
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");	<!-- If web socket not supported, message is displayed -->
                }
            }
			
            ws = new WebSocket('ws://192.168.43.29:8080/ws_signlog');	//Setting up a web socket on the mentioned url
            ws.onopen = function(evt) {//Defining what happens when socket connection opens
                $('#messages').append('<li>Connected to server</li>');
                $('#redirect').hide();	//Hiding redirect button
           }
		   
           ws.onmessage = function(evt) {	//Defining what happens when message is received
				$('#messages').append('<li>' + evt.data + '</li>');	//Appending the message to the module
				if(evt.data=="Login successfull, redirecting..."||evt.data=="Signup successfull, redirecting...")	//Checking for login or Signup
				$('#redirect').trigger('click');	//Triggering click of a button
           }
		   
           $('#btn').click(function(){	//Defining what happens on the click of the button with id=btn, this is for Signup
				ws.send($('#usrnm').val());	//Sending username to server to be stored in database
				ws.send($('#usrid').val());
				ws.send($('#pwd').val());
				ws.send($('#stat').val());	//Sending status to server to be stored in database, status here will be Signup
            });
			
           $('#btn1').click(function(){	//Defining what happens on the click of the button with id=btn, this is for Login
				ws.send($('#usrnm1').val());
				ws.send($('#usrid1').val());
				ws.send($('#pwd1').val());
				ws.send($('#stat1').val());	//Status will be Login
            });
			
           ws.onclose = function()	//Defining what happens when web socket connection is closed
            {
				$('#messages').append('<li>' + "Connection is closed..." + '</li>'); 
            }
	});
</script>
</head>

<body>

	<h2><b>Signup</b></h2><br/>
	<input id="usrnm" type="text" placeholder="Username" name="usrnm">
	<br/><br/>
	<input id="usrid" type="text" placeholder="User ID" name="usrid">
	<br/><br/>
	<input id="pwd" type="text" placeholder="Password" name="pwd">
	<br/><br/>
	<input id="stat" type="text" placeholder="Enter Signup" name="stat">
	<br/><br/>
	<button id="btn">Signup</button>
	<br/><br/>
	<b>OR</b><br/>
	<h2><b>Login</b></h2><br/>
	<input id="usrnm1" type="text" placeholder="Username" name="usrnm1">
	<br/><br/>
	<input id="usrid1" type="text" placeholder="User ID" name="usrid1">
	<br/><br/>
	<input id="pwd1" type="text" placeholder="Password" name="pwd1">
	<br/><br/>
	<input id="stat1" type="text" placeholder="Enter Login" name="stat1">
	<br/><br/>
	<button id="btn1">Login</button><br/><br/>
	<input id="redirect" type="button" onclick="location.href='http://192.168.43.29:8080/user';" value="Redirect" /> 	<!-- Redirecting to another url on clicking the button -->
	<div id="messages"></div>
	
</body>
</html>