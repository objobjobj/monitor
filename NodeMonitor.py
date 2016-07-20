# -*- coding:utf-8 -*-  
import threading
import time
import socket
import uuid
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import ConnectionLossException
from kazoo.exceptions import NoAuthException
from kazoo.handlers.threading import KazooTimeoutError

#from kazoo.handlers.gevent import SequentialGeventHandler
from collectMachineInfo import *
from CollectProcessInfo import CollectProcessInfo


#perms: read:1<<0; write:1<<1; create:1<<2; delete:1<<3; admin:1<<4
#  perms: 0x1f: READ | WRITE | CREATE | DELETE | ADMIN
#scheme: "world":has a single id, anyone, that represents anyone.
#      : "auth": doesn't use any id, represents any authenticated user.
#ZOO_OPEN_ACL_UNSAFE = {"perms":0x1f, "scheme":"world", "id" :"anyone"}

def get_mac_address(): 
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return "".join([mac[e:e+2] for e in range(0,11,2)])


class NodeMonitor:
	# use mac address to divide different virtual machine
    STATIC_NODE_MAC_ADDRESS = get_mac_address()
    global t
    def __init__(self):
        self.zk = None
        #self.SERVER_IP_AND_PORT = "127.0.0.1:2181"
        self.SERVER_IP_AND_PORT = "172.18.229.251:2181"
        #STATIC_NODE_MAC_ADDRESS = get_mac_address()
        self.NODE_ID = str(NodeMonitor.STATIC_NODE_MAC_ADDRESS)
        print self.NODE_ID

    def start_zk(self):
        #self.zk = KazooClient("127.0.0.1:2181")
        self.zk = KazooClient("172.18.229.251:2181")
        
        self.zk.add_listener(self._connection_listener)
        #self.zk.start();
        try:
            self.zk.start()
            #print "zk-start-try"
        except (KazooTimeoutError):
            print "connect fail, going to reconnect"
            time.sleep(5.0)
            self.start_zk()
            
        self.zk.ensure_path("/monitorData/"+ self.NODE_ID)
    
    def start_update_info(self):
        t = threading.Timer(0.0, self._update_info)
        t.start()

        t2 = threading.Timer(0.0, self._update_info_10_second_once_time)
        t2.start()
    
    def _update_info_once(self):
        cmi = CollectMachineInfo()
        #print self.NODE_ID
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
        self.zk.ensure_path("/monitorData/"+ self.NODE_ID)
        self._update_info_once()
        t = threading.Timer(3.0, self._update_info)
        t.start()

    def _update_info_10_second_once_time(self):
    	self.zk.ensure_path("/monitorDataProcessInfo/"+ self.NODE_ID)
        self._update_info_once_10_second()
        t = threading.Timer(10.0, self._update_info_10_second_once_time)
        t.start()    	
        
    def _update_info_once_10_second(self):
    	cpi = CollectProcessInfo()
        #print self.NODE_ID
        async_obj = self.zk.set_async("/monitorDataProcessInfo/"+ self.NODE_ID, (cpi._get_process_info()).encode(encoding="utf-8"))
        async_obj.rawlink(self._update_info_callback)

    def _update_info_just_one_time(self):
    	print "just one time to update"
    	self.zk.ensure_path("/monitorDataJustOneTime/"+ self.NODE_ID)
    	cmi_just_one_time = CollectMachineInfo()
    	async_obj_just_one_time = self.zk.set_async("/monitorDataJustOneTime/"+ self.NODE_ID,
    		(cmi_just_one_time.collectInfoJustOneTime()).encode(encoding="utf-8"))
        async_obj_just_one_time.rawlink(self._update_info_callback)

if __name__ == "__main__":
    nm = NodeMonitor()
    nm.start_zk()
    nm._update_info_just_one_time()
    nm.start_update_info()
    
        