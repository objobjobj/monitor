#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

class ProcessInfoPageHandler(tornado.web.RequestHandler):
    def get(self, req):
        self.render("detailProcess.html")
