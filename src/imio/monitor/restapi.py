# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from plone.rest.service import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class Monitor(Service):

    def __init__(self, context, request):
        super(Monitor, self).__init__(context, request)
        self.params = []
        self.portal = api.portal.get()
        self.portal_catalog = api.portal.get_tool('portal_catalog')
        self.content_type = 'application/json'

    def publishTraverse(self, request, name):
        # Consume any path segments after /@users as parameters
        self.params.append(name)
        return self

    @property
    def _get_probe_id(self):
        if len(self.params) != 1:
            raise Exception(
                'Must supply exactly one parameter (probe id)')
        return self.params[0]

    @property
    def _probe_list(self):
        probe_list = []
        attrs = [i for i in dir(self) if not callable(i)]
        for attr in attrs:
            if not attr.startswith('_') and \
               not attr.startswith('aq_') and \
               attr not in self.__dict__.keys() and \
               attr not in ['method', 'publishTraverse', 'render']:
                probe_list.append(attr)
        return probe_list

    @property
    def last_modified_plone_object_time(self):
        query = {}
        query['path'] = '/'.join(self.portal.getPhysicalPath())
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        query['sort_limit'] = 1
        brain = self.portal_catalog(query)
        if len(brain) == 0:
            return 0
        return brain[0].modified.timeTime()

    @property
    def valid_users(self):
        """User connected since 90 days"""
        valid_users = []
        users = api.user.get_users()
        for user in users:
            if user.getProperty('last_login_time') > (DateTime() - 90):
                valid_users.append(user)
        return len(valid_users)

    def render(self):
        if len(self.params) == 0:
            # Someone is asking for all probes
            content = {'probes': self._probe_list}
        else:
            probe_id = self._get_probe_id
            if probe_id not in self._probe_list:
                raise Exception(
                    '{0} not impemented'.format(probe_id))
            content = {probe_id: getattr(self, probe_id)}
        self.request.response.setHeader('Content-Type', self.content_type)
        return json.dumps(content, indent=2, sort_keys=True)
