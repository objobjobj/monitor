var prev = 0
var curr = 0

function fill_mem_data(data) {
    var records = eval('(' + data + ')')
    $("#total-mem").text(records["vmem_total"]+"GB")
    $("#avail-mem").text(records["vmem_available"]+"GB")
    $("#mem-used-percent").text(records["vmem_percent"]+"%")
    $("#mem-used").text(records["vmem_used"]+"GB")
    $("#mem-free").text(records["vmem_free"]+"GB")
    $("#total-swap").text(records["swap_total"]+"GB")
    $("#swap-used").text(records["swap_used"]+"GB")
    $("#swap-free").text(records["swap_free"]+"GB")
    $("#swap-used-percent").text(records["swap_percent"]+"%")
}

function drawMemline() {
    $('#mem-charts').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = curr;
                        series.addPoint([x, y], true, true);
                    }, 1000);
                }
            }
        },

        title: {
             text: '内存利用率'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '利用率%'
            },
            plotLines: [{
                value: 0,
                width: 100,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function () {
                return '<b>' + '内存利用率' + '</b><br/>' +
                    /*Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +*/
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'memory percent',
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


function get_mem_data() {
    var ip = $("#machine_ip").text().trim()
    $.ajax({
            type: "GET",
            url:"/machine/" + ip + "/memory/request",
            data: null,
            async: true,
            dataType: "text",
            error: function(request) {
                console.log("connection error");
                prev = curr
                curr = 0
            },
            success: function(data) {
                if (data != null || data != "") {
                    prev = curr
                    var records = eval('(' + data + ')')
                    curr = Number(records["vmem_percent"])
                    fill_mem_data(data)
                } else {
                    prev = curr
                    curr = 0
                }
               
            }
   });

}

function continuously_get_mem_data() {
    get_mem_data()
    setTimeout("continuously_get_mem_data()", 1000);
}

$(document).ready(function() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    continuously_get_mem_data()
    drawMemline();
});