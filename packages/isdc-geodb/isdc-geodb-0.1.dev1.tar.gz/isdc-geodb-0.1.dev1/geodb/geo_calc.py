from geodb.models import (
	AfgAdmbndaAdm1,
	AfgAdmbndaAdm2,
	AfgAirdrmp,
	# AfgAvsa,
	AfgCapaGsmcvr,
	AfgCaptAdm1ItsProvcImmap,
	AfgCaptAdm1NearestProvcImmap,
	AfgCaptAdm2NearestDistrictcImmap,
	AfgCaptAirdrmImmap,
	AfgCaptHltfacTier1Immap,
	AfgCaptHltfacTier2Immap,
	AfgCaptHltfacTier3Immap,
	AfgCaptHltfacTierallImmap,
	# AfgFldzonea100KRiskLandcoverPop, 
	AfgHltfac,
	# AfgIncidentOasis,
	AfgLndcrva,
	AfgPplp,
	AfgRdsl,
	districtsummary,
	# earthquake_events,
	# earthquake_shakemap,
	# FloodRiskExposure, 
	# forecastedLastUpdate, 
	LandcoverDescription,
	provincesummary,
	tempCurrentSC,
	# villagesummaryEQ,
	)
import json
import time, datetime
from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.constants import ALL
from django.db.models import Count, Sum, F, When, Case
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.authorization import DjangoAuthorization
from urlparse import urlparse
from geonode.maps.models import Map
from geonode.maps.views import _resolve_map, _PERMISSION_MSG_VIEW
from django.db import connection, connections
from itertools import *
# addded by boedy
from matrix.models import matrix
from tastypie.cache import SimpleCache
from pytz import timezone, all_timezones
from django.http import HttpResponse

from djgeojson.serializers import Serializer as GeoJSONSerializer

# from geodb.geoapi import getRiskNumber

from graphos.sources.model import ModelDataSource
from graphos.renderers import flot, gchart
from graphos.sources.simple import SimpleDataSource
from django.test import RequestFactory
import urllib2, urllib
import pygal
from geodb.radarchart import RadarChart
# from geodb.riverflood import getFloodForecastBySource

from django.utils.translation import ugettext as _
# from securitydb.models import SecureFeature
import pprint

#added by razinal
import pickle
import visvalingamwyatt as vw
from shapely.wkt import loads as load_wkt
from vectorformats.Formats import Django, GeoJSON
from vectorformats.Feature import Feature
from vectorformats.Formats.Format import Format

# ISDC
from geonode.utils import include_section, none_to_zero, query_to_dicts, RawSQL_nogroupby, dict_ext, list_ext, linenum
from django.conf import settings

import importlib
from .enumerations import (
	DEPTH_TYPES_INVERSE,
	DEPTH_TYPES,
	HEALTHFAC_TYPES,
	LANDCOVER_TYPES,
	LANDCOVER_TYPES_GROUP,
	LANDCOVER_TYPES_GROUP_INVERSE,
	PROVINCESUMMARY_LANDCOVER_TYPES,
	LIKELIHOOD_INDEX,
	ROAD_TYPES,
	HEALTHFAC_TYPES_INVERSE,
	LIKELIHOOD_TYPES,
)

def getCommonUse(request,flag, code):
	response = {}
	response['parent_label']=_('Custom Selection')
	response['qlinks']=_('Select provinces')
	response['adm_child'] = []
	response['adm_prov'] = []
	response['adm_dist'] = []
	# response['parent_label_dash']='Custom Selection'

	# if flag == 'entireAfg':
	#     response['parent_label']='Afghanistan'
	#     response['parent_label_dash']='Afghanistan'
	# elif flag == 'currentProvince':
	#     if code<=34:
	#         lblTMP = AfgAdmbndaAdm1.objects.filter(prov_code=code)
	#         response['parent_label_dash'] = 'Afghanistan - '+lblTMP[0].prov_na_en
	#         response['parent_label'] = lblTMP[0].prov_na_en
	#     else:
	#         lblTMP = AfgAdmbndaAdm2.objects.filter(dist_code=code)
	#         response['parent_label_dash'] = 'Afghanistan - '+ lblTMP[0].prov_na_en + ' - ' +lblTMP[0].dist_na_en
	#         response['parent_label'] = lblTMP[0].dist_na_en

	main_resource = AfgAdmbndaAdm1.objects.all().values('prov_code','prov_na_en').order_by('prov_na_en')
	# clusterPoints = AfgAdmbndaAdm1.objects.all()
	response['parent_label_dash']=[]
	if flag == 'entireAfg':
		response['areatype']='nation'
		response['parent_label']=_('Afghanistan')
		response['parent_label_dash'].append({'name':_('Afghanistan'),'query':'','code':0})
		response['qlinks']=_('Select province')
		resource = main_resource
		# clusterPoints = AfgAdmbndaAdm1.objects.all()
		for i in resource:
			response['adm_child'].append({'code':i['prov_code'],'name':i['prov_na_en']})
	elif flag == 'currentProvince':
		if code<=34:
			lblTMP = AfgAdmbndaAdm1.objects.filter(prov_code=code)
			response['parent_label_dash'].append({'name':_('Afghanistan'),'query':'','code':0})
			response['parent_label_dash'].append({'name':lblTMP[0].prov_na_en,'query':'&code='+str(code),'code':code})
			response['parent_label'] = lblTMP[0].prov_na_en
			response['qlinks']=_('Select district')
			response['areatype']='province'
			resource = AfgAdmbndaAdm2.objects.all().values('dist_code','dist_na_en').filter(prov_code=code).order_by('dist_na_en')
			# clusterPoints = AfgAdmbndaAdm2.objects.all()
			for i in resource:
				response['adm_child'].append({'code':i['dist_code'],'name':i['dist_na_en']})
			for i in main_resource:
				response['adm_prov'].append({'code':i['prov_code'],'name':i['prov_na_en']})
		else:
			lblTMP = AfgAdmbndaAdm2.objects.filter(dist_code=code)
			response['parent_label_dash'].append({'name':_('Afghanistan'),'query':'','code':0})
			response['parent_label_dash'].append({'name':lblTMP[0].prov_na_en,'query':'&code='+str(lblTMP[0].prov_code),'code':lblTMP[0].prov_code})
			response['parent_label_dash'].append({'name':lblTMP[0].dist_na_en,'query':'&code='+str(code),'code':code})
			response['parent_label'] = lblTMP[0].dist_na_en
			response['qlinks']=''
			response['areatype']='district'
			for i in main_resource:
				response['adm_prov'].append({'code':i['prov_code'],'name':i['prov_na_en']})
			resource = AfgAdmbndaAdm2.objects.all().values('dist_code','dist_na_en').filter(prov_code=lblTMP[0].prov_code).order_by('dist_na_en')
			for i in resource:
				response['adm_dist'].append({'code':i['dist_code'],'name':i['dist_na_en']})
	else:
		response['parent_label_dash'].append({'name':_('Custom Selection'),'query':'','code':0})
		response['qlinks']=''
		response['areatype']='custom'

	# response['poi_points'] = []
	# for i in clusterPoints:
	#     response['poi_points'].append({'code':i.prov_code,'x':i.wkb_geometry.point_on_surface.x,'y':i.wkb_geometry.point_on_surface.y})
	return response

