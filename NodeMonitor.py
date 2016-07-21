# -*- coding:utf-8 -*-  
import threading
import time
import socket
import uuid
import sys
import socket
import fcntl
import struct
import os
import fcntl, sys, time, os
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

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

class NodeMonitor:
    
    global t

    def __init__(self, argv1):
        # the client net card eth0
        self.static_net_card = 'eth0'
        self.static_path_for_data_3_second_once_time = "/monitorData"
        self.static_path_for_data_10_second_once_time = "/monitorDataProcessInfo"
        self.static_path_for_data_just_one_time = "/monitorDataJustOneTime"
        
        if argv1 == '-server':
            self._set_up_server_path()

        # use mac address to divide different virtual machine
        self.STATIC_NODE_IP_ADDRESS = get_ip_address(self.static_net_card)
        self.STATIC_NODE_MAC_ADDRESS = get_mac_address()
        

        self.zk = None
        #self.SERVER_IP_AND_PORT = "127.0.0.1:2181"
        self.SERVER_IP_AND_PORT = "172.18.229.251:2181"
        #STATIC_NODE_MAC_ADDRESS = get_mac_address()
        self.NODE_ID = str(self.STATIC_NODE_IP_ADDRESS)
        self.NODE_ID_PATH = '/' + self.NODE_ID
        #print self.NODE_ID

    def _set_up_server_path(self):
        # the server net card eth1
        self.static_net_card = 'eth1'
        self.static_path_for_data_3_second_once_time += "Server"
        self.static_path_for_data_10_second_once_time += "Server"
        self.static_path_for_data_just_one_time += "Server"

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
            
        self.zk.ensure_path(self.static_path_for_data_3_second_once_time
            + self.NODE_ID_PATH)
    
    def start_update_info(self):
        t = threading.Timer(0.0, self._update_info)
        t.start()

        t2 = threading.Timer(0.0, self._update_info_10_second_once_time)
        t2.start()
    
    def _update_info_once(self):
        cmi = CollectMachineInfo()
        #print self.NODE_ID
        async_obj = self.zk.set_async(self.static_path_for_data_3_second_once_time
            + self.NODE_ID_PATH, (cmi.collectInfo()).encode(encoding="utf-8"))
        async_obj.rawlink(self._update_info_callback)
    
        
    def _connection_listener(self, state):
        if state == KazooState.LOST:
            print "connection lost, going to connect again"
            self.start_zk();
        elif state == KazooState.SUSPENDED:
            print "suspended"
        else:
            #print "connected ok"
            return
    
    def _update_info_callback(self, async_obj):
        try:
            #print "update success"
            return
        except (ConnectionLossException, NoAuthException):
            print "exception!"
    
    def _update_info(self):
        #print "begin to update"
        self.zk.ensure_path(self.static_path_for_data_3_second_once_time
            + self.NODE_ID_PATH)
        self._update_info_once()
        t = threading.Timer(1.0, self._update_info)
        t.start()

    def _update_info_10_second_once_time(self):
    	self.zk.ensure_path(self.static_path_for_data_10_second_once_time
            + self.NODE_ID_PATH)
        self._update_info_once_10_second()
        t = threading.Timer(10.0, self._update_info_10_second_once_time)
        t.start()    	
        
    def _update_info_once_10_second(self):
    	cpi = CollectProcessInfo()
        #print self.NODE_ID
        async_obj = self.zk.set_async(self.static_path_for_data_10_second_once_time
            + self.NODE_ID_PATH, (cpi._get_process_info()).encode(encoding="utf-8"))
        async_obj.rawlink(self._update_info_callback)

    def _update_info_just_one_time(self):
    	#print "just one time to update"
    	self.zk.ensure_path(self.static_path_for_data_just_one_time
            + self.NODE_ID_PATH)
    	cmi_just_one_time = CollectMachineInfo()
    	async_obj_just_one_time = self.zk.set_async(self.static_path_for_data_just_one_time
            + self.NODE_ID_PATH,
    		(cmi_just_one_time.collectInfoJustOneTime()).encode(encoding="utf-8"))
        async_obj_just_one_time.rawlink(self._update_info_callback)

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):  
     #重定向标准文件描述符（默认情况下定向到/dev/null）  
    try:   
        pid = os.fork()   
          #父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。  
        if pid > 0:  
            sys.exit(0)   #父进程退出  
    except OSError, e:   
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )  
        sys.exit(1)  
  
     #从母体环境脱离  
    os.chdir("/")  #chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录  
    os.umask(0)    #调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。  
    os.setsid()    #setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。  
  
     #执行第二次fork  
    try:   
        pid = os.fork()   
        if pid > 0:  
            sys.exit(0)   #第二个父进程退出  
    except OSError, e:   
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )  
        sys.exit(1)  
  
     #进程已经是守护进程了，重定向标准文件描述符  
  
    for f in sys.stdout, sys.stderr: f.flush()  
    si = open(stdin, 'r')  
    so = open(stdout, 'a+')  
    se = open(stderr, 'a+', 0)  
    os.dup2(si.fileno(), sys.stdin.fileno())    #dup2函数原子化关闭和复制文件描述符  
    os.dup2(so.fileno(), sys.stdout.fileno())  
    os.dup2(se.fileno(), sys.stderr.fileno())  
  
# running main  
def main(argv1):    
    sys.stdout.write('Node Monitor daemon started with pid %d\n' % os.getpid())  
    sys.stdout.write('Node Monitor daemon stdout output\n')  
    sys.stderr.write('Node Monitor daemon stderr output\n')  

    nm = NodeMonitor(argv1)
    nm.start_zk()
    nm._update_info_just_one_time()
    nm.start_update_info()


if __name__ == "__main__":
    ## set is server or not
    argv1 = ''
    if len(sys.argv) > 1:
        if sys.argv[1] == '-server':
            argv1 = '-server'

    daemonize('/dev/null','/tmp/daemon_stdout.log','/tmp/daemon_error.log')  
    main(argv1)
    
        