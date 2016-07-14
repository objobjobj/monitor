# -*- coding:utf-8 -*- 
from kazoo.client import KazooClient
import json

class GetInfo:
    def __init__(self):
        self.all_info = {}
        self.SERVER_IP_AND_PORT = "localhost:2181"
        self.zk = None
    
    def start_zk(self):
        self.zk = KazooClient(hosts=self.SERVER_IP_AND_PORT)
        self.zk.start();
    
    def getInfo(self):
        children = self.zk.get_children("/monitorData")
        node_nums = len(children)
        for i in range(node_nums):
            data, stat = self.zk.get("/monitorData/" + str(children[i]))
            print data
            self.all_info[children[i]] = json.loads(data.decode("utf-8"))
        return self.all_info
        


if __name__ == "__main__":
    gi = GetInfo()
    gi.start_zk();
    print gi.getInfo()
