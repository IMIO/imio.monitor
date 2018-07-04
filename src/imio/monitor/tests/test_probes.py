# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from DateTime import DateTime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from imio.monitor.testing import IMIO_MONITOR_FUNCTIONAL_TESTING  # noqa

# import requests
import transaction
import unittest


class TestProbes(unittest.TestCase):
    """Test probes from imio.monitor."""

    layer = IMIO_MONITOR_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        # self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def test_get_probe_list(self):
        response = self.api_session.get('/@monitor')
        self.assertEqual(200, response.status_code)
        results = response.json()
        self.assertIn('last_modified_plone_object_time', results['probes'])
        self.assertEqual(len(results['probes']), 1)

    def test_probe_last_modified_plone_object_time(self):
        probe = 'last_modified_plone_object_time'
        response = self.api_session.get('/@monitor/{0}'.format(probe))
        self.assertEqual(200, response.status_code)
        results = response.json()
        self.assertEqual(results[probe], 0)

        doc = api.content.create(self.portal, 'Document', 'mydoc')
        transaction.commit()
        # make request with w user because doc is not published
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        response = self.api_session.get('/@monitor/{0}'.format(probe))
        self.assertEqual(200, response.status_code)
        results = response.json()

        self.assertEqual(
            doc.modification_date,
            DateTime(results[probe])
        )

    def test_valid_users(self):
        probe = 'valid_users'
        response = self.api_session.get('/@monitor/{0}'.format(probe))
        self.assertEqual(200, response.status_code)
        results = response.json()
        self.assertEqual(results[probe], 0)

        user = api.user.create(username='jamesbond', email='jamesbond@imio.be')
        user.setProperties({'last_login_time': DateTime()})
        transaction.commit()
        # make request with admin user
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        response = self.api_session.get('/@monitor/{0}'.format(probe))
        self.assertEqual(200, response.status_code)
        results = response.json()
        self.assertEqual(results[probe], 1)
