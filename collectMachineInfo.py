# -*- coding:utf-8 -*- 

import psutil
import json
import time

static_all_info = {}
static_all_info["cpu_percent"] = []
static_all_info["virtual_memory"] = []
static_all_info["net_io"] = []
static_all_info["cpu_times_percent"] = []
static_max_length = 60

## just get info once time
static_all_info_just_one_time = {}
static_all_info_just_one_time["cpu_count"] = []
static_all_info_just_one_time["disk_usage"] = []
static_all_info_just_one_time["users"] = []


class CollectMachineInfo:

    def collectInfoJustOneTime(self):
        static_all_info_just_one_time["cpu_count"].append(self._get_cpu_count())
        static_all_info_just_one_time["disk_usage"].append(self._get_disk_usage())
        static_all_info_just_one_time["users"].append(self._get_users())

        return json.dumps(static_all_info_just_one_time)


    def collectInfo(self):
        # set the max_length
        if len(static_all_info["cpu_percent"]) > static_max_length:
            static_all_info["cpu_percent"] = static_all_info["cpu_percent"][1:len(static_all_info["cpu_percent"])]
            #static_all_info["virtual_memory"].append(self._get_timestamp() + "\t" + self._get_virtual_memory())

    	static_all_info["cpu_percent"].append({self._get_timestamp():self._get_cpu_percent()})
        static_all_info["cpu_times_percent"].append({self._get_timestamp():self._get_cpu_times_percent()})
        static_all_info["virtual_memory"].append({self._get_timestamp():self._get_virtual_memory()})
        static_all_info["net_io"].append({self._get_timestamp():self._get_net_io_sent()+':'+self._get_net_io_recv()})
        return json.dumps(static_all_info)

    def _get_users(self):
        return str(psutil.users())

    def _get_cpu_count(self):
        return str(psutil.cpu_count())
        
    def _get_disk_usage(self):
        return str(psutil.disk_usage('/'))

    def _get_virtual_memory(self):
    	return str(psutil.virtual_memory())
    
    def _get_cpu_percent(self):
        return str(psutil.cpu_percent(interval=1, percpu=True))

    def _get_cpu_times_percent(self):
        return str(psutil.cpu_times_percent(interval = 1, percpu=True))

    def _get_net_io_sent(self):
        return str(psutil.net_io_counters().bytes_sent)

    def _get_net_io_recv(self):
        return str(psutil.net_io_counters().bytes_recv)

    def _get_timestamp(self):
    	return str(int(time.time()))
