from django.urls import reverse
from django.test import TestCase, tag
import aristotle_mdr.models as MDR
import aristotle_mdr.tests.utils as utils
from aristotle_mdr import perms
from aristotle_mdr.utils import url_slugify_concept
from aristotle_mdr.contrib.reviews import models
from aristotle_mdr.contrib.reviews.const import REVIEW_STATES

from django.contrib.auth import get_user_model
User = get_user_model()

import datetime
from aristotle_mdr.utils import setup_aristotle_test_environment


setup_aristotle_test_environment()

# I wanted to call this review-R-Ls or rev-U-R-Ls.
review_urls = [
    'aristotle_reviews:review_details',
    'aristotle_reviews:review_list',
    'aristotle_reviews:request_impact',
    # 'aristotle_reviews:request_checks',
    'aristotle_reviews:request_update',
    'aristotle_reviews:request_issues',
]

review_accept_urls = [
    'aristotle_reviews:accept_review',
    'aristotle_reviews:endorse_review',
]


class ReviewRequestBulkActions(utils.AristotleTestUtils, TestCase):
    def setUp(self):
        super().setUp()

        # There would be too many tests to test every item type against every other
        # But they all have identical logic, so one test should suffice
        self.item1 = MDR.ObjectClass.objects.create(name="Test Item 1 (visible to tested viewers)",definition="my definition",workgroup=self.wg1)
        self.item2 = MDR.ObjectClass.objects.create(name="Test Item 2 (NOT visible to tested viewers)",definition="my definition",workgroup=self.wg2)
        self.item3 = MDR.ObjectClass.objects.create(name="Test Item 3 (only visible to the editor)",definition="my definition",workgroup=None,submitter=self.editor)

        self.item4 = MDR.ValueDomain.objects.create(name='Test Value Domain', definition='my definition', workgroup=self.wg1)
        self.item5 = MDR.DataElement.objects.create(name='Test data element', definition='my definition', workgroup=self.wg1, valueDomain=self.item4)

        from django.core.cache import cache
        cache.clear()

    def test_bulk_review_request_on_permitted_items(self):
        self.login_viewer()

        self.assertTrue(perms.user_can_view(self.viewer, self.item1))
        self.assertFalse(perms.user_can_view(self.viewer, self.item2))

        self.assertTrue(models.ReviewRequest.objects.count() == 0)

        response = self.client.post(
            reverse('aristotle:bulk_action'),
            {
                'bulkaction': 'aristotle_mdr.contrib.reviews.forms.RequestReviewBulkActionForm',
                'items': [self.item1.id, self.item2.id],
            },
            follow=True
        )

        from urllib.parse import urlencode
        params = {'items': [self.item1.id]} #, self.item2.id]}
        url = "{}?{}".format(
            reverse("aristotle_reviews:review_create"),
            urlencode(params, True)
        )
        self.assertRedirects(response, url)

        self.assertContains(response, "items when registering metadata")
        self.assertTrue(self.item1 in response.context['form']['concepts'].initial)
        self.assertTrue(self.item2 not in response.context['form']['concepts'].initial)
        self.assertTrue(len(response.context['form']['concepts'].initial) == 1)


    def test_bulk_review_request_on_forbidden_items(self):
        self.login_viewer()

        self.assertTrue(perms.user_can_view(self.viewer, self.item1))
        self.assertTrue(perms.user_can_view(self.viewer, self.item4))

        self.assertTrue(models.ReviewRequest.objects.count() == 0)

        response = self.client.post(
            reverse('aristotle:bulk_action'),
            {
                'bulkaction': 'aristotle_mdr.contrib.reviews.forms.RequestReviewBulkActionForm',
                'items': [self.item1.id, self.item4.id],
            },
            follow=True
        )

        from urllib.parse import urlencode
        params = {'items': [self.item1.id, self.item4.id]}
        url = "{}?{}".format(
            reverse("aristotle_reviews:review_create"),
            urlencode(params, True)
        )
        self.assertRedirects(response, url)
        self.assertContains(response, "items when registering metadata")
        self.assertTrue(self.item1 in response.context['form']['concepts'].initial)
        self.assertTrue(self.item4 in response.context['form']['concepts'].initial)
        self.assertTrue(len(response.context['form']['concepts'].initial) == 2)


