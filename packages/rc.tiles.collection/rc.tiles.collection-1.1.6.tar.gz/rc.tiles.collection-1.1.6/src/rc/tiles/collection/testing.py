# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import rc.tiles.collection


class RcTilesCollectionLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=rc.tiles.collection)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rc.tiles.collection:default')


RC_TILES_COLLECTION_FIXTURE = RcTilesCollectionLayer()


RC_TILES_COLLECTION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RC_TILES_COLLECTION_FIXTURE,),
    name='RcTilesCollectionLayer:IntegrationTesting',
)


RC_TILES_COLLECTION_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RC_TILES_COLLECTION_FIXTURE,),
    name='RcTilesCollectionLayer:FunctionalTesting',
)


RC_TILES_COLLECTION_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RC_TILES_COLLECTION_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RcTilesCollectionLayer:AcceptanceTesting',
)