def getRawBaseLine(filterLock, flag, code, includes=[], excludes=[]):
	targetBase = AfgLndcrva.objects.all()
	response = {}
	parent_data = getRiskNumber(targetBase, filterLock, 'agg_simplified_description', 'area_population', 'area_sqm', 'area_buildings', flag, code, None)

	temp = dict([(c['agg_simplified_description'], c['count']) for c in parent_data])
	response['built_up_pop'] = round(temp.get('Build Up', 0) or 0,0)
	response['cultivated_pop'] = round(temp.get('Fruit Trees', 0) or 0,0)+round(temp.get('Irrigated Agricultural Land', 0) or 0,0)+round(temp.get('Rainfed', 0) or 0,0)+round(temp.get('Vineyards', 0) or 0,0)
	response['barren_pop'] = round(temp.get('Water body and Marshland', 0) or 0,0)+round(temp.get('Barren land', 0) or 0,0)+round(temp.get('Snow', 0) or 0,0)+round(temp.get('Rangeland', 0) or 0,0)+round(temp.get('Sand Covered Areas', 0) or 0,0)+round(temp.get('Forest & Shrub', 0) or 0,0)+round(temp.get('Sand Dunes', 0) or 0,0)

	response['built_up_pop_build_up'] = round(temp.get('Build Up', 0) or 0,0)
	response['cultivated_pop_fruit_trees'] = round(temp.get('Fruit Trees', 0) or 0,0)
	response['cultivated_pop_irrigated_agricultural_land'] = round(temp.get('Irrigated Agricultural Land', 0) or 0,0)
	response['cultivated_pop_rainfed'] = round(temp.get('Rainfed', 0) or 0,0)
	response['cultivated_pop_vineyards'] = round(temp.get('Vineyards', 0) or 0,0)
	response['barren_pop_water_body_and_marshland'] = round(temp.get('Water body and Marshland', 0) or 0,0)
	response['barren_pop_barren_land'] = round(temp.get('Barren land', 0) or 0,0)
	response['barren_pop_snow'] = round(temp.get('Snow', 0) or 0,0)
	response['barren_pop_rangeland'] = round(temp.get('Rangeland', 0) or 0,0)
	response['barren_pop_sand_covered_areas'] = round(temp.get('Sand Covered Areas', 0) or 0,0)
	response['barren_pop_forest_shrub'] = round(temp.get('Forest & Shrub', 0) or 0,0)
	response['barren_pop_sand_dunes'] = round(temp.get('Sand Dunes', 0) or 0,0)

	temp = dict([(c['agg_simplified_description'], c['houseatrisk']) for c in parent_data])
	response['built_up_buildings'] = temp.get('Build Up', 0) or 0
	response['cultivated_buildings'] = temp.get('Fruit Trees', 0) or 0+temp.get('Irrigated Agricultural Land', 0) or 0+temp.get('Rainfed', 0) or 0+temp.get('Vineyards', 0) or 0
	response['barren_buildings'] = temp.get('Water body and Marshland', 0) or 0+temp.get('Barren land', 0) or 0+temp.get('Snow', 0) or 0+temp.get('Rangeland', 0) or 0+temp.get('Sand Covered Areas', 0) or 0+temp.get('Forest & Shrub', 0) or 0+temp.get('Sand Dunes', 0) or 0

	response['built_up_buildings_build_up'] = round(temp.get('Build Up', 0) or 0,0)
	response['cultivated_buildings_fruit_trees'] = round(temp.get('Fruit Trees', 0) or 0,0)
	response['cultivated_buildings_irrigated_agricultural_land'] = round(temp.get('Irrigated Agricultural Land', 0) or 0,0)
	response['cultivated_buildings_rainfed'] = round(temp.get('Rainfed', 0) or 0,0)
	response['cultivated_buildings_vineyards'] = round(temp.get('Vineyards', 0) or 0,0)
	response['barren_buildings_water_body_and_marshland'] = round(temp.get('Water body and Marshland', 0) or 0,0)
	response['barren_buildings_barren_land'] = round(temp.get('Barren land', 0) or 0,0)
	response['barren_buildings_snow'] = round(temp.get('Snow', 0) or 0,0)
	response['barren_buildings_rangeland'] = round(temp.get('Rangeland', 0) or 0,0)
	response['barren_buildings_sand_covered_areas'] = round(temp.get('Sand Covered Areas', 0) or 0,0)
	response['barren_buildings_forest_shrub'] = round(temp.get('Forest & Shrub', 0) or 0,0)
	response['barren_buildings_sand_dunes'] = round(temp.get('Sand Dunes', 0) or 0,0)

	temp = dict([(c['agg_simplified_description'], c['areaatrisk']) for c in parent_data])
	response['built_up_area'] = round((temp.get('Build Up', 0) or 1)/1000000,1)
	response['cultivated_area'] = round((temp.get('Fruit Trees', 0) or 1)/1000000,1)+round((temp.get('Irrigated Agricultural Land', 0) or 1)/1000000,1)+round((temp.get('Rainfed', 0) or 1)/1000000,1)+round((temp.get('Vineyards', 0) or 1)/1000000,1)
	response['barren_area'] = round((temp.get('Water body and Marshland', 0) or 1)/1000000,1)+round((temp.get('Barren land', 0) or 1)/1000000,1)+round((temp.get('Snow', 0) or 1)/1000000,1)+round((temp.get('Rangeland', 0) or 1)/1000000,1)+round((temp.get('Sand Covered Areas', 0) or 1)/1000000,1)+round((temp.get('Forest & Shrub', 0) or 1)/1000000,1)+round((temp.get('Sand Dunes', 0) or 1)/1000000,1)

	response['built_up_area_build_up'] = round((temp.get('Build Up', 0) or 1)/1000000,1)
	response['cultivated_area_fruit_trees'] = round((temp.get('Fruit Trees', 0) or 1)/1000000,1)
	response['cultivated_area_irrigated_agricultural_land'] = round((temp.get('Irrigated Agricultural Land', 0) or 1)/1000000,1)
	response['cultivated_area_rainfed'] = round((temp.get('Rainfed', 0) or 1)/1000000,1)
	response['cultivated_area_vineyards'] = round((temp.get('Vineyards', 0) or 1)/1000000,1)
	response['barren_area_water_body_and_marshland'] = round((temp.get('Water body and Marshland', 0) or 1)/1000000,1)
	response['barren_area_barren_land'] = round((temp.get('Barren land', 0) or 1)/1000000,1)
	response['barren_area_snow'] = round((temp.get('Snow', 0) or 1)/1000000,1)
	response['barren_area_rangeland'] = round((temp.get('Rangeland', 0) or 1)/1000000,1)
	response['barren_area_sand_covered_areas'] = round((temp.get('Sand Covered Areas', 0) or 1)/1000000,1)
	response['barren_area_forest_shrub'] = round((temp.get('Forest & Shrub', 0) or 1)/1000000,1)
	response['barren_area_sand_dunes'] = round((temp.get('Sand Dunes', 0) or 1)/1000000,1)

	return response

def getQuickOverview(request, filterLock, flag, code, includes=[], excludes=[]):
	response = dict_ext()
	tempData = getShortCutData(flag,code)
	# response['Population']= tempData['Population']
	# response['Area']= tempData['Area']
	# response['Buildings']= tempData['total_buildings']
	# response['settlement']= tempData['settlements']
	initresponse = dict_ext(getCommonUse(request, flag, code))
	if include_section('', includes, excludes):
		response.update(getBaseline(request, filterLock, flag, code, 
			excludes=['getProvinceSummary', 'getProvinceAdditionalSummary'],
			response=initresponse,
			inject={
				'forward':True,
				'Population': tempData['Population'],
				'Area': tempData['Area'],
				'total_buildings': tempData['total_buildings'],
				'settlements': tempData['settlements']
			}
		))

		# add response from optional modules
		for modulename in settings.QUICKOVERVIEW_MODULES:
			module = importlib.import_module(modulename+'.views')
			tpl, data = module.getQuickOverview(request, filterLock, flag, code)
			response.path('quickoverview_templates')[modulename] = tpl
			response.path('quickoverview_data')[modulename] = data
		
		# response.update(getFloodForecastMatrix(filterLock, flag, code, includes=['flashflood_forecast_risk_pop']))
		# response.update(getFloodForecast(request, filterLock, flag, code, excludes=['getCommonUse','detail']))
		# response.update(getRawFloodRisk(filterLock, flag, code, excludes=['landcoverfloodrisk']))
		# response.update(getRawAvalancheForecast(request, filterLock, flag, code))
		# response.update(getRawAvalancheRisk(filterLock, flag, code))
		# response.update(getLandslideRisk(request, filterLock, flag, code, includes=['lsi_immap']))
		# response.update(getEarthquake(request, filterLock, flag, code, excludes=['getListEQ']))

		# response.update(GetAccesibilityData(filterLock, flag, code, includes=['AfgCaptAirdrmImmap', 'AfgCaptHltfacTier1Immap', 'AfgCaptHltfacTier2Immap', 'AfgCaptAdm1ItsProvcImmap', 'AfgCapaGsmcvr']))
		# response['pop_coverage_percent'] = int(round((response['pop_on_gsm_coverage']/response['Population'])*100,0))

	# if include_section('getSAMParams', includes, excludes):
	#     rawFilterLock = filterLock if 'flag' in request.GET else None
	#     if 'daterange' in request.GET:
	#         daterange = request.GET.get('daterange')
	#     elif 'daterange' in request.POST:
	#         daterange = request.POST.get('daterange')
	#     else:
	#         enddate = datetime.date.today()
	#         startdate = datetime.date.today() - datetime.timedelta(days=365)
	#         daterange = startdate.strftime("%Y-%m-%d")+','+enddate.strftime("%Y-%m-%d")
	#     main_type_raw_data = getSAMParams(request, daterange, rawFilterLock, flag, code, group='main_type', includeFilter=True)
	#     response['incident_type'] = (i['main_type'] for i in main_type_raw_data)
	#     if 'incident_type' in request.GET:
	#         response['incident_type'] = request.GET['incident_type'].split(',')
	#     response['incident_type_group']=[]
	#     for i in main_type_raw_data:
	#         response['incident_type_group'].append({'count':i['count'],'injured':i['injured'],'violent':i['violent']+i['affected'],'dead':i['dead'],'main_type':i['main_type'],'child':list(getSAMIncident(request, daterange, rawFilterLock, flag, code, 'type', i['main_type']))})
	#     response['main_type_child'] = getSAMParams(request, daterange, rawFilterLock, flag, code, 'main_type', False)

	if include_section('GeoJson', includes, excludes):
		response['GeoJson'] = json.dumps(getGeoJson(request, flag, code))

	return response

