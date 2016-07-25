#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from helpers.ResourceInfo import *


class RequestDiskInfoHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-13]
        # print "req disk: ", ip
        ri = ResourceInfo()
        ri.start_zk()
        disk_info = ri.get_disk_info_of(ip)
        # print disk_info
        ri.stop_zk()
        if disk_info != '{}':
            self.write(disk_info)
        else:
            self.write("Bad Request")
