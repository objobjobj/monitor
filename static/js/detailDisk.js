var prev = 0
var curr = 0

function drawDiskline() {
    $('#disk-charts').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    var series2 = this.series[1];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = Math.random()*200;
                            y2 = Math.random()*200;
                        series.addPoint([x, y], true, true);
                        series2.addPoint([x, y2], true, true);
                    }, 1000);
                }
            }
        },

        title: {
             text: '磁盘读写速度'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '读写速度MB/s'
            },
            plotLines: [{
                value: 0,
                width: 1000,
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + '速度:' + '</b><br/>' +
                    /*Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +*/
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: true
        },
        exporting: {
            enabled: false
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled:false
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '读出速度',
            /*yAxis: 0,*/
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: 0
                    });
                }
                return data;
            }())
        },
        
        {
            name: '写入速度',
            /*yAxis: 1,*/
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: 0
                    });
                }
                return data;
            }())
        }]

    });
}





$(document).ready(function() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    drawDiskline();
});