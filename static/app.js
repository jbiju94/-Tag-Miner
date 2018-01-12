var socket = io.connect('http://' + document.domain + ':' + location.port);

$(document).ready(function()    {

});

socket.on('connect', function() {
    console.log("Client: Connection Request");
    socket.emit('client_connected', {data: 'New client!'});
});

socket.on('connection_accepted', function() {
    console.log("Server: Connection Accepted");
});

socket.on('notification', function() {
    console.log("New Notification");
});

$('#idBtnStart').click(function(){
    console.log("Fire Service");
    socket.emit('fire_start', {data: 'New client!'});
});