var prev = 0
var curr = 0

function fill_cpu_time(records) {
    $("#us").text(records["user"]+"%")
    $("#sy").text(records["system"]+"%")
    $("#ni").text(records["nice"]+"%")
    $("#id").text(records["idle"]+"%")
}


function first_fill_cpus_percent(cpu_percent_list) {
    var cpu_percent_data_div = $('#cpu-percent-data-div')
    var cpu_num = cpu_percent_list.length
    var i = 0
    var current_ul
    for (i = 0; i < cpu_num; i++) {
        if (i % 4 == 0) {
            current_ul = $("<ul class='row-list'></ul>")
        }
        current_ul.append($("<li>CPU" + (i+1) + ": <span id='cpu" + (i+1) +"'>" + cpu_percent_list[i] + "%</span></li>"))
        if (i %4 == 3) {
            cpu_percent_data_div.append(current_ul)
        }
        if (i %4 != 3 && i == cpu_num-1) {
            cpu_percent_data_div.append(current_ul)
        }
    }

}

function fill_cpu_data_for_first(data) {
    var records = eval('(' + data + ')')
    fill_cpu_time(records)
    first_fill_cpus_percent(eval('(' + records['each_cpu_percent'] + ')'))
}

function fill_cpu_data_for_after(data) {
    var records = eval('(' + data + ')')
    fill_cpu_time(records)
    var cpu_percent_list = eval('(' + records['each_cpu_percent'] + ')')
    var i
    for (i = 0 ; i < cpu_percent_list.length; i++) {
        $('#cpu'+(i+1)).text(cpu_percent_list[i]+"%")
    }
}

function drawCPUline() {
    $('#cpu-charts').highcharts({
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
             text: 'CPU利用率'
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
                return '<b>' + 'CPU利用率' + '</b><br/>' +
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
            name: 'cpu percent',
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



function get_cpu_data_first() {
    var ip = $("#machine_ip").text().trim()
    $.ajax({
            type: "GET",
            url:"/machine/" + ip + "/cpu/request",
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
                    curr = Number(records["average_cpu_percent"])
                    fill_cpu_data_for_first(data)
                } else {
                    prev = curr
                    curr = 0
                }
               
            }
   });

}

function get_cpu_data_after() {
    var ip = $("#machine_ip").text().trim()
    $.ajax({
            type: "GET",
            url:"/machine/" + ip + "/cpu/request",
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
                    curr = Number(records["average_cpu_percent"])
                    fill_cpu_data_for_after(data)
                } else {
                    prev = curr
                    curr = 0
                }
               
            }
   });

}

function continuously_get_cpu_data() {
    get_cpu_data_after()
    setTimeout("continuously_get_cpu_data()", 1000);
}




$(document).ready(function() {
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    get_cpu_data_first()
    setTimeout("continuously_get_cpu_data()", 1000);
    drawCPUline();
});

