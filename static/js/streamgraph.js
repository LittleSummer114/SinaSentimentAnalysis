function bindSentimentData(topic_id, streamtype){
    //时间格式
    var formatDate = d3.time.format("%Y-%m-%d");
    
    
    $.ajax({
    type: "GET",
    url: "getSentimentData",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        //扇形图
        //console.log(data);
        
        var temp_sum = 0;
        for (var i = 0; i < data[0].length; i++){
            temp_sum += parseFloat(data[0][i][1]);
        }
        var peichartdata = [];
        for (var i = 0; i < data[0].length; i++){
            peichartdata.push({name: data[0][i][0], percent: parseFloat(data[0][i][1]/temp_sum*100).toFixed(2)})
        }
        
        
        var streamgraphdata = [];
        var percentdata = [];
        
        //画数值图
        for (var i = 0; i < data[1].length; i++){
            streamgraphdata.push({date:formatDate.parse(data[1][i][0]),date_str:data[1][i][0], happiness: parseFloat(data[1][i][2]), good: parseFloat(data[1][i][3]), anger: parseFloat(data[1][i][4]), sadness: parseFloat(data[1][i][5]), fear: parseFloat(data[1][i][6]), evil: parseFloat(data[1][i][7]), surprise: parseFloat(data[1][i][8])})
        }
        
        //画比例图
        for (var i = 0; i < data[1].length; i++){

            var temp_sum = 0;
            for (var j = 0; j < 7; j++){
                data[1][i][j+2] += 1;
                temp_sum += parseFloat(data[1][i][j+2]);
            }

            percentdata.push({date:formatDate.parse(data[1][i][0]), date_str:data[1][i][0], happiness: parseFloat(data[1][i][2]/temp_sum), good: parseFloat(data[1][i][3]/temp_sum), anger: parseFloat(data[1][i][4]/temp_sum), sadness: parseFloat(data[1][i][5]/temp_sum), fear: parseFloat(data[1][i][6]/temp_sum), evil: parseFloat(data[1][i][7]/temp_sum), surprise: parseFloat(data[1][i][8]/temp_sum)})
        }
        drawSentimentGraph(peichartdata, streamgraphdata, percentdata, streamtype);
    }})
}

function drawSentimentGraph(pieData, streamgraphdata, percentdata, streamtype) {
    //console.log(pieData);
    //console.log(streamgraphdata);
    var divid = '#piechart'
    
    //画布周边的空白
    var margin = {top: 30, right: 50, bottom: 30, left: 50 };

    //画布大小
    var legend_width = 80;
    var pie_width = 380;
    var pie_height = 340;
    var piesvg_width = pie_width - margin.left - margin.right, //200是legend的长度
        piesvg_height = pie_height + legend_width - margin.top - margin.bottom;

    //扇形半径
    var radius = Math.min(piesvg_width, piesvg_height) / 2;

    //颜色选择器
//    var color = d3.scale.category20();
    
    var color = ["#FFFF00","#ADFF2F", "FF0000","#C0C0C0","#00008B","#DC143C","#800080"];
    
//    var color = ["#ffea00", "#00cd00", "#bd0000", "#9b9b9b", "#25ceff", "#000000", "#ff9000"];
    
//    var color = d3.scale.ordinal()
//        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
    
    //扇形区间
    var arc = d3.svg.arc()
        .outerRadius(radius)
        .innerRadius(0);

    //标签扇形
    var labelArc = d3.svg.arc()
        .outerRadius(radius - 80)
        .innerRadius(radius - 80);
    
    //扇形数据整合
    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) { return d.percent; });

    var pie_svg = d3.select(divid)
        .append("svg")
        .attr("width", piesvg_width + margin.left + margin.right )
        .attr("height", piesvg_height + margin.top + margin.bottom)
        //.attr("style","border:2px solid black")
      .append("g")
        .attr("transform", "translate(" + (pie_width) / 2 + "," + (pie_height) / 2 + ")");
    
    //显示扇形
    var g = pie_svg.selectAll(".arc")
        .data(pie(pieData))
        .enter().append("g")
        .attr("class", "arc");

    //圈出扇形的边框
    g.append("path")
        .attr("d", arc)
        .style("fill", function(d,i) { return color[i]; });
    
    //显示文字
