# -*- coding:utf-8 -*- 
from kazoo.client import KazooClient
import json
from RRDDrawDir.RRDDraw import RRDDraw


##
##                 -----                                  |----   cpu_precent
#  all_info struct|
#                  -----  Virutal Machine Mac Address ----|----   virtual_memory    |---  net_io_sent
#                 |
#                  -----                                  |----   net_io     -------|---  net_io_recv
##
##
class GetInfo:
    def __init__(self):
        self.all_info = {}
        #self.SERVER_IP_AND_PORT = "127.0.0.1:2181"
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
            data2, stat2 = self.zk.get("/monitorDataJustOneTime/" + str(children[i]))
            print json.loads(data2.decode("utf-8"))
            #print data
            #print str(children[i])
            #print json.loads(data.decode("utf-8"))
            self.all_info[children[i]] = json.loads(data.decode("utf-8"))
            #for key in self.all_info[children[i]].keys():
            #    print self.all_info[children[i]][key]
        return self.all_info


if __name__ == "__main__":
    gi = GetInfo()
    gi.start_zk()

    rrdDraw = RRDDraw(gi.getInfo())
    rrdDraw.draw()

