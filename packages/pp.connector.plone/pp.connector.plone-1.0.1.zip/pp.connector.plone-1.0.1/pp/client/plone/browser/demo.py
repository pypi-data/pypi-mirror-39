# -*- coding: utf-8 -*-

################################################################
# pp.client-plone
# (C) 2013-2019,  ZOPYX, D-72074 Tuebingen, www.zopyx.com
################################################################


import os

import pkg_resources

from zope.component import getUtility
from Products.Five.browser import BrowserView

from pp.client.plone.interfaces import IPPServer


class Demo(BrowserView):
    """ P&P server demo """

    def demo(self):
        service = getUtility(IPPServer)
        base_dir = pkg_resources.get_distribution('pp.client-python').location
        data_dir = os.path.join(base_dir, 'pp', 'client', 'python', 'test_data', 'html')
        output_filename = service(data_dir, 'princexml')
        with open(output_filename, 'rb') as fp:
            self.request.response.setHeader('content-type', 'application/pdf')
            self.request.response.setHeader('content-length', str(os.path.getsize(output_filename)))
            self.request.response.write(fp.read())
