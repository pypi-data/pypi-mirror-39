from django_filters.filterset import FilterSet
from django_filters.constants import ALL_FIELDS
from django_filters.utils import get_all_model_fields
import django_filters
from django.db import models
from aristotle_mdr.models import _concept


class AristotleFilterSet(FilterSet):
    pass

    # @classmethod
    # def get_fields(cls):

    #     model = cls._meta.model
    #     fields = cls._meta.fields
    #     exclude = cls._meta.exclude
    #     logger.warning([model,fields,exclude])

    #     # Setting exclude with no fields implies all other fields.
    #     if exclude is not None and fields is None:
    #         fields = ALL_FIELDS

    #     # Resolve ALL_FIELDS into all fields for the filterset's model.
    #     if fields == ALL_FIELDS:
    #         fields = get_all_model_fields(model)

    #     if not isinstance(fields, dict):

    #         field_dict = {}

    #         for field in fields:
    #             dbfield = model._meta.get_field(field)

    #             if isinstance(dbfield, models.CharField) or isinstance(dbfield, models.TextField):
    #                 field_dict[field] = ['exact', 'icontains', 'iexact']
    #             else:
    #                 field_dict[field] = ['exact']

    #         cls._meta.fields = field_dict

    #     return super().get_fields()


class IdentifierFilterSet(FilterSet):
    namespace = django_filters.CharFilter(name='namespace__shorthand_prefix', lookup_expr='iexact', distinct=True)
    class Meta:
        fields = ['namespace']


class StatusFilterSet(FilterSet):
    is_current = django_filters.BooleanFilter(method='filter_is_current')
    ra = django_filters.CharFilter(name='registrationAuthority__uuid', lookup_expr='iexact', distinct=True)
    class Meta:
        fields = ['is_current', 'ra']

    def filter_is_current(self, qs, name, value):
        if name=="is_current" and value:
            return qs.current()
        else:
            return qs


class ConceptFilterSet(FilterSet):

    identifier = django_filters.CharFilter(name='identifiers__identifier', lookup_expr='iexact', distinct=True)
    identifier_namespace = django_filters.CharFilter(name='identifiers__namespace__shorthand_prefix', lookup_expr='iexact', distinct=True)
    identifier_version = django_filters.CharFilter(name='identifiers__version', lookup_expr='iexact', distinct=True)
