var socket = io.connect('http://' + document.domain + ':' + location.port);
$('.counter-count').each(function(){$(this).prop('Counter',0).animate({Counter:$(this).text()},{duration:2000,easing:'swing',step:function(now){$(this).text(Math.ceil(now))}})})
var tweetItem = $('<li class="left clearfix"> <span class="chat-img pull-left"> <img src="$userImage$" class="img-circle" /> </span> <div class="chat-body clearfix"> <div class="header"> <a class="user-url" href="#" ><strong class="primary-font">$username$</strong></a><small class="user-handle"></small> <small class="pull-right text-muted"> <span class="tweet-time">$tweetTime$</span></small> </div> <p class="tweet-text"> $tweetText$ </p> </div> </li>');

function new_tweet(userImageUrl, username, tweetTime, tweetText, userHandle){
    var $clone = tweetItem.clone();

    $('.img-circle', $clone).attr("src",userImageUrl);
    $('.primary-font', $clone).text(username);
    var timeOfTweet = tweetTime.split(" ");
    $('.tweet-time', $clone).text(timeOfTweet[1] + " " + timeOfTweet[2] + "  " + timeOfTweet[3]);
    $('.user-handle', $clone).text("  @" + userHandle);
    $('.user-url', $clone).attr("href","https://twitter.com/" + userHandle);
    $('.tweet-text', $clone).text(tweetText);

    return $clone
}

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
    $('#idConnectionStatus').text("CONNECTED");
});

socket.on('notification', function(data) {
    // new_tweet(userImageUrl, username, tweetTime, tweetText, userUrl, userHandle)
    var tweet = new_tweet(data.tweet.userImage,data.tweet.userName,data.tweet.tweetTime,
                            data.tweet.text, data.tweet.userId);

    $('#idTotalTweetCount').text(data.count.total);

    var positive_p = (data.count.positive/data.count.total)*100;
    //$('#idPositiveBarChart').attr('data-percent',positive_p)
    $('#idPositiveBarChartP').text( positive_p + "%")
    $('#idPositiveTweetCount').text(data.count.positive);

    var neutral_p = (data.count.neutral/data.count.total)*100;
    //$('#idNeutralBarChart').attr('data-percent',neutral_p)
    $('#idNeutralBarChartP').text(neutral_p + "%")
    $('#idNeutralTweetCount').text(data.count.neutral);

    var negative_p = (data.count.negative/data.count.total)*100;
    //$('#idNegativeBarChart').data("percent","60")
    $('#idNegativeBarChartP').text(negative_p + "%")
    $('#idNegativeTweetCount').text(data.count.negative);

    $('#idTweetBoxList').append(tweet);

    // Scroll Fix Needed.
    //$("#idTweetBoxList").animate({ scrollTop: $("#idTweetBoxList").height() }, 1000);
});

$('#idBtnStart').click(function(event){
    event.preventDefault();
    var hashText = $('#idHashTag').val();
    if (hashText == ""){
        alert("Enter Value");
    }
    else{
        socket.emit('fire_start', {data: hashText});
    }
});