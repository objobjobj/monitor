#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from helpers.ResourceInfo import ResourceInfo
import json


class InstancePageHandler(tornado.web.RequestHandler):
    def get(self):
        ri = ResourceInfo()
        ri.start_zk()
        instance_info = json.loads(ri.get_vms_static_info())
        ri.stop_zk()
        # print instance_info
        self.render("instance.html", instance_info=instance_info)
