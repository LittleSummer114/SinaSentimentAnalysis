

var comment_lists = $('.rightWindow .tab li');
var comment_contents = $('.rightWindow .content .inner');
function bindCommentEvent(topic_id){
    comment_lists.each(function(index_li, li){
        $(this).on('click', function(event){
            if (index_li == 0)
                getCommentListData(topic_id, "getBestCommentSet", '#bestcommentlist');
            else if (index_li == 1)
                getCommentListData(topic_id, "getTopCommentSet", '#topcommentlist');
            

            comment_lists.removeClass('tab-active');
            $(this).addClass('tab-active');
            comment_contents.each(function(index_content, content){
                if(index_li === index_content){
                    $(this).show();
                }else{
                    $(this).hide();
                }
            });
        });
    });
}


function getCommentListData(topic_id, url_name, div_name) {
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
                wordList.push(new commentInfoli(data[i], i).create());
            }
            $(div_name).html(wordList.join(""));
        }
    })
}


function commentInfoli(data, i) {
    this.index = i + 1;
    this.cid = data[0];
    this.count = data[1];
    this.area = data[2];
    this.time = data[3];
    this.name = data[4];
    this.body = data[5];
}

commentInfoli.prototype.create = function () {
//    var href_str = '<a href="/comment/?cid=' + this.cid + '">'
//    console.log(href_str);
    result = '<li><div class="title"><h1><span>TOP' + this.index + ': </span>' + this.name + '</h1></div><div class="body">' + this.body + '<a href="/comment/?cid=' + this.cid + '">查看详细分析</a></div><div class="info">' + '<span class="info-right">点赞数:' + this.count + '</span><span class="info-right">来自:' + this.area + '</span><span class="info-right">' + this.time + '</span></div></li>';
    
    return result;
}