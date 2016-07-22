#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from helpers.ResourceInfo import *


class RequestMemInfoHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-15]
        print "req memory: ", ip
        ri = ResourceInfo()
        ri.start_zk()
        memory_info = ri.get_memory_info_of(ip)
        ri.stop_zk()
        # print memory_info
        if memory_info != '{}':
            self.write(memory_info)
        else:
            self.write("Bad Request")
