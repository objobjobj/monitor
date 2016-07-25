#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from helpers.ResourceInfo import ResourceInfo
import json


class HomePageHandler(tornado.web.RequestHandler):
    def get(self):
        ri = ResourceInfo()
        ri.start_zk()
        server_info = json.loads(ri.get_vms_static_info())
        ri.stop_zk()
        # print server_info
        self.render("hypervisors.html", instance_info=server_info)
