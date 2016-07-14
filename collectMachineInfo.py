# -*- coding:utf-8 -*- 

import psutil
import json
import time

static_all_info = {}
static_all_info["cpu_percent"] = []
static_all_info["virtual_memory"] = []

class CollectMachineInfo:
    
    def __init__(self):
        self.count = 0

    def collectInfo(self):
        if self.count <= 3:
            static_all_info["cpu_percent"].append(self._get_timestamp() + "\t" + self._get_cpu_percent())
            static_all_info["virtual_memory"].append(self._get_timestamp() + "\t" + self._get_virtual_memory())
            self.count++
        else:
        return json.dumps(static_all_info)
        
    def _get_virtual_memory(self):
    	return str(psutil.virtual_memory())
    
    def _get_cpu_percent(self):
        return str(psutil.cpu_percent(interval=1, percpu=True))

    def _get_timestamp(self):
    	return str(int(time.time()))
