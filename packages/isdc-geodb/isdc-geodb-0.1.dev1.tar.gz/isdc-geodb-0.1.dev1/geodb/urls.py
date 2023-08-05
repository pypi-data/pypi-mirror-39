from .geoapi import (
    BaselineStatisticResource,
    # FloodRiskStatisticResource,
    getProvince,
    # EarthQuakeStatisticResource,
    # getEQEvents,
    # getAccessibilities,
    # getSAMParameters,
    # getIncidentsRaw,
    getVillages,
    getLastUpdatedStatus,
    # getLandslide
)
from django.conf.urls import include, patterns, url
from tastypie.api import Api

geoapi = Api(api_name='geoapi')

geoapi.register(BaselineStatisticResource())
# geoapi.register(FloodRiskStatisticResource())
geoapi.register(getProvince())
# geoapi.register(EarthQuakeStatisticResource())
# geoapi.register(getEQEvents())
# geoapi.register(getAccessibilities())
# geoapi.register(getSAMParameters())
# geoapi.register(getIncidentsRaw())
geoapi.register(getVillages())
geoapi.register(getLastUpdatedStatus())
# geoapi.register(getLandslide())

urlpatterns_getoverviewmaps = patterns(
    'geodb.views',
    # url(r'^$', 'exportdata', name='exportdata'),
    url(r'^$', 'getOverviewMaps', name='getOverviewMaps'),
    url(r'^generalinfo$', 'getGeneralInfoVillages', name='getGeneralInfoVillages'),
    # url(r'^snowinfo$', 'getSnowVillage', name='getSnowVillage'),
    # url(r'^accessibilityinfo$', 'getAccesibilityInfoVillages', name='getAccesibilityInfoVillages'),
    # url(r'^floodinfo$', 'getFloodInfoVillages', name='getFloodInfoVillages'),
    # url(r'^earthquakeinfo$', 'getEarthquakeInfoVillages', name='getEarthquakeInfoVillages'),
    url(r'^getWMS$', 'getWMS', name='getWMS'),
    # url(r'^getGlofasChart$', 'getGlofasChart', name='getGlofasChart'),
    # url(r'^getGlofasPointsJSON$', 'getGlofasPointsJSON', name='getGlofasPointsJSON'),
    # url(r'^weatherinfo$', 'getWeatherInfoVillages', name='getWeatherInfoVillages'),
    url(r'^demographic$', 'getDemographicInfo', name='getDemographicInfo'),
    # url(r'^landslideinfo$', 'getLandSlideInfoVillages', name='getLandSlideInfoVillages'),
    # url(r'^climateinfo$', 'getClimateVillage', name='getClimateVillage'),   
)

urlpatterns = [
    # api
    url(r'', include(geoapi.urls)),

    url(r'^getOverviewMaps/', include(urlpatterns_getoverviewmaps)),
]
