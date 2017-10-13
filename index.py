#!/usr/bin/python
#-*- coding:UTF-8 -*-

import os
import sys
def application(environ, start_response):
    status = '200'
    output = '不懂为什么'
    response_headers = [('Content-type', 'text/plain'),('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return output
