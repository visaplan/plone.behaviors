# -*- coding: utf-8 -*-
from visaplan.plone.behaviors.interfaces.folderish_animation import IFolderishAnimation  # NOQA E501
from visaplan.plone.behaviors.testing import VISAPLAN_PLONE_BEHAVIORS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class FolderishAnimationIntegrationTest(unittest.TestCase):

    layer = VISAPLAN_PLONE_BEHAVIORS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_folderish_animation_schema(self):
        fti = queryUtility(IDexterityFTI, name='FolderishAnimation')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('FolderishAnimation')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_folderish_animation_fti(self):
        fti = queryUtility(IDexterityFTI, name='FolderishAnimation')
        self.assertTrue(fti)

    def test_ct_folderish_animation_factory(self):
        fti = queryUtility(IDexterityFTI, name='FolderishAnimation')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IFolderishAnimation.providedBy(obj),
            u'IFolderishAnimation not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_folderish_animation_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='FolderishAnimation',
            id='folderish_animation',
        )

        self.assertTrue(
            IFolderishAnimation.providedBy(obj),
            u'IFolderishAnimation not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_folderish_animation_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='FolderishAnimation')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_folderish_animation_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='FolderishAnimation')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'folderish_animation_id',
            title='FolderishAnimation container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )