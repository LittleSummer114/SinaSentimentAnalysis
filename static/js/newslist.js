

var news_lists = $('.leftWindow .tab li');
var news_contents = $('.leftWindow .content .inner');
function bindNewsEvent(topic_id){
    news_lists.each(function(index_li, li){
        $(this).on('click', function(event){
            if (index_li == 0)
                getNewsListData(topic_id, "getTopNewsSet", '#topnewslist');
            else if (index_li == 1)
                getNewsListData(topic_id, "getTopNewsSet", '#recentnewsList');
            
            news_lists.removeClass('tab-active');
            $(this).addClass('tab-active');
            news_contents.each(function(index_content, content){
                if(index_li === index_content){
                    $(this).show();
                }else{
                    $(this).hide();
                }
            });
        });
    });
}

function getNewsListData(topic_id, url_name, div_name) {
    $.ajax({
        type: "GET",
        url: url_name,
        dataType: 'json',
        data: {
            tid: topic_id
        },
        success: function (data) {
            var wordList = [];
            var len = data.length;
            console.log(len);
            for (var i = 0; i < len; i++) {
                wordList.push(new newsInfoli(data[i], i).create());
            }
            $(div_name).html(wordList.join(""));
        }
    })
}


function newsInfoli(data, i) {
    this.index = i + 1;
    this.nid = data[0];
    this.count = data[1];
    this.title = data[2];
    this.time = data[3];
    this.url = data[4];
    this.body = data[5];
}

newsInfoli.prototype.create = function () {
//    var href_str = '<a href="/comment/?cid=' + this.cid + '">'
//    console.log(href_str);
    result = '<li><div class="title"><h1><span>TOP' + this.index + ': </span>' + this.title + '</h1></div><div class="body">' + this.body + '<a href="' + this.url + '">查看原文</a></div><div class="info">' + '<span class="info-right">评论数:' + this.count + '</span><span class="info-right">' + this.time + '</span></div></li>';
    
    return result;
}