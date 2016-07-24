function fill_daemon_data(data) {
    var records = eval('(' + data + ')')
    var table_body = $('#daemon-table tbody')
    var trs = $(table_body).children('tr')
    var trs_num = trs.length
    var row_record = null
    var count = 0
    var curr_tr = null
    var tds = null
    for (key in records) {
        //row_record = eval('('+records[key]+')')
        row_record = records[key]
        if (count >= trs_num) {
            table_body.append($("<tr><td class='sortable normal_column'>"+ row_record["id"] +"</td><td class='sortable normal_column'>"+ row_record["name"] +"</td><td class='sortable normal_column'>" + Math.round(row_record["memory_percent"]*1000)/1000 +"</td><td class='sortable normal_column'>" + row_record["exe"] +"</td></tr>"))
        } else {
            curr_tr = $(trs[count])
            tds = curr_tr.children('td')
            $(tds[0]).text(row_record["id"])
            $(tds[1]).text(row_record["name"])
            $(tds[2]).text(Math.round(row_record["memory_percent"]*1000)/1000)
            $(tds[3]).text(row_record["exe"])
            curr_tr.css("display", "table-row")
        }
        count = count+1
    }

    var i 
    var total = count
    for (i = count; i < trs_num; i++) {
        $(trs[i]).css("display", "none")
        total++
    }
    $('#record_count').text(total)

}


function get_daemon_data() {
    var ip = $("#machine_ip").text().trim()
    $.ajax({
            type: "GET",
            url:"/machine/" + ip + "/daemon/request",
            data: null,
            async: true,
            dataType: "text",
            error: function(request) {
                console.log("connection error");
            },
            success: function(data) {
                if (data != null || data != "") {
                    fill_daemon_data(data)
                }
               
            }
   });

}

function continuously_get_daemon_data() {
    get_daemon_data()
    setTimeout("continuously_get_daemon_data()", 10000);
}

$(document).ready(function() {
    continuously_get_daemon_data();
    //get_daemon_data()
});

