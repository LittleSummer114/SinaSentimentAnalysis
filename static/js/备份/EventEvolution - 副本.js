

function bindEventEvolutionData(topic_id){
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
            entity_name.push({entity: data[0][i]})
        }
        //console.log(entity_name);
        
        var node_data = [];
        for (var i = 0; i < data[1].length; i++){
            node_data.push({p_x: data[1][i][1], p_y: data[1][i][2], p_c: data[1][i][1], date: data[1][i][0], weight: data[1][i][3], name: data[1][i][4]})
        }
        //console.log(node_data);
        
        var edge_data = [];
        for (var i = 0; i < data[2].length; i++){
            edge_data.push({p_1: data[2][i][0], p_2: data[2][i][1], weight: data[2][i][2]})
        }
        //console.log(edge_data);
        
        var entity_event_data = []
        for (var i = 0; i < data[3].length; i++){
            entity_event_data.push({entity_index: data[3][i][0], event_index: data[3][i][1]})
        }
        //console.log(entity_event_data);
    
        drawEventGraph(node_data, edge_data, entity_name, entity_event_data);
    }
    })
}

//读取csv文件
//var nodepath = "../../data/results/node.csv";
//console.log(nodepath);
//d3.csv("../../data/results/node.csv")
//    .row(function(d) { 
////        temp_index = d.position_x - 0.5 + Math.random();
//        temp_index = d.position_x;
//        return {p_x: temp_index, p_y: d.position_y, p_c: d.position_x, date:formatDate.parse(d.date), weight: d.weight, name: d.name}; 
//    })
//    .get(function(error, row) { 
//        console.log(row);
//        getEdgeCSV(row);
//    });
//
////读取第二个csv文件
//function getEdgeCSV(positiondata){
//    d3.csv("../../data/results/edge.csv")
//        .row(function(d) { return {p_1: d.position_1, p_2: d.position_2, weight: d.weight}; })
//        .get(function(error, row) {
//            //console.log(row);
//            getEntityCSV(positiondata,row)
////            drawEventForceGraph(positiondata, row, 9);                       
//        });
//}
//
//function getEntityCSV(positiondata, edgedata){
//    d3.csv("../../data/entities/entities.csv")
//        .row(function(d) { 
//            return { entity: d.entity}; 
//        })
//        .get(function(error, row) { 
//            var entityname = row;
//            d3.csv("../../data/entities/entities_events.csv")
//                .row(function(d) { 
//                    return { entity_index: d.entity_index, event_index: d.news_index }; 
//                })
//                .get(function(error, row) { 
//                    //console.log(row);
//                    drawEventGraph(positiondata, edgedata, entityname, row);
//                });
//        });
//}

