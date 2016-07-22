#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from helpers.ResourceInfo import *


class RequestCPUInfoHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-12]
        print "req cpu: ", ip
        ri = ResourceInfo()
        ri.start_zk()
        cpu_info = ri.get_cpu_info_of(ip)
        ri.stop_zk()
        if cpu_info != '{}':
            self.write(cpu_info)
        else:
            self.write("Bad Request")
