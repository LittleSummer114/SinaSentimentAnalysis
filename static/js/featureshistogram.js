function bindPosFeaturesData(topic_id){
    $.ajax({
    type: "GET",
    url: "getPositiveFeatures",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        var featuresHistodata = [];
        for (var i = 0; i < data.length; i++){
            featuresHistodata.push({feature: data[i][0], count: parseInt(data[i][1])})
        }
        //console.log(featuresHistodata);
        darwFeaturesHistogramMap(featuresHistodata, 1);
    }
    })
}

function bindNegFeaturesData(topic_id){
    $.ajax({
    type: "GET",
    url: "getNegativeFeatures",
    dataType: 'json',
    data: {
        tid: topic_id
    },
    success: function (data) {
        var featuresHistodata = [];
        for (var i = 0; i < data.length; i++){
            featuresHistodata.push({feature: data[i][0], count: parseInt(data[i][1])})
        }
        //console.log(featuresHistodata);
        darwFeaturesHistogramMap(featuresHistodata, 0);
    }
    })
}



//readPosFeaturesHistogramData();

//读取地图数据
function readPosFeaturesHistogramData(){
    d3.csv("../../data/sentiment/positive_features.csv")
        .row(function(d) { 
            return { feature: d.feature, count: parseInt(d.count)}; 
        })
        .get(function(error, row) { 
            //console.log(row);
            darwFeaturesHistogramMap(row);
        });
}

//绘制中国地图
function darwFeaturesHistogramMap(FeaturesHistodata, is_pos){
    
    //画布周边的空白
    var margin = {top: 10, right: 10, bottom: 50, left: 30 };

    //画布大小
    var width = 420 - margin.left - margin.right,
        height = 325 - margin.top - margin.bottom;
    
	
    //svg
    var divid = '#PosFeaturesHisto';
    if (is_pos == 0)
        divid = '#NegFeaturesHisto';
    
	var svg = d3.select(divid).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        //.attr("style","border:2px solid black")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	
    //绘制的个数
    var darw_feature_num = 12;
    var topk_histogramdata = [];
    for (var i = 0; i < darw_feature_num; i++) {
        topk_histogramdata.push(FeaturesHistodata[i]);
    }
    //console.log(topk_histogramdata[0]);
    
    //文字的x轴比例尺
    var topk_feature_name = [];
    for (var i = 0; i < darw_feature_num; i++)
        topk_feature_name.push(topk_histogramdata[i].feature);
	var xScale = d3.scale.ordinal()
		.domain(topk_feature_name)
		.rangeRoundBands([0, width]);

	//y轴的比例尺
    var max_y_value = (parseInt(topk_histogramdata[0].count/10.0) + 1 ) * 10;
    //console.log(max_y_value);
	var yScale = d3.scale.linear()
		.domain([0, max_y_value])
		.range([height, 0]);
    

	//定义x轴
	var xAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom");
		
	//定义y轴
	var yAxis = d3.svg.axis()
		.scale(yScale)
		.orient("left");

	//矩形之间的空白
	var rectPadding = 15;

	//添加矩形元素
//    var topk_his_tooltip;
	svg.selectAll(".MyRect")
		.data(topk_histogramdata)
		.enter()
		.append("rect")
		.attr("x", function(d,i){
			return xScale(d.feature) + rectPadding/2;
		} )
		.attr("y",function(d){
			return yScale(d.count);
		})
		.attr("width", xScale.rangeBand() - rectPadding )
		.attr("height", function(d){
			return height - yScale(d.count);
		})
        .attr("fill", function(){
            if (is_pos)
                return "steelblue";
            else
                return "#B766AD";
        });
//        .on("mouseover",function(d,i){
//                //修改颜色
//                d3.select(this)
//                    .attr("fill","yellow");
//                
//                //基本信息条
//                topk_his_tooltip=d3.select("body")
//                    .append("div")
//                    .attr("class","tooltip")
//                    .html(function(){
//                        var info_str = d.area + "<br>" + "比例" + (d.percent) + "%";
//                        return info_str;
//                    })
//                    .style("left",(d3.event.pageX+10)+"px")
//                    .style("top",(d3.event.pageY)+"px")
//                    .style("opacity",1.0);
//            })
//            .on("mouseout",function(d,i){
//                //恢复颜色
//                d3.select(this)
//                    .attr("fill","steelblue");
//                //去掉基本信息条
//                topk_his_tooltip.remove();
//            });
    
    //添加文字元素
//    svg.selectAll("featuretext")
//        .data(topk_histogramdata)
//        .enter()
//        .append("text")
//        .attr("transform", "rotate(-45)")
//        .text(function(d, i) {
//            return d.feature;
//        })
//        .attr("x", function(d,i){
//			return xScale(d.feature);
//		} )
//		.attr("y",function(d){
//			return yScale(d.count);
//		})
//        .attr("font-family", "微软雅黑")
//        .attr("font-size", "11px")
//        .attr("fill", "black");
    
    
	//添加x轴
	svg.append("g")
		.attr("class","axis")
        .attr("transform", "translate(0," + height + ")")
		.call(xAxis)
        .attr("font-family", "微软雅黑")
        .attr("font-size", "15px")
      .selectAll("text")
        .attr("y", 15)
        .attr("x", -20)
        .attr("dy", ".35em")
        .attr("transform", "rotate(-45)");
		
	//添加y轴
	svg.append("g")
		.attr("class","axis")
        .attr("transform", "translate(0,0)")
		.call(yAxis)
        .attr("font-family", "sans-serif")
        .attr("font-size", "11px")
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .attr("font-family", "微软雅黑")
        .text("频次");

}