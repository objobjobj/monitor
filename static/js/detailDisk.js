var prev_read = 0
var curr_read = 0

var prev_write = 0
var curr_write = 0

function fill_disk_data(data) {
    var records = eval('(' + data + ')')
    $("#disk-total").text(records["disk_total"]+"GB")
    $("#disk-used").text(records["disk_used"]+"GB")
    $("#disk-free").text(records["disk_free"]+"GB")
    $("#disk-used-percent").text(records["disk_percent"]+"%")
    $("#write-speed").text(records["disk_write_speed"]+"byte/s")
    $("#read-speed").text(records["disk_read_speed"]+"byte/s")
    
}

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
                            y = curr_read;
                            y2 = curr_write;
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
                text: '读写速度B/s'
            },
            plotLines: [{
                value: 0,
                width: 1000*1024*1024,
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


function get_disk_data() {
    var ip = $("#machine_ip").text().trim()
    $.ajax({
            type: "GET",
            url:"/machine/" + ip + "/disk/request",
            data: null,
            async: true,
            dataType: "text",
            error: function(request) {
                console.log("connection error");
                prev_write = curr_write
                curr_write = 0
                prev_read = curr_read
                curr_read = 0
            },
            success: function(data) {
                if (data != null || data != "") {
                    prev_write = curr_write
                    prev_read = curr_read
                    var records = eval('(' + data + ')')
                    curr_read = Number(records["disk_read_speed"])
                    curr_write = Number(records["disk_write_speed"])
                    fill_disk_data(data)
                } else {
                    prev_write = curr_write
                    curr_write = 0
                    prev_read = curr_read
                    curr_read = 0
                }
               
            }
   });

}

function continuously_get_disk_data() {
    get_disk_data()
    setTimeout("continuously_get_disk_data()", 1000);
}

$(document).ready(function() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    continuously_get_disk_data()
    drawDiskline();
});