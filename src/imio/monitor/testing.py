# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import imio.monitor


class ImioMonitorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=imio.monitor)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'imio.monitor:default')


IMIO_MONITOR_FIXTURE = ImioMonitorLayer()


IMIO_MONITOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_MONITOR_FIXTURE,),
    name='ImioMonitorLayer:IntegrationTesting',
)


IMIO_MONITOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_MONITOR_FIXTURE,),
    name='ImioMonitorLayer:FunctionalTesting',
)


IMIO_MONITOR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIO_MONITOR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ImioMonitorLayer:AcceptanceTesting',
)
