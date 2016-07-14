# -*- coding:utf-8 -*-  
import threading
import time
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import ConnectionLossException
from kazoo.exceptions import NoAuthException
from kazoo.handlers.threading import KazooTimeoutError

#from kazoo.handlers.gevent import SequentialGeventHandler
from collectMachineInfo import *


#perms: read:1<<0; write:1<<1; create:1<<2; delete:1<<3; admin:1<<4
#  perms: 0x1f: READ | WRITE | CREATE | DELETE | ADMIN
#scheme: "world":has a single id, anyone, that represents anyone.
#      : "auth": doesn't use any id, represents any authenticated user.
#ZOO_OPEN_ACL_UNSAFE = {"perms":0x1f, "scheme":"world", "id" :"anyone"}

class NodeMonitor:
    STATIC_NODE_ID = 0
    global t
    def __init__(self):
        self.zk = None
        self.SERVER_IP_AND_PORT = "localhost:2181"
        self.NODE_ID = str(NodeMonitor.STATIC_NODE_ID)
        NodeMonitor.STATIC_NODE_ID += 1 
    
    def start_zk(self):
        self.zk = KazooClient(hosts=self.SERVER_IP_AND_PORT)
        
        self.zk.add_listener(self._connection_listener)
        #self.zk.start();
        try:
            self.zk.start()
        except (KazooTimeoutError):
            print "connect fail, going to reconnect"
            time.sleep(5.0)
            self.start_zk()
            
        self.zk.ensure_path("/monitorData/"+ self.NODE_ID + "/cpu--")
        self.zk.ensure_path("/monitorData/"+ self.NODE_ID + "/mem--")
    
    def start_update_info(self):
        t = threading.Timer(0.0, self._update_info)
        t.start()
        
    
    def _update_info_once(self):
        cmi = CollectMachineInfo()
        async_obj = self.zk.set_async("/monitorData/"+ self.NODE_ID, (cmi.collectInfo()).encode(encoding="utf-8"))
        async_obj.rawlink(self._update_info_callback)
    
        
    def _connection_listener(self, state):
        if state == KazooState.LOST:
            print "connection lost, going to connect again"
            self.start_zk();
        elif state == KazooState.SUSPENDED:
            print "suspended"
        else:
            print "connected ok"
    
    def _update_info_callback(self, async_obj):
        try:
            print "update success"
        except (ConnectionLossException, NoAuthException):
            print "exception!"
    
    def _update_info(self):
        print "begin to update"
        self._update_info_once()
        t = threading.Timer(5.0, self._update_info)
        t.start()
        

if __name__ == "__main__":
    nm = NodeMonitor()
    nm.start_zk()
    nm.start_update_info()
    
        