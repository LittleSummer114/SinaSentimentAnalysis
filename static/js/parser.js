
function bindParserTreeData(comment_id){
    console.log(comment_id)
    $.ajax({
    type: "GET",
    url: "getParserTreeData",
    dataType: 'json',
    data: {
        cid: comment_id
    },
    success: function (data) {
        console.log(data);
        darwParserTree(data);
    }
    })
}

function darwParserTree(treedata){
    var data = eval(treedata);
    
//    data = [{'cont': '\xe4\xb8\x96\xe7\x95\x8c', 'parent': 1, 'semparent': 3, 'relate': 'ATT', 'semrelate': 'Loc', 'ne': 'O', 'pos': 'n', 'arg': [], 'id': 0}, {'cont': '\xe5\xa5\x87\xe8\x91\xa9', 'parent': 3, 'semparent': 3, 'relate': 'SBV', 'semrelate': 'Loc', 'ne': 'O', 'pos': 'n', 'arg': [], 'id': 1}, {'cont': '\xe5\xa4\xa9\xe5\xa4\xa9', 'parent': 3, 'semparent': 3, 'relate': 'ADV', 'semrelate': 'mMod', 'ne': 'O', 'pos': 'n', 'arg': [], 'id': 2}, {'cont': '\xe6\x9c\x89', 'parent': -1, 'semparent': -1, 'relate': 'HED', 'semrelate': 'Root', 'ne': 'O', 'pos': 'v', 'arg': [{'end': 1, 'type': 'A0', 'id': 0, 'beg': 0}, {'end': 2, 'type': 'TMP', 'id': 1, 'beg': 2}], 'id': 3}, {'cont': '\xef\xbc\x8c', 'parent': 3, 'semparent': 3, 'relate': 'WP', 'semrelate': 'mPunc', 'ne': 'O', 'pos': 'wp', 'arg': [], 'id': 4}, {'cont': '\xe4\xb8\xad\xe5\x9b\xbd', 'parent': 10, 'semparent': 10, 'relate': 'SBV', 'semrelate': 'Exp', 'ne': 'S-Ns', 'pos': 'ns', 'arg': [], 'id': 5}, {'cont': '\xe8\xbf\x99', 'parent': 7, 'semparent': 7, 'relate': 'ATT', 'semrelate': 'Sco', 'ne': 'O', 'pos': 'r', 'arg': [], 'id': 6}, {'cont': '\xe4\xb8\x80', 'parent': 8, 'semparent': 8, 'relate': 'ATT', 'semrelate': 'Quan', 'ne': 'O', 'pos': 'm', 'arg': [], 'id': 7}, {'cont': '\xe5\xb9\xb4', 'parent': 10, 'semparent': 10, 'relate': 'ADV', 'semrelate': 'Proc', 'ne': 'O', 'pos': 'q', 'arg': [], 'id': 8}, {'cont': '\xe5\xb0\xa4\xe5\x85\xb6', 'parent': 10, 'semparent': 10, 'relate': 'ADV', 'semrelate': 'mConj', 'ne': 'O', 'pos': 'd', 'arg': [], 'id': 9}, {'cont': '\xe5\xa4\x9a', 'parent': 3, 'semparent': 3, 'relate': 'COO', 'semrelate': 'eSucc', 'ne': 'O', 'pos': 'a', 'arg': [{'end': 6, 'type': 'ADV', 'id': 0, 'beg': 6}, {'end': 9, 'type': 'ADV', 'id': 1, 'beg': 9}], 'id': 10}, {'cont': '\xe3\x80\x82', 'parent': 3, 'semparent': 10, 'relate': 'WP', 'semrelate': 'mPunc', 'ne': 'O', 'pos': 'wp', 'arg': [], 'id': 11}];
    
    //画布周边的空白
    var margin = {top: 20, right: 25, bottom: 20, left: 25, middle: 60, text_top: 30 };
	
	//椭圆弧的半轴长比例
	var macroaxis=5;
	var minoraxis=3;
	
	
	data.unshift({"id": -1, 
				"cont": "Root", "pos": "",});  
    
    var graph_width;
    data.forEach(function(d,i){
        d.x = i * margin.middle;
        d.y = 0;
        graph_width = d.x;
    });	
    
    while (graph_width > 1200) {
        margin.middle *= 0.9;
        margin.text_top *= 0.9;
        data.forEach(function(d,i){
            d.x = i * margin.middle;
            d.y = 0;
            graph_width = d.x;
        });	
    }

	var width = graph_width;
	var height = graph_width/(macroaxis*2)*minoraxis;
	
	data.forEach(function(x,y){
			x.y = height-10;
    });	
	data.forEach(function(item_x){
		data.forEach(function(item_y){
			if(item_x.parent == item_y.id)
			{
				//指向时可以做一些调整 指出去+1 被指-1...
				var aim = {x: item_x.x, y: item_x.y};
				var start = {x: item_y.x, y: item_y.y};
				var dir = 1//1为顺指针 0为逆时针
				if (item_x.id < item_y.id) {
					 dir = 0;
				}
					
				item_x.curve_path = "M"+start.x+","+start.y+
				" A"+macroaxis+","+minoraxis+" 0 1,"
				+dir+" "+aim.x+","+aim.y;
				
				//计算文字标签的坐标
				item_x.tagX = (start.x + aim.x)/2
				item_x.tagY = start.y - Math.abs(start.x-aim.x)/(macroaxis*2)*minoraxis;
				//console.log(x);
			}
		
		});
	});
    
    
    var divid = '#parserTree';
	var svg = d3.select(divid).append("svg")
        .attr("width", width  + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom + margin.text_top*2)
        //.attr("style","border:2px solid black")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
				

	/*SVG的<defs>元素用于预定义一个元素使其能够在SVG图像中重复使用。
	例如你可以将一些图形制作为一个组，并用<defs>元素来定义它，然后
	你就可以在SVG图像中将它当做简单图形来重复使用。*/

	//创建箭头
	var defs = svg.append("defs");
	var arrowMarker = defs.append ("marker")
							.attr("id","arrow")
							.attr("markerUnits","strokeWidth")
							.attr("markerWidth","9")
							.attr("markerHeight","9")
							.attr("viewBox","0 0 12 12")
							//refX refY在 viewBox 内的基准点，绘制时此点在直线端点上
							.attr("refX","6")
							.attr("refY",6)
							.attr("orient","auto");
	//画出箭头的样子
	var arrow_path = "M2,2 L10,6 L2,10 L6,6 L2,2";
	arrowMarker.append("path")
			.attr("d",arrow_path)
			.attr("fill","blue");
		
	var curve = svg.selectAll(".curve")
				.data(data)
				.enter()
				.append("path")
				.attr("d",function(d,i){ 
                    return d.curve_path;
                })
				//在曲线所围的区域的填充色
				.attr("fill","none")
				.attr("stroke","red")
				.attr("stroke-width",2)
				.attr("marker-end","url(#arrow)")
				.attr("class","curve");			
		
			
    //关系标签
	var tag = svg.selectAll(".tag")
				.data(data)
				.enter().append("text")
				.attr("class","tag")
				.attr("x",function(d){
                    return d.tagX;
                })
				.attr("y",function(d){
					return d.tagY - 2;
                })
				.attr("text-anchor", "middle")
				.text(function(d){
                    return d.relate;
                });		

	//显示单词		
    svg.append("g")
        .selectAll("cont_text")
        .data(data)
        .enter()
        .append("text")
        .attr("x",function(d){
            return d.x;
        })
        .attr("y",function(d){
            return d.y + margin.text_top;})
        .attr("text-anchor", "middle")
        .html(function(d, i){
            return d.cont;
        })
        .on("mouseover",function(d){
            tag.style("fill-opacity",function(tag){
                if( tag.id != d.id && tag.parent != d.id )
                    return 0;
                });
            curve.style("opacity",function(curve){
                if( curve.id != d.id && curve.parent != d.id )
                    return 0;
                });	
        })
        .on("mouseout",function(d){
            tag.style("fill-opacity",function(tag){
                if( tag.id != d.id && tag.parent != d.id )
                    return 1;
            });
            curve.style("opacity",function(curve){
                if( curve.id != d.id && curve.parent != d.id )
                    return 1;
            });	
        });
    
    //显示词性
    svg.append("g")
        .selectAll("pos_text")
        .data(data)
        .enter()
        .append("text")
        .attr("x",function(d){
            return d.x;
        })
        .attr("y",function(d){
            return d.y + margin.text_top*1.7;})
        .attr("text-anchor", "middle")
        .text(function(d, i){
            return d.pos;
        })
}













