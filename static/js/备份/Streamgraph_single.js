var divid = '#div_streamgraph'

readStreamgraphData()

//读取csv文件
function readStreamgraphData(){
    //时间格式
    var formatDate = d3.time.format("%Y-%m-%d");
    
    //画数值图
//    d3.csv("../dataFolder/sentiment/streamgraph.csv")
//    .row(function(d) {
//        return {date:formatDate.parse(d.date), happiness: parseInt(d.happiness), good: parseInt(d.good), anger: parseInt(d.anger), sadness: parseInt(d.sadness), fear: parseInt(d.fear), evil: parseInt(d.evil), surprise: parseInt(d.surprise)}; 
//    })
//    .get(function(error, row) { 
//        console.log(row);
//        darwStreamgraph(row);
//    });
    
    
    //画比例图
    d3.csv("/static/data/sentiment/streamgraphpercent.csv")
    .row(function(d) {
        return {date:formatDate.parse(d.date), happiness: parseFloat(d.happiness), good: parseFloat(d.good), anger: parseFloat(d.anger), sadness: parseFloat(d.sadness), fear: parseFloat(d.fear), evil: parseFloat(d.evil), surprise: parseFloat(d.surprise)}; 
    })
    .get(function(error, row) { 
        console.log(row);
        darwStreamgraph(row);
    });

}

//绘图函数
function darwStreamgraph(streamgraphData){
    
    //画布周边的空白
    var margin = {top: 30, right: 100, bottom: 30, left: 50 };

    //画布大小
    var width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    
    //基本参数
    var n = 7, // number of layers，即情感类型个数
        m = streamgraphData.length; // number of samples per layer,即横轴时间长度
    
    
    //拆分成n个的等级的颜色
    var color = d3.scale.category20();
    
    //var stack = d3.layout.stack().offset("wiggle");
    //var layerData = stack(bumpLayerData(streamgraphData));
    var layerData = bumpLayerData(streamgraphData);
    console.log(layerData);

    
    //x轴的比例尺（时间刻度）
    var xtScale = d3.time.scale()
        .domain(d3.extent(streamgraphData, function(d) { return d.date; }))
        .range([0, width]);
    
    //定义x轴（时间刻度）
    var xAxis = d3.svg.axis()
        .scale(xtScale)
        .orient("bottom");
    
    //定义x轴比例尺（index）
    var x = d3.scale.linear()
        .domain([0, m - 1])
        .range([0, width]);
    
    //定义y轴比例尺
    var max_value = d3.max(layerData, function(layer) { return d3.max(layer, function(d, i) { return d.y0 + 1 * d.y; }); })
    var y = d3.scale.linear()
        .domain([0, max_value])
        .range([height, 0]);
    
    //定义y轴
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    //定义绘图区域
    var area = d3.svg.area()
        .x(function(d) { return x(d.x); })
        .y0(function(d) { return y(d.y0); })
        .y1(function(d) { return y(d.y0 + d.y); });
    

    var svg = d3.select(divid)
        .append("svg")
        .attr("width", width + margin.left + margin.right )
        .attr("height", height+ margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.selectAll("path")
        .data(layerData)
      .enter().append("path")
        .attr("d", area)
        .style("fill", function(d,i) { return color(i); });
    
    //画说明标签
    var sentimentName = ["happiness","good","anger","sadness","fear","evil","surprise"]
    
    //数据说明 Legend	
    var legend = svg.append("g")
        .attr("class", "legend")
        .attr("height", 100)
        .attr("width", 200);

    //颜色序列
	legend.selectAll('rect')
        .data(sentimentName)
        .enter()
        .append("rect")
        .attr("x", width + 10)
        .attr("y", function(d, i){ return 90 + i * 30;})
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i){ return color(i);});
    
    legend.selectAll('text')
        .data(sentimentName)
        .enter()
        .append("text")
        .attr("x", width + 30)
        .attr("y", function(d, i){ return 90+ i * 30 + 9;})
        .attr("font-size", "11px")
        .attr("fill", "black")
        .text(function(d,i) { return d; })
    
    //添加x轴
    svg.append("g")
        .attr("class","axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    
     //添加y轴
    svg.append("g")
        .attr("class","axis")
        .call(yAxis);
    
    
    //数据转换
    function bumpLayerData(streamgraphData){
        var max_value = -1;
        var y0_value = new Array();
        for (var j = 0; j < m; j++)
            y0_value[j] = 0;
        var d = new Array();
        for (var i = 0; i < n; i++)
        {
            d[i] = new Array();
            for (var j = 0; j < m; j++)
            {
                var y_value = 0;
                if (i == 0){
                    y_value = streamgraphData[j].happiness;
                }
                else if(i == 1){
                    y_value = streamgraphData[j].good;
                    y0_value[j] += streamgraphData[j].happiness;
                }
                else if(i == 2){
                    y_value = streamgraphData[j].anger;
                    y0_value[j] += streamgraphData[j].good;
                }
                else if(i == 3){
                    y_value = streamgraphData[j].sadness;
                    y0_value[j] += streamgraphData[j].anger;
                }
                else if(i == 4){
                    y_value = streamgraphData[j].fear;
                    y0_value[j] += streamgraphData[j].sadness;
                }
                else if(i == 5){
                    y_value = streamgraphData[j].evil;
                    y0_value[j] += streamgraphData[j].fear;
                }
                else if(i == 6){
                    y_value = streamgraphData[j].surprise;
                    y0_value[j] += streamgraphData[j].evil;
                }
                
                if (y_value > max_value)
                    max_value = y_value;
                
                var temp_date = {x:j, y: y_value, y0: y0_value[j]};
                d[i][j] = temp_date;
            }
        }
//        console.log(max_value)
        return d;
    }

}


