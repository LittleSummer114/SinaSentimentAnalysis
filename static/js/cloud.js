//readCloudData();

//读取csv文件
function readCloudData(){
    d3.csv("../../data/features/cloud_features.csv")
        .row(function(d) {
            return {text: d.feature, size: d.weight/2}; 
        })
        .get(function(error, row) { 
            generateCloudGraph(row);
        });
}

function bindCloudData(topic_id){
    $.ajax({
    type: "GET",
    url: "getFrequentFeatures",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        var featuredata = [];
        for (var i = 0; i < data.length; i++){
            featuredata.push({text: data[i][0], size: data[i][1]/2})
        }
        //console.log(featuredata);
        generateCloudGraph(featuredata);
    }
    })
}

//构造字云
function generateCloudGraph(featuredata){ 
    //画布大小
    var width = 325;
    var height = 325;

    //产生字符集的坐标、旋转角度等
    fill = d3.scale.category20();
    d3.layout.cloud()
        .size([width, height])
        .words(featuredata)
	    //旋转角度：~~的作用是单纯的去掉小数部分，不论正负都不会改变整数部分
        .rotate(function(){
            
            return ~~(Math.random() * 6) * 30 - 90;
        })
        .font("Impact")
        .fontSize(function(d){
            return d.size; 
        })
        .on("end", drawCloudGraph)//结束时运行draw函数
        .start(); 
	  
    // 在svg上绘图
    function drawCloudGraph(words) {
        
        var divid='#WordCloud'
        var svg = d3.select(divid)
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        
        svg.append("g")
//            .attr("transform", "translate(320,240)")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("border","1px solid blue")
            .style("font-size", function(d) {
                return d.size + "px";
            })
            .style("font-family", "微软雅黑")
            .style("font-weight", "bold")
            .style("fill", function(d, i){
                return fill(i);
            })//fill 在前面15行定义为颜色集
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x + width/2, d.y  + height/2] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) {
                return d.text;
            });
        }
}
