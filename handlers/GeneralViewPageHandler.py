#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from helpers.ResourceInfo import *
import json


class GeneralViewPageHandler(tornado.web.RequestHandler):
    def get(self):
        ri = ResourceInfo()
        ri.start_zk()
        general_info = ri.get_general_dynamic_info()
        general_info_decode = json.loads(general_info)
        ri.stop_zk()
        if general_info_decode != '{}':
            # ips = []
            # infos = []
            # for item in general_info_decode:
            #     ips.append(str(item))
            #     infos.append(json.loads(general_info_decode[item]))
            self.render("briefmonitor.html", general_info=general_info_decode)
        else:
            self.write("Bad Request")