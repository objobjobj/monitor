#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from helpers.ResourceInfo import *


class RequestDaemonInfoHandler(tornado.web.RequestHandler):
    def get(self, req):
        if True:
            ri = ResourceInfo()
            ri.start_zk()
            general_info = ri.get_general_dynamic_info()
            ri.stop_zk()
            self.write(general_info)
            #self.render("briefmonitor.html")
        else:
            err_msg = 'Bad Request'
            self.write(err_msg)
