# -*- coding: utf-8 -*-

################################################################
# pp.client-plone
# (C) 2013-2019,  ZOPYX, D-72074 Tuebingen, www.zopyx.com
################################################################

import furl

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from pp.client.python import pdf
from pp.client.plone.interfaces import IPPClientPloneSettings
from pp.client.plone.logger import LOG


def convert(work_directory, converter):
    """ Convert content from given `work_directory` using `converter`
        through Produce & Publish server.
    """

    registry = getUtility(IRegistry)
    settings = registry.forInterface(IPPClientPloneSettings)

    r = furl.furl(settings.server_url)
    if settings.server_username:
        r.username = settings.server_username
    if settings.server_password:
        r.password = settings.server_password
    server_url = str(r)

    result = pdf.pdf(work_directory, converter, server_url=server_url)
    if result['status'] == 'OK':
        output_filename = result['output_filename']
        LOG.info('Output file: %s' % output_filename)
        return output_filename
    else:
        LOG.error('Conversion failed ({})'.format(result['output']))
        raise RuntimeError(result['output'])
