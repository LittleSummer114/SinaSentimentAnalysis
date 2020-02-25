
//readPieData()

//读取csv文件
function readPieData(){
    d3.csv("/static/data/sentiment/data.csv")
    .row(function(d) {
        return {name: d.name, percent: parseFloat(d.percent*100).toFixed(2)}; 
    })
    .get(function(error, row) { 
        console.log(row);
        darwPieChart(row);
    });

}

function bindPieChartData(comment_id){
    $.ajax({
    type: "GET",
    url: "getPieChartData",
    dataType: 'json',
    data: {
        cid: comment_id
    },
    success: function (data) {
        //console.log(data);
        var peichartdata = [];
        for (var i = 0; i < data.length; i++){
//            peichartdata.push({name: data[i][0], percent: parseFloat(data[i][1]*100).toFixed(2)})
            peichartdata.push({name: data[i][0], percent: data[i][1])
        }
        console.log(peichartdata);
        darwPieChart(peichartdata);
    }
    })
}

//绘图函数
function darwPieChart(pieData){
    var divid = '#piechart'
    
    //画布周边的空白
    var margin = {top: 5, right: 50, bottom: 5, left: 50 };

    //画布大小
    var legend_width = 200;
    var pie_width = 380;
    var width = pie_width + legend_width - margin.left - margin.right, //200是legend的长度
        height = 270 - margin.top - margin.bottom;

    //扇形半径
    var radius = Math.min(width, height) / 2;

    //颜色选择器
    //var color = d3.scale.category20();
    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
    
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

    var svg = d3.select(divid)
        .append("svg")
        .attr("width", width + margin.left + margin.right )
        .attr("height", height + margin.top + margin.bottom)
//        .attr("style","border:2px solid black")
      .append("g")
        .attr("transform", "translate(" + (pie_width) / 2 + "," + (height + margin.top + margin.bottom) / 2 + ")");
    
    //显示扇形
    var g = svg.selectAll(".arc")
        .data(pie(pieData))
        .enter().append("g")
        .attr("class", "arc");

    //圈出扇形的边框
    g.append("path")
        .attr("d", arc)
        .style("fill", function(d,i) { return color(i); });
    
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
    var legend = svg.append("g")
        .attr("class", "legend")
        .attr("height", 100)
        .attr("width", 200);
    
    var extra_width = 45;
	//Create colour squares
	legend.selectAll('rect')
        .data(pieData)
        .enter()
        .append("rect")
        .attr("x", pie_width/2 )
        .attr("y", function(d, i){ return extra_width + i * 30 - height/2;})
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i){ return color(i);});
    
	//Create text next to squares
	legend.selectAll('text')
        .data(pieData)
        .enter()
        .append("text")
        .attr("x", pie_width/2 + 20)
        .attr("y", function(d, i){ return extra_width + i * 30 - height/2 + 9;})
        .attr("font-size", "16px")
        .attr("fill", "black")
        .text(function(d) { return d.name; })
        .on('mouseover', function (d){
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
        })
        .on('mouseout', function(){
            //恢复原样
			g.transition()
                .duration(500)
                .style("fill-opacity", 1.0)
                .attr("stroke-width",0);
        
            g.selectAll("text")
                .text(function(d) { return ""; });
		})
    ;	

}






