var divid = '#div_eventDecreaseRate'

readEventDecreaseRateData()

//读取csv文件
function readEventDecreaseRateData(){
    //时间格式
    var formatDate = d3.time.format("%Y-%m-%d");
    
    //画数值图
    d3.csv("../dataFolder/representNews/eventDecreaseRate_single.csv")
    .row(function(d) {return {date: formatDate.parse(d.date), comment_num: d.comment_num}; 
    })
    .get(function(error, row) { 
        console.log(row);
        darwEventDecreaseRateraph(row);
    });
    

}

//绘图函数
function darwEventDecreaseRateraph(eventData){
    
    //画布周边的空白
    var margin = {top: 30, right: 30, bottom: 30, left: 50 };

    //画布大小
    var width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    
    

    //x轴的比例尺（时间刻度）
    var xtScale = d3.time.scale()
        .domain(d3.extent(eventData, function(d) { return d.date; }))
        .range([0, width]);
    
    //定义y轴比例尺
    var yScale = d3.scale.linear()
        .domain([0, d3.max(eventData, function(d) { return 1 * d.comment_num; })])
        .range([height, 0]);

    //x轴的比例尺
    var xAxis = d3.svg.axis()
        .scale(xtScale)
        .orient("bottom");

    //y轴的比例尺
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");
    
    
    //dingyisvg
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    
    //评论数据-折线图
    var comment_line = d3.svg.line()
        .x(function(d) { return xtScale(d.date); })
        .y(function(d) { return yScale(d.comment_num); });

    svg.append("path")
        .datum(eventData)
        .attr("class", "line")
        .style("stroke","red")
        .attr("d", comment_line);
    
    
    //添加x轴
    svg.append("g")
        .attr("class","axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    
     //添加y轴
    svg.append("g")
        .attr("class","axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Comment Number");
    

}