def getShortCutData(flag, code):
	response = {}
	if flag=='entireAfg':
		px = provincesummary.objects.aggregate(Sum('high_ava_population'),Sum('med_ava_population'),Sum('low_ava_population'),Sum('total_ava_population'),Sum('high_ava_area'),Sum('med_ava_area'),Sum('low_ava_area'),Sum('total_ava_area'), \
			Sum('high_risk_population'),Sum('med_risk_population'),Sum('low_risk_population'),Sum('total_risk_population'), Sum('high_risk_area'),Sum('med_risk_area'),Sum('low_risk_area'),Sum('total_risk_area'),  \
			Sum('water_body_pop_risk'),Sum('barren_land_pop_risk'),Sum('built_up_pop_risk'),Sum('fruit_trees_pop_risk'),Sum('irrigated_agricultural_land_pop_risk'),Sum('permanent_snow_pop_risk'),Sum('rainfed_agricultural_land_pop_risk'),Sum('rangeland_pop_risk'),Sum('sandcover_pop_risk'),Sum('vineyards_pop_risk'),Sum('forest_pop_risk'), Sum('sand_dunes_pop_risk'), \
			Sum('water_body_area_risk'),Sum('barren_land_area_risk'),Sum('built_up_area_risk'),Sum('fruit_trees_area_risk'),Sum('irrigated_agricultural_land_area_risk'),Sum('permanent_snow_area_risk'),Sum('rainfed_agricultural_land_area_risk'),Sum('rangeland_area_risk'),Sum('sandcover_area_risk'),Sum('vineyards_area_risk'),Sum('forest_area_risk'), Sum('sand_dunes_area_risk'), \
			Sum('water_body_pop'),Sum('barren_land_pop'),Sum('built_up_pop'),Sum('fruit_trees_pop'),Sum('irrigated_agricultural_land_pop'),Sum('permanent_snow_pop'),Sum('rainfed_agricultural_land_pop'),Sum('rangeland_pop'),Sum('sandcover_pop'),Sum('vineyards_pop'),Sum('forest_pop'), Sum('sand_dunes_pop'), \
			Sum('water_body_area'),Sum('barren_land_area'),Sum('built_up_area'),Sum('fruit_trees_area'),Sum('irrigated_agricultural_land_area'),Sum('permanent_snow_area'),Sum('rainfed_agricultural_land_area'),Sum('rangeland_area'),Sum('sandcover_area'),Sum('vineyards_area'),Sum('forest_area'), Sum('sand_dunes_area'), \
			Sum('settlements_at_risk'), Sum('settlements'), Sum('Population'), Sum('Area'), Sum('ava_forecast_low_pop'), Sum('ava_forecast_med_pop'), Sum('ava_forecast_high_pop'), Sum('total_ava_forecast_pop'),
			Sum('total_buildings'), Sum('total_risk_buildings'), Sum('high_ava_buildings'), Sum('med_ava_buildings'), Sum('total_ava_buildings') )
	else:
		if len(str(code)) > 2:
			px = districtsummary.objects.filter(district=code).aggregate(Sum('high_ava_population'),Sum('med_ava_population'),Sum('low_ava_population'),Sum('total_ava_population'),Sum('high_ava_area'),Sum('med_ava_area'),Sum('low_ava_area'),Sum('total_ava_area'), \
				Sum('high_risk_population'),Sum('med_risk_population'),Sum('low_risk_population'),Sum('total_risk_population'), Sum('high_risk_area'),Sum('med_risk_area'),Sum('low_risk_area'),Sum('total_risk_area'),  \
				Sum('water_body_pop_risk'),Sum('barren_land_pop_risk'),Sum('built_up_pop_risk'),Sum('fruit_trees_pop_risk'),Sum('irrigated_agricultural_land_pop_risk'),Sum('permanent_snow_pop_risk'),Sum('rainfed_agricultural_land_pop_risk'),Sum('rangeland_pop_risk'),Sum('sandcover_pop_risk'),Sum('vineyards_pop_risk'),Sum('forest_pop_risk'), Sum('sand_dunes_pop_risk'), \
				Sum('water_body_area_risk'),Sum('barren_land_area_risk'),Sum('built_up_area_risk'),Sum('fruit_trees_area_risk'),Sum('irrigated_agricultural_land_area_risk'),Sum('permanent_snow_area_risk'),Sum('rainfed_agricultural_land_area_risk'),Sum('rangeland_area_risk'),Sum('sandcover_area_risk'),Sum('vineyards_area_risk'),Sum('forest_area_risk'), Sum('sand_dunes_area_risk'), \
				Sum('water_body_pop'),Sum('barren_land_pop'),Sum('built_up_pop'),Sum('fruit_trees_pop'),Sum('irrigated_agricultural_land_pop'),Sum('permanent_snow_pop'),Sum('rainfed_agricultural_land_pop'),Sum('rangeland_pop'),Sum('sandcover_pop'),Sum('vineyards_pop'),Sum('forest_pop'), Sum('sand_dunes_pop'), \
				Sum('water_body_area'),Sum('barren_land_area'),Sum('built_up_area'),Sum('fruit_trees_area'),Sum('irrigated_agricultural_land_area'),Sum('permanent_snow_area'),Sum('rainfed_agricultural_land_area'),Sum('rangeland_area'),Sum('sandcover_area'),Sum('vineyards_area'),Sum('forest_area'), Sum('sand_dunes_area'), \
				Sum('settlements_at_risk'), Sum('settlements'), Sum('Population'), Sum('Area'), Sum('ava_forecast_low_pop'), Sum('ava_forecast_med_pop'), Sum('ava_forecast_high_pop'), Sum('total_ava_forecast_pop'),
				Sum('total_buildings'), Sum('total_risk_buildings'), Sum('high_ava_buildings'), Sum('med_ava_buildings'), Sum('total_ava_buildings') )
		else :
			px = provincesummary.objects.filter(province=code).aggregate(Sum('high_ava_population'),Sum('med_ava_population'),Sum('low_ava_population'),Sum('total_ava_population'),Sum('high_ava_area'),Sum('med_ava_area'),Sum('low_ava_area'),Sum('total_ava_area'), \
				Sum('high_risk_population'),Sum('med_risk_population'),Sum('low_risk_population'),Sum('total_risk_population'), Sum('high_risk_area'),Sum('med_risk_area'),Sum('low_risk_area'),Sum('total_risk_area'),  \
				Sum('water_body_pop_risk'),Sum('barren_land_pop_risk'),Sum('built_up_pop_risk'),Sum('fruit_trees_pop_risk'),Sum('irrigated_agricultural_land_pop_risk'),Sum('permanent_snow_pop_risk'),Sum('rainfed_agricultural_land_pop_risk'),Sum('rangeland_pop_risk'),Sum('sandcover_pop_risk'),Sum('vineyards_pop_risk'),Sum('forest_pop_risk'), Sum('sand_dunes_pop_risk'), \
				Sum('water_body_area_risk'),Sum('barren_land_area_risk'),Sum('built_up_area_risk'),Sum('fruit_trees_area_risk'),Sum('irrigated_agricultural_land_area_risk'),Sum('permanent_snow_area_risk'),Sum('rainfed_agricultural_land_area_risk'),Sum('rangeland_area_risk'),Sum('sandcover_area_risk'),Sum('vineyards_area_risk'),Sum('forest_area_risk'), Sum('sand_dunes_area_risk'), \
				Sum('water_body_pop'),Sum('barren_land_pop'),Sum('built_up_pop'),Sum('fruit_trees_pop'),Sum('irrigated_agricultural_land_pop'),Sum('permanent_snow_pop'),Sum('rainfed_agricultural_land_pop'),Sum('rangeland_pop'),Sum('sandcover_pop'),Sum('vineyards_pop'),Sum('forest_pop'), Sum('sand_dunes_pop'), \
				Sum('water_body_area'),Sum('barren_land_area'),Sum('built_up_area'),Sum('fruit_trees_area'),Sum('irrigated_agricultural_land_area'),Sum('permanent_snow_area'),Sum('rainfed_agricultural_land_area'),Sum('rangeland_area'),Sum('sandcover_area'),Sum('vineyards_area'),Sum('forest_area'), Sum('sand_dunes_area'), \
				Sum('settlements_at_risk'), Sum('settlements'), Sum('Population'), Sum('Area'), Sum('ava_forecast_low_pop'), Sum('ava_forecast_med_pop'), Sum('ava_forecast_high_pop'), Sum('total_ava_forecast_pop'),
				Sum('total_buildings'), Sum('total_risk_buildings'), Sum('high_ava_buildings'), Sum('med_ava_buildings'), Sum('total_ava_buildings') )

	for p in px:
		response[p[:-5]] = px[p]
	return response

