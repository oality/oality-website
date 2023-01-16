from oality_website import logger
from oality_website.setuphandlers import content
from oality_website.setuphandlers import users
from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from zope.component import queryUtility
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "oality_website:uninstall",
        ]


def populate_portal(context):
    """Post install script"""
    portal = api.portal.get()
    # Delete content
    content.delete_content(portal)
    logger.info("Deleted default portal content")
    user = users.create_default_user()
    creators = [user.id]
    logger.info("Created default user")
    # Create other users
    users.create_team_accounts()
    logger.info("Created team accounts")
    # Create Initial content
    content.populate_portal(portal, creators)
    logger.info("Created initial content")
    # Update cover content
    content.update_home(portal, creators)
    reg = queryUtility(IRegistry, context=portal)
    reg["plone.default_language"] = "en"
    reg["plone.available_languages"] = ["fr", "en"]
    reg["plone.use_combined_language_codes"] = False
    sms = SetupMultilingualSite(portal)
    sms.setupSite(portal)
