#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from helpers.ResourceInfo import ResourceInfo


class NetworkInfoPageHandler(tornado.web.RequestHandler):
    def get(self, req):
        uri = self.request.uri
        ip = uri[9:][:-8]
        # print "network: ", ip
        ri = ResourceInfo()
        ri.start_zk()
        net_info = ri.get_net_info_of(ip)
        # print net_info
        ri.stop_zk()
        if net_info != '{}':
            self.render("detailNetwork.html", computer_name=ip)
        else:
            self.write("Bad Request")
