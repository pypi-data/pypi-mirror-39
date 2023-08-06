from django.test import TestCase

import aristotle_mdr.models as models
import aristotle_mdr.perms as perms
from django.contrib.auth import get_user_model

import datetime
from time import sleep

from aristotle_mdr.utils import setup_aristotle_test_environment


setup_aristotle_test_environment()


class CachingForRawPermissions(TestCase):

    def setUp(self):
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA")
        self.wg = models.Workgroup.objects.create(name="Test WG 1")
        self.wg.registrationAuthorities=[self.ra]
        self.wg.save()
        self.submitter = get_user_model().objects.create_user('suzie@example.com', 'submitter')
        self.wg.submitters.add(self.submitter)
        self.item = models.ObjectClass.objects.create(name="Test OC1", workgroup=self.wg)

    def test_can_edit_cache(self):
        self.assertTrue(perms.user_can_edit(self.submitter, self.item))
        self.item.definition = "edit name, then quickly check permission"
        self.item.save()
        self.assertTrue(perms.user_can_edit(self.submitter, self.item))
        self.item.definition = "edit name, then wait 30 secs for 'recently edited to expire'"
        self.item.save()
        sleep(models.VERY_RECENTLY_SECONDS + 2)
        self.assertTrue(perms.user_can_edit(self.submitter, self.item))
        # register then immediately check the permissions to make sure the cache is ignored
        # technically we haven't edited the item yet, although ``concept.recache_states`` will be called.
        reg, c = models.Status.objects.get_or_create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2009, 4, 28),
            state=models.STATES.standard
        )
        self.assertFalse(perms.user_can_edit(self.submitter, self.item))

    def test_can_view_cache(self):
        self.viewer = get_user_model().objects.create_user('vicky@example.com', 'viewer')  # Don't need to assign any workgroups

        self.assertTrue(perms.user_can_view(self.submitter, self.item))
        self.assertFalse(perms.user_can_view(self.viewer, self.item))
        self.item.definition = "edit name, then quickly check permission"
        self.item.save()
        self.assertTrue(perms.user_can_view(self.submitter, self.item))
        self.assertFalse(perms.user_can_view(self.viewer, self.item))
        self.item.definition = "edit name, then wait 30 secs for 'recently edited to expire'"
        self.item.save()
        sleep(models.VERY_RECENTLY_SECONDS + 2)
        self.assertTrue(perms.user_can_view(self.submitter, self.item))
        self.assertFalse(perms.user_can_view(self.viewer, self.item))
        # register then immediately check the permissions to make sure the cache is ignored
        # technically we haven't edited the item yet, although ``concept.recache_states`` will be called.
        reg, c = models.Status.objects.get_or_create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2009, 4, 28),
            state=models.STATES.standard
        )
        self.assertTrue(perms.user_can_view(self.submitter, self.item))
        self.assertTrue(perms.user_can_view(self.viewer, self.item))
