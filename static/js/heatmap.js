function bindHeatmapData(topic_id){
    $.ajax({
    type: "GET",
    url: "getHeatmapData",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        
        //读取实体名字
        var entity_name = [];
        for (var i = 0; i < data[0].length; i++){
            entity_name.push({entity: data[0][i]})
        }
        
        //读取时间变量
        var date_name = [];
        for (var i = 0; i < data[1].length; i++){
            date_name.push({date: data[1][i]})
        }
        
        //读取实体相关数据
        var entity_data = [];
        for (var i = 0; i < data[2].length; i++){
            entity_data.push({date_index: data[2][i][0], entity_index: data[2][i][1], weight: data[2][i][2]})
        }
        //console.log(entity_data);
        
        //读取实体名字
        var entity_profile = [];
        for (var i = 0; i < data[3].length; i++){
            entity_profile.push({text: data[3][i][0], size: parseInt(data[3][i][1])})
        }
        //console.log(entity_profile);
        
        
        
        darwHeatmap(entity_name, date_name, entity_data, entity_profile);
    }
    })
}


//getHeatmapEntityCSV();

//读取实体数据
function getHeatmapEntityCSV(){
    //读取实体名字
    d3.csv("../../data/entities/entities.csv")
        .row(function(d) { 
            return { entity: d.entity}; 
        })
        .get(function(error, row) { 
            //console.log(row);
            getHeatmapDateCSV(row);
        });
}

//读取时间变量
function getHeatmapDateCSV(entity_name){
    d3.csv("../../data/entities/date.csv")
        .row(function(d) { 
            return { date: d.date}; 
        })
        .get(function(error, row) { 
            //console.log(row);
            getHeatmapDataCSV(entity_name, row);
        });
}

//读取实体相关数据
function getHeatmapDataCSV(entity_name, date_name){

    //时间格式
    var formatDate = d3.time.format("%Y-%m-%d");
    
    d3.csv("../../data/entities/entities_count.csv")
    .row(function(d) { 
//        var temp_date = formatDate.parse(d.date)
        return { date_index: d.date_index, entity_index: d.entity_index, weight: d.count}; 
    })
    .get(function(error, row) { 
        //console.log(row);
        darwHeatmap(entity_name, date_name, row);
    });
}

