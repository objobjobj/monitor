#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import os
import sys

from handlers.HomePageHandler import *
from handlers.GeneralViewPageHandler import *
from handlers.InstancePageHandler import *
from handlers.CPUInfoPageHandler import *
from handlers.DiskInfoPageHandler import *
from handlers.MemInfoPageHandler import *
from handlers.NetworkInfoPageHandler import *
from handlers.ProcessInfoPageHandler import *
from handlers.RequestGeneralInfoHandler import *
from handlers.RequestCPUInfoHandler import *
from handlers.RequestMemInfoHandler import *
from handlers.RequestDiskInfoHandler import *
from handlers.RequestNetworkInfoHandler import *
from handlers.RequestDaemonInfoHandler import *

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

sys.path.append(os.path.join(sys.path[0], 'handlers'))

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "debug": "True",
    }
    # (r'/course/(\w+)/(\d+)', CourseDetailHandler),
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", HomePageHandler),
        (r"/instances", InstancePageHandler),
        (r"/machines", GeneralViewPageHandler),
        (r"/machines/request", RequestGeneralInfoHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/cpu", CPUInfoPageHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/cpu/request", RequestCPUInfoHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/disk", DiskInfoPageHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/disk/request", RequestDiskInfoHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/memory", MemInfoPageHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/memory/request", RequestMemInfoHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/network", NetworkInfoPageHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/network/request", RequestNetworkInfoHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/daemon", ProcessInfoPageHandler),
        (r"/machine/(\d+\.\d+\.\d+\.\d+)/daemon/request", RequestDaemonInfoHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


def daemonize():
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except OSError, e:
        # sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

        # 从母体环境脱离
    # os.chdir("/")  # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

        # 进程已经是守护进程了，重定向标准文件描述符

if __name__ == "__main__":
    daemonize()
    main()


