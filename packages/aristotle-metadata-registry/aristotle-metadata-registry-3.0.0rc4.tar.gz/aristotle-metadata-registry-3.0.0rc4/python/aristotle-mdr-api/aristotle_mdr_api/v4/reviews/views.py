from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from aristotle_mdr.contrib.reviews.models import ReviewRequest, ReviewComment, REVIEW_STATES
from aristotle_mdr_api.v4.permissions import AuthCanViewEdit, AuthFinePerms
from aristotle_mdr import perms

from . import serializers


# class ReviewView(generics.RetrieveUpdateAPIView):
#     """Retrive and update and issue"""
#     permission_classes=(AuthCanViewEdit,)
#     serializer_class=serializers.IssueSerializer
#     queryset=ReviewRequest.objects.all()


# class ReviewCreateView(generics.CreateAPIView):
#     """Create a new review"""
#     permission_classes=(AuthCanViewEdit,)
#     serializer_class=serializers.IssueSerializer


class ReviewCommentCreateView(generics.CreateAPIView):
    """Create a comment against a review"""
    permission_classes=(AuthCanViewEdit,)
    serializer_class=serializers.ReviewCommentSerializer


class ReviewCommentRetrieveView(generics.RetrieveAPIView):
    permission_classes=(AuthCanViewEdit,)
    serializer_class=serializers.ReviewCommentSerializer
    queryset=ReviewComment.objects.all()


class ReviewUpdateAndCommentView(generics.UpdateAPIView):
    """Open or close a review, with optional comment"""
    permission_classes=(AuthCanViewEdit,)
    serializer_class=serializers.ReviewUpdateAndCommentSerializer
    pk_url_kwarg='pk'

    http_method_names = ['patch']

    def get_object(self):
        pk = self.kwargs[self.pk_url_kwarg]
        obj = get_object_or_404(ReviewRequest, pk=pk)
        if not perms.user_can_close_or_reopen_review(self.request.user, obj):
            raise PermissionDenied
        return obj