//绘图
function drawEventGraph(positiondata, edgedata, entityname, entityeventdata){

    //时间格式
    var formatDate = d3.time.format("%Y-%m-%d");
    

    //画布周边的空白
    var margin = {left:30, right:100, top:20, bottom:20};

    //画布大小
    var width = 1200 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;
    
//    console.log(positiondata);
//    console.log(edgedata);
    
    //在 body 里添加一个 SVG 画布
    var divid='#EventEvolution'
    var svg = d3.select(divid)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    //横纵坐标长度
    var x_length = d3.max(positiondata, function(d) { return 1 * d.p_c; });
    var y_length = 10;

    //x轴的比例尺
    var xScale = d3.scale.linear()
        .domain([0,x_length])
        .range([0, width]);
    
    //x轴的比例尺（时间刻度）
    var xtScale = d3.time.scale()
        .domain(d3.extent(positiondata, function(d) { return d.date; }))
        .range([0, width]);
    

    //y轴的比例尺
    var yScale = d3.scale.linear()
        .domain([0,y_length])
        .range([height, 0]);

    //定义x轴（时间刻度）
    var xAxis = d3.svg.axis()
        .scale(xtScale)
//        .ticks(d3.time.date,2) 
        .orient("bottom");

    //定义y轴
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");
    


    // 实现点的拖拉
    var drag = d3.behavior.drag()
        .on("drag", dragmove);
    function dragmove(d, i) {
        var index_xl = xScale(d.p_c - 0.5);
        var index_xr = xScale(1*d.p_c + 0.5);
        var index_x = d3.event.x;

        d3.select(this)
            .attr("cx", function(d) {
                if (index_x < index_xl)
                    index_x = index_xl
                else if (index_x > index_xr)
                    index_x = index_xr
                return index_x;
            } )
            .attr("cy", d.cy = d3.event.y );
        
        changeLine(index_x, d3.event.y, i)
    }
    
    // 计算偏差值
    var ix = document.getElementById('EventEvolution').offsetLeft + margin.left;
    var iy = document.getElementById('EventEvolution').offsetTop + margin.top;

    // 画点
    var nodes_information_id = [];
    var nodes_tooltip = [];
    var tooltip;
    var nodes = svg.selectAll("circle")
        .data(positiondata)
        .enter()
        .append("circle")
        .attr("cx", function(d, i) {
            return xScale(d.p_x);
        })
        .attr("cy", function(d) {
            return yScale(d.p_y);
        })
        .attr("r", function(d) {
            return d.weight;
        })
        .call(drag)
        .attr("fill","steelblue")
        .on("mouseover",function(d,i){
            d3.select(this)
                .attr("fill","yellow");

            // 显示事件名
            tooltip=d3.select(divid)
            .append("div")
            .attr("class","tooltip")
            .html(d.name)
            .style("left",(d3.event.pageX+10)+"px")
            .style("top",(d3.event.pageY)+"px")
            .style("opacity",1.0);
        
            //其他的边变化
			d3.select("svg").selectAll("line")
                .transition()
                .duration(500)
                .style("opacity", 0.2)
                .style("stroke-width", 1); 
            
            //选中节点的变化
            var change_edge  = edges.filter(function(ed){
                if (ed.p_1 == i){
                    nodes_information_id.push(ed.p_2)
                    return true;
                }
                if (ed.p_2 == i){
                    nodes_information_id.push(ed.p_1)
                    return true;
                }
            })
            change_edge 
                .transition()
                .duration(500)
                .style("stroke","red")
                .style("stroke-width",function(d) {
                    return d.weight;
                })
            
            //显示相应节点的信息
            var change_node = nodes.filter(function(nd, i){
                for (var j = 0; j < nodes_information_id.length; j++) { 
                    if (i == nodes_information_id[j])
                        return true;
                }
            })
            change_node
                .attr("fill","green")
                .html(function(d) {
                    var temp_tooltip=d3.select(divid)
                        .append("div")
                        .attr("class","tooltip")
                        .html(d.name)
                        .style("left",(xScale(d.p_x)+ ix+10)+"px")
                        .style("top",(yScale(d.p_y)+ iy)+"px")
                        .style("opacity",1.0);
                    nodes_tooltip.push(temp_tooltip);
                })
        })
        .on("mouseout",function(d,i){
            d3.select(this)
                .transition()
                .duration(500)
                .attr("fill","steelblue");
//            tooltip.style("opacity",0.0);
            tooltip.remove();
        
            //其他的例子变化
			d3.select("svg").selectAll("line")
                .transition()
                .duration(500) 
                .style("opacity", 1.0)
                .style("stroke","#ccc")
                .style("stroke-width",function(d) {
                    return d.weight;
                })
            
            //还原相应节点的信息
            var change_node = nodes.filter(function(nd, i){
                for (var j = 0; j < nodes_information_id.length; j++) { 
                    if (i == nodes_information_id[j])
                        return true;
                }
            });
            change_node
                .attr("fill","steelblue");
            
            //清空列表
            for (var j = 0; j < nodes_tooltip.length; j++)
                nodes_tooltip[j].remove();
                
            nodes_information_id = [];
            nodes_tooltip = [];
        })
    
        .on("click", function(d,i){
//            console.log(d3.event);
//            console.log(i);
//                drawEventForceGraph(positiondata, edgedata, i);
        });

    //添加文字元素
//        svg.selectAll("text")
//            .data(positiondata)
//            .enter()
//            .append("text")
//            .text(function(d, i) {
//                return i;
//            })
//            .attr("x", function(d) {
//                return xScale(d.p_x) + margin.left;
//            })
//            .attr("y", function(d) {
//                return yScale(d.p_y) + margin.top;
//            })
//            .attr("font-family", "sans-serif")
//            .attr("font-size", "11px")
//            .attr("fill", "red");
    
    //绘制箭头
    var defs = svg.append("defs");
    var arrowMarker = defs.append("marker")
                            .attr("id","arrow")
                            .attr("markerUnits","strokeWidth")
                            .attr("markerWidth","8")
                            .attr("markerHeight","8")
                            .attr("viewBox","0 0 12 12") 
                            .attr("refX","6")
                            .attr("refY","6")
                            .attr("orient","auto");

    var arrow_path = "M2,2 L10,6 L2,10 L6,6 L2,2";
    arrowMarker.append("path")
                .attr("d",arrow_path)
                .attr("fill","#ccc");

    //画直线
    var count = 0
    //console.log(svg.selectAll("line"));
    var edges = svg.selectAll("line")
        .data(edgedata)
        .enter()
        .append("line")
        .attr("x1",function(d) {
            return xScale(positiondata[d.p_1].p_x);
        })
        .attr("y1",function(d) {
            return yScale(positiondata[d.p_1].p_y);
        })
        .attr("x2",function(d) {
            return xScale(positiondata[d.p_2].p_x);
        })
        .attr("y2",function(d) {
            return yScale(positiondata[d.p_2].p_y);
        })
        .style("stroke","#ccc")
        .style("stroke-width",function(d) {
            return d.weight;
        })
        .attr("marker-end","url(#arrow)");
    
    //console.log(count);

    // 修改直线
    function changeLine(index_x, index_y,i){
        var temp_index_x = index_x * x_length / width;
        var temp_index_y = y_length - y_length * index_y / height;
        positiondata[i].p_x = temp_index_x;
        positiondata[i].p_y = temp_index_y;

        var change_edge_s = edges.filter(function(ed){
            if (ed.p_1 == i){
                return true;
            }
        })
        change_edge_s
            .attr("x1",function(d) {
                return xScale(positiondata[i].p_x);
            })
            .attr("y1",function(d) {
                return yScale(positiondata[i].p_y);
            })
        var change_edge_e = edges.filter(function(ed){
            if (ed.p_2 == i){
                return true;
            }
        })
        change_edge_e
            .attr("x2",function(d) {
                return xScale(positiondata[i].p_x);
            })
            .attr("y2",function(d) {
                return yScale(positiondata[i].p_y);
            })
    }
    
    //数据说明 Legend	
    var legend = svg.append("g")
        .attr("class", "legend")
        .attr("height", 100)
        .attr("width", 200);

    //颜色序列
    var colorscale = d3.scale.category10();
	legend.selectAll('rect')
        .data(entityname)
        .enter()
        .append("rect")
        .attr("x", width + margin.left)
        .attr("y", function(d, i){ return 10 + i * 30;})
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i){ return colorscale(i);});
    
	//Create text next to squares
    var change_node;
	legend.selectAll('text')
        .data(entityname)
        .enter()
        .append("text")
        .attr("x", width + margin.left + 20)
        .attr("y", function(d, i){ return 10+ i * 30 + 9;})
        .attr("font-size", "11px")
        .attr("fill", "black")
        .text(function(d) { return d.entity; })
        .on('mouseover', function (d,i){
            //找到相关节点
            var change_node_index = [];
            for (var index = 0; index < entityeventdata.length; index += 1)
                if (entityeventdata[index].entity_index == i)
                    change_node_index.push(entityeventdata[index].event_index);
            
            change_node = nodes.filter(function(nd, ni){
                if (change_node_index.length != 0)
                    for (var index = 0; index < change_node_index.length; index += 1)
                        if (change_node_index[index] == ni)
                            return true;
            })
            change_node
                .attr("fill","yellow");
            
            //修改其他的边
			d3.select("svg").selectAll("line")
                .transition()
                .duration(500)
                .style("opacity", 0.2)
                .style("stroke-width", 1); 
            
            //找到相关的边
            var change_edge  = edges.filter(function(ed){
                for (var index = 0; index < change_node_index.length; index += 1)
                {
                    if (ed.p_1 == change_node_index[index]){
                        nodes_information_id.push(ed.p_2)
                        return true;
                    }
                    if (ed.p_2 == change_node_index[index]){
                        nodes_information_id.push(ed.p_1)
                        return true;
                    }
                }
            })
            change_edge 
                .transition()
                .duration(500)
                .style("stroke","red")
                .style("stroke-width",function(d) {
                    return d.weight;
                })
        
        })
        .on('mouseout', function(){
            //恢复原样
            change_node
                .transition()
                .duration(200) 
                .attr("fill","steelblue");
        
            //边恢复原状
            d3.select("svg").selectAll("line")
                .transition()
                .duration(200) 
                .style("opacity", 1.0)
                .style("stroke","#ccc")
                .style("stroke-width",function(d) {
                    return d.weight;
                })
		});	
    
    
    //添加x轴
    svg.append("g")
        .attr("class","axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    //添加y轴
    svg.append("g")
        .attr("class","axis")
        .call(yAxis);
    
}

