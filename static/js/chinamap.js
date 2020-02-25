var geo_path = "/static/js/china.geojson";

//readChinaMapData();

//读取地图数据
function readChinaMapData(){
    d3.csv("../data/area/area_count.csv")
        .row(function(d) { 
            return { area: d.area, rank: parseInt(d.rank), comment_num: parseInt(d.comment_num), percent: parseFloat(parseFloat(d.percent*100).toFixed(2))}; 
        })
        .get(function(error, row) { 
            console.log(row);
//            darwChinaMap(row);
        });
}

function bindChinaMapData(topic_id){
    $.ajax({
    type: "GET",
    url: "getAreaData",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        //console.log(data);
        var chinamapdata = [];
        for (var i = 0; i < data.length; i++){
            chinamapdata.push({area: data[i][0], rank: parseInt(data[i][1]), comment_num: parseInt(data[i][2]), percent: parseFloat(parseFloat(data[i][3]*100).toFixed(2))})
        }
        //console.log(chinamapdata);
        darwChinaMap(chinamapdata);
    }
    })
}

//绘制中国地图
function darwChinaMap(chinamapdata){
    
    //画布周边的空白
    var margin = {top: 20, right: 10, bottom: 20, left: 20 };

    //画布大小
    var map_size = 500;
    var map_width = map_size + 100 - margin.left - margin.right,
        height = map_size - 70 - margin.top - margin.bottom;
    var histogram_width = 600;
    
	
    //svg
    var divid = '#chinamap';
	var svg = d3.select(divid).append("svg")
        .attr("width", map_width + histogram_width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        //.attr("style","border:2px solid black")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	//投影函数
	var projection = d3.geo.mercator()
						.center([107, 37])
						.scale(map_size)
    					.translate([map_width/2, height/2]);
	//地理路径生成器
	var path = d3.geo.path()
					.projection(projection);
	
	
//	var colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]; 
//    
//    //拆分成9个的等级的颜色
//    var colorScale = d3.scale.quantile()
//        .domain([0, d3.max(chinamapdata, function (d) { return d.percent; })])
//        .range(colors);
    
    //颜色
    var a = d3.rgb(187,255,255);
    var b = d3.rgb(0,0,255);
    var colors = d3.interpolate(a,b);
    var colorScale = d3.scale.linear()
				.domain([0, d3.max(chinamapdata, function (d) { return d.percent; })])
				.range([0,1]);
    
    
    // 计算偏差值
    //var ix = document.getElementById(divid_w).offsetLeft + margin.left;
    //var iy = document.getElementById(divid_w).offsetTop + margin.top;
	
	//绘制地图
    var tooltip;
	d3.json(geo_path, function(error, root) {
		if (error) 
			return console.error(error);
		//console.log(root.features);
		
		svg.selectAll("mappath")
			.data(root.features)
			.enter()
			.append("path")
			.attr("stroke","#000")
			.attr("stroke-width",1)
			.attr("fill", function(d,i){
                for (var j = 0; j < chinamapdata.length; j++) { 
                    if (d.properties.name == chinamapdata[j].area){
                        return colors(colorScale(chinamapdata[j].percent));
                    }
                }
			})
			.attr("d", path )
			.on("mouseover",function(d,i){
                //修改颜色
                d3.select(this)
                    .attr("fill","yellow");
                
                //基本信息条
                tooltip=d3.select("body")
                    .append("div")
                    .attr("class","tooltip")
                    .html(function(){
                        var info_str = d.properties.name + "<br>";
                        for (var j = 0; j < chinamapdata.length; j++)
                            if (d.properties.name == chinamapdata[j].area)
                                info_str += "排名" + chinamapdata[j].rank + "<br>" + "比例" + chinamapdata[j].percent + "%";
                        return info_str;
                    })
                    .style("left",(d3.event.pageX+10)+"px")
                    .style("top",(d3.event.pageY)+"px")
                    .style("opacity",1.0);
            })
            .on("mouseout",function(d,i){
                //恢复颜色
                d3.select(this)
                    .attr("fill",function(){
                     for (var j = 0; j < chinamapdata.length; j++)
                        if (d.properties.name == chinamapdata[j].area)
                            return colors(colorScale(chinamapdata[j].percent));
                });
                //去掉基本信息条
                tooltip.remove();
            });
	});
    
    

    //定义一个线性渐变
    var defs = svg.append("defs");

    var linearGradient = defs.append("linearGradient")
                            .attr("id","linearColor")
                            .attr("x1","0%")
                            .attr("y1","0%")
                            .attr("x2","100%")
                            .attr("y2","0%");

    var stop1 = linearGradient.append("stop")
                    .attr("offset","0%")
                    .style("stop-color",a.toString());

    var stop2 = linearGradient.append("stop")
                    .attr("offset","100%")
                    .style("stop-color",b.toString());
    
    var colorRect = svg.append("rect")
				.attr("x", map_width*0.04)
				.attr("y", height*0.85)
				.attr("width", map_width*0.25)
				.attr("height", height*0.04)
				.style("fill","url(#" + linearGradient.attr("id") + ")");
    
    //添加文字元素
    var text_date = ["低","高"];
    svg.selectAll("text")
        .data(text_date)
        .enter()
        .append("text")
        .text(function(d) {
            return d;
        })
        .attr("x", function(d, i) {
            return map_width * (0.04 + i * 0.22);
        })
        .attr("y", height*0.84)
        .attr("font-family", "sans-serif")
        .attr("font-size", "16px")
        .attr("fill", "black");
    

    
    
    
    //**************添加统计的直方图**************
    //width
    var histogram_height = height * 0.95;
    
//	var svg_h = d3.select(divid).append("svg")
//        .attr("width", histogram_width + margin.left*3 + margin.right)
//        .attr("height", height + margin.top + margin.bottom)
//        .attr("style","border:2px solid red")
//        .append("g")
//        .attr("transform", "translate(" + margin.left*3 + "," + margin.top*3 + ")");
    
    var svg_h = svg;

    //绘制的个数
    var darw_area_num = 12;
    var topk_histogramdata = [];
    for (var i = 0; i < darw_area_num; i++) {
        topk_histogramdata.push(chinamapdata[i]);
    }
    
    //文字的x轴比例尺
    var topk_area_name = [];
    for (var i = 0; i < darw_area_num; i++)
        topk_area_name.push(topk_histogramdata[i].area);
	var xScale = d3.scale.ordinal()
		.domain(topk_area_name)
		.rangeRoundBands([map_width, map_width + histogram_width]);

	//y轴的比例尺
    var max_y_value = (parseInt(d3.max(chinamapdata, function(d) { return d.percent; })/5.0) + 1 ) * 5;
	var yScale = d3.scale.linear()
		//.domain([0,d3.max(chinamapdata, function(d) { return d.percent; })])
		.domain([0, max_y_value])
		.range([histogram_height, 0]);
    

	//定义x轴
	var xAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom");
		
	//定义y轴
	var yAxis = d3.svg.axis()
		.scale(yScale)
		.orient("left");

	//矩形之间的空白
	var rectPadding = 20;

	//添加矩形元素
    var topk_his_tooltip;
	var rects = svg_h.selectAll(".MyRect")
		.data(topk_histogramdata)
		.enter()
		.append("rect")
		.attr("x", function(d,i){
			return xScale(d.area) + rectPadding/2;
		} )
		.attr("y",function(d){
			return yScale(d.percent);
		})
		.attr("width", xScale.rangeBand() - rectPadding )
		.attr("height", function(d){
			return histogram_height - yScale(d.percent);
		})
        .attr("fill","steelblue")
        .on("mouseover",function(d,i){
                //修改颜色
                d3.select(this)
                    .attr("fill","yellow");
                
                //基本信息条
                topk_his_tooltip=d3.select("body")
                    .append("div")
                    .attr("class","tooltip")
                    .html(function(){
                        var info_str = d.area + "<br>" + "比例" + (d.percent) + "%";
                        return info_str;
                    })
                    .style("left",(d3.event.pageX+10)+"px")
                    .style("top",(d3.event.pageY)+"px")
                    .style("opacity",1.0);
            })
            .on("mouseout",function(d,i){
                //恢复颜色
                d3.select(this)
                    .attr("fill","steelblue");
                //去掉基本信息条
                topk_his_tooltip.remove();
            });
    
    
	//添加x轴
	svg_h.append("g")
		.attr("class","axis")
        .attr("transform", "translate(0," + histogram_height + ")")
		.call(xAxis); 
		
	//添加y轴
	svg_h.append("g")
		.attr("class","axis")
        .attr("transform", "translate(" + map_width + ",0)")
		.call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("比例");

}