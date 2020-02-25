//
//
//var news_lists = $('.leftWindow .tab li');
//var news_contents = $('.leftWindow .content .inner');
//function bindTopicList(topic_id){
//    news_lists.each(function(index_li, li){
//        $(this).on('click', function(event){
//            if (index_li == 0)
//                getNewsListData(topic_id, "getTopNewsSet", '#topnewslist');
//            else if (index_li == 1)
//                getNewsListData(topic_id, "getTopNewsSet", '#recentnewsList');
//            
//            news_lists.removeClass('tab-active');
//            $(this).addClass('tab-active');
//            news_contents.each(function(index_content, content){
//                if(index_li === index_content){
//                    $(this).show();
//                }else{
//                    $(this).hide();
//                }
//            });
//        });
//    });
//}

var TopicTypeNameList = ['财经', '社会', '民生', '军事', '政治'];

function getTopicListData() {
    $.ajax({
        type: "GET",
        url: "getTopicList",
        dataType: 'json',
        data: {
        },
        success: function (data) {
            //console.log(data);
            var dataList = [];
            for (var i = 0; i < data.length; i++) {
                dataList.push(new topicInfoli(data[i], i).create());
            }
            $('#topiclist').html(dataList.join(""));
        }
    })
}


function topicInfoli(data, i) {
    this.index = i + 1;
    this.id = data[0];
    this.name = data[1];
    this.keywords = data[2];
    this.type = TopicTypeNameList[parseInt(data[3])];
    this.date = data[4];
    this.abstrct = data[5];
    this.status = data[6];
    this.influence = data[7];
}

topicInfoli.prototype.create = function () {
//    var href_str = '<a href="/comment/?cid=' + this.cid + '">'
//    console.log(href_str);
    result = '<li><div class="block"><div class="head"><a href="/topic/?tid=' + this.id + '">' + this.name + '</a><div class="type">' + this.type + '</div><div class="situation">' + this.status +'</div><div class="otherinfo">' + this.date +'</div><div class="otherinfo">关键词：' + this.keywords + '</div></div><div class="body">'+this.abstrct+'</div></div></li>';
    
    return result;
}