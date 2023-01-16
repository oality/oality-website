"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from oality_website.testing import OALITY_WEBSITE_INTEGRATION_TESTING  # noqa: E501
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that oality_website is properly installed."""

    layer = OALITY_WEBSITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if oality_website is installed."""
        self.assertTrue(self.installer.is_product_installed("oality_website"))

    def test_browserlayer(self):
        """Test that IOALITY_WEBSITELayer is registered."""
        from plone.browserlayer import utils
        from oality_website.interfaces import IOALITY_WEBSITELayer

        self.assertIn(IOALITY_WEBSITELayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("oality_website:default")[0],
            "20230116001",
        )


class TestUninstall(unittest.TestCase):

    layer = OALITY_WEBSITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("oality_website")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if oality_website is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("oality_website"))

    def test_browserlayer_removed(self):
        """Test that IOALITY_WEBSITELayer is removed."""
        from plone.browserlayer import utils
        from oality_website.interfaces import IOALITY_WEBSITELayer

        self.assertNotIn(IOALITY_WEBSITELayer, utils.registered_layers())