def getShortCutDataFormatter(dic):
	response_tree = dict_ext()

	response_tree.path('baseline')['pop_total'] = dic['Population']
	response_tree.path('baseline')['area_total'] = dic['Area']
	response_tree.path('baseline')['settlement_total'] = dic['settlements']
	response_tree.path('baseline')['building_total'] = dic['total_buildings']
	response_tree.path('avalancherisk')['pop_total'] = dic['total_ava_population']
	response_tree.path('avalancherisk')['area_total'] = dic['total_ava_area']
	response_tree.path('avalancherisk')['building_total'] = dic['total_ava_buildings']
	response_tree.path('avalancheforecast')['pop_total'] = dic['total_ava_forecast_pop']
	response_tree.path('floodrisk')['pop_likelihood_total'] = dic['total_risk_population']
	response_tree.path('floodrisk')['area_likelihood_total'] = dic['total_risk_area']
	response_tree.path('floodrisk')['building_likelihood_total'] = dic['total_risk_buildings']
	response_tree.path('floodrisk')['settlement_likelihood_total'] = dic['settlements_at_risk']

	for key, value in dic.items():
		parts = list_ext(key.split('_'))
		if key in ['Population','Area','settlements','total_buildings','total_ava_population','total_ava_area','total_ava_buildings','total_ava_forecast_pop','total_risk_population','total_risk_area','total_risk_buildings','settlements_at_risk']:
			pass
		elif key.endswith('ava_population') and parts[0] in DEPTH_TYPES:
			response_tree.path('avalancherisk','pop_likelihood')[parts[0]] = value
		elif key.endswith('ava_area') and parts[0] in DEPTH_TYPES:
			response_tree.path('avalancherisk','area_likelihood')[parts[0]] = value
		elif key.endswith('risk_population') and parts[0] in DEPTH_TYPES:
			response_tree.path('floodrisk','pop_depth')[parts[0]] = value
		elif key.endswith('risk_area') and parts[0] in DEPTH_TYPES:
			response_tree.path('floodrisk','area_depth')[parts[0]] = value
		elif key.endswith('pop_risk'):
			response_tree.path('floodrisk','pop_lc')[PROVINCESUMMARY_LANDCOVER_TYPES.get(key[:-9],key[:-9])] = value
		elif key.endswith('area_risk'):
			response_tree.path('floodrisk','area_lc')[PROVINCESUMMARY_LANDCOVER_TYPES.get(key[:-10],key[:-10])] = value
		elif key.startswith('ava_forecast') and key.endswith('pop') and parts[2] in DEPTH_TYPES:
			response_tree.path('avalancheforecast','pop_depth')[parts[2]] = value
		elif key.endswith('ava_buildings') and parts[0] in DEPTH_TYPES:
			response_tree.path('avalancherisk','building_likelihood')[parts[0]] = value
		elif key.endswith('pop'):
			response_tree.path('baseline','pop_lc')[PROVINCESUMMARY_LANDCOVER_TYPES.get(key[:-4],key[:-4])] = value
		elif key.endswith('area'):
			response_tree.path('baseline','area_lc')[PROVINCESUMMARY_LANDCOVER_TYPES.get(key[:-5],key[:-5])] = value
		else:
			response_tree[key] = value

	return none_to_zero(response_tree)
 
def getBaseline(request, filterLock, flag, code, includes=[], excludes=[], inject={'forward':False}, response=dict_ext(), baselineonly=True):
	targetBase = AfgLndcrva.objects.all()

	cached = flag in ['entireAfg','currentProvince']
	# cache_data = None if not cached else (inject if inject['forward'] else getShortCutData(flag,code))

	# response['pop_total'] = getTotalPop(filterLock, flag, code, targetBase) if not cached else cache_data['Population']
	# response['area_total'] = getTotalArea(filterLock, flag, code, targetBase) if not cached else cache_data['Area']
	# response['building_total'] = getTotalBuildings(filterLock, flag, code, targetBase) if not cached else cache_data['total_buildings']
	# response['settlement_total'] = getTotalSettlement(filterLock, flag, code, targetBase) if not cached else cache_data['settlements']

	# response['healthfacility_total'] = getTotalHealthFacilities(filterLock, flag, code, AfgHltfac)
	# response['road_total'] = getTotalRoadNetwork(filterLock, flag, code, AfgRdsl) or 0.00000000001

	if include_section(['pop_lc','area_lc','building_lc'], includes, excludes):
		if cached:
			response = getShortCutDataFormatter(getShortCutData(flag, code))
			baseline = response.path('baseline')

			# separate query for building_lc because not cached
			counts = getRiskNumber(targetBase, filterLock, 'agg_simplified_description', None, None, 'area_buildings', flag, code, None)

			sliced = {c['agg_simplified_description']: c['houseatrisk'] for c in counts}
			baseline['building_lc'] = {k:round(sliced.get(v, 0), 0) for k,v in LANDCOVER_TYPES.items()}
			# baseline['building_total'] = sum(baseline['building_lc'].values()) # noqa, replace getTotalBuildings

		else:
			counts = getRiskNumber(targetBase, filterLock, 'agg_simplified_description', 'area_population', 'area_sqm', 'area_buildings', flag, code, None, settlField = 'vuid')
			baseline = response.path('baseline')

			sliced = {c['agg_simplified_description']: c['count'] for c in counts}
			baseline['pop_lc'] = {k:round(sliced.get(v, 0), 0) for k,v in LANDCOVER_TYPES.items()}
			baseline['pop_total'] = sum(baseline['pop_lc'].values()) # noqa, replace getTotalPop

			sliced = {c['agg_simplified_description']: c['areaatrisk'] for c in counts}
			baseline['area_lc'] = {k:round(sliced.get(v, 0), 0) for k,v in LANDCOVER_TYPES.items()}
			baseline['area_total'] = sum(baseline['area_lc'].values()) # noqa, replace getTotalArea

			sliced = {c['agg_simplified_description']: c['houseatrisk'] for c in counts}
			baseline['building_lc'] = {k:round(sliced.get(v, 0), 0) for k,v in LANDCOVER_TYPES.items()}
			baseline['building_total'] = sum(baseline['building_lc'].values()) # noqa, replace getTotalBuildings

			# exclude 'Water body and Marshland'
			baseline['settlement_total'] = len(set(c['settlatrisk'] for c in counts if c['agg_simplified_description'] not in ['Water body and Marshland']))
			# baseline['settlement_total'] = getTotalSettlement(filterLock, flag, code, targetBase) if not cached else cache_data['settlements']

		for sub in ['pop','area','building']:
			for k,v in LANDCOVER_TYPES_GROUP.items():
				baseline.path(sub+'_lcgroup')[k] = sum([baseline[sub+'_lc'].get(i) or 0 for i in v])

	if include_section('healthfacility', includes, excludes):
		hltParentData = getParentHltFacRecap(filterLock, flag, code)
		sliced = {HEALTHFAC_TYPES_INVERSE[c['facility_types_description']]:c['numberhospital'] for c in hltParentData}
		baseline['healthfacility'] = {k:round(sliced.get(v) or 0, 0) for k,v in HEALTHFAC_TYPES.items()}
		baseline['healthfacility_total'] = sum(baseline['healthfacility'].values())

	if include_section('road', includes, excludes):
		roadParentData = getParentRoadNetworkRecap(filterLock, flag, code)
		sliced = {c['type_update']:c['road_length'] for c in roadParentData}
		baseline['road'] = {k:round(sliced.get(k) or 0, 0) for k in ROAD_TYPES}
		baseline['road_total'] = sum(baseline['road'].values())

	if include_section('adm_lc', includes, excludes):
		baseline['adm_lc'] = getProvinceSummary(filterLock, flag, code)

	if include_section('adm_hlt_road', includes, excludes):
		baseline['adm_hlt_road'] = getProvinceAdditionalSummary(filterLock, flag, code)

	if include_section('GeoJson', includes, excludes):
		baseline['GeoJson'] = getGeoJson(request, flag, code)

	return baseline if baselineonly else response

