//定义基本画布
var margin = {top: 20, right: 40, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var formatDate = d3.time.format("%Y-%m-%d");

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


//读取csv文件
d3.csv("../../data/dayCount/day_count.csv")
    .row(function(d) {
        return {date: formatDate.parse(d.date), news_num: d.news_num, comment_num: d.comment_num}; 
    })
    .get(function(error, row) {
//        console.log(row);
        darwLineGraph(row);
    });

//绘制直线图
function darwLineGraph(linedata){
    
    var xScale = d3.time.scale()
        .domain(d3.extent(linedata, function(d) { return d.date; }))
        .range([0, width]);
    
    var ylScale = d3.scale.linear()
        .domain([0, d3.max(linedata, function(d) { return 1 * d.news_num; })])
        .range([height, 0]);
    
    var yrScale = d3.scale.linear()
        .domain([0, d3.max(linedata, function(d) { return 1 * d.comment_num; })])
        .range([height, 0]);

    //x轴的比例尺
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom");

    //左y轴的比例尺
    var ylAxis = d3.svg.axis()
        .scale(ylScale)
        .orient("left");
    
    //右y轴的比例尺
    var yrAxis = d3.svg.axis()
        .scale(yrScale)
        .orient("right");

    //添加坐标轴
    svg.append("g")
        .attr("class","axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
    
    svg.append("g")
        .attr("class", "y axis")
        .call(ylAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("News Number");
    
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + width + ",0)")
        .call(yrAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -10)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Comment Number");

    //新闻数据-折线图
//    var news_line = d3.svg.line()
//        .x(function(d) { return xScale(d.date); })
//        .y(function(d) { return ylScale(d.news_num); });
//
//    svg.append("path")
//        .datum(linedata)
//        .attr("class", "line")
//        .attr("d", news_line);
    
    //新闻数据-柱状图
    var rect_width = 10
    svg.selectAll("rect")
        .data(linedata)
        .enter()
        .append("rect")
        .attr("x",function(d,i){
             return xScale(d.date) - rect_width/2;
        })
        .attr("y",function(d){
             return ylScale(d.news_num);   //在这里用比例尺
        })
        .attr("width",rect_width)
        .attr("height",function(d){
             return height - ylScale(d.news_num);   //在这里用比例尺
        })
        .attr("fill","steelblue");
    
    //评论数据-折线图
    var comment_line = d3.svg.line()
        .x(function(d) { return xScale(d.date); })
        .y(function(d) { return yrScale(d.comment_num); });

    svg.append("path")
        .datum(linedata)
        .attr("class", "line")
        .style("stroke","red")
        .attr("d", comment_line);
}

