# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.smartlink.testing import COLLECTIVE_SMARTLINK_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.smartlink is properly installed."""

    layer = COLLECTIVE_SMARTLINK_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.smartlink is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.smartlink'))

    def test_browserlayer(self):
        """Test that ICollectiveSmartlinkLayer is registered."""
        from collective.smartlink.interfaces import (
            ICollectiveSmartlinkLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveSmartlinkLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_SMARTLINK_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.smartlink'])

    def test_product_uninstalled(self):
        """Test if collective.smartlink is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.smartlink'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveSmartlinkLayer is removed."""
        from collective.smartlink.interfaces import ICollectiveSmartlinkLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveSmartlinkLayer, utils.registered_layers())
