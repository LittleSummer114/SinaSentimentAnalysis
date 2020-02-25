

function bindEventEvolutionData(topic_id){
    //时间格式
    var formatDate = d3.time.format("%Y-%m-%d");
    
    
    $.ajax({
    type: "GET",
    url: "getEventEvolutionData",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        //console.log(data);
        var entity_name = [];
        for (var i = 0; i < data[0].length; i++){
        //for (var i = 0; i < 10; i++){
            entity_name.push({entity: data[0][i]})
        }
        //console.log(entity_name);
        
        var node_data = [];
        for (var i = 0; i < data[1].length; i++){
            node_data.push({p_x: data[1][i][1], p_y: data[1][i][2], p_c: data[1][i][1], date: formatDate.parse(data[1][i][0]), weight: data[1][i][3], name: data[1][i][4]})
        }
        //console.log(node_data);
        
        var edge_data = [];
        for (var i = 0; i < data[2].length; i++){
            edge_data.push({source: data[2][i][0], target: data[2][i][1], weight: data[2][i][2]})
        }
        //console.log(edge_data);
        
        var entity_event_data = []
        for (var i = 0; i < data[3].length; i++){
            entity_event_data.push({entity_index: data[3][i][0], event_index: data[3][i][1]})
        }
        //console.log(entity_event_data);
        
        var date_count_data = []
        for (var i = 0; i < data[4].length; i++){
            date_count_data.push({date: formatDate.parse(data[4][i][0]), news_num: data[4][i][1], comment_num: data[4][i][2], num_date: String(data[4][i][0])})
        }
        //console.log(date_count_data);
    
        drawEventGraph(node_data, edge_data, entity_name, entity_event_data, date_count_data);
    }
    })
}


