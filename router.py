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


if __name__ == "__main__":
    main()