def getParentRoadNetworkRecap(filterLock, flag, code):
	values = ['type_update']
	annotates = {'counter':Count('pk'),'road_length':Sum('road_length')/1000}
	basequery = AfgRdsl.objects.all().values(*values)
	if flag=='drawArea':
		annotates['road_length']=RawSQL_nogroupby('SUM( \
			case \
				when ST_CoveredBy(wkb_geometry,%s) then road_length \
				else ST_Length(st_intersection(wkb_geometry::geography,%s)) / road_length end \
			)/1000', (filterLock,filterLock))
		query = basequery.annotate(**annotates).extra(where={'ST_Intersects(wkb_geometry,%s)'%(filterLock)})
	elif flag=='entireAfg':
		query = basequery.annotate(**annotates)
	elif flag=='currentProvince':
		ff0001 = "dist_code  = '%s'"%(code) if len(str(code)) > 2 else ("left(cast(dist_code as text),{})='{}' and length(cast(dist_code as text))={}".format(*[1,code,3] if len(str(code))==1 else [2,code,4]))
		# ff0001 = "dist_code  = '%s'"%(code) if len(str(code)) > 2 else ("left(cast(dist_code as text),%s)='%s' and length(cast(dist_code as text))=%s"%(*[1,code,3] if len(str(code))==1 else *[2,code,4]))
		query = basequery.annotate(**annotates).extra(where={ff0001})
	elif flag=='currentBasin':
		print 'currentBasin'
	else:
		query = basequery.annotate(**annotates).extra(where={'ST_Within(wkb_geometry,%s)'%(filterLock)})
	return query
	# if flag=='drawArea':
	#     # countsRoadBase = AfgRdsl.objects.all().values('type_update').annotate(counter=Count('ogc_fid')).extra(
	#     # select={
	#     #     'road_length' : 'SUM(  \
	#     #             case \
	#     #                 when ST_CoveredBy(wkb_geometry'+','+filterLock+') then road_length \
	#     #                 else ST_Length(st_intersection(wkb_geometry::geography'+','+filterLock+')) / road_length end \
	#     #         )/1000'
	#     # },
	#     # where = {
	#     #     'ST_Intersects(wkb_geometry'+', '+filterLock+')'
	#     # }).values('type_update','road_length')
	#     countsRoadBase = AfgRdsl.objects.all().values(*values).\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length=RawSQL_nogroupby('SUM(  \
	#                 case \
	#                         when ST_CoveredBy(wkb_geometry'+','+filterLock+') then road_length \
	#                         else ST_Length(st_intersection(wkb_geometry::geography'+','+filterLock+')) / road_length end \
	#                 )/1000', ())).\
	#         extra(
	#             where = {
	#                 'ST_Intersects(wkb_geometry'+', '+filterLock+')'
	#             })

	# elif flag=='entireAfg':
	#     # countsRoadBase = AfgRdsl.objects.all().values('type_update').annotate(counter=Count('ogc_fid')).extra(
	#     #         select={
	#     #             'road_length' : 'SUM(road_length)/1000'
	#     #         }).values('type_update', 'road_length')
	#     print AfgRdsl.objects.all().values(*values).\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length=RawSQL_nogroupby('SUM("road_length")',())/1000).query
	#     countsRoadBase = AfgRdsl.objects.all().values(*values).\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length=Sum('road_length')/1000)

	# elif flag=='currentProvince':
	#     if len(str(code)) > 2:
	#         ff0001 =  "dist_code  = '"+str(code)+"'"
	#     else :
	#         if len(str(code))==1:
	#             ff0001 =  "left(cast(dist_code as text),1)  = '"+str(code)+"' and length(cast(dist_code as text))=3"
	#         else:
	#             ff0001 =  "left(cast(dist_code as text),2)  = '"+str(code)+"' and length(cast(dist_code as text))=4"

	#     countsRoadBase = AfgRdsl.objects.all().values(*values).annotate(counter=Count('ogc_fid')).extra(
	#         select={
	#              'road_length' : 'SUM(road_length)/1000'
	#         },
	#         where = {
	#             ff0001
	#          })

	# elif flag=='currentBasin':
	#     print 'currentBasin'
	# else:
	#     countsRoadBase = AfgRdsl.objects.all().values(*values).annotate(counter=Count('ogc_fid')).extra(
	#         select={
	#             'road_length' : 'SUM(road_length)/1000'
	#         },
	#         where = {'ST_Within(wkb_geometry'+', '+filterLock+')'})
	# return countsRoadBase

def getParentHltFacRecap(filterLock, flag, code):
	values = ['facility_types_description']
	annotates = {'counter':Count('pk'),'numberhospital':Count('pk')}
	targetBase = AfgHltfac.objects.all().filter(activestatus='Y').values(*values).annotate(**annotates)
	if flag=='drawArea':
		countsHLTBase = targetBase.extra(where={'ST_Intersects(wkb_geometry,%s)'%(filterLock)})
	elif flag=='entireAfg':
		countsHLTBase = targetBase
	elif flag=='currentProvince':
		ff0001 =  "%s = '%s'"%('dist_code' if len(str(code)) > 2 else 'prov_code', code)
		countsHLTBase = targetBase.extra(where={ff0001})
	elif flag=='currentBasin':
		print 'currentBasin'
	else:
		countsHLTBase = targetBase.extra(where={'ST_Within(wkb_geometry,%s)'%(filterLock)})
	return countsHLTBase

def getTotalBuildings(filterLock, flag, code, targetBase):
	# All population number
	if flag=='drawArea':
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(  \
						case \
							when ST_CoveredBy(wkb_geometry,'+filterLock+') then area_buildings \
							else st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_buildings end \
					)'
			},
			where = {
				'ST_Intersects(wkb_geometry, '+filterLock+')'
			}).values('countbase')
	elif flag=='entireAfg':
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_buildings)'
			}).values('countbase')
	elif flag=='currentProvince':
		if len(str(code)) > 2:
			ff0001 =  "dist_code  = '"+str(code)+"'"
		else :
			ff0001 =  "prov_code  = '"+str(code)+"'"
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_buildings)'
			},
			where = {
				ff0001
			}).values('countbase')
	elif flag=='currentBasin':
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_buildings)'
			},
			where = {"vuid = '"+str(code)+"'"}).values('countbase')
	else:
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_buildings)'
			},
			where = {
				'ST_Within(wkb_geometry, '+filterLock+')'
			}).values('countbase')

	return round(countsBase[0]['countbase'] or 0,0)

