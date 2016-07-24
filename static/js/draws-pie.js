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

function get_virtual_resource_data() {
    var total_core = Number($('#total-core-td').text())
    var used_core = Number($('#used-core-td').text())

    var total_mem_str = $('#total-memory-td').text()
    var used_mem_str = $('#used-memory-td').text()
    var total_mem = Number(total_mem_str.substring(0, total_mem_str.length-2))
    var used_mem = Number(used_mem_str.substring(0, used_mem_str.length-2))

    var total_disk_str = $('#total-disk-td').text()
    var used_disk_str = $('#used-disk-td').text()
    var total_disk = Number(total_disk_str.substring(0, total_disk_str.length-2))
    var used_disk = Number(used_disk_str.substring(0, used_disk_str.length-2))

    $('#total-core').text(total_core)
    $('#total-used-core').text(used_core)
    $('#total-memory').text(total_mem_str)
    $('#total-used-memory').text(used_mem_str)
    $('#total-disk').text(total_disk_str)
    $('#total-used-disk').text(used_disk_str)

    draw_pie("#core-pie", used_core/total_core*100);
    draw_pie("#memory-pie", used_mem/total_mem*100);
    draw_pie("#disk-pie", used_disk/total_disk*100);
}

$(document).ready(function() {
   get_virtual_resource_data()
});