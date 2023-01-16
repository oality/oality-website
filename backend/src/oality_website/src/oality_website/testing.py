from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import oality_website


class OALITY_WEBSITELayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=oality_website)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "oality_website:default")
        applyProfile(portal, "oality_website:initial")


OALITY_WEBSITE_FIXTURE = OALITY_WEBSITELayer()


OALITY_WEBSITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(OALITY_WEBSITE_FIXTURE,),
    name="OALITY_WEBSITELayer:IntegrationTesting",
)


OALITY_WEBSITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OALITY_WEBSITE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="OALITY_WEBSITELayer:FunctionalTesting",
)


OALITY_WEBSITEACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        OALITY_WEBSITE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="OALITY_WEBSITELayer:AcceptanceTesting",
)