def getTotalPop(filterLock, flag, code, targetBase):
	# All population number
	if flag=='drawArea':
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(  \
						case \
							when ST_CoveredBy(wkb_geometry,'+filterLock+') then area_population \
							else st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_population end \
					)'
			},
			where = {
				'ST_Intersects(wkb_geometry, '+filterLock+')'
			}).values('countbase')
	elif flag=='entireAfg':
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_population)'
			}).values('countbase')
	elif flag=='currentProvince':
		if len(str(code)) > 2:
			ff0001 =  "dist_code  = '"+str(code)+"'"
		else :
			ff0001 =  "prov_code  = '"+str(code)+"'"
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_population)'
			},
			where = {
				ff0001
			}).values('countbase')
	elif flag=='currentBasin':
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_population)'
			},
			where = {"vuid = '"+str(code)+"'"}).values('countbase')
	else:
		countsBase = targetBase.extra(
			select={
				'countbase' : 'SUM(area_population)'
			},
			where = {
				'ST_Within(wkb_geometry, '+filterLock+')'
			}).values('countbase')

	return round(countsBase[0]['countbase'] or 0,0)

def getTotalArea(filterLock, flag, code, targetBase):
	if flag=='drawArea':
		countsBase = targetBase.extra(
			select={
				'areabase' : 'SUM(  \
						case \
							when ST_CoveredBy(wkb_geometry,'+filterLock+') then area_sqm \
							else st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_sqm end \
					)'
			},
			where = {
				'ST_Intersects(wkb_geometry, '+filterLock+')'
			}).values('areabase')
	elif flag=='entireAfg':
		countsBase = targetBase.extra(
			select={
				'areabase' : 'SUM(area_sqm)'
			}).values('areabase')
	elif flag=='currentProvince':
		if len(str(code)) > 2:
			ff0001 =  "dist_code  = '"+str(code)+"'"
		else :
			ff0001 =  "prov_code  = '"+str(code)+"'"
		countsBase = targetBase.extra(
			select={
				'areabase' : 'SUM(area_sqm)'
			},
			where = {
				ff0001
			}).values('areabase')
	elif flag=='currentBasin':
		countsBase = targetBase.extra(
			select={
				'areabase' : 'SUM(area_sqm)'
			},
			where = {"vuid = '"+str(code)+"'"}).values('areabase')

	else:
		countsBase = targetBase.extra(
			select={
				'areabase' : 'SUM(area_sqm)'
			},
			where = {
				'ST_Within(wkb_geometry, '+filterLock+')'
			}).values('areabase')

	return round((countsBase[0]['areabase'] or 0)/1000000,0)

def getTotalSettlement(filterLock, flag, code, targetBase):
	if flag=='drawArea':
		countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
			select={
				'numbersettlements': 'count(distinct vuid)'},
			where = {'st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_sqm > 1 and ST_Intersects(wkb_geometry, '+filterLock+')'}).values('numbersettlements')
	elif flag=='entireAfg':
		countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
			select={
				'numbersettlements': 'count(distinct vuid)'}).values('numbersettlements')
	elif flag=='currentProvince':
		if len(str(code)) > 2:
			ff0001 =  "dist_code  = '"+str(code)+"'"
		else :
			ff0001 =  "prov_code  = '"+str(code)+"'"
		countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
			select={
				'numbersettlements': 'count(distinct vuid)'},
			where = {ff0001}).values('numbersettlements')
	elif flag=='currentBasin':
		countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
			select={
				'numbersettlements': 'count(distinct vuid)'},
			where = {"vuid = '"+str(code)+"'"}).values('numbersettlements')
	else:
		countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
			select={
				'numbersettlements': 'count(distinct vuid)'},
			where = {'ST_Within(wkb_geometry, '+filterLock+')'}).values('numbersettlements')

	return round(countsBase[0]['numbersettlements'],0)

def getTotalHealthFacilities(filterLock, flag, code, targetBase):
	# targetBase = targetBase.objects.all().filter(activestatus='Y').values('facility_types_description')
	targetBase = targetBase.objects.all().filter(activestatus='Y')
	if flag=='drawArea':
		countsHLTBase = targetBase.extra(
				select={
					'numberhospital' : 'count(*)'
				},
				where = {
					'ST_Intersects(wkb_geometry'+', '+filterLock+')'
				}).values('numberhospital')

	elif flag=='entireAfg':
		countsHLTBase = targetBase.extra(
				select={
					'numberhospital' : 'count(*)'
				}).values('numberhospital')

	elif flag=='currentProvince':
		if len(str(code)) > 2:
			ff0001 =  "dist_code  = '"+str(code)+"'"
		else :
			ff0001 = "prov_code  = '"+str(code)+"'"

		countsHLTBase = targetBase.extra(
			select={
					'numberhospital' : 'count(*)'
			},where = {
				ff0001
			}).values('numberhospital')
	elif flag=='currentBasin':
		print 'currentBasin'
	else:
		countsHLTBase = targetBase.extra(
			select={
					'numberhospital' : 'count(*)'
			},where = {
				'ST_Within(wkb_geometry'+', '+filterLock+')'
			}).values('numberhospital')
	return round(countsHLTBase[0]['numberhospital'],0)

def getTotalRoadNetwork(filterLock, flag, code, targetBase):
	# targetBase = targetBase.objects.all().filter(activestatus='Y').values('facility_types_description')
	if flag=='drawArea':
		countsRoadBase = targetBase.objects.all().extra(
		select={
			'road_length' : 'SUM(  \
					case \
						when ST_CoveredBy(wkb_geometry'+','+filterLock+') then road_length \
						else ST_Length(st_intersection(wkb_geometry::geography'+','+filterLock+')) / road_length end \
				)/1000'
		},
		where = {
			'ST_Intersects(wkb_geometry'+', '+filterLock+')'
		}).values('road_length')

	elif flag=='entireAfg':
		countsRoadBase = targetBase.objects.all().extra(
				select={
					'road_length' : 'SUM(road_length)/1000'
				}).values('road_length')

	elif flag=='currentProvince':
		if len(str(code)) > 2:
			ff0001 =  "dist_code  = '"+str(code)+"'"
		else :
			if len(str(code))==1:
				ff0001 =  "left(cast(dist_code as text),1)  = '"+str(code)+"'  and length(cast(dist_code as text))=3"
			else:
				ff0001 =  "left(cast(dist_code as text),2)  = '"+str(code)+"'  and length(cast(dist_code as text))=4"

		countsRoadBase = targetBase.objects.all().extra(
			select={
				 'road_length' : 'SUM(road_length)/1000'
			},
			where = {
				ff0001
			 }).values('road_length')

	elif flag=='currentBasin':
		print 'currentBasin'
	else:
		countsRoadBase = targetBase.objects.all().extra(
			select={
				'road_length' : 'SUM(road_length)/1000'
			},
			where = {
				'ST_Within(wkb_geometry'+', '+filterLock+')'
			}).values('road_length')
	return round(float(countsRoadBase[0]['road_length'] or 0),0)

