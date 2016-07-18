# -*- coding:utf-8 -*- 

import psutil
import json
import time

static_all_info = {}
static_all_info["cpu_percent"] = []
static_all_info["virtual_memory"] = []
static_max_length = 60

class CollectMachineInfo:

    def collectInfo(self):
        if len(static_all_info["cpu_percent"]) > static_max_length:
            static_all_info["cpu_percent"] = static_all_info["cpu_percent"][1:len(static_all_info["cpu_percent"])]
            #static_all_info["virtual_memory"].append(self._get_timestamp() + "\t" + self._get_virtual_memory())

    	static_all_info["cpu_percent"].append({self._get_timestamp():self._get_cpu_percent()})
        static_all_info["virtual_memory"].append({self._get_timestamp():self._get_virtual_memory()})
        return json.dumps(static_all_info)
        
    def _get_virtual_memory(self):
    	return str(psutil.virtual_memory())
    
    def _get_cpu_percent(self):
        return str(psutil.cpu_percent(interval=1, percpu=True))

    def _get_timestamp(self):
    	return str(int(time.time()))
