# -*- coding: utf-8 -*-

################################################################
# pp.client-plone
# (C) 2013-2019,  ZOPYX, D-72074 Tuebingen, www.zopyx.com
################################################################

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
