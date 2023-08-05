from django.conf.urls import url, include

from rest_framework import routers

from .views import ConditionsView, ConditionsExportView, ConditionsImportXMLView
from .viewsets import (
    ConditionViewSet,
    AttributeViewSet,
    OptionViewSet,
    RelationViewSet,
    ConditionApiViewSet
)

# regular views

conditions_patterns = [
    url(r'^$', ConditionsView.as_view(), name='conditions'),
    url(r'^export/(?P<format>[a-z]+)/$', ConditionsExportView.as_view(), name='conditions_export'),
    url(r'^import/(?P<format>[a-z]+)/$', ConditionsImportXMLView.as_view(), name='conditions_import'),
]

# internal AJAX API

internal_router = routers.DefaultRouter()
internal_router.register(r'conditions', ConditionViewSet, base_name='condition')
internal_router.register(r'attributes', AttributeViewSet, base_name='attribute')
internal_router.register(r'options', OptionViewSet, base_name='option')
internal_router.register(r'relations', RelationViewSet, base_name='relation')

conditions_patterns_internal = [
    url(r'^', include(internal_router.urls)),
]

# programmable API

api_router = routers.DefaultRouter()
api_router.register(r'conditions', ConditionApiViewSet, base_name='condition')

conditions_patterns_api = [
    url(r'^', include(api_router.urls)),
]
