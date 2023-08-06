from django.conf.urls import include, url

from aristotle_mdr.forms.search import PermissionSearchForm
from aristotle_mdr.views.search import PermissionSearchView

from haystack.views import search_view_factory
from haystack.query import SearchQuerySet


urlpatterns = [
    url(r'^', include('aristotle_mdr.urls')),
    url(r'^extension_test/', include('extension_test.extension_urls', app_name="extension_test", namespace="extension_test")),
    url(
        r'^fail_search/?',
        search_view_factory(
            view_class=PermissionSearchView,
            template='search/search.html',
            searchqueryset= SearchQuerySet(),
            form_class=PermissionSearchForm
            ),
        name='fail_search'
    ),

    url(r'^', include('aristotle_mdr.contrib.links.urls', app_name="aristotle_mdr_links", namespace="aristotle_mdr_links")),
    url(r'^publish/', include('aristotle_mdr.contrib.self_publish.urls', app_name="aristotle_self_publish", namespace="aristotle_self_publish")),
    url(r'^', include('aristotle_mdr.contrib.slots.urls', app_name="aristotle_slots", namespace="aristotle_slots")),
    url(r'^', include('aristotle_mdr.contrib.identifiers.urls', app_name="aristotle_mdr_identifiers", namespace="aristotle_identifiers")),
]
