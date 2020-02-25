
function bindNewsInfo(topic_id){
    $.ajax({
    type: "GET",
    url: "getEventListData",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        //console.log(data);
        var eventinfodata = [];
        for (var i = 0; i < data.length; i++){
            eventinfodata.push({date: data[i][0], dateindex: parseInt(data[i][1]), title: data[i][2], leader: data[i][3], comment_num: parseInt(data[i][4]), url: data[i][5]})
        }
        //console.log(eventinfodata)
        drawEventInfo(eventinfodata);
    }
    })
}


function drawEventInfo(eventinfodata) {
    var color = d3.scale.category20();
    
    var textList = [];
    for (var i = 1; i < eventinfodata.length; i++) {
        var textEvent = '<li>' + eventinfodata[i].date +' '+ eventinfodata[i].title + '</li>';
        textList.push(textEvent);
    }
    d3.select("#EventList")
        .style("background", color(0))
        .select("ul")
        .html(textList.join(""));
    
    d3.select("#EventInfo")
        .html(getEventInfoText(0));
    
    
    var event_list = d3.selectAll("#EventList li")
        .on("mouseover", function (d, i) {
            event_list.style("opacity", 0.2);
            d3.select(this).style("opacity", 1.0);
            
            d3.select("#EventInfo")
                .html(getEventInfoText(i));
        })
        .on("mouseout", function (d, i) {
            event_list.style("opacity", 1.0);
        })
        .on("click", function (d, i) {
            window.open(eventinfodata[i].url)
        });
    
    
    function getEventInfoText(i) {
        var EventInfoText = '<div class = "title">' + eventinfodata[i].title + '</div><div class = "date">' + eventinfodata[i].date + '</div><div class = "abstract">' + eventinfodata[i].leader + '</div><div class = "otherinfo">评论数量：' + eventinfodata[i].comment_num + '</div><div class = "otherinfo"><a href='+ eventinfodata[i].url + '>查看原文</a></div><div class = "eventweight"><a href='+'>事件影响力：' + eventinfodata[i].comment_num + '</div>';
        return EventInfoText;
    }

}