// 针对特定事件画力学图
function drawEventForceGraph(positiondata, edgedata, index){

    var force_nodes_data = [];
    var force_edges_data = [];

    var main_node = {name:positiondata[index].name, node_weight:positiondata[index].weight};
    force_nodes_data.push(main_node);
    for (var i = 0; i < edgedata.length;i++)
    {
        if (edgedata[i].p_1 == index)
        {
            var temp_node = {name:positiondata[edgedata[i].p_2].name, node_weight:positiondata[edgedata[i].p_2].weight};
            force_nodes_data.push(temp_node);

            var temp_length = positiondata[edgedata[i].p_2].p_c - positiondata[index].p_c
            var temp_edge = {source:0, target:force_nodes_data.length - 1, edge_weight: edgedata[i].weight, edge_length:temp_length};
            force_edges_data.push(temp_edge);
        }
        if (edgedata[i].p_2 == index)
        {
            var temp_node = {name:positiondata[edgedata[i].p_1].name, node_weight:positiondata[edgedata[i].p_1].weight};
            force_nodes_data.push(temp_node);

            var temp_length = positiondata[index].p_c - positiondata[edgedata[i].p_1].p_c
            var temp_edge = {source:force_nodes_data.length - 1, target: 0, edge_weight: edgedata[i].weight, edge_length:temp_length};
            force_edges_data.push(temp_edge);
        }
    }
    console.log(force_nodes_data);
    console.log(force_edges_data);
    
    
    

    //画布大小
    var force_width = 1200 - margin.left - margin.right;
    var force_height = 500 - margin.top - margin.bottom;


    var svg_2 = d3.select(divid)
                .append("svg")
                .attr("width",force_width + margin.left + margin.right)
                .attr("height",force_height + margin.top + margin.bottom);

    var eventLength = [100, 150, 200, 250, 300, 350, 400]
    var force = d3.layout.force()
                .nodes(force_nodes_data)		//指定节点数组
                .links(force_edges_data)		//指定连线数组
                .size([width,height])	//指定范围
                .linkDistance(function(d){
                    length_index = d.edge_length
                    if (length_index > 5)
                        length_index = 6
                    return eventLength[length_index];
                })	//指定连线长度
                .charge(-200);	//相互之间的作用力

    force.start();	//开始作用

    //添加连线
    var svg_edges = svg_2.selectAll("line")
                        .data(force_edges_data)
                        .enter()
                        .append("line")
                        .style("stroke","#ccc")
                        .style("stroke-width",function(d){
                            return d.edge_weight;
                        });

    var color = d3.scale.category20();

    //添加节点
    var svg_nodes = svg_2.selectAll("circle")
                        .data(force_nodes_data)
                        .enter()
                        .append("circle")
                        .attr("r",function(d){
                            return 2 * d.node_weight;
                        })
                        .style("fill",function(d,i){
                            return color(i);
                        })
                        .call(force.drag);	//使得节点能够拖动

    //添加描述节点的文字
    var svg_texts = svg_2.selectAll("text")
                        .data(force_nodes_data)
                        .enter()
                        .append("text")
                        .style("fill", "black")
                        .attr("dx", 20)
                        .attr("dy", 8)
                        .text(function(d){
                            return d.name;
                        });

    //设定力学图更新时调用的函数
    force.on("tick", function(){	//对于每一个时间间隔
         //更新连线坐标
         svg_edges.attr("x1",function(d){ return d.source.x; })
                .attr("y1",function(d){ return d.source.y; })
                .attr("x2",function(d){ return d.target.x; })
                .attr("y2",function(d){ return d.target.y; });

         //更新节点坐标
         svg_nodes.attr("cx",function(d){ return d.x; })
                .attr("cy",function(d){ return d.y; });

         //更新文字坐标
         svg_texts.attr("x", function(d){ return d.x; })
            .attr("y", function(d){ return d.y; });
    });

}