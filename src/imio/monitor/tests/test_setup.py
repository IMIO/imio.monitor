# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from imio.monitor.testing import IMIO_MONITOR_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that imio.monitor is properly installed."""

    layer = IMIO_MONITOR_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if imio.monitor is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'imio.monitor'))

    def test_browserlayer(self):
        """Test that IImioMonitorLayer is registered."""
        from imio.monitor.interfaces import (
            IImioMonitorLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IImioMonitorLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IMIO_MONITOR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['imio.monitor'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.monitor is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'imio.monitor'))

    def test_browserlayer_removed(self):
        """Test that IImioMonitorLayer is removed."""
        from imio.monitor.interfaces import \
            IImioMonitorLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IImioMonitorLayer,
            utils.registered_layers())
