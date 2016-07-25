function fill_data(data) {
    var records = eval('(' + data + ')')
    var trs = $('#hypervisors tbody').children('tr')
    var index = 1
    var tmp = 0
    for (key in records) {
        var resource_data = eval('(' + records[key] + ')')
        if (resource_data["is_server"] == 'True') {
            tmp = 0
        } else {
            tmp = index
            index = index+1
        }

        var curr_tds = $(trs[tmp]).children('td')
        $(curr_tds[1]).text(key)
        if (resource_data["status"] == "negative") {
            $(curr_tds[2]).text("-")
            $(curr_tds[3]).text("-")
            $(curr_tds[4]).text("-")
            $(curr_tds[5]).text("-")
            $(curr_tds[6]).text("-")
            $(curr_tds[8]).text("-")
            $($(curr_tds[9]).children('a')[0]).attr("onclick", "return false")
        } else {
            $(curr_tds[2]).text(resource_data["cpu_percent_average"])
            $(curr_tds[3]).text(resource_data["memory_percent"])
            $(curr_tds[4]).text(resource_data["disk_percent"])
            $(curr_tds[5]).text(resource_data["net_io_sent"])
            $(curr_tds[6]).text(resource_data["net_io_recv"])
            $(curr_tds[8]).text(resource_data["remote_desktop_count"])
            $($(curr_tds[9]).children('a')[0]).attr("onclick", "return true")
        }
        $(curr_tds[7]).text(resource_data["status"])
        if (tmp == 0) {
            $(curr_tds[0]).text("服务器")
        } else {
            $(curr_tds[0]).text("虚拟机")
        }

    }
}


function captureInfo() {
    $.ajax({
            type: "GET",
            url:"/machines/request",
            data: null,
            async: true,
            dataType: "text",
            error: function(request) {
                console.log("connection error");
            },
            success: function(data) {
               if (data != null || data != "") {
                    fill_data(data)
               }
               
            }
   });
}

function continuously_capture() {
    captureInfo()
    setTimeout("continuously_capture()", 2000);
}

$(document).ready(function() {
   continuously_capture()
});
