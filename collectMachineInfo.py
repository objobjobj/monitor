# -*- coding:utf-8 -*- 

import psutil
import json

class CollectMachineInfo:
    
    def __init__(self):
        self.all_info = {}
    
    def collectInfo(self):
        self.all_info["cpu_percent"] = self._get_cpu_percent()
        
        return json.dumps(self.all_info)
        
    
    def _get_cpu_percent(self):
        return psutil.cpu_percent(interval=1, percpu=True)
