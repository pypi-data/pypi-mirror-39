from django.contrib import admin
from aristotle_dse import models

from aristotle_mdr.register import register_concept


class DSSDEInclusionInline(admin.TabularInline):
    model=models.DSSDEInclusion
    extra=0
    classes = ('grp-collapse grp-closed', )
    raw_id_fields = ('data_element', )
    autocomplete_lookup_fields = {
        'fk': ['data_element']
    }


class DSSClusterInclusionInline(admin.TabularInline):
    model=models.DSSClusterInclusion
    extra=0
    classes = ('grp-collapse grp-closed', )
    fk_name = 'dss'
    raw_id_fields = ('child', )
    autocomplete_lookup_fields = {
        'fk': ['child']
    }


register_concept(
    models.DataSetSpecification,
    extra_fieldsets=[
        (
            'Methodology',
            {'fields': [
                'statistical_unit',
                'collection_method',
                'ordered',
                ('implementation_start_date', 'implementation_end_date'),
            ]}
        ),
    ],
    extra_inlines=[DSSDEInclusionInline, DSSClusterInclusionInline],
    reversion={
        'follow': ['dssdeinclusion_set', 'dssclusterinclusion_set'],
        'follow_classes': [models.DSSClusterInclusion, models.DSSDEInclusion]
    },
)


register_concept(
    models.DataCatalog,
    extra_fieldsets=[
        ('Data Source',
            {'fields': ['issued', 'publisher', 'homepage', 'spatial', 'license']}),
    ]
)


register_concept(
    models.Dataset,
    extra_fieldsets=[
        ('Coverage',
            {'fields': ['spatial', 'temporal']}),
        ('Publishing',
            {'fields': [
                'publisher', 'contact_point', 'landing_page',
                'dct_modified', 'issued', 'accrual_periodicity'
                ]}),
    ]
)


register_concept(
    models.Distribution,
    extra_fieldsets=[
        ('File details',
            {'fields': [
                'access_URL', 'download_URL',
                'byte_size', 'media_type', 'format_type',
            ]}),
        ('Publishing',
            {'fields': [
                'license', 'rights', 'publisher',
                'dct_modified', 'issued',
                ]}),
    ],
    reversion={
        'follow': ['distributiondataelementpath_set'],
        'follow_classes': [models.DistributionDataElementPath]
    }
)
