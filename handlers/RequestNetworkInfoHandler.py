#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from helpers.ResourceInfo import *


class RequestNetworkInfoHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-16]
        # print ip
        ri = ResourceInfo()
        ri.start_zk()
        net_info = ri.get_net_info_of(ip)
        # print net_info
        ri.stop_zk()
        if net_info != '{}':
            self.write(net_info)
        else:
            self.write("Bad Request")
