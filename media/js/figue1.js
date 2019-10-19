var myChart = echarts.init(document.getElementById('main'));

var words = new Array(0);
$.getJSON('../media/js/dic.json',function (data) {
    $.each(data,function (i,v) {
        //console.log(i);
        //console.log(v);
        words.push({"name":i,
        "value":v.value,
        "symbolSize":v.symbolSize,
        "draggable":v.draggable,
        "itemStyle":v.itemStyle,
        "label":v.value
        })
    });
    var option = {
        //backgroundColor: '#2e3131',
        backgroundColor: '#fff',

        tooltip: {},
        hoverAnimation:true,
        animationDurationUpdate: function(idx) {
            return idx * 100;
        },
        animationEasingUpdate: 'bounceIn',
        color: ['#fff', '#fff', '#fff'],
        series: [{
            type: 'graph',
            layout: 'force',
            force: {
                repulsion: 200,
                edgeLength: 15
            },
            roam: true,
            label: {
                show:true,
                fontFamily:'Times_New_Roman',
                fontSize:15
            },
            focusNodeAdjacency: true,
            data:words,
            /*silent : false,
            onclick:function () {
                console.log("1")
            }*/
        }],
    };
    myChart.setOption(option);
});
//console.log(words);