def getProvinceSummary(filterLock, flag, code, **kwargs):
	# cursor = connections['geodb'].cursor()

	print flag, code

	if flag == 'entireAfg':
		sql = "select b.prov_code as code, b.prov_na_en as na_en, a.*, \
			a.fruit_trees_pop+a.irrigated_agricultural_land_pop+a.rainfed_agricultural_land_pop+a.vineyards_pop as cultivated_pop,  \
			a.fruit_trees_area+a.irrigated_agricultural_land_area+a.rainfed_agricultural_land_area+a.vineyards_area as cultivated_area,  \
			a.water_body_pop+a.barren_land_pop+a.permanent_snow_pop+a.rangeland_pop+a.sandcover_pop+a.forest_pop+a.sand_dunes_pop as barren_pop,  \
			a.water_body_area+a.barren_land_area+a.permanent_snow_area+a.rangeland_area+a.sandcover_area+a.forest_area+a.sand_dunes_area as barren_area,  \
			 \
			a.fruit_trees_pop_risk+a.irrigated_agricultural_land_pop_risk+a.rainfed_agricultural_land_pop_risk+a.vineyards_pop_risk as cultivated_pop_risk, \
			a.fruit_trees_area_risk+a.irrigated_agricultural_land_area_risk+a.rainfed_agricultural_land_area_risk+a.vineyards_area_risk as cultivated_area_risk, \
			a.barren_land_pop_risk+a.permanent_snow_pop_risk+a.rangeland_pop_risk+a.sandcover_pop_risk+a.forest_pop_risk+a.sand_dunes_pop_risk as barren_pop_risk, \
			a.barren_land_area_risk+a.permanent_snow_area_risk+a.rangeland_area_risk+a.sandcover_area_risk+a.forest_area_risk+a.sand_dunes_area_risk as barren_area_risk \
			from provincesummary a \
			inner join afg_admbnda_adm1 b on cast(a.province as integer)=b.prov_code \
			order by a.\"Population\" desc"
	elif flag == 'currentProvince':
		sql = "select b.dist_code as code, b.dist_na_en as na_en, a.*, \
			a.fruit_trees_pop+a.irrigated_agricultural_land_pop+a.rainfed_agricultural_land_pop+a.vineyards_pop as cultivated_pop,  \
			a.fruit_trees_area+a.irrigated_agricultural_land_area+a.rainfed_agricultural_land_area+a.vineyards_area as cultivated_area,  \
			a.water_body_pop+a.barren_land_pop+a.permanent_snow_pop+a.rangeland_pop+a.sandcover_pop+a.forest_pop+a.sand_dunes_pop as barren_pop,  \
			a.water_body_area+a.barren_land_area+a.permanent_snow_area+a.rangeland_area+a.sandcover_area+a.forest_area+a.sand_dunes_area as barren_area,  \
			 \
			a.fruit_trees_pop_risk+a.irrigated_agricultural_land_pop_risk+a.rainfed_agricultural_land_pop_risk+a.vineyards_pop_risk as cultivated_pop_risk, \
			a.fruit_trees_area_risk+a.irrigated_agricultural_land_area_risk+a.rainfed_agricultural_land_area_risk+a.vineyards_area_risk as cultivated_area_risk, \
			a.barren_land_pop_risk+a.permanent_snow_pop_risk+a.rangeland_pop_risk+a.sandcover_pop_risk+a.forest_pop_risk+a.sand_dunes_pop_risk as barren_pop_risk, \
			a.barren_land_area_risk+a.permanent_snow_area_risk+a.rangeland_area_risk+a.sandcover_area_risk+a.forest_area_risk+a.sand_dunes_area_risk as barren_area_risk \
			from districtsummary a \
			inner join afg_admbnda_adm2 b on cast(a.district as integer)=b.dist_code \
			where b.prov_code="+str(code)+" \
			order by a.\"Population\" desc"
	else:
		return []

	# row = query_to_dicts(cursor, sql)

	# response = []

	# for i in row:
	# 	response.append(i)

	# cursor.close()

	with connections['geodb'].cursor() as cursor:
		response = list(query_to_dicts(cursor, sql))

	return response

def getProvinceAdditionalSummary(filterLock, flag, code):
	# cursor = connections['geodb'].cursor()

	if flag == 'entireAfg':
		sql = "select b.prov_code as code, b.prov_na_en as na_en, a.*, \
		a.hlt_special_hospital+a.hlt_rehabilitation_center+a.hlt_maternity_home+a.hlt_drug_addicted_treatment_center+a.hlt_private_clinic+a.hlt_malaria_center+a.hlt_mobile_health_team+a.hlt_other as hlt_others, \
		a.hlt_special_hospital+a.hlt_rehabilitation_center+a.hlt_maternity_home+a.hlt_drug_addicted_treatment_center+a.hlt_private_clinic+a.hlt_malaria_center+a.hlt_mobile_health_team+a.hlt_other+a.hlt_h1+a.hlt_h2+a.hlt_h3+a.hlt_chc+a.hlt_bhc+a.hlt_shc as hlt_total, \
		a.road_highway+a.road_primary+a.road_secondary+a.road_tertiary+a.road_residential+a.road_track+a.road_path+a.road_river_crossing+a.road_bridge as road_total \
		from province_add_summary a \
		inner join afg_admbnda_adm1 b on cast(a.prov_code as integer)=b.prov_code"
	elif flag == 'currentProvince':
		sql = "select b.dist_code as code, b.dist_na_en as na_en, a.*, \
		a.hlt_special_hospital+a.hlt_rehabilitation_center+a.hlt_maternity_home+a.hlt_drug_addicted_treatment_center+a.hlt_private_clinic+a.hlt_malaria_center+a.hlt_mobile_health_team+a.hlt_other as hlt_others, \
		a.hlt_special_hospital+a.hlt_rehabilitation_center+a.hlt_maternity_home+a.hlt_drug_addicted_treatment_center+a.hlt_private_clinic+a.hlt_malaria_center+a.hlt_mobile_health_team+a.hlt_other+a.hlt_h1+a.hlt_h2+a.hlt_h3+a.hlt_chc+a.hlt_bhc+a.hlt_shc as hlt_total, \
		a.road_highway+a.road_primary+a.road_secondary+a.road_tertiary+a.road_residential+a.road_track+a.road_path+a.road_river_crossing+a.road_bridge as road_total \
		from district_add_summary a \
		inner join afg_admbnda_adm2 b on cast(a.dist_code as integer)=b.dist_code \
		where b.prov_code="+str(code)
	else:
		return []

	# row = query_to_dicts(cursor, sql)

	# response = []

	# for i in row:
	# 	response.append(i)

	# cursor.close()

	with connections['geodb'].cursor() as cursor:
		response = list(query_to_dicts(cursor, sql))

	return response

def getProvinceSummary_glofas(filterLock, flag, code, YEAR, MONTH, DAY, merge, **kwargs):
	# cursor = connections['geodb'].cursor()
	# table = 'get_glofas_detail'
	# if merge:
	# 	table = 'get_merge_glofas_gfms_detail'
	table = 'get_merge_glofas_gfms_detail' if merge else 'get_glofas_detail'

	if flag == 'entireAfg':
		sql = "select b.prov_code as code, b.prov_na_en as na_en, \
				a.flashflood_forecast_extreme_pop, \
				a.flashflood_forecast_veryhigh_pop, \
				a.flashflood_forecast_high_pop, \
				a.flashflood_forecast_med_pop, \
				a.flashflood_forecast_low_pop, \
				a.flashflood_forecast_verylow_pop, \
				a.riverflood_forecast_extreme_pop, \
				a.riverflood_forecast_veryhigh_pop, \
				a.riverflood_forecast_high_pop, \
				a.riverflood_forecast_med_pop, \
				a.riverflood_forecast_low_pop, \
				a.riverflood_forecast_verylow_pop, \
				c.extreme, \
				c.veryhigh, \
				c.high, \
				c.med, \
				c.low, \
				c.verylow \
				from afg_admbnda_adm1 b \
				left join provincesummary a  on cast(a.province as integer)=b.prov_code \
				left join (\
				select \
				prov_code,\
				sum(extreme) as extreme,\
				sum(veryhigh) as veryhigh,\
				sum(high) as high, \
				sum(moderate) as med, \
				sum(low) as low, \
				sum(verylow) as verylow \
				from %s('%s-%s-%s') \
				group by prov_code \
				) c on b.prov_code = c.prov_code \
				order by a.\"Population\" desc" %(table,YEAR,MONTH,DAY)
	elif flag == 'currentProvince':
		sql = "select b.dist_code as code, b.dist_na_en as na_en, \
				a.flashflood_forecast_extreme_pop, \
				a.flashflood_forecast_veryhigh_pop, \
				a.flashflood_forecast_high_pop, \
				a.flashflood_forecast_med_pop, \
				a.flashflood_forecast_low_pop, \
				a.flashflood_forecast_verylow_pop, \
				a.riverflood_forecast_extreme_pop, \
				a.riverflood_forecast_veryhigh_pop, \
				a.riverflood_forecast_high_pop, \
				a.riverflood_forecast_med_pop, \
				a.riverflood_forecast_low_pop, \
				a.riverflood_forecast_verylow_pop, \
				c.extreme, \
				c.veryhigh, \
				c.high, \
				c.med, \
				c.low, \
				c.verylow \
				from afg_admbnda_adm2 b \
				left join districtsummary a  on cast(a.district as integer)=b.dist_code \
				left join (\
				select \
				dist_code,\
				sum(extreme) as extreme,\
				sum(veryhigh) as veryhigh,\
				sum(high) as high, \
				sum(moderate) as med, \
				sum(low) as low, \
				sum(verylow) as verylow \
				from %s('%s-%s-%s') \
				group by dist_code \
				) c on b.dist_code = c.dist_code \
				where b.prov_code=%s \
				order by a.\"Population\" desc" %(table,YEAR,MONTH,DAY,code)

	else:
		return []

	# row = query_to_dicts(cursor, sql)

	# response = []

	# for i in row:
	# 	response.append(i)

	# cursor.close()

	with connections['geodb'].cursor() as cursor:
		response = list(query_to_dicts(cursor, sql))
		response = getProvinceSummary_glofas_formatter(response) if kwargs.get('formatted') else response

	return response

