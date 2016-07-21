function draw_pie(renderToStr, usedpercent) {
    $(renderToStr).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie',
            height: "150"
        },

        exporting:{
            enabled:false
        },

        credits: {
            enabled: false
        },
            
        title: {
            text:null
        },

        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                /*size:130,*/
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                /*showInLegend: true*/
            }
        },
        series: [{
            name: '比例',
            colorByPoint: true,
            data: [
                {name: '未使用', y: 100-usedpercent}, 
                {name: '已使用',y: usedpercent /*sliced: true, selected: true*/}
            ]
        }]
    });

}