//    g.append("text")
//        .attr("transform", function(d) { 
//            //console.log(labelArc.centroid(d));
//            return "translate(" + labelArc.centroid(d) + ")"; 
//        })
//        .attr("dy", ".35em")
//        .text(function(d) { return d.data.name; })
//        .attr("fill", "white");
    
    
    
    
    //数据说明 Legend	
    var legend = pie_svg.append("g")
        .attr("class", "legend")
        .attr("height", 100)
        .attr("width", 200);
    
    var extra_width = 45;
	//Create colour squares
	legend.selectAll('rect')
        .data(pieData)
        .enter()
        .append("rect")
        .attr("x", function(d, i){ return extra_width + i * 30 - piesvg_width/2 + 3 ;} )
        .attr("y", pie_height/2 + 20)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i){ return color[i];});
    
	//Create text next to squares
	legend.selectAll('text')
        .data(pieData)
        .enter()
        .append("text")
        .attr("x", function(d, i){ return extra_width + i * 30 - piesvg_width/2;})
        .attr("y", pie_height/2 + 50)
        .attr("font-size", "16px")
        .attr("fill", "black")
        .style("cursor","pointer")
        .text(function(d) { return d.name; })
        .on('mouseover', function (d, i){
            var change_arc = g.filter(function(ed){
                if (ed.data.name == d.name){
                    return true;
                }
            })
            
            g.transition()
                .duration(500)
                .style("fill-opacity", 0.3);
                
            change_arc 
                .transition()
                .duration(500)
                .style("fill-opacity", 1.0)
                .attr("stroke","#000")
                .attr("stroke-width",1);
        
            change_arc.append("text")
                .attr("transform", function(d) {
                    return "translate(" + labelArc.centroid(d) + ")"; 
                })
                .attr("dy", ".35em")
                .text(function(d) {
                    p_str = d.data.percent + "%";
                    return p_str; 
                })
                .attr("fill", "red");
        
        
        
            change_path = stream_svg.selectAll("path").filter(function(nd, ni){
                if (ni != i)
                    return true;
            })
            change_path
                .style("fill-opacity", 0.02);
        
        })
        .on('mouseout', function(){
            //恢复原样
			g.transition()
                .duration(500)
                .style("fill-opacity", 1.0)
                .attr("stroke-width",0);
        
            g.selectAll("text")
                .text(function(d) { return ""; });
        
            stream_svg.selectAll("path")
                .style("fill-opacity", 1.0);
		});	
    
    

    //画布周边的空白
    var stream_margin = {top: 20, right: 50, bottom: 30, left: 50 };
    
    //情感流图大小
    var stream_width = 860 - stream_margin.left - stream_margin.right,
        stream_height = 420 - stream_margin.top - stream_margin.bottom;
    
    var stream_divid = '#div_streamgraph'
    var stream_svg = d3.select(stream_divid)
            .append("svg")
            .attr("width", stream_width + stream_margin.left + stream_margin.right )
            .attr("height", stream_height+ stream_margin.top + stream_margin.bottom)
            .append("g")
            .attr("transform", "translate(" + stream_margin.left + "," + stream_margin.top + ")");

    if (streamtype == 0)
        darwStreamgraph_p(streamgraphdata);
    else
        darwStreamgraph_v(streamgraphdata);
    
    //绘图函数
    function darwStreamgraph_v(streamgraphData){
        //基本参数
        var n = 7, // number of layers，即情感类型个数
            m = streamgraphData.length; // number of samples per layer,即横轴时间长度


        //拆分成n个的等级的颜色
        //var color = d3.scale.category20();

        //var stack = d3.layout.stack().offset("wiggle");
        //var layerData = stack(bumpLayerData(streamgraphData));

        var upLayerData = bumpUpLayerData(streamgraphData);
        var downLayerData = bumpDownLayerData(streamgraphData);
    //    console.log(upLayerData);
    //    console.log(downLayerData);


        //x轴的比例尺（时间刻度）
        var xtScale = d3.time.scale()
            .domain(d3.extent(streamgraphData, function(d) { return d.date; }))
            .range([0, stream_width]);

        //定义x轴（时间刻度）
        var xAxis = d3.svg.axis()
            .scale(xtScale)
            .orient("bottom");

        //定义x轴（index）
        var x = d3.scale.linear()
            .domain([0, m - 1])
            .range([0, stream_width]);

        //定义上层y轴
        var max_up_value = d3.max(upLayerData, function(layer) { return d3.max(layer, function(d, i) { return d.y0 + 1 * d.y; }); })
        var y_up = d3.scale.linear()
            .domain([0, max_up_value])
            .range([stream_height/2, 0]);

        //定义下层y轴
        var max_down_value = d3.max(downLayerData, function(layer) { return d3.max(layer, function(d, i) { return d.y0 + 1 * d.y; }); })
        var y_down = d3.scale.linear()
            .domain([0, max_down_value])
            .range([stream_height/2, stream_height]);

        //定义绘图区域
        var area_up = d3.svg.area()
            .x(function(d) { return x(d.x); })
            .y0(function(d) { return y_up(d.y0); })
            .y1(function(d) { return y_up(d.y0 + d.y); })
            .interpolate("cardinal");
        
        var area_down = d3.svg.area()
            .x(function(d) { return x(d.x); })
            .y0(function(d) { return y_down(d.y0); })
            .y1(function(d) { return y_down(d.y0 + d.y); })
            .interpolate("cardinal");


        //绘制上层
        stream_svg.selectAll("path_up")
            .data(upLayerData)
          .enter().append("path")
            .attr("d", area_up)
            
            .style("fill", function(d,i) { return color[i]; });


        //绘制下层
        stream_svg.selectAll("path_down")
            .data(downLayerData)
          .enter().append("path")
            .attr("d", area_down)
            .style("fill", function(d,i) { return color[i+2]; });

        //画说明标签
        //var sentimentName = ["happiness","good","anger","sadness","fear","evil","surprise"];
        var sentimentName = ["乐","好","怒","哀","惧","恶","惊"];

        //添加x轴
        stream_svg.append("g")
            .attr("class","axis")
            .attr("transform", "translate(0," + stream_height/2 + ")")
            .call(xAxis);
        
        addTipPie();
        function addTipPie() {
            //添加交互饼图
            var pieTip = d3.select("#div_streamgraph")
                .append("div")
                .attr("class", "pieTip")
                .style("opacity", 0);


            var svgPie = pieTip.append("svg")
                .attr("width", 100)
                .attr("height", 100)
                .append("g")
                .attr("transform", "translate(50,50)");

            var tipLine = stream_svg.append("g")
                .attr("class", "tipLine")
                .append("line")
                .style("opacity", 0);

            var interval = xtScale(24 * 3600 * 1000) - xtScale(0);

            var pie_arc = d3.svg.arc()
                .outerRadius(50)
                .innerRadius(0);

            var pie = d3.layout.pie();


            //标签扇形
            var pie_labelArc = d3.svg.arc()
                .outerRadius(20)
                .innerRadius(20);


            d3.select("#div_streamgraph")
                .on("mousemove", function () {

                    var x = d3.mouse(this)[0];
                    var y = d3.mouse(this)[1];
                    var tip_x;
                    var tip_y;
                    var date;
                    var date_str;
                    var percentJson;

                    streamgraphData.forEach(function (d, i) {
                        if (Math.abs(xtScale(d.date) + stream_margin.left - x) < interval / 2) {
                            date = d.date;
                            date_str = d.date_str;
                            tip_x = xtScale(d.date);
                            return;
                        }
                    });


                    pieTip.selectAll("text").remove();
                    pieTip.append("text")
                        .attr("x",  tip_x + stream_margin.left + 20 + "px")
                        .attr("y", stream_margin.top + "px")
                        .attr("text-anchor", "start")
                        .style("font-size", "10px")
                        .style("fill", "#aaa")
                        .text(date_str);

                    if (date) {

                        tipLine.attr("x1", tip_x)
                            .attr("x2", tip_x)
                            .attr("y2", stream_height)
                            .style("opacity", 1.0);

                        pieTip.style("left", tip_x + stream_margin.left + 20 + "px")
                            .style("top", stream_margin.top + stream_height / 5 + "px")
                            .style("opacity", 1.0);


                        percentdata.forEach(function (d, i) {
                            if (d.date - date == 0) {
                                percentJson = d;
                                return;
                            }
                        });

                        var pieData = [];
                        pieData.push(percentJson.good);
                        pieData.push(percentJson.anger);
                        pieData.push(percentJson.sadness);
                        pieData.push(percentJson.fear);
                        pieData.push(percentJson.evil);
                        pieData.push(percentJson.surprise);

                        //显示扇形
                        var g = svgPie.selectAll("path")
                            .data(pie(pieData));


                        g.enter().append("path");
                        g.exit().remove();
                        
                       
//                        var g = svgPie.selectAll(".arc")
//                                    .data(pie(pieData))
//                                    .enter().append("g")
//                                    .attr("class", "arc");
//                        g.append("path")
//                            .attr("d", pie_arc)
//                            .style("fill", function(d,i) { return color[i]; });

                        g.attr("d", pie_arc)
                            .style("fill", function (d, i) {
                                return color[i];
                            })
                            .style("stroke", "none");
                        
                        g.selectAll("text").remove();
                        g.append("text")
                            .attr("transform", function(d) { 
                                return "translate(" + pie_labelArc.centroid(d) + ")"; 
                            })
                            .attr("dy", ".35em")
                            .style("font-size", "10px")
                            .text(function(d) { 
                                //console.log(parseFloat(d.data*100).toFixed(2));
                                return parseFloat(d.data*100).toFixed(2) + "%"; 
                            })
                            .attr("fill", "black");


                    }
                })
                .on("mouseout", function () {
                    tipLine.style("opacity", 0);
                    pieTip.style("opacity", 0);
    //                tipLine.remove();
    //                pieTip.remove();
                });
        }
        

        //数据转换
        function bumpLayerData(streamgraphData){
            var max_value = -1;
            var d = new Array();
            for (var i = 0; i < n; i++)
            {
                d[i] = new Array();
                var y0_value = 0;
                for (var j = 0; j < m; j++)
                {
                    var y_value = 0;
                    if (i == 0){
                        y_value = streamgraphData[j].happiness;
                    }
                    else if(i == 1){
                        y_value = streamgraphData[j].good;
                        y0_value = streamgraphData[j].happiness;
                    }
                    else if(i == 2){
                        y_value = streamgraphData[j].anger;
                        y0_value = streamgraphData[j].good;
                    }
                    else if(i == 3){
                        y_value = streamgraphData[j].sadness;
                        y0_value = streamgraphData[j].anger;
                    }
                    else if(i == 4){
                        y_value = streamgraphData[j].fear;
                        y0_value = streamgraphData[j].sadness;
                    }
                    else if(i == 5){
                        y_value = streamgraphData[j].evil;
                        y0_value = streamgraphData[j].fear;
                    }
                    else if(i == 6){
                        y_value = streamgraphData[j].surprise;
                        y0_value = streamgraphData[j].evil;
                    }

                    if (y_value > max_value)
                        max_value = y_value;

                    var temp_date = {x:j, y: y_value, y0: y0_value};
                    d[i][j] = temp_date;
                }
            }
    //        console.log(max_value)
            return d;
        }


        //数据转换(上层)
        function bumpUpLayerData(streamgraphData){
            var d = new Array();
            for (var i = 0; i < 2; i++)
            {
                d[i] = new Array();
                var y0_value = 0;
                for (var j = 0; j < m; j++)
                {
                    var y_value = 0;
                    if (i == 0){
                        y_value = streamgraphData[j].happiness;
                    }
                    else if(i == 1){
                        y_value = streamgraphData[j].good;
                        y0_value = streamgraphData[j].happiness;
                    }
                    var temp_date = {x:j, y: y_value, y0: y0_value};
                    d[i][j] = temp_date;
                }
            }
            return d;
        }


        //数据转换(下层)
        function bumpDownLayerData(streamgraphData){
            var d = new Array();
            var y0_value = new Array();
            for (var j = 0; j < m; j++)
            {
                y0_value[j] = 0
            }

            for (var i = 0; i < 5; i++)
            {
                d[i] = new Array();
                for (var j = 0; j < m; j++)
                {
                    var y_value = 0;
                    if(i == 0){
                        y_value = streamgraphData[j].anger;
                    }
                    else if(i == 1){
                        y_value = streamgraphData[j].sadness;
                        y0_value[j] += streamgraphData[j].anger;
                    }
                    else if(i == 2){
                        y_value = streamgraphData[j].fear;
                        y0_value[j] += streamgraphData[j].sadness;
                    }
                    else if(i == 3){
                        y_value = streamgraphData[j].evil;
                        y0_value[j] += streamgraphData[j].fear;
                    }
                    else if(i == 4){
                        y_value = streamgraphData[j].surprise;
                        y0_value[j] += streamgraphData[j].evil;
                    }
                    var temp_date = {x:j, y: y_value, y0: y0_value[j]};
                    d[i][j] = temp_date;
                }
            }
            return d;
        }
    }


    //绘图函数
    function darwStreamgraph_p(streamgraphData){
        

        //基本参数
        var n = 7, // number of layers，即情感类型个数
            m = streamgraphData.length; // number of samples per layer,即横轴时间长度


        //拆分成n个的等级的颜色
        //var color = d3.scale.category20();

        //var stack = d3.layout.stack().offset("wiggle");
        //var layerData = stack(bumpLayerData(streamgraphData));
        var layerData = bumpLayerData(streamgraphData);
        //console.log(layerData);


        //x轴的比例尺（时间刻度）
        var xtScale = d3.time.scale()
            .domain(d3.extent(streamgraphData, function(d) { return d.date; }))
            .range([0, stream_width]);

        //定义x轴（时间刻度）
        var xAxis = d3.svg.axis()
            .scale(xtScale)
            .orient("bottom");

        //定义x轴比例尺（index）
        var x = d3.scale.linear()
            .domain([0, m - 1])
            .range([0, stream_width]);

        //定义y轴比例尺
        var max_value = d3.max(layerData, function(layer) { return d3.max(layer, function(d, i) { return d.y0 + 1 * d.y; }); })
        var y = d3.scale.linear()
            .domain([0, max_value])
            .range([stream_height, 0]);

        //定义y轴
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        //定义绘图区域
        var area = d3.svg.area()
            .x(function(d) { return x(d.x); })
            .y0(function(d) { return y(d.y0); })
            .y1(function(d) { return y(d.y0 + d.y); });
        

        stream_svg.selectAll("path")
            .data(layerData)
          .enter().append("path")
            .attr("d", area)
            .style("fill", function(d,i) { return color[i]; });

        //画说明标签
        //var sentimentName = ["happiness","good","anger","sadness","fear","evil","surprise"];
        var sentimentName = ["乐","好","怒","哀","惧","恶","惊"];

        

        //添加x轴
        stream_svg.append("g")
            .attr("class","axis")
            .attr("transform", "translate(0," + stream_height + ")")
            .call(xAxis);

         //添加y轴
        stream_svg.append("g")
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
    
}