//绘图
function drawEventGraph(nodedata, edgedata, entityname, entityeventdata, datecountdata){
    //画布周边的空白
    var margin1 = {
        left: 15,
        right: 15,
        top: 20,
        bottom: 80
    };

    var margin2 = {
        left: 100,
        right: 100,
        top: 10,
        bottom: 5
    }

    //画布大小
    var eventWidth = 1030 - margin1.left - margin1.right;
    var eventHeight = 500 - margin1.top - margin1.bottom;
    var countWidth = 1200 - margin2.left - margin2.right;
    var countHeight = 120 - margin2.top - margin2.bottom;

    //在 body 里添加一个 SVG 画布
    eventdivid = "#EventEvolutionGraph"
    var svgEvent = d3.select(eventdivid)
        .append("svg")
        .attr("width", 1030)
        .attr("height", eventHeight + margin1.top + margin1.bottom)
        .append("g")
        .attr("transform", "translate(" + margin1.left + "," + margin1.top + ")");

    var svgCount = d3.select("#DayCount")
        .append("svg")
        .attr("width", countWidth + margin2.left + margin2.right)
        .attr("height", countHeight + margin2.top + margin2.bottom)
        .append("g")
        .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

    var svgScale = d3.select("#TimeScale")
        .append("svg")
        .attr("width", countWidth + margin2.left + margin2.right)
        .attr("height", 20)
        .append("g")
        .attr("transform", "translate(" + margin2.left + ",0)");
    
    var svgEventLegend = d3.select("#EventEvolutionLegend")
        .append("svg")
        .attr("width", countWidth + margin2.left + margin2.right)
        .attr("height", 90)
        .append("g")
        .attr("transform", "translate(" + margin2.left + "," + 0 + ")");
    
   
    //时间范围
    var minDate;
    var maxDate;
    //定义反向时间比例尺
    var dateScale;
    minDate = d3.min(nodedata, function (d) {
        return d.date;
    });
    maxDate = d3.max(nodedata, function (d) {
        return d.date;
    });
    dateScale = d3.scale.linear()
        .domain([0, eventWidth])
        .range([minDate, maxDate]);


    //画事件演变图
    //横纵坐标长度
    var x_length = d3.max(nodedata, function(d) { return 1 * d.p_c; });
    var y_length = 10;
    
    //x轴的比例尺
    var xpScale = d3.scale.linear()
        .domain([0,x_length])
        .range([0, eventWidth]);
    
    
    //x轴的比例尺（时间刻度）
    var xScale = d3.time.scale()
        .domain([minDate, maxDate])
        .range([0, eventWidth]);

    //y轴的比例尺
    var yScale = d3.scale.linear()
        .domain([0,y_length])
        .range([eventHeight, 0]);
    

    // 实现点的拖拉
    var drag = d3.behavior.drag()
        .on("drag", dragmove);
    
    function dragmove(d, i) {
        var index_y = d3.event.y;
        if (index_y < 0) {
            index_y = 0;
        }
        if (index_y > eventHeight) {
            index_y = eventHeight;
        }
        d3.select(this)
            .attr("cy", function (d) {
                d.drag_y = index_y;
                return index_y;
            });

        var change_edges_s = event_edges.filter(function (edge) {
            return edge.source == i;
        });

        change_edges_s.attr("y1", function (d) {
            return index_y;
        });

        var change_edges_t = event_edges.filter(function (edge) {
            return edge.target == i;
        });

        change_edges_t.attr("y2", function (d) {
            return index_y;
        });
    }

    
//    function dragmove(d, i) {
//        var index_xl = xpScale(d.p_c - 0.5);
//        var index_xr = xpScale(1*d.p_c + 0.5);
//        var index_x = d3.event.x;
//        var index_y = d3.event.y;
//
//        d3.select(this)
//            .attr("cx", function(d) {
//                if (index_x < index_xl)
//                    index_x = index_xl
//                else if (index_x > index_xr)
//                    index_x = index_xr
//                d.drag_x = index_x;
//                return index_x;
//            } )
//            .attr("cy", function (d) {
//                if (index_y < 0) {
//                    index_y = 0;
//                }
//                if (index_y > eventHeight) {
//                    index_y = eventHeight;
//                }
//                d.drag_y = index_y;
//                return index_y;
//            });
//        
//        changeLine(index_x, index_y, i)
//    }
//    
//    // 修改直线
//    function changeLine(index_x, index_y,i){
//        var temp_index_x = index_x * x_length / eventWidth;
//        var temp_index_y = y_length - y_length * index_y / eventHeight;
//        nodedata[i].p_x = temp_index_x;
//        nodedata[i].p_y = temp_index_y;
//
//        var change_edge_s = event_edges.filter(function(ed){
//            if (ed.source == i){
//                return true;
//            }
//        })
//        change_edge_s
//            .attr("x1",function(d) {
//                return xpScale(nodedata[i].p_x);
//            })
//            .attr("y1",function(d) {
//                return yScale(nodedata[i].p_y);
//            })
//        var change_edge_e = event_edges.filter(function(ed){
//            if (ed.target == i){
//                return true;
//            }
//        })
//        change_edge_e
//            .attr("x2",function(d) {
//                return xpScale(nodedata[i].p_x);
//            })
//            .attr("y2",function(d) {
//                return yScale(nodedata[i].p_y);
//            })
//    }
    
    
    
    // 计算偏差值
    var ix = document.getElementById('EventEvolutionGraph').offsetLeft + margin1.left;
    var iy = document.getElementById('EventEvolutionGraph').offsetTop + margin1.top;

    
    //绘制箭头
    var defs = svgEvent.append("defs");
    var arrowMarker = defs.append("marker")
        .attr("id", "arrow")
        .attr("markerUnits", "strokeWidth")
        .attr("markerWidth", "8")
        .attr("markerHeight", "8")
        .attr("viewBox", "0 0 12 12")
        .attr("refX", "6")
        .attr("refY", "6")
        .attr("orient", "auto");

    var arrow_path = "M2,2 L10,6 L2,10 L6,6 L2,2";
    arrowMarker.append("path")
        .attr("d", arrow_path)
        .attr("fill", "#dddddd");

    //画直线
    var max_value = d3.max(edgedata, function (d) {
        return d.weight;
    });
    var min_value = d3.min(edgedata, function (d) {
        return d.weight;
    });
    var vScale = d3.scale.linear()
        .domain([min_value, max_value])
        .range([1, 4]);
    
    var count = 0
    var event_edges = svgEvent.selectAll(".eventEdge")
        .data(edgedata)
        .enter()
        .append("line")
        .attr("class", "eventEdge")
        .attr("x1",function(d) {
            return xScale(nodedata[d.source].date);
        })
        .attr("y1",function(d) {
            return yScale(nodedata[d.source].p_y);
        })
        .attr("x2",function(d) {
            return xScale(nodedata[d.target].date);
        })
        .attr("y2",function(d) {
            return yScale(nodedata[d.target].p_y);
        })
        .style("stroke-width",function(d) {
            return vScale(d.weight);
        })
        .attr("marker-end","url(#arrow)");
    
   
    
    // 画点
    var nodes_information_id = [];
    var tooltip;
    
    var max_weight = d3.max(nodedata, function (d) {
        return d.weight;
    });
    var min_weight = d3.min(nodedata, function (d) {
        return d.weight;
    });
    var wScale = d3.scale.linear()
        .domain([min_weight, max_weight])
        .range([2, 4]);
    
    var event_nodes = svgEvent.selectAll(".eventNode")
        .data(nodedata)
        .enter()
        .append("circle")
        .attr("class", "eventNode")
        .attr("cx", function(d, i) {
            return xScale(d.date);
        })
        .attr("cy", function(d) {
            return yScale(d.p_y);
        })
        .attr("r", function(d) {
            return wScale(d.weight);
        })
        .call(drag)
        .on("mouseover",function(d,i){
            d3.select(this)
                .style("fill", "#ff99c4");

            // 显示事件名
            tooltip=d3.select(eventdivid)
                .append("div")
                .attr("class","tooltip")
                .html(d.name)
                .style("left", function() {
                    return (xScale(d.date) + margin1.left + wScale(d.weight) + 10)+"px";
                })
                .style("top", function() {
                    return d.drag_y ? d.drag_y + "px" : (yScale(d.p_y) + margin1.top - wScale(d.weight) - 10 )+"px";
                })
                .style("opacity",1.0);
            
//            tooltip = d3.select(eventdivid)
//                .append("div")
//                .attr("class", "tooltip")
//                .html(d.name)
//                .style("left", (xScale(d.date) + margin1.left + wScale(d.weight) + 10) + "px")
//                .style("top", d.drag_y ? d.drag_y + "px" : (yScale(d.p_y) + margin1.top - wScale(d.weight) - 10 + "px"));

        
            //其他的边变化
			event_edges.transition()
                .duration(200)
                .style("opacity", 0.2); 
            
            //选中节点的变化
            var change_edges = event_edges.filter(function(ed){
                if (ed.source == i){
                    nodes_information_id.push(ed.target)
                    return true;
                }
                if (ed.target == i){
                    nodes_information_id.push(ed.source)
                    return true;
                }
            })
            change_edges 
                .transition()
                .duration(200)
                .style("stroke","#ff99c4");
            
            //显示相应节点的信息
            var change_nodes = event_nodes.filter(function(nd, i){
                for (var j = 0; j < nodes_information_id.length; j++) { 
                    if (i == nodes_information_id[j])
                        return true;
                }
            })
            change_nodes
                .attr("fill","#fdf864");
            change_nodes.each(function (d) {
                var temp_tooltip=d3.select(eventdivid)
                    .append("div")
                    .attr("class","tooltip")
                    .html(d.name)
                    .style("left",(xScale(d.date) + margin1.left + wScale(d.weight) +10)+"px")
                    .style("top",(yScale(d.p_y))+"px")
                    .style("opacity",1.0);
            })
        })
        .on("mouseout",function(d,i){
            d3.selectAll(".tooltip").remove();
            
            event_edges.transition()
                .duration(200)
                .style("opacity", 1.0)
                .style("stroke", "#dddddd");

            event_nodes.style("fill", "#32b2ec");
            nodes_information_id = [];
        })
    
        .on("click", function(d,i){
//            console.log(d3.event);
//            console.log(i);
//                drawEventForceGraph(nodedata, edgedata, i);
        });
    
    
    var xAxis = d3.svg.axis()
        .scale(xScale)
        .ticks(d3.time.weeks)
        .orient("bottom");

    //添加x轴
    svgEvent.append("g")
        .attr("class", "axis timeAxis")
        .attr("transform", "translate(0," + (eventHeight + 50) + ")")
        .call(xAxis);

    
    
    //数据说明 Legend	
    var legend = svgEventLegend.append("g")
        .attr("class", "legend")
        .attr("height", 60)
        .attr("width", countWidth);

    //颜色序列
    var colorscale = d3.scale.category20();
    legend.selectAll('legendrect')
        .data(entityname)
        .enter()
        .append("rect")
        .attr("x", function(d, i){
            return 200 * (i % 5) + margin2.left;
        })
        .attr("y", function(d, i){
            if (i>=10)
                return 60;
            else if (i>=5)
                return 35;
            else
                return 10;
        })
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i){ return colorscale(i);});
    
    legend.selectAll('text')
        .data(entityname)
        .enter()
        .append("text")
        .attr("x", function(d, i){
            return 200 * (i % 5) + margin2.left + 20;
        })
        .attr("y", function(d, i){ 
            if (i>=10)
                return 70;
            else if (i>=5)
                return 45;
            else
                return 20;
        })
        .attr("font-size", "11px")
        .attr("fill", "black")
        .style("cursor","pointer")
        .text(function(d) { return d.entity; });
    
    legend
        .append("text")
        .attr("x", -30)
        .attr("y", 30)
        .attr("text-anchor", "start")
        .style("fill", "#aaa")
        .text("关键");
    legend
        .append("text")
        .attr("x", -30)
        .attr("y", 55)
        .attr("text-anchor", "start")
        .style("fill", "#aaa")
        .text("实体");
    
    changeEventLegend(0,countWidth);


    //绘制折线图
    darwLineGraph();
    function darwLineGraph() {
        var xScale = d3.time.scale()
            .domain(d3.extent(datecountdata, function (d) {
                return d.date;
            }))
            .range([0, countWidth]);

        var ylScale = d3.scale.linear()
            .domain([0, d3.max(datecountdata, function (d) {
                return 1 * d.news_num;
            })])
            .range([countHeight, 0]);

        var yrScale = d3.scale.linear()
            .domain([0, d3.max(datecountdata, function (d) {
                return 1 * d.comment_num;
            })])
            .range([countHeight, 0]);

        var min = d3.min(datecountdata, function (d) {
            return d.date;
        });
        var max = d3.max(datecountdata, function (d) {
            return d.date;
        });
        var duration = (max - min) / 3600 / 24 / 1000;
        var interval = 1 / duration * countWidth;
        var barWidth = interval * 0.9;

        var tipLine;
        var tipBox;

        //新闻数据-柱状图
        var rects = svgCount.selectAll("rect")
            .data(datecountdata)
            .enter()
            .append("rect")
            .attr("class", "rect")
            .attr("x", function (d, i) {
                return xScale(d.date) - barWidth / 2;
            })
            .attr("y", function (d) {
                return ylScale(d.news_num); //在这里用比例尺
            })
            .attr("width", function (d) {
                return barWidth;
            })
            .attr("height", function (d) {
                return countHeight - ylScale(d.news_num); //在这里用比例尺
            });


        //评论数据-折线图
        var comment_line = d3.svg.line()
            .x(function (d) {
                return xScale(d.date);
            })
            .y(function (d) {
                return yrScale(d.comment_num);
            })
            .interpolate("cardinal");

        svgCount.append("path")
            .datum(datecountdata)
            .attr("class", "line")
            .attr("d", comment_line);

        var nodes = svgCount.selectAll(".node")
            .data(datecountdata)
            .enter()
            .append("circle")
            .attr("class", "node")
            .attr("r", 3)
            .attr("cx", function (d) {
                return xScale(d.date);
            })
            .attr("cy", function (d) {
                return yrScale(d.comment_num);
            });

        d3.select("#DayCount")
            .on("mouseover", function () {
                tipLine = svgCount.append("g")
                    .attr("class", "tipLine")
                    .append("line")
                    .style("opacity", 0);

                tipBox = d3.select("#DayCount")
                    .append("div")
                    .attr("class", "tipBox")
                    .style("left", "0px")
                    .style("top", "0px")
                    .style("opacity", 0);
            })
            .on("mousemove", function () {
                var x = d3.mouse(this)[0];
                var y = d3.mouse(this)[1];
                var tip_x;
                var tip_y;
                var date;
                var newsNum;
                var commentNum;
                rects.classed("selectRect", function (d) {
                    if (Math.abs(xScale(d.date) + margin2.left - x) < interval / 2) {
                        date = d.num_date;
                        newsNum = d.news_num;
                        return true;
                    }
                });
                nodes.classed("selectNode", function (d) {
                    if (Math.abs(xScale(d.date) + margin2.left - x) < interval / 2) {
                        tip_x = xScale(d.date);
                        tip_y = yrScale(d.comment_num);
                        commentNum = d.comment_num;
                        return true;
                    }
                });

                if (date) {
                    tipLine.attr("x1", tip_x)
                        .attr("x2", tip_x)
                        .attr("y2", countHeight)
                        .style("opacity", 1.0);

                    tipBox.html('<p>' + date + '</p><p>新闻数量：' + newsNum + '</p><p>评论数量：' + commentNum + '</p>')
                        .style("left", tip_x + margin2.left + 20 + 'px')
                        .style("top", (tip_y - 20) + 'px')
                        .style("opacity", 1.0);
                }
            })
            .on("mouseout", function () {
                rects.classed("selectRect", function (d) {
                    return false;
                });
                nodes.classed("selectNode", function (d) {
                    return false;
                });
                svgCount.selectAll(".tipLine").remove();
                d3.selectAll(".tipBox").remove();
            });

        //左y轴的比例尺
        var ylAxis = d3.svg.axis()
            .scale(ylScale)
            .ticks(4)
            .tickSize(10)
            .orient("left");

        //右y轴的比例尺
        var yrAxis = d3.svg.axis()
            .scale(yrScale)
            .ticks(5)
            .tickSize(10)
            .orient("right");

        var yl = svgCount.append("g")
            .attr("class", "yl axis")
            .call(ylAxis);

        var yr = svgCount.append("g")
            .attr("class", "yr axis")
            .attr("transform", "translate(" + countWidth + ",0)")
            .call(yrAxis);

        //添加注释
        yl.append("rect")
            .attr("x", -60)
            .attr("y", 0)
            .attr("width", 12)
            .attr("height", 10)
            .style("fill", "#41db00");

        yl.append("text")
            .attr("x", -60)
            .attr("y", 30)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("评");
        yl.append("text")
            .attr("x", -60)
            .attr("y", 50)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("论");
        yl.append("text")
            .attr("x", -60)
            .attr("y", 70)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("数");
        yl.append("text")
            .attr("x", -60)
            .attr("y", 90)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("量");

        yr.append("rect")
            .attr("x", 60)
            .attr("y", 0)
            .attr("width", 12)
            .attr("height", 10)
            .style("fill", "#b5e4fa");

        yr.append("text")
            .attr("x", 60)
            .attr("y", 30)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("新");
        yr.append("text")
            .attr("x", 60)
            .attr("y", 50)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("闻");
        yr.append("text")
            .attr("x", 60)
            .attr("y", 70)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("数");
        yr.append("text")
            .attr("x", 60)
            .attr("y", 90)
            .attr("text-anchor", "start")
            .style("fill", "#aaa")
            .text("量");
    }
    
    

    //实现横向拖拉
    drawScaleRange();
    function drawScaleRange() {
        var defs = svgCount.append("defs");
        var gAll = defs.append("g")
            .attr("id", "myScale");
        gAll.append("polygon")
            .attr("points", "0 5 5 0 10 5 10 18 0 18")
            .style("fill", "#000");
        gAll.append("line")
            .attr("x1", 2)
            .attr("y1", 8)
            .attr("x2", 8)
            .attr("y2", 8)
            .style("stroke", "#fff")
            .style("stroke-width", 2);
        gAll.append("line")
            .attr("x1", 2)
            .attr("y1", 13)
            .attr("x2", 8)
            .attr("y2", 13)
            .style("stroke", "#fff")
            .style("stroke-width", 2);

        // 实现缩放
        var dragScale = d3.behavior.drag()
            .on("drag", dragscale);

        function dragscale(d, i) {
            var index_x = d3.event.x;
            if (index_x < 0) {
                index_x = 0;
            }
            if (index_x > countWidth) {
                index_x = countWidth;
            }
            var that = d3.select(this);
            that.attr("x", function (d) {
                return index_x - 5;
            });
            if (that.attr("class") == "startBtn") {
                start = index_x;
                scaleLine.attr("x", start)
                    .attr("width", end - start);
            } else {
                end = index_x;
                scaleLine.attr("x", start)
                    .attr("width", end - start);
            }

            rescale(start, end);
            changeEventLegend(start, end);
        }

        var start = 0;
        var end = countWidth;

        var scaleLine = svgScale.append("rect")
            .attr("class", "scaleLine")
            .attr("x", start)
            .attr("y", 5)
            .attr("width", end - start)
            .attr("height", 10)
            .style("fill", "#32b2ec");

        var startBtn = svgScale.append("use")
            .attr("class", "startBtn")
            .attr("xlink:href", "#myScale")
            .attr("x", start - 5)
            .call(dragScale);

        var endBtn = svgScale.append("use")
            .attr("class", "endBtn")
            .attr("xlink:href", "#myScale")
            .attr("x", end - 5)
            .call(dragScale);
    }

    function rescale(start, end) {
        var startDate = new Date(dateScale(start));
        var endDate = new Date(dateScale(end));

        var xScale = d3.time.scale()
            .domain([startDate, endDate])
            .range([0, eventWidth]);

        var y_length = 10;

        var yScale = d3.scale.linear()
            .domain([0, y_length])
            .range([eventHeight, 0]);

        var event_edges = svgEvent.selectAll(".eventEdge")
            .attr("x1", function (d) {
                return xScale(nodedata[d.source].date);
            })
            .attr("x2", function (d) {
                return xScale(nodedata[d.target].date);
            });

        var tooltip;
        var max_weight = d3.max(nodedata, function (d) {
            return d.weight;
        });
        var min_weight = d3.min(nodedata, function (d) {
            return d.weight;
        });
        var wScale = d3.scale.linear()
            .domain([min_weight, max_weight])
            .range([2, 4]);

        var event_nodes = svgEvent.selectAll(".eventNode")
            .attr("cx", function (d, i) {
                return xScale(d.date);
            })
            .on("mouseover", function (d, i) {
                d3.select(this)
                    .style("fill", "#ff99c4");

                // 显示事件名
                tooltip = d3.select(eventdivid)
                    .append("div")
                    .attr("class", "tooltip")
                    .html(d.name)
                    .style("left", (xScale(d.date) + margin1.left + wScale(d.weight) + 10) + "px")
                    .style("top", (yScale(d.p_y) + margin1.top - wScale(d.weight) - 10 + "px"));

                //其他的边变化
                event_edges.transition()
                    .duration(200)
                    .style("opacity", 0.2);

                //选中节点的变化
                var related_nodes = [];
                var change_edges = event_edges.filter(function (edge) {
                    if (edge.source == i) {
                        related_nodes.push(edge.target);
                        return true;
                    }
                    if (edge.target == i) {
                        related_nodes.push(edge.source);
                        return true;
                    }
                })
                change_edges.transition()
                    .duration(200)
                    .style("stroke", "#ff99c4");

                var change_nodes = event_nodes.filter(function (node, i) {
                    for (var j = 0; j < related_nodes.length; j++) {
                        if (i == related_nodes[j])
                            return true;
                    }
                })
                change_nodes.style("fill", "#fdf864");
                change_nodes.each(function (d) {
                    var temp_tooltip = d3.select(eventdivid)
                        .append("div")
                        .attr("class", "tooltip")
                        .html(d.name)
                        .style("left", (xScale(d.date) + margin1.left + wScale(d.weight) + 10) + "px")
                        .style("top", (yScale(d.p_y) + margin1.top - wScale(d.weight) - 10 + "px"))
                        .style("opacity", 1.0);
                });
            });

        var xAxis = d3.svg.axis()
            .scale(xScale)
            .orient("bottom");

        if (endDate - startDate < 14 * 24 * 3600 * 1000) {
            xAxis.ticks(d3.time.days);
        } else {
            xAxis.ticks(d3.time.weeks);
        }

        svgEvent.select(".timeAxis")
            .call(xAxis);
    }
    
    //说明legend
    function changeEventLegend(start, end){
        var startDate = new Date(dateScale(start));
        var endDate = new Date(dateScale(end));

        var xScale = d3.time.scale()
            .domain([startDate, endDate])
            .range([0, eventWidth]);

        
    	//Create text next to squares
        var change_node;
    	legend.selectAll('text')
            .on('mouseover', function (d,i){
                //找到相关节点
                var change_node_index = [];
                for (var index = 0; index < entityeventdata.length; index += 1)
                    if (entityeventdata[index].entity_index == i)
                        change_node_index.push(entityeventdata[index].event_index);
                
                change_nodes = event_nodes.filter(function(nd, ni){
                    if (change_node_index.length != 0)
                        for (var index = 0; index < change_node_index.length; index += 1)
                            if (change_node_index[index] == ni)
                                return true;
                })
                change_nodes
                    .attr("fill", "#ff99c4");
            
                change_nodes.each(function (d) {
                    var temp_tooltip=d3.select(eventdivid)
                        .append("div")
                        .attr("class","tooltip")
                        .html(d.name)
                        .style("left",(xScale(d.date) + margin1.left + wScale(d.weight) +10)+"px")
                        .style("top",(yScale(d.p_y))+"px")
                        .style("opacity",1.0);
                })
            
                
                //修改其他的边
    			d3.select("svg").selectAll("line")
                    .transition()
                    .duration(500)
                    .style("opacity", 0.2)
                    .style("stroke-width", 1); 
                
                //找到相关的边
                var change_edges  = event_edges.filter(function(ed){
                    for (var index = 0; index < change_node_index.length; index += 1)
                    {
                        if (ed.source == change_node_index[index]){
                            nodes_information_id.push(ed.target)
                            return true;
                        }
                        if (ed.target == change_node_index[index]){
                            nodes_information_id.push(ed.source)
                            return true;
                        }
                    }
                })
                change_edges 
                    .transition()
                    .duration(200)
                    .style("stroke","#ff99c4");
            
            })
            .on('mouseout', function(){
                d3.selectAll(".tooltip").remove();
            
                //恢复原样
                event_nodes.style("fill", "#32b2ec");
            
                //边恢复原状
                event_edges.transition()
                    .duration(200)
                    .style("opacity", 1.0)
                    .style("stroke", "#dddddd");
    		});	
    }
    
}