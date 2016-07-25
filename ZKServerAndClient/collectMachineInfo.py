# -*- coding:utf-8 -*- 

import psutil
import json
import time

static_all_info = {}
#static_all_info["cpu_percent"] = []
#static_all_info["virtual_memory"] = []
#static_all_info["net_io"] = []
#static_all_info["cpu_times_percent"] = []
static_all_info["disk_io"] = [{},{}]
static_all_info["net_io_sent"] = [{},{}]
static_all_info["net_io_recv"] = [{},{}]

static_max_length = 60

## just get info once time
static_all_info_just_one_time = {}
#static_all_info_just_one_time["cpu_count"] = []
#static_all_info_just_one_time["disk_usage"] = []
#static_all_info_just_one_time["users"] = []
#static_all_info_just_one_time["virtual_memory"] = []


class CollectMachineInfo:

    def __init__(self, is_server):
        self.is_server = is_server

    def collectInfoJustOneTime(self):
        static_all_info_just_one_time["is_server"] = (self.is_server)
        static_all_info_just_one_time["cpu_count"] = (self._get_cpu_count())
        static_all_info_just_one_time["disk_usage"] = (self._get_disk_usage())
        static_all_info_just_one_time["users"] = (self._get_users())
        static_all_info_just_one_time["virtual_memory"] = (self._get_virtual_memory())

        return json.dumps(static_all_info_just_one_time)


    def collectInfo(self):
        # set the max_length
        #if len(static_all_info["cpu_percent"]) > static_max_length:
        #    static_all_info["cpu_percent"] = static_all_info["cpu_percent"][1:len(static_all_info["cpu_percent"])]
            #static_all_info["virtual_memory"].append(self._get_timestamp() + "\t" + self._get_virtual_memory())

        #print static_all_info
        static_all_info["is_server"] = {self._get_timestamp():self.is_server}
    	static_all_info["cpu_percent"] = {self._get_timestamp():self._get_cpu_percent()}
        static_all_info["cpu_percent_average"] = {self._get_timestamp():self._get_cpu_percent_average()}
        static_all_info["cpu_times_percent"] = {self._get_timestamp():self._get_cpu_times_percent()}
        static_all_info["virtual_memory"] = {self._get_timestamp():self._get_virtual_memory()}
        static_all_info["swap_memory"] = {self._get_timestamp():self._get_swap_memory()}
        static_all_info["disk_usage"] = {self._get_timestamp():self._get_disk_usage()}
        static_all_info["remote_desktop_count"] = {self._get_timestamp():self._get_remote_desktop_count()}

        # need to storage to calculate speed
        static_all_info["disk_io"] = static_all_info["disk_io"][1:len(static_all_info["disk_io"])]
        static_all_info["disk_io"].append(
            {self._get_timestamp():self._get_disk_io()})
        static_all_info["net_io_sent"] = static_all_info["net_io_sent"][1:len(static_all_info["net_io_sent"])]
        static_all_info["net_io_sent"].append(
            {self._get_timestamp():self._get_net_io_sent()})
        static_all_info["net_io_recv"] = static_all_info["net_io_recv"][1:len(static_all_info["net_io_recv"])]
        static_all_info["net_io_recv"].append(
            {self._get_timestamp():self._get_net_io_recv()})
        return json.dumps(static_all_info)

    def _get_users(self):
        return str(psutil.users()[0])

    def _get_cpu_count(self):
        return str(psutil.cpu_count())
        
    def _get_disk_usage(self):
        return str(psutil.disk_usage('/'))

    def _get_virtual_memory(self):
    	return str(psutil.virtual_memory())

    def _get_swap_memory(self):
        return str(psutil.swap_memory())

    def _get_disk_io(self):
        return str(psutil.disk_io_counters(perdisk=False))
    
    def _get_cpu_percent(self):
        return str(psutil.cpu_percent(interval=1, percpu=True))

    def _get_cpu_percent_average(self):
        return str(psutil.cpu_percent())

    def _get_cpu_times_percent(self):
        return str(psutil.cpu_times_percent())

    def _get_net_io_sent(self):
        return str(psutil.net_io_counters().bytes_sent)

    def _get_net_io_recv(self):
        return str(psutil.net_io_counters().bytes_recv)

    def _get_remote_desktop_count(self):
        count = 0
        port = 3389
        records = psutil.net_connections()
        for record in records:
            if record.laddr[1] == port and record.status=='ESTABLISHED':
                count += 1
        #print count
        return count

    def _get_timestamp(self):
    	return str(int(time.time()))
