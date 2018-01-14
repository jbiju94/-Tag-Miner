var socket = io.connect('http://' + document.domain + ':' + location.port);

$(document).ready(function()    {
    barChart();

    $(window).resize(function(){
        barChart();
    });

    function barChart(){
        $('.bar-chart').find('.item-progress').each(function(){
            var itemProgress = $(this),
            itemProgressWidth = $(this).parent().width() * ($(this).data('percent') / 100);
            itemProgress.css('width', itemProgressWidth);
        });
    };
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

$('#idBtnStart').click(function(event){
    event.preventDefault();
    var hashText = $('#idHashTag').val();
    console.log("Fire Service");
    if (hashText == ""){
        alert("Enter Value");
    }
    else{
        socket.emit('fire_start', {data: hashText});
    }
});