class ReviewRequestPermissions(utils.AristotleTestUtils, TestCase):
    def setUp(self):
        super().setUp()
        self.other_ra = MDR.RegistrationAuthority.objects.create(name="Other RA")
        self.other_registrar = User.objects.create(email="otto@other-register.com")
        self.other_ra.registrars.add(self.other_registrar)
        
        review = self.make_review_request_iterable([],
            request_kwargs = {
                "requester": self.viewer,
                "title": "My Review",
                "target_registration_state": MDR.STATES.standard,
                "registration_date": "2018-01-01",
            }
        )

    def test_user_can_view_review(self):
        perm = perms.user_can_view_review

        self.assertTrue(perm(self.viewer, self.review_request))
        self.assertTrue(perm(self.registrar, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

        # Revoke review
        self.review_request.status = REVIEW_STATES.revoked

        self.assertTrue(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

    def test_user_can_approve_review(self):
        perm = perms.user_can_approve_review
        self.assertTrue(perm(self.registrar, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertFalse(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

        # Closed review
        self.review_request.status = REVIEW_STATES.closed
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertFalse(perm(self.su, self.review_request))
        self.assertFalse(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

        # Revoked review
        self.review_request.status = REVIEW_STATES.revoked
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertFalse(perm(self.su, self.review_request))
        self.assertFalse(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

        # Approved review
        self.review_request.status = REVIEW_STATES.approved
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertFalse(perm(self.su, self.review_request))
        self.assertFalse(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

    def test_user_can_close_or_reopen_review(self):
        perm = perms.user_can_close_or_reopen_review
        self.assertTrue(perm(self.registrar, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertTrue(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

        # Revoked review
        self.review_request.status = REVIEW_STATES.revoked
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertTrue(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

    def test_user_can_edit_review(self):
        perm = perms.user_can_edit_review

        self.assertTrue(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertTrue(perm(self.ramanager, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))

        # Revoke review
        self.review_request.status = REVIEW_STATES.revoked

        self.assertTrue(perm(self.viewer, self.review_request))
        self.assertFalse(perm(self.registrar, self.review_request))
        self.assertFalse(perm(self.ramanager, self.review_request))
        self.assertTrue(perm(self.su, self.review_request))
        self.assertFalse(perm(self.editor, self.review_request))
        self.assertFalse(perm(self.other_registrar, self.review_request))


# TODO: More testing for reviews
# class ReviewRequestActionsPage(utils.AristotleTestUtils, TestCase):
#     def setUp(self):
#         super().setUp()

#         # There would be too many tests to test every item type against every other
#         # But they all have identical logic, so one test should suffice
#         self.item1 = MDR.ObjectClass.objects.create(name="Test Item 1 (visible to tested viewers)",definition="my definition",workgroup=self.wg1)
#         self.item2 = MDR.ObjectClass.objects.create(name="Test Item 2 (NOT visible to tested viewers)",definition="my definition",workgroup=self.wg2)
#         self.item3 = MDR.ObjectClass.objects.create(name="Test Item 3 (only visible to the editor)",definition="my definition",workgroup=None,submitter=self.editor)

#         self.item4 = MDR.ValueDomain.objects.create(name='Test Value Domain', definition='my definition', workgroup=self.wg1)
#         self.item5 = MDR.DataElement.objects.create(name='Test data element', definition='my definition', workgroup=self.wg1, valueDomain=self.item4)

#     def check_item_status(self, item, review, updated):

#         self.assertEqual(item.is_public(), updated)
#         self.assertEqual(item.current_statuses().count() == 1, updated)

#         if updated:
#             state = item.current_statuses().first()

#             self.assertTrue(state.registrationAuthority == review.registration_authority)
#             self.assertTrue(state.state == review.state)
#             self.assertTrue(state.registrationDate == review.registration_date)
#         else:
#             self.assertTrue(item.current_statuses().count() == 0)

#     def post_public_rr(self, items, ra=None):
#         if ra is None:
#             ra = self.ra
#         response = self.client.post(
#             reverse('aristotle_reviews:review_create'),
#             {
#                 'concepts': [i.pk for i in items],
#                 'registration_authority': ra.id,
#                 'target_registration_state': self.ra.public_state,
#                 'cascade_registration': 0,
#                 'title': "Please review this",
#                 'registration_date':datetime.date(2010,1,1)
#             }
#         )
#         return response

#     def check_urls(self, review_pk, urls, status_code):
#         for url in urls:
#             try:
#                 response = self.client.get(
#                     reverse(url, args=[review_pk])
#                 )
#                 self.assertEqual(response.status_code, status_code)
#             except: #pragma: no cover
#                 print(url)
#                 print(response)
#                 raise

#     # def test_viewer_cannot_request_review_for_private_item(self):
#     #     self.login_viewer()

#     #     response = self.client.get(reverse('aristotle:request_review',args=[self.item3.id]))
#     #     self.assertEqual(response.status_code,403)

#     #     response = self.client.get(reverse('aristotle:request_review',args=[self.item2.id]))
#     #     self.assertEqual(response.status_code,403)

#     #     response = self.client.get(reverse('aristotle:request_review',args=[self.item1.id]))
#     #     self.assertEqual(response.status_code,200)

#     def test_viewer_can_request_review(self):
#         self.login_editor()

#         response = self.client.get(reverse('aristotle_reviews:review_create'))
#         self.assertEqual(response.status_code,200)

#         self.assertEqual(self.item1.rr_review_requests.count(),0)
#         response = self.post_public_rr([self.item1])
#         self.assertEqual(self.item1.rr_review_requests.count(),1)

#         review_pk = response.url.rstrip("/").rsplit("/")[-2]

#         # response = self.client.get(
#         #     reverse('aristotle_reviews:review_list'),
#         #     args=[review_pk]
#         # )
#         self.check_urls(review_pk, review_urls, 200)
#         self.check_urls(review_pk, review_accept_urls, 403)

#         # Can't see, can't reviews
#         self.assertEqual(self.item2.rr_review_requests.count(),0)
#         response = self.post_public_rr([self.item2])
#         self.assertEqual(self.item2.rr_review_requests.count(),0)

#         self.assertTrue("concepts" in response.context['form'].errors.keys())
#         self.assertTrue(
#             "{} is not one of the available choices".format(self.item2.pk)
#             in str(response.context['form'].errors['concepts'])
#         )
        

#     def test_registrar_can_view_review(self):
#         self.login_editor()

#         self.assertEqual(self.item1.rr_review_requests.count(),0)
#         response = self.post_public_rr([self.item1])
#         self.assertEqual(self.item1.rr_review_requests.count(),1)

#         review_pk = response.url.rstrip("/").rsplit("/")[-2]

#         self.login_registrar()

#         self.check_urls(review_pk, review_urls, 200)
#         self.check_urls(review_pk, review_accept_urls, 200)

#     def test_registrar_cant_view_other_ra_reviews(self):
#         self.login_editor()

#         other_ra = MDR.RegistrationAuthority.objects.create(name="Other RA!", definition="")

#         self.assertEqual(self.item1.rr_review_requests.count(),0)
#         response = self.post_public_rr([self.item1], ra=other_ra)
#         self.assertEqual(self.item1.rr_review_requests.count(),1)

#         review_pk = response.url.rstrip("/").rsplit("/")[-2]

#         self.login_registrar()

#         self.check_urls(review_pk, review_rls, 403)
#         self.check_urls(review_pk, review_accept_urls, 403)

#     def test_registrar_has_valid_items_in_review(self):

#         item1 = MDR.ObjectClass.objects.create(name="Test Item 1",definition="my definition",workgroup=self.wg1)
#         item2 = MDR.ObjectClass.objects.create(name="Test Item 2",definition="my definition",workgroup=self.wg2)
#         item3 = MDR.ObjectClass.objects.create(name="Test Item 3",definition="my definition",workgroup=self.wg1)
#         item4 = MDR.ObjectClass.objects.create(name="Test Item 4",definition="my definition",workgroup=self.wg2)

#         self.login_registrar()

#         response = self.client.get(reverse('aristotle:userReadyForReview',))
#         self.assertEqual(response.status_code,200)

#         self.assertEqual(len(response.context['page']),0)

#         review = self.make_review_request_iterable([item1, item4], request_kwargs=dict(
#             requester=self.su,
#             registration_authority=self.ra,
#             target_registration_state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         response = self.client.get(reverse('aristotle:userReadyForReview',))
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(len(response.context['page']),1)

#         review = self.make_review_request_iterable([item1], request_kwargs=dict(
#             requester=self.su,
#             registration_authority=self.ra,
#             target_registration_state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         response = self.client.get(reverse('aristotle:userReadyForReview',))
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(len(response.context['page']),2)

#         other_ra = MDR.RegistrationAuthority.objects.create(name="A different ra")

#         review = self.make_review_request_iterable([item2], request_kwargs=dict(
#             requester=self.su,
#             registration_authority=other_ra,
#             target_registration_state=other_ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         response = self.client.get(reverse('aristotle:userReadyForReview',))
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(len(response.context['page']),2)

#         other_ra.giveRoleToUser('registrar',self.registrar)
#         response = self.client.get(reverse('aristotle:userReadyForReview',))
#         self.assertEqual(response.status_code,200)
#         self.assertEqual(len(response.context['page']),3)

#     def test_superuser_can_see_review(self):
#         self.login_superuser()
#         other_ra = MDR.RegistrationAuthority.objects.create(name="A different ra")

#         review = self.make_review_request_iterable([item2], request_kwargs=dict(
#             requester=self.editor,
#             registration_authority=other_ra,
#             target_registration_state=other_ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review.status = REVIEW_STATES.cancelled
#         review.save()

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#     def test_registrar_can_see_review(self):
#         self.login_registrar()
#         other_ra = MDR.RegistrationAuthority.objects.create(name="A different ra")

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=other_ra,
#             state=other_ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,404)

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review.status = REVIEW_STATES.cancelled
#         review.save()

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,404)

#     def test_anon_cannot_see_review(self):

#         review = self.make_review_request_iterable([self.item1], request_kwargs=dict(
#             requester=self.editor,
#             registration_authority=self.ra,
#             target_registration_state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         # logged out user cannot see request
#         self.logout()
#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,302)
#         # is redirected to login

#     def test_editor_can_see_review(self):
#         self.login_editor()

#         review = self.make_review_request_iterable([self.item1], request_kwargs=dict(
#             requester=self.editor,
#             registration_authority=self.ra,
#             target_registration_state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review.status = REVIEW_STATES.revoked
#         review.save()

#         response = self.client.get(reverse('aristotle_reviews:review_details',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#     def registrar_can_accept_review(self, review_changes=False):
#         self.login_registrar()
#         other_ra = MDR.RegistrationAuthority.objects.create(name="A different ra")

#         review = self.make_review_request_iterable([self.item1], request_kwargs=dict(
#             requester=self.editor,
#             registration_authority=other_ra,
#             target_registration_state=other_ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertEqual(response.status_code,403)

#         review = self.make_review_request_iterable([self.item1, self.item2], request_kwargs=dict(
#             requester=self.editor,
#             registration_authority=self.ra,
#             target_registration_state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review.status = REVIEW_STATES.cancelled
#         review.save()

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertEqual(response.status_code,403)

#         response = self.client.post(reverse('aristotle:userReviewAccept',args=[review.pk]),
#             {
#                 'review_accept-response': "I can't accept this, its cancelled",
#                 'review_accept_view-current_step': 'review_accept',
#                 'submit_skip': 'value',
#             })

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         self.assertEqual(response.status_code,403)
#         self.assertEqual(review.status, REVIEW_STATES.revoked)
#         self.assertTrue(bool(review.response) == False)

#         review.status = REVIEW_STATES.submitted
#         review.save()

#         self.assertTrue(self.item1.current_statuses().count() == 0)

#         self.item1 = MDR.ObjectClass.objects.get(pk=self.item1.pk) # decache
#         self.assertFalse(self.item1.is_public())

#         if review_changes:
#             button = "submit_next"
#         else:
#             button = "submit_skip"

#         response = self.client.post(reverse('aristotle:userReviewAccept',args=[review.pk]),
#             {
#                 'review_accept-response': "I can accept this!",
#                 'review_accept_view-current_step': 'review_accept',
#                 button: 'value',
#             })

#         if review_changes:
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(response.context['wizard']['steps'].step1, 2) # check we are now on second setep
#             selected_for_change = [self.item1.id]
#             selected_for_change_strings = [str(a) for a in selected_for_change]

#             review_response = self.client.post(reverse('aristotle:userReviewAccept',args=[review.pk]),
#                 {
#                     'review_changes-selected_list': selected_for_change_strings,
#                     'review_accept_view-current_step': 'review_changes'
#                 })

#             self.assertRedirects(review_response,reverse('aristotle:userReadyForReview'))

#         else:
#             self.assertRedirects(response,reverse('aristotle:userReadyForReview'))

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         self.assertEqual(review.response, "I can accept this!")
#         self.assertEqual(review.status,REVIEW_STATES.accepted)
#         self.assertEqual(review.reviewer, self.registrar)

#         self.item1 = MDR.ObjectClass.objects.get(pk=self.item1.pk) # decache
#         self.item2 = MDR.ObjectClass.objects.get(pk=self.item2.pk) # decache

#         if review_changes:
#             updated_items = [self.item1.pk]
#         else:
#             updated_items = [self.item1.pk, self.item2.pk]

#         for item in [self.item1, self.item2]:
#             if item.id in updated_items:
#                 updated = True
#             else:
#                 updated = False

#             self.check_item_status(item, review, updated)

#     @tag('changestatus')
#     def test_registrar_can_accept_review_direct(self):
#         self.registrar_can_accept_review(review_changes=False)

#     @tag('changestatus')
#     def test_registrar_can_accept_review_alter_changes(self):
#         self.registrar_can_accept_review(review_changes=True)

#     def test_registrar_can_reject_review(self):
#         self.login_registrar()
#         other_ra = MDR.RegistrationAuthority.objects.create(name="A different ra")

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=other_ra,
#             state=other_ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle:userReviewReject',args=[review.pk]))
#         self.assertEqual(response.status_code,403)

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle:userReviewReject',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review.status = REVIEW_STATES.cancelled
#         review.save()

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         response = self.client.get(reverse('aristotle:userReviewReject',args=[review.pk]))
#         self.assertEqual(response.status_code,403)

#         response = self.client.post(reverse('aristotle:userReviewReject',args=[review.pk]),
#             {
#                 'response':"I can't reject this, its cancelled"
#             })

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         self.assertEqual(response.status_code,403)
#         self.assertEqual(review.status, REVIEW_STATES.cancelled)
#         self.assertTrue(bool(review.response) == False)

#         review.status = REVIEW_STATES.submitted
#         review.save()

#         response = self.client.post(reverse('aristotle:userReviewReject',args=[review.pk]),
#             {
#                 'response':"I can reject this!",
#             })
#         #self.assertEqual(response.status_code,200)
#         self.assertRedirects(response,reverse('aristotle:userReadyForReview',))

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         self.assertEqual(review.response, "I can reject this!")
#         self.assertEqual(review.status,REVIEW_STATES.rejected)
#         self.assertEqual(review.reviewer, self.registrar)

#         self.item1 = MDR.ObjectClass.objects.get(pk=self.item1.pk) # decache
#         self.assertFalse(self.item1.is_public())

#     # Function used by the 2 tests below
#     def registrar_can_accept_cascade_review(self, review_changes=True):
#         self.login_registrar()

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1),
#             cascade_registration=1,
#         )

#         review.concepts.add(self.item5)

#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         if review_changes:
#             button = 'submit_next'
#         else:
#             button = 'submit_skip'

#         response = self.client.post(reverse('aristotle:userReviewAccept',args=[review.pk]),
#             {
#                 'review_accept-response': "I can accept this!",
#                 'review_accept_view-current_step': 'review_accept',
#                 button: 'value',
#             })

#         if review_changes:
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(response.context['wizard']['steps'].step1, 2) # check we are now on second setep
#             selected_for_change = [self.item4.id, self.item5.id]
#             selected_for_change_strings = [str(a) for a in selected_for_change]

#             review_response = self.client.post(reverse('aristotle:userReviewAccept',args=[review.pk]),
#                 {
#                     'review_changes-selected_list': selected_for_change_strings,
#                     'review_accept_view-current_step': 'review_changes'
#                 })

#             self.assertRedirects(review_response,reverse('aristotle:userReadyForReview'))

#         else:
#             self.assertEqual(response.status_code, 302)

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         self.assertEqual(review.response, "I can accept this!")
#         self.assertEqual(review.status,REVIEW_STATES.accepted)
#         self.assertEqual(review.reviewer, self.registrar)

#         self.item4 = models.ValueDomain.objects.get(pk=self.item4.pk) # decache
#         self.item5 = models.DataElement.objects.get(pk=self.item5.pk) # decache

#         for item in [self.item4, self.item5]:
#             self.check_item_status(item, review, True)

#     @tag('changestatus')
#     def test_registrar_can_accept_cascade_review_direct(self):
#         self.registrar_can_accept_review(review_changes=False)

#     @tag('changestatus')
#     def test_registrar_can_accept_cascade_review_revstep(self):
#         self.registrar_can_accept_review(review_changes=True)

#     def test_user_can_cancel_review(self):
#         self.login_editor()

#         review = models.ReviewRequest.objects.create(
#             requester=self.viewer,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle:userReviewCancel',args=[review.pk]))
#         self.assertEqual(response.status_code,403)

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle:userReviewCancel',args=[review.pk]))
#         self.assertEqual(response.status_code,200)

#         review.status = REVIEW_STATES.cancelled
#         review.save()

#         response = self.client.get(reverse('aristotle:userReviewCancel',args=[review.pk]))
#         self.assertRedirects(response,reverse('aristotle_reviews:review_details',args=[review.pk]))

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         self.assertFalse(review.status == REVIEW_STATES.cancelled)
#         response = self.client.post(reverse('aristotle:userReviewCancel',args=[review.pk]),{})
#         self.assertRedirects(response,reverse('aristotle:userMyReviewRequests',))

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache
#         self.assertTrue(review.status == REVIEW_STATES.cancelled)

#     def test_registrar_cant_load_rejected_or_accepted_review(self):
#         self.login_registrar()
#         MDR.RegistrationAuthority.objects.create(name="A different ra")

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             status=REVIEW_STATES.accepted,
#             state=models.STATES.standard,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle:userReviewReject',args=[review.pk]))
#         self.assertRedirects(response,reverse('aristotle_mdr:review_details', args=[review.pk]))

#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertRedirects(response,reverse('aristotle_mdr:review_details', args=[review.pk]))

#         review = models.ReviewRequest.objects.create(
#             requester=self.editor,
#             registration_authority=self.ra,
#             status=REVIEW_STATES.rejected,
#             state=models.STATES.standard,
#             registration_date=datetime.date(2010,1,1)
#         )

#         review.concepts.add(self.item1)

#         response = self.client.get(reverse('aristotle:userReviewReject',args=[review.pk]))
#         self.assertRedirects(response,reverse('aristotle_mdr:review_details', args=[review.pk]))

#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertRedirects(response,reverse('aristotle_mdr:review_details', args=[review.pk]))

#         review = self.make_review_request(self.item1, self.registrar, requester=self.editor)

#         response = self.client.get(reverse('aristotle:userReviewReject',args=[review.pk]))
#         self.assertEqual(response.status_code,403)
#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertEqual(response.status_code,403)

#     def test_who_can_see_review(self):
#         from aristotle_mdr.perms import user_can_view_review

#         review = self.make_review_request(self.item1, self.registrar, requester=self.editor)

#         self.assertTrue(user_can_view_review(self.editor,review))
#         self.assertTrue(user_can_view_review(self.registrar,review))
#         self.assertTrue(user_can_view_review(self.su,review))
#         self.assertFalse(user_can_view_review(self.viewer,review))

#         review.status = REVIEW_STATES.cancelled
#         review.save()

#         review = models.ReviewRequest.objects.get(pk=review.pk) #decache

#         self.assertTrue(user_can_view_review(self.editor,review))
#         self.assertFalse(user_can_view_review(self.registrar,review))
#         self.assertTrue(user_can_view_review(self.su,review))
#         self.assertFalse(user_can_view_review(self.viewer,review))

#     def test_notifications(self):
#         viewer_num_notifications = self.viewer.notifications.count()
#         registrar_num_notifications = self.registrar.notifications.count()
#         editor_num_notifications = self.editor.notifications.count()

#         review = self.make_review_request_iterable([], request_kwargs=dict(
#             requester=self.viewer,
#             registration_authority=self.ra,
#             state=self.ra.public_state,
#             registration_date=datetime.date(2010,1,1)
#         ))

#         # Review requested, does a registrar get the notification?
#         self.assertTrue(self.viewer.notifications.count() == viewer_num_notifications)
#         self.assertTrue(self.registrar.notifications.count() == registrar_num_notifications + 1)
#         self.assertTrue(self.editor.notifications.count() == editor_num_notifications)

#         self.assertTrue(self.registrar.notifications.first().target == review)

#         review.status = REVIEW_STATES.accepted
#         review.save()

#         # Review updated, does the requester get the notification?
#         self.assertTrue(self.viewer.notifications.count() == viewer_num_notifications + 1)
#         self.assertTrue(self.registrar.notifications.count() == registrar_num_notifications + 1)
#         self.assertTrue(self.editor.notifications.count() == editor_num_notifications)

#         self.assertTrue(self.viewer.notifications.first().target == review)

#     @tag('inactive_ra')
#     def test_cannot_create_rr_against_incative_ra(self):
#         self.login_editor()
#         self.ra.active = 1
#         self.ra.save()

#         self.assertEqual(self.item1.review_requests.count(),0)

#         response = self.post_public_rr([self.item1])
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('registrationAuthorities' in response.context['form'].errors)
#         self.assertEqual(self.item1.review_requests.count(),0)

#     @tag('inactive_ra')
#     def test_cannot_accept_rr_with_inactive_ra(self):
#         self.login_editor()

#         # Create review request
#         response = self.post_public_rr([self.item3])
#         self.assertEqual(self.item3.review_requests.count(),1)
#         review = self.item3.review_requests.all()[0]

#         # Make ra inactive
#         self.ra.active = 1
#         self.ra.save()

#         response = self.client.get(reverse('aristotle:userReviewAccept',args=[review.pk]))
#         self.assertEqual(response.status_code, 404)

#         response = self.client.post(reverse('aristotle:userReviewAccept',args=[review.pk]),
#             {
#                 'review_accept-response': "I can accept this!",
#                 'review_accept_view-current_step': 'review_accept',
#                 'submit_skip': 'value',
#             })

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(self.item3.review_requests.count(),1)

#     @tag('inactive_ra')
#     def test_reviews_hidden_from_lists_when_ra_inactive(self):
#         self.login_viewer()

#         # Create review request
#         response = self.post_public_rr([self.item1])
#         self.assertEqual(self.item1.review_requests.count(),1)

#         # Make ra inactive
#         self.ra.active = 1
#         self.ra.save()

#         # My review requests
#         response = self.client.get(reverse('aristotle_mdr:userMyReviewRequests'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['reviews']), 0)

#         # Registrar Review list
#         self.login_registrar()
#         response  = self.client.get(reverse('aristotle_mdr:userReadyForReview'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['reviews']), 0)
