from __future__ import print_function
import os
import sys
import tempfile
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.urlresolvers import reverse

import aristotle_dse.models as models
import aristotle_mdr.perms as perms
import aristotle_mdr.tests.utils as utils
from wcag_zoo.validators import parade

import subprocess
import pprint

from aristotle_mdr.utils import setup_aristotle_test_environment
setup_aristotle_test_environment()

from aristotle_mdr.tests.accessibility import MEDIA_TYPES, TestWebPageAccessibilityBase


TMP_STATICPATH = tempfile.mkdtemp(suffix='static')
STATICPATH = TMP_STATICPATH+'/static'
if not os.path.exists(STATICPATH):
    os.makedirs(STATICPATH)


class DSSTestWebPageAccessibilityBase(TestWebPageAccessibilityBase):

    @classmethod
    @override_settings(STATIC_ROOT = STATICPATH)
    def setUpClass(self):
        super(DSSTestWebPageAccessibilityBase, self).setUpClass()
        self.dss = models.DataSetSpecification.objects.create(
            name="Test Spec 1",)


class TestStaticPageAccessibility(DSSTestWebPageAccessibilityBase, TestCase):
    def test_static_pages(self):
        from aristotle_dse.urls import urlpatterns
        pages = [
            reverse("aristotle_dse:%s" % u.name) for u in urlpatterns
            if hasattr(u, 'name') and u.name is not None and u.regex.groups == 0
        ]

        self.pages_tester(pages)

class TestMetadataItemPageAccessibility(DSSTestWebPageAccessibilityBase, TestCase):
    def test_metadata_object_pages(self):
        self.login_superuser()

        pages = [
            item.get_absolute_url() for item in [
                self.dss,
            ]
        ]
        self.pages_tester(pages)


class TestMetadataActionPageAccessibility(DSSTestWebPageAccessibilityBase, TestCase):
    def test_metadata_object_action_pages(self):
        self.login_superuser()

        items = [
            self.dss,
        ]
        
        pages = [
            url
            for item in items
            for url in [
                reverse("aristotle:supersede", args=[item.id]),
                reverse("aristotle:deprecate", args=[item.id]),
                reverse("aristotle:edit_item", args=[item.id]),
                reverse("aristotle:clone_item", args=[item.id]),
                reverse("aristotle:item_history", args=[item.id]),
                reverse("aristotle:registrationHistory", args=[item.id]),
                reverse("aristotle:check_cascaded_states", args=[item.id]),
                # reverse("aristotle:item_history", args=[item.id]),
                # reverse("aristotle:item_history", args=[item.id]),
            ]
            if self.client.get(url, follow=True).status_code == 200
        ]
        # We skip those pages that don't exist (like object class 'child metadata' pages)

        self.pages_tester(pages, media_types = [[], ['(min-width: 600px)']])
