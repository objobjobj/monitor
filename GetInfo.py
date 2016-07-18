# -*- coding:utf-8 -*- 
from kazoo.client import KazooClient
import json
import RRDDraw


##
##                 -----                                  |----   cpu_precent
#  all_info struct|
#                  -----  Virutal Machine Mac Address ----|----   virtual_memory
#                 |
#                  -----    
##
##
class GetInfo:
    def __init__(self):
        self.all_info = {}
        self.SERVER_IP_AND_PORT = "172.18.229.251:2181"
        self.zk = None
    
    def start_zk(self):
        self.zk = KazooClient(hosts=self.SERVER_IP_AND_PORT)
        self.zk.start();
    
    def getInfo(self):
        children = self.zk.get_children("/monitorData")
        node_nums = len(children)
        for i in range(node_nums):
            data, stat = self.zk.get("/monitorData/" + str(children[i]))
            #print data
            #print str(children[i])
            #print json.loads(data.decode("utf-8"))
            self.all_info[children[i]] = json.loads(data.decode("utf-8"))
            #for key in self.all_info[children[i]].keys():
            #    print self.all_info[children[i]][key]
        return self.all_info
        
    def decodeInfo(self):
        #print self.all_info.keys()
        for mac_key in self.all_info.keys():
            mac_address = mac_key
            #print self.all_info[mac_address].keys()
            for key in self.all_info[mac_address].keys():
                print key
                if key == "cpu_percent":
                    print self.all_info[mac_address][key]
                if key == "virtual_memory":
                    print self.all_info[mac_address][key]


if __name__ == "__main__":
    gi = GetInfo()
    gi.start_zk()
    gi.getInfo()

    rrdDraw = RRDDraw

    #_rrdDraw.draw(gi.getInfo())
    #print gi.all_info
