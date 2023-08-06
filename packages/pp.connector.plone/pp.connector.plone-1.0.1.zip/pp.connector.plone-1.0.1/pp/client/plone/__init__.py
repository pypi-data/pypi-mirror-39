################################################################
# pp.client-plone
# (C) 2013-2019,  ZOPYX, D-72074 Tuebingen, www.zopyx.com
################################################################

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)
