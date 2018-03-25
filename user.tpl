<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>WebSocket Connection Testing</title>

    <style>
        li { list-style: none; }
    </style>

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
            ws = new WebSocket('ws://localhost:8080/websocket');
            ws.onopen = function(evt) {
                $('#messages').append('<li>Connected to server</li>');
                $('#btn2').hide();
                $('#btn2').trigger("click");
            }
            ws.onmessage = function(evt) {
                $('#messages').append('<li>' + evt.data + '</li>');
            }
            $('#btn1').click(function(){
            var now2 = new Date(Date.now());
            var formatted2 = now2.getHours() + ":" + now2.getMinutes() + ":" + now2.getSeconds();
            });
            $('#btn2').click(function(){
            var now = new Date(Date.now());
            var formatted = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
            ws.send("Online");
            ws.send(formatted);
            });            
            $('#btn').click(function(){
            var now1 = new Date(Date.now());
            var formatted1 = now1.getHours() + ":" + now1.getMinutes() + ":" + now1.getSeconds();
            ws.send($('#ipt1').val());
            ws.send($('#ipt2').val());
            ws.send(formatted1);
            });
            ws.onclose = function()
            {
            $('#messages').append('<li>' + "Connection is closed..." + '</li>'); 
            }
        });
    </script>
</head>
<body>
    <h2>WebSocket Connection Testing</h2>
<button id="btn2">Data On</button><br/>
<br/>

<input id="ipt1" type="text" name="msg" value="msg" placeholder="Message">
<input id="ipt2" type="text" name="rec" value="abc" placeholder="Receiver">
<button id="btn">Send msg!</button><br/>

<br/>
<div id="messages"></div>
</body>
</html>