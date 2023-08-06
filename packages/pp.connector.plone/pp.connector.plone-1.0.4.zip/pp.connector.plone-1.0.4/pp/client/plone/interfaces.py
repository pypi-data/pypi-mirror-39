################################################################
# pp.client-plone
# (C) 2013-2019,  ZOPYX, D-72074 Tuebingen, www.zopyx.com
################################################################

from zope import schema
from zope.interface import Interface
from pp.client.plone.i18n import MessageFactory as _


class IPPServer(Interface):
    """ Marker interface for Produce & Publish server """


class IPloneClientConnectorLayer(Interface):
    """A brower layer specific to my product """


class IPPClientPloneSettings(Interface):
    """ pp.client-plone settings """

    server_url = schema.TextLine(
        title=_(u'URL of Produce & Publish webservice'),
        description=_(u'URL of Produce & Publish webservice'),
        default=u'https://pp-server.zopyx.com')

    server_username = schema.TextLine(
        title=_(u'Username for webservice'),
        description=_(u'Username for webservice'),
        required=False,
        default=u'')

    server_password = schema.TextLine(
        title=_(u'Password for webservice'),
        description=_(u'Password for webservice'),
        required=False,
        default=u'')
