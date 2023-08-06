from django.http import Http404
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied

from rest_framework import serializers, status, mixins
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route

from django.forms import model_to_dict
from aristotle_mdr import models, perms
from aristotle_mdr.forms.search import PermissionSearchQuerySet
from aristotle_mdr_api.v3.permissions import AuthAndTokenOrRO
from .concepts import ConceptListSerializer

from rest_framework import viewsets

from .utils import (
    DescriptionStubSerializerMixin,
    MultiSerializerViewSetMixin,
    ConceptResultsPagination,
    UUIDLookupModelMixin
)


#class PermissionSearchForm
class ConceptSearchSerializer(serializers.Serializer):
    name = serializers.CharField()
    object = serializers.SerializerMethodField()
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request',None)
        super(ConceptSearchSerializer,self).__init__(*args,**kwargs)
    def get_object(self,instance):
        data = {}
        return ConceptListSerializer(instance.object,context={'request': self.request}).data


from haystack.models import SearchResult
#class SearchList(APIView):
class SearchViewSet(viewsets.GenericViewSet):
    "Search."

    serializer_class = ConceptSearchSerializer
    pagination_class = ConceptResultsPagination
    base_name="search"

    permission_key = 'search'
    permission_classes = (AuthAndTokenOrRO,)
    queryset = "None"


    def list(self, request):
        if not self.request.query_params.keys():
            return Response({'search_options':'q models state ra'.split()})

        items = PermissionSearchQuerySet().auto_query(self.request.query_params['q'])
        if self.request.query_params.get('models') is not None:
            search_models = []
            models = self.request.query_params.get('models')
            if type(models) != type([]):
                models = [models]
            for mod in models:
                if len(mod.split('.',1)) == 2:
                    app_label,model=mod.split('.',1)
                    i = ContentType.objects.get(app_label=app_label,model=model)
                else:
                    i = ContentType.objects.get(model=mod)
                search_models.append(i.model_class())
            items = items.models(*search_models)
        items = items.apply_permission_checks(user=request.user)

        items = items[:10]
        serializer = ConceptSearchSerializer(items, request=self.request, many=True)
        return Response(serializer.data)


class RegistrationAuthoritySerializer(serializers.ModelSerializer):
    state_meanings = serializers.SerializerMethodField()
    class Meta:
        model = models.RegistrationAuthority
        fields = ('uuid','name','definition','locked_state','public_state','state_meanings')
    def get_state_meanings(self,instance):
        return instance.statusDescriptions()


class RegistrationAuthorityViewSet(UUIDLookupModelMixin, viewsets.ReadOnlyModelViewSet):
    __doc__ = """
    Provides access to a list of registration authorities with the fields:

        %s

    """%(RegistrationAuthoritySerializer.Meta.fields,)

    queryset = models.RegistrationAuthority.objects.filter(active__in=[0,1])
    serializer_class = RegistrationAuthoritySerializer

    permission_key = 'ra'
    permission_classes = (AuthAndTokenOrRO,)


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Organization
        fields = ('uuid','name','definition')


class OrganizationViewSet(UUIDLookupModelMixin, viewsets.ReadOnlyModelViewSet):
    __doc__ = """
    Provides access to a list of organizations with the fields:

        %s

    """%(OrganizationSerializer.Meta.fields,)

    queryset = models.Organization.objects.all()
    serializer_class = OrganizationSerializer

    permission_key = 'organization'
    permission_classes = (AuthAndTokenOrRO,)
