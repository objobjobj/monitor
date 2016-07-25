#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from helpers.ResourceInfo import *


class RequestDaemonInfoHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-15]
        # print "req daemon: ", ip
        ri = ResourceInfo()
        ri.start_zk()
        daemon_info = ri.get_daemon_info_of(ip)
        # print daemon_info
        ri.stop_zk()
        if daemon_info != '{}':
            self.write(daemon_info)
        else:
            self.write("Bad Request")
