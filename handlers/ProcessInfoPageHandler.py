#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from helpers.ResourceInfo import ResourceInfo

class ProcessInfoPageHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-7]
        # print "daemon: ", ip
        ri = ResourceInfo()
        ri.start_zk()
        daemon_info = ri.get_daemon_info_of(ip)
        # print net_info
        ri.stop_zk()
        if daemon_info != '{}':
            self.render("detailProcess.html", computer_name=ip)
        else:
            self.write("Bad Request")