//画图函数
function darwHeatmap(entity_name, date_name, entity_data, entity_profile){
    
    var draw_date_num = 30;

    //画布周边的空白
    var margin = {top: 30, right: 50, bottom: 100, left: 60 };

    //画布大小
    var width = 960 - margin.left - margin.right,
        height = 580 - margin.top - margin.bottom;
    
    
    //方格长度、标签长度、颜色变化幅度个数
    var gridSize = Math.floor(width / draw_date_num),
        legendElementWidth = gridSize*2,
        buckets = 9,
        colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]; // alternatively colorbrewer.YlGnBu[9]
    
    var svg = d3.select("#heatmap").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    
    
    //画布大小
    var cloud_width = 315;
    var cloud_height = 455;
    var divid='#entityProfileGraph'
    var cloud_svg = d3.select(divid)
        .append("svg")
        .attr("width", cloud_width)
        .attr("height", cloud_height);
        //.style("border","1px solid blue");
    generateEntityCloudGraph(0);

    
    //纵坐标-实体轴
    var dayLabels = svg.selectAll(".entityLabel")
        .data(entity_name)
        .enter().append("text")
        .text(function (d) { return d.entity; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .attr("font-family", "sans-serif")
        .attr("font-size", "11px")
        .style("text-anchor", "end")
        .style("cursor","pointer")
        .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
        .on('mouseover', function (d,i){
            d3.select(this)
                .attr("fill", "#ff99c4");
            generateEntityCloudGraph(i);
            
        })
        .on('mouseout', function(d,i){
            d3.select(this)
                .attr("fill", "black");
        });
    
    
    
    var draw_entity_data = [];
    var draw_date_name = [];
    for (var i = 0; i < 30; i++){
        draw_date_name.push(date_name[i]);
    }
    for (var i = 0; i < (30)*entity_name.length; i++){
        draw_entity_data.push(entity_data[i]);
    }
    //console.log(draw_entity_data);
    
    //横坐标-时间轴
    var time_lag = 5 //每隔5天显示一个日期
    
    var timeLabels = svg.selectAll(".dayLabel")
            .data(draw_date_name)
            .enter().append("text")
            .attr("class","dayLabel")
            .text(function(d,i) {
                if (i % time_lag == 0)
                    return d.date; 
            })
            .attr("x", function(d, i) {
                if (i % time_lag == 0)
                    return i * gridSize; 
            })
            .attr("y", 0)
            .attr("font-family", "sans-serif")
            .attr("font-size", "11px")
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)");
        
    //拆分成9个的等级的颜色
    var colorScale = d3.scale.quantile()
        .domain([0, buckets - 1, d3.max(entity_data, function (d) { return d.weight; })])
        .range(colors);
    
    //画方格
    var cards = svg.selectAll(".entityHeat")
        .data(draw_entity_data)
        .enter().append("rect")
        .attr("class","entityHeat bordered")
        .attr("x", function(d) { return d.date_index * gridSize; })
        .attr("y", function(d) { return d.entity_index * gridSize; })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", gridSize)
        .attr("height", gridSize)
        .style("fill", function(d) { 
            return colorScale(d.weight); 
        });

//    cards.transition().duration(1000)
//        .style("fill", function(d) { return colorScale(d.weight); });

//    cards.append("title");
//    cards.select("title").text(function(d) { return d.weight; });
    
//    cards.exit().remove();
    
    
    //var change_entity_data = [];
    function changeStartDate(start_day_index) {
        var change_date_name = [];
        for (var i = start_day_index; i < start_day_index+30; i++){
            change_date_name.push(date_name[i]);
        }
        svg.selectAll(".dayLabel")
            .data(change_date_name)
            .text(function(d,i) {
                if (i % time_lag == 0)
                    return d.date; 
            });
        
        draw_entity_data = [];
        for (var i = start_day_index*entity_name.length; i < (start_day_index+30)*entity_name.length; i++){
            draw_entity_data.push(entity_data[i]);
        }
        var heatRect = svg.selectAll(".entityHeat")
            .data(draw_entity_data)
            .style("fill", function(d,i) {
                return colorScale(d.weight); 
        });
        
        
//        svg.selectAll(".entityHeat").remove();
//        
//        //画方格
//        var cards = svg.selectAll(".entityHeat")
//            .attr("class","entityHeat")
//            .data(draw_entity_data, function(d,i) {return d.entity_index+':'+d.date_index;});
//
//        cards.append("title");
//
//        cards.enter().append("rect")
//            .attr("x", function(d) { return d.date_index * gridSize; })
//            .attr("y", function(d) { return d.entity_index * gridSize; })
//            .attr("rx", 4)
//            .attr("ry", 4)
//            .attr("class", "hour bordered")
//            .attr("width", gridSize)
//            .attr("height", gridSize)
//            .style("fill", colors[0]);
//
//        cards.transition().duration(1000)
//            .style("fill", function(d) { return colorScale(d.weight); });
//
//        cards.select("title").text(function(d) { return d.weight; });
//
//        cards.exit().remove();
        
    }
    
    
    //画说明标签
    var legend = svg.selectAll(".legend")
        .data([0].concat(colorScale.quantiles()), function(d) { return d; });

    legend.enter().append("g")
        .attr("class", "legend");

    legend.append("rect")
        .attr("x", function(d, i) { return legendElementWidth * i; })
        .attr("y", (entity_name.length + 1) * gridSize)
        .attr("width", legendElementWidth)
        .attr("height", gridSize / 2)
        .style("fill", function(d, i) { return colors[i]; });

    legend.append("text")
        .attr("class", "mono")
        .text(function(d) { return "≥ " + Math.round(d); })
        .attr("x", function(d, i) { return legendElementWidth * i; })
        .attr("y", (entity_name.length + 2) * gridSize);

    legend.exit().remove();
    
    
    svg.append("text")
        .attr("x", legendElementWidth * 10)
        .attr("y", (entity_name.length + 1) * gridSize+15)
        .attr("text-anchor", "start")
        .style("fill", "#aaa")
        .text("起始日期");
    
    d3.select('#dateselect')
        .selectAll("option")
        .data(date_name)
        .enter()
        .append("option")
        .attr("value", function(d){
            return d.date;
        })
        .text(function(d){
            return d.date;
        });
    
    //修改起始日期
    var select= document.getElementById('dateselect')
    select.onchange=function(){
        var index=select.selectedIndex ;
        //console.log(select.options[index].value);
        changeStartDate(index);
    };
    
    
    //构造字云
    function generateEntityCloudGraph(i){
        temp_entity_profile = []
        for (var j = i*25; j < (i+1)*25; j++){
            temp_entity_profile.push(entity_profile[j]);
        }
        
        d3.select("#entityProfileName")
            .html(entity_name[i].entity);

        //产生字符集的坐标、旋转角度等
        fill = d3.scale.category20();
        d3.layout.cloud()
            .size([cloud_width, cloud_height])
            .words(temp_entity_profile)
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
            cloud_svg.selectAll("text").remove();
            
            cloud_svg.append("g")
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
                    return "translate(" + [d.x + cloud_width/2, d.y  + cloud_height/2] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) {
                    return d.text;
                });
        }
    }
    
}



