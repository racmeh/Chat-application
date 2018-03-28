<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>WebSocket Connection Testing</title>

    <style>
        li { list-style: none; }
    </style>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script><!-- Importing jquery -->
    <script>
   $(document).ready(function() {
            if (!window.WebSocket) {
                if (window.MozWebSocket) {//Checking for web socket support
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
                }
            }
            ws = new WebSocket('ws://192.168.43.29:8080/websocket');//establishing web socket connection on given url
            ws.onopen = function(evt) {//Defining what happens when web socket connection opens
                $('#messages').append('<li>Connected to server</li>');
                $('#btn2').hide();//Hiding btn2
                $('#btn2').trigger("click");//Clicking btn2
            }
            var str="";var str1="";var n=0;
            ws.onmessage = function(evt) {//Defining what happens when message is received
            $('#messages').append('<li>' + evt.data + '</li>');
            }
            $('#btn2').click(function(){//This button is for sending user status as 'Online' as well as current date time
            var now = new Date(Date.now());
            var formatted = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
            ws.send("Online");//Sending user status as Online
            ws.send(formatted);
            });     
            $('#btn3').click(function(){
            ws.send("Offline1234abc5678def90ghij");//Sending a unique string to determine if Signout is pressed
            });
            $('#btn').click(function(){//Defining what happens when the button is clicked
            var now1 = new Date(Date.now());//Getting time
            var formatted1 = now1.getHours() + ":" + now1.getMinutes() + ":" + now1.getSeconds();//Formatting time in the correct manner
            ws.send($('#ipt1').val());//sending message to server
            ws.send($('#ipt2').val());//sending receiver's name to server
            ws.send(formatted1);//sending the datetime
            });
            setTimeout(function(){ ws.close(); }, 3600000);//Timeout function to expire the session in an hour
            ws.onclose = function()//Defining what happens when web socket connection closes
            {
            $('#messages').append('<li>' + "Connection is closed..." + '</li>'); 
            }
        });
    </script>
</head>
<body>
<h2>Chat Section</h2>
<button id="btn2">Data On</button><br/>

<h3>You</h3>
<input id="ipt1" type="text" name="msg" placeholder="Message"><!-- Message will be inserted -->
<input id="ipt2" type="text" name="rec" placeholder="Receiver"><!-- Receiver's name is inserted -->
<button id="btn">Send msg!</button><br/><br/><!-- Sending message through web socket to server then to receiver -->
<button id="btn3">Signout</button><br/><!-- For logging out -->
<br/>
<div id="messages"></div><!-- Importing message module -->
</body>
</html>