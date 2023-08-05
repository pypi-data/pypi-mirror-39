# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from rc.tiles.collection.testing import RC_TILES_COLLECTION_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that rc.tiles.collection is properly installed."""

    layer = RC_TILES_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if rc.tiles.collection is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'rc.tiles.collection'))

    def test_browserlayer(self):
        """Test that IRcTilesCollectionLayer is registered."""
        from rc.tiles.collection.interfaces import (
            IRcTilesCollectionLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRcTilesCollectionLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RC_TILES_COLLECTION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['rc.tiles.collection'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if rc.tiles.collection is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'rc.tiles.collection'))

    def test_browserlayer_removed(self):
        """Test that IRcTilesCollectionLayer is removed."""
        from rc.tiles.collection.interfaces import \
            IRcTilesCollectionLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IRcTilesCollectionLayer,
            utils.registered_layers())
