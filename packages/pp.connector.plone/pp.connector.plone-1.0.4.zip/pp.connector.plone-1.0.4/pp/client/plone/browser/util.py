# -*- coding: utf-8 -*-

################################################################
# pp.client-plone
# (C) 2013-2019,  ZOPYX, D-72074 Tuebingen, www.zopyx.com
################################################################

import lxml.html

import zope.component


def getLanguageForObject(obj):

    # Plone 5
    from plone.i18n.interfaces import ILanguageUtility
    util = zope.component.getUtility(ILanguageUtility)
    language = util.getDefaultLanguage()

    obj_language = None
    try:
        obj_language = obj.Language()
    except AttributeError:
        obj_language = obj.getLanguage()
    if obj_language:
        language = obj_language
    return language


def _findTextInNode(bs_node_or_text):
    if isinstance(bs_node_or_text, basestring):
        return bs_node_or_text
    else:
        html = lxml.html.fromstring(unicode(bs_node_or_text))
        return html.text_content()


def reduce_image_quality(workdir, quality):
    """ Search for all images inside workdir and perform an inplace
        quality reduction. Requires ImageMagick.
    """
    return None


def _findParentDocument(node):
    """ Return the parent node representing the document
        (containing .document-boundary class).
    """

    current = node
    while current is not None:
        if 'document-boundary' in current.get('class', ''):
            return current
        current = current.parent
    return None