def getProvinceSummary_glofas_formatter(rows=[]):
	
	response = []

	for row in rows:
		formatted = dict_ext()
		for k,v in row.items():
			keys = list_ext(k.split('_'))
			if keys.get(0) in LIKELIHOOD_TYPES:
				formatted.path('glofas_likelihood')[keys[0]] = v
			elif keys.get(1) == 'forecast' and keys.get(2) in LIKELIHOOD_TYPES:
				formatted.path('pop_%s_glofas_likelihood'%(keys.get(0)))[keys.get(2)] = v
			else:
				formatted[k] = v

		response.append(formatted)
			
	return response

def getGeoJson (filterLock, flag, code):
	if flag=='drawArea':
		# getprov = AfgAdmbndaAdm1.objects.all().values('type_update').annotate(counter=Count('ogc_fid')).extra(
		# select={
		#     'road_length' : 'SUM(  \
		#             case \
		#                 when ST_CoveredBy(wkb_geometry'+','+filterLock+') then road_length \
		#                 else ST_Length(st_intersection(wkb_geometry::geography'+','+filterLock+')) / road_length end \
		#         )/1000'
		# },
		# where = {
		#     'ST_Intersects(wkb_geometry'+', '+filterLock+')'
		# }).values('type_update','road_length')
		getprov = AfgAdmbndaAdm1.objects.all().extra(select={'code': 'prov_code', 'centroid': 'ST_AsText(wkb_geometry)'})
	elif flag=='entireAfg':
		getprov = AfgAdmbndaAdm1.objects.all().extra(select={'code': 'prov_code', 'centroid': 'ST_AsText(wkb_geometry)'})
	elif flag=='currentProvince':
		if len(str(code)) > 2:
			getprov = AfgAdmbndaAdm2.objects.all().filter(dist_code=code).extra(select={'code': 'dist_code', 'centroid': 'ST_AsText(wkb_geometry)'})
		else:
			getprov =  AfgAdmbndaAdm2.objects.all().filter(prov_code=code).extra(select={'code': 'dist_code', 'centroid': 'ST_AsText(wkb_geometry)'})
	else:
		getprov = AfgAdmbndaAdm1.objects.all().extra(select={'code': 'prov_code', 'centroid': 'ST_AsText(wkb_geometry)'})

	results = []
	ctroid = ''
	for res in getprov:
		feature = Feature(res.ogc_fid)
		ctroid += res.centroid
		geom = res.wkb_geometry
		geometry = {}
		geometry['type'] = geom.geom_type
		geometry['coordinates'] = geom.coords
		feature.geometry = vw.simplify_geometry(geometry, ratio=0.025)

		feature.properties['code'] = res.code
		results.append(feature)

	geojsondata = {}
	if results:
		geoj = GeoJSON.GeoJSON()
		geojsondata = geoj.encode(results, to_string=False)
		getcentroid = load_wkt(ctroid)
		dcentroid = getcentroid.centroid.wkt
		rpoint = dcentroid.replace('POINT ','')
		rspace = rpoint.replace(' ',', ')
		afirst = rspace.replace('(','')
		alast = afirst.replace(')','')
		fixctr = alast.split(",")
		geojsondata['centroid'] = fixctr

	# string = json.dumps(geojsondata)

	return geojsondata
  
def getRiskNumber(data, filterLock, fieldGroup, popField, areaField, houseField, aflag, acode, atablename, **kwargs):
	'''
	Generic query to get at-risk number for population, area, building, settlement
	kwargs['alias'] for compatibility with getFloodForecastRisk, getFlashFloodForecastRisk
	'''

	atablename = atablename+'.' if atablename else ''
	fieldGroup = [fieldGroup] if type(fieldGroup) is not list else fieldGroup
	default_alias = {'pop':'count','area':'areaatrisk','building':'houseatrisk','settlement':'settlatrisk'}
	alias = {k:kwargs.get('alias', {}).get(k, v) for k,v in default_alias.items()}

	annotates = {'counter': Count('pk')}
	annotates.update({alias['pop']: Sum(popField)} if popField else {})
	annotates.update({alias['area']: Sum(areaField)} if areaField else {})
	annotates.update({alias['building']: Sum(houseField)} if houseField else {})
	annotates.update({alias['settlement']: Count(kwargs['settlField'], distinct=True)} if 'settlField' in kwargs else {})
				
	if aflag=='drawArea':

		sum_tpl = '\
			SUM(  \
				case \
					when ST_CoveredBy({atablename}wkb_geometry,{filterLock}) then {aggField} \
					else st_area(st_intersection({atablename}wkb_geometry,{filterLock}) / st_area({atablename}wkb_geometry)*{aggField} \
				end \
			)'

		annotates = {'counter':Count('pk')}
		if popField:
			annotates[alias['pop']] =  RawSQL_nogroupby(sum_tpl.format(**{'atablename':atablename, 'filterLock':filterLock, 'aggField':popField}),[])
		if areaField:
			annotates[alias['area']] =  RawSQL_nogroupby(sum_tpl.format(**{'atablename':atablename, 'filterLock':filterLock, 'aggField':areaField}),[])
		if houseField:
			annotates[alias['building']] =  RawSQL_nogroupby(sum_tpl.format(**{'atablename':atablename, 'filterLock':filterLock, 'aggField':houseField}),[])
		if 'settlField' in kwargs:
			annotates[alias['settlement']] = RawSQL_nogroupby('\
			COUNT (DISTINCT \
				CASE \
					WHEN st_area(st_intersection(wkb_geometry,{filterLock})) / st_area(wkb_geometry)*area_sqm > 1 THEN {aggField} \
					ELSE NULL \
				END\
			)'.format(**{'filterLock':filterLock,'aggField':kwargs['settlField']}),[])

		counts = data.values(*fieldGroup).annotate(**annotates).extra(where = {'ST_Intersects(%swkb_geometry, %s)'%(atablename, filterLock)})

	elif aflag=='entireAfg':
		counts = data.values(*fieldGroup).annotate(**annotates)
	elif aflag=='currentProvince':
		ff0001 =  "%s = '%s'"%('dist_code' if len(str(acode)) > 2 else 'prov_code', acode)
		counts = data.values(*fieldGroup).annotate(**annotates).extra(where = {ff0001})
	elif aflag=='currentBasin':
		counts = data.values(*fieldGroup).annotate(**annotates).extra(where = {"%svuid = '%s'"%(atablename,acode)})
	else:
		counts = data.values(*fieldGroup).annotate(**annotates).extra(where = {'ST_Within(%swkb_geometry, %s)'%(atablename, filterLock)})
	print linenum(), counts.query
	return list(counts)     

