# -*- coding: utf-8 -*-
from rc.tiles.collection import _
from rc.tiles.collection.interfaces import ICollectionTileRenderer
from Products.Five.browser import BrowserView
from zope.interface import implementer


@implementer(ICollectionTileRenderer)
class BaseView(BrowserView):

    display_name = _('Custom renderer 2 - No icons')
