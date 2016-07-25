var prev_rec = 0
var curr_rec = 0

var prev_snd = 0
var curr_snd = 0

function fill_network_data(data) {
    var records = eval('(' + data + ')')
    $("#recv-total").text(records["net_total_recv"]+"B")
    $("#send_total").text(records["net_total_sent"]+"B")
    $("#recv-speed").text(records["net_recv_speed"]+"B/s")
    $("#send-speed").text(records["net_sent_speed"]+"B/s")
    
}

function drawNetworkline() {
    $('#network-charts').highcharts({
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
                            y = curr_rec;
                            y2 = curr_snd;
                        series.addPoint([x, y], true, true);
                        series2.addPoint([x, y2], true, true);
                    }, 1000);
                }
            }
        },

        title: {
             text: '网络收发速度'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '收发速度B/s'
            },
            plotLines: [{
                value: 0,
                width: 1024*1024,
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
            name: '接收速度',
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
            name: '发送速度',
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


function get_network_data() {
    var ip = $("#machine_ip").text().trim()
    $.ajax({
            type: "GET",
            url:"/machine/" + ip + "/network/request",
            data: null,
            async: true,
            dataType: "text",
            error: function(request) {
                console.log("connection error");
                prev_rec = curr_rec
                curr_rec = 0
                prev_snd = curr_snd
                curr_snd = 0
            },
            success: function(data) {
                if (data != null || data != "") {
                    prev_rec = curr_rec
                    prev_snd = curr_snd
                    var records = eval('(' + data + ')')
                    curr_rec = Number(records["net_recv_speed"])
                    curr_snd = Number(records["net_sent_speed"])
                    fill_network_data(data)
                } else {
                    prev_rec = curr_rec
                    curr_rec = 0
                    prev_snd = curr_snd
                    curr_snd = 0
                }
               
            }
   });

}

function continuously_get_network_data() {
    get_network_data()
    setTimeout("continuously_get_network_data()", 1000);
}

$(document).ready(function() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    continuously_get_network_data();
    drawNetworkline();
});