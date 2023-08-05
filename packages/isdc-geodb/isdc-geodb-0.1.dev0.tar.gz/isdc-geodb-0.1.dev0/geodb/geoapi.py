from geodb.models import (
	# AfgFldzonea100KRiskLandcoverPop,
	# FloodRiskExposure,
	AfgLndcrva,
	LandcoverDescription,
	# AfgAvsa,
	AfgAdmbndaAdm1,
	AfgPplp,
	# earthquake_shakemap,
	# earthquake_events,
	# villagesummaryEQ,
	AfgRdsl,
	AfgHltfac,
	forecastedLastUpdate,
	provincesummary,
	districtsummary,
	AfgCaptAdm1ItsProvcImmap,
	AfgCaptAdm1NearestProvcImmap,
	AfgCaptAdm2NearestDistrictcImmap,
	AfgCaptAirdrmImmap,
	AfgCaptHltfacTier1Immap,
	AfgCaptHltfacTier2Immap,
	tempCurrentSC,
	AfgCaptHltfacTier3Immap,
	AfgCaptHltfacTierallImmap,
	# AfgIncidentOasis,
	AfgCapaGsmcvr,
	AfgAirdrmp,
	OasisSettlements
)
import json
import time, datetime
from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.constants import ALL
from django.db.models import Count, Sum, Value
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

# from geodb.riverflood import getFloodForecastBySource
import timeago
from fuzzywuzzy import process, fuzz

from securitydb.models import SecureFeature

# ISDC
from geonode.utils import include_section, none_to_zero, query_to_dicts, RawSQL_nogroupby, merge_dict, dict_ext
from django.conf import settings

import importlib
from geodb.enumerations import HEALTHFAC_TYPES, LANDCOVER_TYPES, ROAD_TYPES, LANDCOVER_TYPES_INVERSE, ROAD_TYPES_INVERSE, HEALTHFAC_TYPES_INVERSE, PANEL_TITLES, LANDCOVER_INDEX, ROAD_TYPES, ROAD_INDEX, HEALTHFAC_INDEX
from geodb.geo_calc import (
	getParentRoadNetworkRecap, 
	getTotalArea,
	getTotalPop,
	getTotalSettlement,
	getParentHltFacRecap,
	getRiskNumber,
	getShortCutData,
	getShortCutDataFormatter,
	getBaseline,
)

from dashboard.views import dashboard_baseline

# # for development only
# from django.core.exceptions import ImproperlyConfigured
# try:
#     from flood.models import AfgFldzonea100KRiskLandcoverPop
#     from flood.riverflood import getFloodForecastBySource
# except ImportError as e:
#     raise ImproperlyConfigured("Error importing. Should import from own module instead of geodb. Only worked in development.")

FILTER_TYPES = {
	# 'flood': AfgFldzonea100KRiskLandcoverPop
}

def getRisk(request):
		# saving the user tracking records
		o = urlparse(request.META.get('HTTP_REFERER')).path
		o=o.split('/')
		mapCode = o[2]
		map_obj = _resolve_map(request, mapCode, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)

		queryset = matrix(user=request.user,resourceid=map_obj,action='Interactive Calculation')
		queryset.save()

		boundaryFilter = json.loads(request.body)
		temp1 = []
		for i in boundaryFilter['spatialfilter']:
			temp1.append('ST_GeomFromText(\''+i+'\',4326)')

		temp2 = 'ARRAY['
		first=True
		for i in temp1:
			if first:
				 temp2 = temp2 + i
				 first=False
			else :
				 temp2 = temp2 + ', ' + i  

		temp2 = temp2+']'
		
		filterLock = 'ST_Union('+temp2+')'
		response = self.getRiskExecute(filterLock)

		return response        

class getProvince(ModelResource):
	"""Provinces api"""
	class Meta:
		queryset = AfgAdmbndaAdm1.objects.all().defer('wkb_geometry')
		resource_name = 'getprovince'
		allowed_methods = ('get')
		filtering = { "id" : ALL }
		object_class=None

class BaselineStatisticResource(ModelResource):

	class Meta:
		# authorization = DjangoAuthorization()
		resource_name = 'statistic_baseline'
		allowed_methods = ['post']
		detail_allowed_methods = ['post']
		cache = SimpleCache()
		object_class=None
		# always_return_data = True
 
	def getRisk(self, request):
		# saving the user tracking records

		o = urlparse(request.META.get('HTTP_REFERER')).path
		o=o.split('/')
		if 'v2' in o:
			mapCode = o[3]
		else:
			mapCode = o[2]
		map_obj = _resolve_map(request, mapCode, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)

		queryset = matrix(user=request.user,resourceid=map_obj,action='Interactive Calculation')
		queryset.save()

		boundaryFilter = json.loads(request.body)

		bring = None
		temp1 = []
		for i in boundaryFilter['spatialfilter']:
			temp1.append('ST_GeomFromText(\''+i+'\',4326)')
			bring = i

		temp2 = 'ARRAY['
		first=True
		for i in temp1:
			if first:
				 temp2 = temp2 + i
				 first=False
			else :
				 temp2 = temp2 + ', ' + i  

		temp2 = temp2+']'
		
		filterLock = 'ST_Union('+temp2+')'
		yy = None
		mm = None
		dd = None

		if 'date' in boundaryFilter:
			tempDate = boundaryFilter['date'].split("-")
			dateSent = datetime.datetime(int(tempDate[0]), int(tempDate[1]), int(tempDate[2]))

			if (datetime.datetime.today() - dateSent).days == 0:
				yy = None
				mm = None
				dd = None
			else:    
				yy = tempDate[0]
				mm = tempDate[1]
				dd = tempDate[2]

		response = getBaselineStatistic(request, filterLock,boundaryFilter['flag'],boundaryFilter['code'], yy, mm, dd, boundaryFilter['rf_type'], bring)

		return response

	def post_list(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		response = self.getRisk(request)
		return self.create_response(request, response)  

	# def get_list(self, request, **kwargs):
	#     self.method_check(request, allowed=['get'])
	#     response = self.getRisk(request)
	#     return self.create_response(request, response)    

class FloodRiskStatisticResource_ORIG(ModelResource):
	"""Flood api.
	Combined from module: geodb, flood, avalanche """

	class Meta:
		# authorization = DjangoAuthorization()
		resource_name = 'floodrisk'
		allowed_methods = ['post']
		detail_allowed_methods = ['post']
		cache = SimpleCache()
		object_class=None
		# always_return_data = True
 
	def getRisk(self, request):
		# saving the user tracking records

		o = urlparse(request.META.get('HTTP_REFERER')).path
		o=o.split('/')
		if 'v2' in o:
			mapCode = o[3]
		else:
			mapCode = o[2]
		map_obj = _resolve_map(request, mapCode, 'base.view_resourcebase', _PERMISSION_MSG_VIEW)

		queryset = matrix(user=request.user,resourceid=map_obj,action='Interactive Calculation')
		queryset.save()

		boundaryFilter = json.loads(request.body)

		bring = None
		temp1 = []
		for i in boundaryFilter['spatialfilter']:
			temp1.append('ST_GeomFromText(\''+i+'\',4326)')
			bring = i

		temp2 = 'ARRAY['
		first=True
		for i in temp1:
			if first:
				 temp2 = temp2 + i
				 first=False
			else :
				 temp2 = temp2 + ', ' + i  

		temp2 = temp2+']'
		
		filterLock = 'ST_Union('+temp2+')'
		yy = None
		mm = None
		dd = None

		if 'date' in boundaryFilter:
			tempDate = boundaryFilter['date'].split("-")
			dateSent = datetime.datetime(int(tempDate[0]), int(tempDate[1]), int(tempDate[2]))

			if (datetime.datetime.today() - dateSent).days == 0:
				yy = None
				mm = None
				dd = None
			else:    
				yy = tempDate[0]
				mm = tempDate[1]
				dd = tempDate[2]

		response = getRiskExecuteExternal(filterLock,boundaryFilter['flag'],boundaryFilter['code'], yy, mm, dd, boundaryFilter['rf_type'], bring)

		return response

	def post_list(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		response = self.getRisk(request)
		return self.create_response(request, response)  

	# def get_list(self, request, **kwargs):
	#     self.method_check(request, allowed=['get'])
	#     response = self.getRisk(request)
	#     return self.create_response(request, response)    

def getBaselineStatistic(request,filterLock, flag, code, yy=None, mm=None, dd=None, rf_type=None, bring=None):

	response_dashboard_baseline = dashboard_baseline(request, filterLock, flag, code)
	response = dict_ext()
	response['source'] = response_dashboard_baseline['source']

	# response['source'] = baseline = getBaseline(request, filterLock, flag, code)
	# response['panels'] = {k:{'title':v} for k,v in PANEL_TITLES.items()}
	# for i,j in {'pop':'pop_lc','area':'area_lc','building':'building_lc'}.items():
	# 	response.path('panels',i)['child'] = [{'value':baseline[j][v], 'title':LANDCOVER_TYPES[v]} for k,v in LANDCOVER_INDEX.items()]
	# for k,v in {'pop':'pop_total','area':'area_total','building':'building_total','settlement':'settlement_total','healthfacility':'healthfacility_total','road':'road_total'}.items():
	# 	response.path('panels',k)['total'] = baseline[v]
	# response.path('panels','healthfacility')['child'] = [{'value':baseline['healthfacility'][v], 'title':HEALTHFAC_TYPES[v]} for k,v in HEALTHFAC_INDEX.items()]
	# response.path('panels','road')['child'] = [{'value':baseline['road'][v], 'title':ROAD_TYPES[v]} for k,v in ROAD_INDEX.items()]

	trans = {'pop_lc':'pop','area_lc':'area','building_lc':'building','healthfacility':'healthfacility','road':'road'}
	trans_order = ['pop_lc','area_lc','building_lc','healthfacility','road']
	response.path('panels_list')['chart'] = []
	for k in trans_order:
		p = {}
		p['child'] = [{'value':response_dashboard_baseline['panels'][k]['value'][i], 'title':t} for i,t in enumerate(response_dashboard_baseline['panels'][k]['title'])]
		p['title'] = PANEL_TITLES.get(trans.get(k))
		p['total'] = response_dashboard_baseline['panels'][k]['total']
		response['panels_list']['chart'].append(p)
	response.path('panels_list')['tables'] = [{
		'title':response_dashboard_baseline['panels'][i]['title'],
		'child':[response_dashboard_baseline['panels'][i]['parentdata']]+[j['value'] for j in response_dashboard_baseline['panels'][i]['child']]
	} for i in ['adm_lcgroup_pop_area','adm_healthfacility','adm_road']]
	for k,v in {'pop':'pop_total','area':'area_total','building':'building_total','settlement':'settlement_total','healthfacility':'healthfacility_total','road':'road_total'}.items():
		response.path('panels_list','total')[k] = response_dashboard_baseline['source'][v]
	
	return response

def getRiskExecuteExternal(filterLock, flag, code, yy=None, mm=None, dd=None, rf_type=None, bring=None):
	date_params = yy and mm and dd
	YEAR, MONTH, DAY = yy, mm, dd if date_params else datetime.datetime.utcnow().strftime("%Y %m %d").split()
	# if yy and mm and dd:
	#     date_params = True
	#     YEAR = yy
	#     MONTH = mm
	#     DAY = dd
	# else:    
	#     YEAR = datetime.datetime.utcnow().strftime("%Y")
	#     MONTH = datetime.datetime.utcnow().strftime("%m")
	#     DAY = datetime.datetime.utcnow().strftime("%d")
	
	# targetRiskIncludeWater = AfgFldzonea100KRiskLandcoverPop.objects.all()
	# targetRisk = targetRiskIncludeWater.exclude(agg_simplified_description='Water body and Marshland')
	targetBase = AfgLndcrva.objects.all()
	# targetAvalanche = AfgAvsa.objects.all()
	response_tree = dict_ext()

	if flag not in ['entireAfg','currentProvince'] or date_params:

		# #Avalanche Risk
		# counts =  getRiskNumber(targetAvalanche, filterLock, 'avalanche_cat', 'avalanche_pop', 'sum_area_sqm', 'area_buildings', flag, code, None)
		# # pop at risk level
		# temp = dict([(c['avalanche_cat'], c['count']) for c in counts])
		# response['high_ava_population']=round(temp.get('High', 0) or 0,0)
		# response['med_ava_population']=round(temp.get('Moderate', 0) or 0,0)
		# response['low_ava_population']=0
		# response['total_ava_population']=response['high_ava_population']+response['med_ava_population']+response['low_ava_population']

		# # area at risk level
		# temp = dict([(c['avalanche_cat'], c['areaatrisk']) for c in counts])
		# response['high_ava_area']=round((temp.get('High', 0) or 0)/1000000,1)
		# response['med_ava_area']=round((temp.get('Moderate', 0) or 0)/1000000,1)
		# response['low_ava_area']=0    
		# response['total_ava_area']=round(response['high_ava_area']+response['med_ava_area']+response['low_ava_area'],2) 

		# # Number of Building on Avalanche Risk
		# temp = dict([(c['avalanche_cat'], c['houseatrisk']) for c in counts])
		# response['high_ava_buildings']=temp.get('High', 0) or 0
		# response['med_ava_buildings']=temp.get('Moderate', 0) or 0
		# response['total_ava_buildings'] = response['high_ava_buildings']+response['med_ava_buildings']

		# # Flood Risk
		# counts =  getRiskNumber(targetRisk.exclude(mitigated_pop__gt=0), filterLock, 'deeperthan', 'fldarea_population', 'fldarea_sqm', 'area_buildings', flag, code, None)
		
		# # pop at risk level
		# temp = dict([(c['deeperthan'], c['count']) for c in counts])
		# response['high_risk_population']=round((temp.get('271 cm', 0) or 0),0)
		# response['med_risk_population']=round((temp.get('121 cm', 0) or 0), 0)
		# response['low_risk_population']=round((temp.get('029 cm', 0) or 0),0)
		# response['total_risk_population']=response['high_risk_population']+response['med_risk_population']+response['low_risk_population']

		# # area at risk level
		# temp = dict([(c['deeperthan'], c['areaatrisk']) for c in counts])
		# response['high_risk_area']=round((temp.get('271 cm', 0) or 0)/1000000,1)
		# response['med_risk_area']=round((temp.get('121 cm', 0) or 0)/1000000,1)
		# response['low_risk_area']=round((temp.get('029 cm', 0) or 0)/1000000,1)    
		# response['total_risk_area']=round(response['high_risk_area']+response['med_risk_area']+response['low_risk_area'],2) 

		# # buildings at flood risk
		# temp = dict([(c['deeperthan'], c['houseatrisk']) for c in counts])
		# response['total_risk_buildings'] = 0
		# response['total_risk_buildings']+=temp.get('271 cm', 0) or 0
		# response['total_risk_buildings']+=temp.get('121 cm', 0) or 0
		# response['total_risk_buildings']+=temp.get('029 cm', 0) or 0

		# counts =  getRiskNumber(targetRiskIncludeWater.exclude(mitigated_pop__gt=0), filterLock, 'agg_simplified_description', 'fldarea_population', 'fldarea_sqm', 'area_buildings', flag, code, None)

		# # landcover/pop/atrisk
		# temp = dict([(c['agg_simplified_description'], c['count']) for c in counts])
		# response['water_body_pop_risk']=round(temp.get('Water body and Marshland', 0) or 0,0)
		# response['barren_land_pop_risk']=round(temp.get('Barren land', 0) or 0,0)
		# response['built_up_pop_risk']=round(temp.get('Build Up', 0) or 0,0)
		# response['fruit_trees_pop_risk']=round(temp.get('Fruit Trees', 0) or 0,0)
		# response['irrigated_agricultural_land_pop_risk']=round(temp.get('Irrigated Agricultural Land', 0) or 0,0)
		# response['permanent_snow_pop_risk']=round(temp.get('Snow', 0) or 0,0)
		# response['rainfed_agricultural_land_pop_risk']=round(temp.get('Rainfed', 0) or 0,0)
		# response['rangeland_pop_risk']=round(temp.get('Rangeland', 0) or 0,0)
		# response['sandcover_pop_risk']=round(temp.get('Sand Covered Areas', 0) or 0,0)
		# response['vineyards_pop_risk']=round(temp.get('Vineyards', 0) or 0,0)
		# response['forest_pop_risk']=round(temp.get('Forest & Shrub', 0) or 0,0)
		# response['sand_dunes_pop_risk']=round(temp.get('Sand Dunes', 0) or 0,0)

		# temp = dict([(c['agg_simplified_description'], c['areaatrisk']) for c in counts])
		# response['water_body_area_risk']=round((temp.get('Water body and Marshland', 0) or 0)/1000000,1)
		# response['barren_land_area_risk']=round((temp.get('Barren land', 0) or 0)/1000000,1)
		# response['built_up_area_risk']=round((temp.get('Build Up', 0) or 0)/1000000,1)
		# response['fruit_trees_area_risk']=round((temp.get('Fruit Trees', 0) or 0)/1000000,1)
		# response['irrigated_agricultural_land_area_risk']=round((temp.get('Irrigated Agricultural Land', 0) or 0)/1000000,1)
		# response['permanent_snow_area_risk']=round((temp.get('Snow', 0) or 0)/1000000,1)
		# response['rainfed_agricultural_land_area_risk']=round((temp.get('Rainfed', 0) or 0)/1000000,1)
		# response['rangeland_area_risk']=round((temp.get('Rangeland', 0) or 0)/1000000,1)
		# response['sandcover_area_risk']=round((temp.get('Sand Covered Areas', 0) or 0)/1000000,1)
		# response['vineyards_area_risk']=round((temp.get('Vineyards', 0) or 0)/1000000,1)
		# response['forest_area_risk']=round((temp.get('Forest & Shrub', 0) or 0)/1000000,1)
		# response['sand_dunes_area_risk']=round((temp.get('Sand Dunes', 0) or 0)/1000000,1)

		# landcover all
		counts = getRiskNumber(targetBase, filterLock, 'agg_simplified_description', 'area_population', 'area_sqm', 'area_buildings', flag, code, None)
		sliced = {c['agg_simplified_description']: c['count'] for c in counts}
		response_tree.path('baseline')['pop_lc'] = {t:round(sliced.get(LANDCOVER_TYPES[t]) or 0, 0) for t in LANDCOVER_TYPES}
		# for lctype in LANDCOVER_TYPES:
		#     response_tree.path('baseline','pop','lc')[lctype] = round(temp.get(LANDCOVER_TYPES[lctype], 0), 0)
		# response['water_body_pop']=round(temp.get('Water body and Marshland', 0),0)
		# response['barren_land_pop']=round(temp.get('Barren land', 0),0)
		# response['built_up_pop']=round(temp.get('Build Up', 0),0)
		# response['fruit_trees_pop']=round(temp.get('Fruit Trees', 0),0)
		# response['irrigated_agricultural_land_pop']=round(temp.get('Irrigated Agricultural Land', 0),0)
		# response['permanent_snow_pop']=round(temp.get('Snow', 0),0)
		# response['rainfed_agricultural_land_pop']=round(temp.get('Rainfed', 0),0)
		# response['rangeland_pop']=round(temp.get('Rangeland', 0),0)
		# response['sandcover_pop']=round(temp.get('Sand Covered Areas', 0),0)
		# response['vineyards_pop']=round(temp.get('Vineyards', 0),0)
		# response['forest_pop']=round(temp.get('Forest & Shrub', 0),0)
		# response['sand_dunes_pop']=round(temp.get('Sand Dunes', 0),0)

		sliced = dict([(c['agg_simplified_description'], c['areaatrisk']) for c in counts])
		response_tree.path('baseline')['area_lc'] = {t:round((sliced.get(LANDCOVER_TYPES[t]) or 0)/1000000, 1) for t in LANDCOVER_TYPES}
		# for lctype in LANDCOVER_TYPES:
		#     response_tree.path('baseline','area','lc')[lctype] = round(temp.get(LANDCOVER_TYPES[lctype], 0)/1000000, 1)
		# response['water_body_area']=round(temp.get('Water body and Marshland', 0)/1000000,1)
		# response['barren_land_area']=round(temp.get('Barren land', 0)/1000000,1)
		# response['built_up_area']=round(temp.get('Build Up', 0)/1000000,1)
		# response['fruit_trees_area']=round(temp.get('Fruit Trees', 0)/1000000,1)
		# response['irrigated_agricultural_land_area']=round(temp.get('Irrigated Agricultural Land', 0)/1000000,1)
		# response['permanent_snow_area']=round(temp.get('Snow', 0)/1000000,1)
		# response['rainfed_agricultural_land_area']=round(temp.get('Rainfed', 0)/1000000,1)
		# response['rangeland_area']=round(temp.get('Rangeland', 0)/1000000,1)
		# response['sandcover_area']=round(temp.get('Sand Covered Areas', 0)/1000000,1)
		# response['vineyards_area']=round(temp.get('Vineyards', 0)/1000000,1)
		# response['forest_area']=round(temp.get('Forest & Shrub', 0)/1000000,1)
		# response['sand_dunes_area']=round(temp.get('Sand Dunes', 0)/1000000,1)

		# total buildings
		response_tree.path('baseline')['building_lc_total'] = sum([c['houseatrisk'] for c in counts])
		# temp = dict([(c['agg_simplified_description'], c['houseatrisk']) for c in counts])
		# response_tree.path('baseline','building')['total_lc'] = sum([temp.get(LANDCOVER_TYPES_INVERSE[t]) or 0 for t in LANDCOVER_TYPES])
		# response['total_buildings']+=temp.get('Water body and Marshland', 0) or 0
		# response['total_buildings']+=temp.get('Barren land', 0) or 0
		# response['total_buildings']+=temp.get('Build Up', 0) or 0
		# response['total_buildings']+=temp.get('Fruit Trees', 0) or 0
		# response['total_buildings']+=temp.get('Irrigated Agricultural Land', 0) or 0
		# response['total_buildings']+=temp.get('Snow', 0) or 0
		# response['total_buildings']+=temp.get('Rainfed', 0) or 0
		# response['total_buildings']+=temp.get('Rangeland', 0) or 0
		# response['total_buildings']+=temp.get('Sand Covered Areas', 0) or 0
		# response['total_buildings']+=temp.get('Vineyards', 0) or 0
		# response['total_buildings']+=temp.get('Forest & Shrub', 0) or 0
		# response['total_buildings']+=temp.get('Sand Dunes', 0) or 0

		# # Number settlement at risk of flood
		# if flag=='drawArea':
		#     countsBase = targetRisk.exclude(mitigated_pop__gt=0).filter(agg_simplified_description='Build Up').extra(
		#         select={
		#             'numbersettlementsatrisk': 'count(distinct vuid)'}, 
		#         where = {'st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*fldarea_sqm > 1 and ST_Intersects(wkb_geometry, '+filterLock+')'}).values('numbersettlementsatrisk')
		# elif flag=='entireAfg':
		#     countsBase = targetRisk.exclude(mitigated_pop__gt=0).filter(agg_simplified_description='Build Up').extra(
		#         select={
		#             'numbersettlementsatrisk': 'count(distinct vuid)'}).values('numbersettlementsatrisk')
		# elif flag=='currentProvince':
		#     if len(str(code)) > 2:
		#         ff0001 =  "dist_code  = '"+str(code)+"'"
		#     else :
		#         ff0001 =  "prov_code  = '"+str(code)+"'"
		#     countsBase = targetRisk.exclude(mitigated_pop__gt=0).filter(agg_simplified_description='Build Up').extra(
		#         select={
		#             'numbersettlementsatrisk': 'count(distinct vuid)'}, 
		#         where = {ff0001}).values('numbersettlementsatrisk')
		# elif flag=='currentBasin':
		#     countsBase = targetRisk.exclude(mitigated_pop__gt=0).filter(agg_simplified_description='Build Up').extra(
		#         select={
		#             'numbersettlementsatrisk': 'count(distinct vuid)'}, 
		#         where = {"vuid = '"+str(code)+"'"}).values('numbersettlementsatrisk')    
		# else:
		#     countsBase = targetRisk.exclude(mitigated_pop__gt=0).filter(agg_simplified_description='Build Up').extra(
		#         select={
		#             'numbersettlementsatrisk': 'count(distinct vuid)'}, 
		#         where = {'ST_Within(wkb_geometry, '+filterLock+')'}).values('numbersettlementsatrisk')

		# response['settlements_at_risk'] = round(countsBase[0]['numbersettlementsatrisk'],0)

		# number all settlements
		# if flag=='drawArea':
		#     countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
		#         select={
		#             'numbersettlements': 'count(distinct vuid)'}, 
		#         where = {'st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_sqm > 1 and ST_Intersects(wkb_geometry, '+filterLock+')'}).values('numbersettlements')
		# elif flag=='entireAfg':
		#     countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
		#         select={
		#             'numbersettlements': 'count(distinct vuid)'}).values('numbersettlements')
		# elif flag=='currentProvince':
		#     if len(str(code)) > 2:
		#         ff0001 =  "dist_code  = '"+str(code)+"'"
		#     else :
		#         ff0001 =  "prov_code  = '"+str(code)+"'"
		#     countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
		#         select={
		#             'numbersettlements': 'count(distinct vuid)'}, 
		#         where = {ff0001}).values('numbersettlements')
		# elif flag=='currentBasin':
		#     countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
		#         select={
		#             'numbersettlements': 'count(distinct vuid)'}, 
		#         where = {"vuid = '"+str(code)+"'"}).values('numbersettlements')   
		# else:
		#     countsBase = targetBase.exclude(agg_simplified_description='Water body and Marshland').extra(
		#         select={
		#             'numbersettlements': 'count(distinct vuid)'}, 
		#         where = {'ST_Within(wkb_geometry, '+filterLock+')'}).values('numbersettlements')
		
		# response = response_tree['baseline']['settlements']['table']
		# response['settlements'] = round(countsBase[0]['numbersettlements'],0)

		response_tree.path('baseline')['settlement_total'] = getTotalSettlement(filterLock, flag, code, targetBase)

		# All population number
		# if flag=='drawArea':
		#     countsBase = targetBase.extra(
		#         select={
		#             'countbase' : 'SUM(  \
		#                     case \
		#                         when ST_CoveredBy(wkb_geometry,'+filterLock+') then area_population \
		#                         else st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_population end \
		#                 )'
		#         },
		#         where = {
		#             'ST_Intersects(wkb_geometry, '+filterLock+')'
		#         }).values('countbase')
		# elif flag=='entireAfg':
		#     countsBase = targetBase.extra(
		#         select={
		#             'countbase' : 'SUM(area_population)'
		#         }).values('countbase')
		# elif flag=='currentProvince':
		#     if len(str(code)) > 2:
		#         ff0001 =  "dist_code  = '"+str(code)+"'"
		#     else :
		#         ff0001 =  "prov_code  = '"+str(code)+"'"
		#     countsBase = targetBase.extra(
		#         select={
		#             'countbase' : 'SUM(area_population)'
		#         },
		#         where = {
		#             ff0001
		#         }).values('countbase')
		# elif flag=='currentBasin':
		#     countsBase = targetBase.extra(
		#         select={
		#             'countbase' : 'SUM(area_population)'
		#         }, 
		#         where = {"vuid = '"+str(code)+"'"}).values('countbase')     
		# else:
		#     countsBase = targetBase.extra(
		#         select={
		#             'countbase' : 'SUM(area_population)'
		#         },
		#         where = {
		#             'ST_Within(wkb_geometry, '+filterLock+')'
		#         }).values('countbase')
					
		# response = response_tree['baseline']['pop']['table']
		# response['Population']=round(none_to_zero(countsBase)[0]['countbase'],0)

		response_tree.path('baseline')['pop_total'] = getTotalPop(filterLock, flag, code, targetBase)

		# if flag=='drawArea':
		#     countsBase = targetBase.extra(
		#         select={
		#             'areabase' : 'SUM(  \
		#                     case \
		#                         when ST_CoveredBy(wkb_geometry,'+filterLock+') then area_sqm \
		#                         else st_area(st_intersection(wkb_geometry,'+filterLock+')) / st_area(wkb_geometry)*area_sqm end \
		#                 )'
		#         },
		#         where = {
		#             'ST_Intersects(wkb_geometry, '+filterLock+')'
		#         }).values('areabase')
		# elif flag=='entireAfg':
		#     countsBase = targetBase.extra(
		#         select={
		#             'areabase' : 'SUM(area_sqm)'
		#         }).values('areabase')
		# elif flag=='currentProvince':
		#     if len(str(code)) > 2:
		#         ff0001 =  "dist_code  = '"+str(code)+"'"
		#     else :
		#         ff0001 =  "prov_code  = '"+str(code)+"'"
		#     countsBase = targetBase.extra(
		#         select={
		#             'areabase' : 'SUM(area_sqm)'
		#         },
		#         where = {
		#             ff0001
		#         }).values('areabase')
		# elif flag=='currentBasin':
		#     countsBase = targetBase.extra(
		#         select={
		#             'areabase' : 'SUM(area_sqm)'
		#         },
		#         where = {"vuid = '"+str(code)+"'"}).values('areabase')      

		# else:
		#     countsBase = targetBase.extra(
		#         select={
		#             'areabase' : 'SUM(area_sqm)'
		#         },
		#         where = {
		#             'ST_Within(wkb_geometry, '+filterLock+')'
		#         }).values('areabase')

		# response = response_tree['baseline']['area']['table']
		# response['Area']=round(none_to_zero(countsBase)[0]['areabase']/1000000,0)

		response_tree.path('baseline')['area_total'] = getTotalArea(filterLock, flag, code, targetBase)

	else:
		px = getShortCutData(flag, code)
		# if flag=='entireAfg':
		#     px = provincesummary.objects.aggregate(Sum('high_ava_population'),Sum('med_ava_population'),Sum('low_ava_population'),Sum('total_ava_population'),Sum('high_ava_area'),Sum('med_ava_area'),Sum('low_ava_area'),Sum('total_ava_area'), \
		#         Sum('high_risk_population'),Sum('med_risk_population'),Sum('low_risk_population'),Sum('total_risk_population'), Sum('high_risk_area'),Sum('med_risk_area'),Sum('low_risk_area'),Sum('total_risk_area'),  \
		#         Sum('water_body_pop_risk'),Sum('barren_land_pop_risk'),Sum('built_up_pop_risk'),Sum('fruit_trees_pop_risk'),Sum('irrigated_agricultural_land_pop_risk'),Sum('permanent_snow_pop_risk'),Sum('rainfed_agricultural_land_pop_risk'),Sum('rangeland_pop_risk'),Sum('sandcover_pop_risk'),Sum('vineyards_pop_risk'),Sum('forest_pop_risk'), Sum('sand_dunes_pop_risk'), \
		#         Sum('water_body_area_risk'),Sum('barren_land_area_risk'),Sum('built_up_area_risk'),Sum('fruit_trees_area_risk'),Sum('irrigated_agricultural_land_area_risk'),Sum('permanent_snow_area_risk'),Sum('rainfed_agricultural_land_area_risk'),Sum('rangeland_area_risk'),Sum('sandcover_area_risk'),Sum('vineyards_area_risk'),Sum('forest_area_risk'), Sum('sand_dunes_area_risk'), \
		#         Sum('water_body_pop'),Sum('barren_land_pop'),Sum('built_up_pop'),Sum('fruit_trees_pop'),Sum('irrigated_agricultural_land_pop'),Sum('permanent_snow_pop'),Sum('rainfed_agricultural_land_pop'),Sum('rangeland_pop'),Sum('sandcover_pop'),Sum('vineyards_pop'),Sum('forest_pop'), Sum('sand_dunes_pop'), \
		#         Sum('water_body_area'),Sum('barren_land_area'),Sum('built_up_area'),Sum('fruit_trees_area'),Sum('irrigated_agricultural_land_area'),Sum('permanent_snow_area'),Sum('rainfed_agricultural_land_area'),Sum('rangeland_area'),Sum('sandcover_area'),Sum('vineyards_area'),Sum('forest_area'), Sum('sand_dunes_area'), \
		#         Sum('settlements_at_risk'), Sum('settlements'), Sum('Population'), Sum('Area'), Sum('ava_forecast_low_pop'), Sum('ava_forecast_med_pop'), Sum('ava_forecast_high_pop'), Sum('total_ava_forecast_pop'),
		#         Sum('total_buildings'), Sum('total_risk_buildings'), Sum('high_ava_buildings'), Sum('med_ava_buildings'), Sum('total_ava_buildings') )
		# else:    
		#     if len(str(code)) > 2:
		#         px = districtsummary.objects.filter(district=code).aggregate(Sum('high_ava_population'),Sum('med_ava_population'),Sum('low_ava_population'),Sum('total_ava_population'),Sum('high_ava_area'),Sum('med_ava_area'),Sum('low_ava_area'),Sum('total_ava_area'), \
		#             Sum('high_risk_population'),Sum('med_risk_population'),Sum('low_risk_population'),Sum('total_risk_population'), Sum('high_risk_area'),Sum('med_risk_area'),Sum('low_risk_area'),Sum('total_risk_area'),  \
		#             Sum('water_body_pop_risk'),Sum('barren_land_pop_risk'),Sum('built_up_pop_risk'),Sum('fruit_trees_pop_risk'),Sum('irrigated_agricultural_land_pop_risk'),Sum('permanent_snow_pop_risk'),Sum('rainfed_agricultural_land_pop_risk'),Sum('rangeland_pop_risk'),Sum('sandcover_pop_risk'),Sum('vineyards_pop_risk'),Sum('forest_pop_risk'), Sum('sand_dunes_pop_risk'), \
		#             Sum('water_body_area_risk'),Sum('barren_land_area_risk'),Sum('built_up_area_risk'),Sum('fruit_trees_area_risk'),Sum('irrigated_agricultural_land_area_risk'),Sum('permanent_snow_area_risk'),Sum('rainfed_agricultural_land_area_risk'),Sum('rangeland_area_risk'),Sum('sandcover_area_risk'),Sum('vineyards_area_risk'),Sum('forest_area_risk'), Sum('sand_dunes_area_risk'), \
		#             Sum('water_body_pop'),Sum('barren_land_pop'),Sum('built_up_pop'),Sum('fruit_trees_pop'),Sum('irrigated_agricultural_land_pop'),Sum('permanent_snow_pop'),Sum('rainfed_agricultural_land_pop'),Sum('rangeland_pop'),Sum('sandcover_pop'),Sum('vineyards_pop'),Sum('forest_pop'), Sum('sand_dunes_pop'), \
		#             Sum('water_body_area'),Sum('barren_land_area'),Sum('built_up_area'),Sum('fruit_trees_area'),Sum('irrigated_agricultural_land_area'),Sum('permanent_snow_area'),Sum('rainfed_agricultural_land_area'),Sum('rangeland_area'),Sum('sandcover_area'),Sum('vineyards_area'),Sum('forest_area'), Sum('sand_dunes_area'), \
		#             Sum('settlements_at_risk'), Sum('settlements'), Sum('Population'), Sum('Area'), Sum('ava_forecast_low_pop'), Sum('ava_forecast_med_pop'), Sum('ava_forecast_high_pop'), Sum('total_ava_forecast_pop'),
		#             Sum('total_buildings'), Sum('total_risk_buildings'), Sum('high_ava_buildings'), Sum('med_ava_buildings'), Sum('total_ava_buildings') )
		#     else :
		#         px = provincesummary.objects.filter(province=code).aggregate(Sum('high_ava_population'),Sum('med_ava_population'),Sum('low_ava_population'),Sum('total_ava_population'),Sum('high_ava_area'),Sum('med_ava_area'),Sum('low_ava_area'),Sum('total_ava_area'), \
		#             Sum('high_risk_population'),Sum('med_risk_population'),Sum('low_risk_population'),Sum('total_risk_population'), Sum('high_risk_area'),Sum('med_risk_area'),Sum('low_risk_area'),Sum('total_risk_area'),  \
		#             Sum('water_body_pop_risk'),Sum('barren_land_pop_risk'),Sum('built_up_pop_risk'),Sum('fruit_trees_pop_risk'),Sum('irrigated_agricultural_land_pop_risk'),Sum('permanent_snow_pop_risk'),Sum('rainfed_agricultural_land_pop_risk'),Sum('rangeland_pop_risk'),Sum('sandcover_pop_risk'),Sum('vineyards_pop_risk'),Sum('forest_pop_risk'), Sum('sand_dunes_pop_risk'), \
		#             Sum('water_body_area_risk'),Sum('barren_land_area_risk'),Sum('built_up_area_risk'),Sum('fruit_trees_area_risk'),Sum('irrigated_agricultural_land_area_risk'),Sum('permanent_snow_area_risk'),Sum('rainfed_agricultural_land_area_risk'),Sum('rangeland_area_risk'),Sum('sandcover_area_risk'),Sum('vineyards_area_risk'),Sum('forest_area_risk'), Sum('sand_dunes_area_risk'), \
		#             Sum('water_body_pop'),Sum('barren_land_pop'),Sum('built_up_pop'),Sum('fruit_trees_pop'),Sum('irrigated_agricultural_land_pop'),Sum('permanent_snow_pop'),Sum('rainfed_agricultural_land_pop'),Sum('rangeland_pop'),Sum('sandcover_pop'),Sum('vineyards_pop'),Sum('forest_pop'), Sum('sand_dunes_pop'), \
		#             Sum('water_body_area'),Sum('barren_land_area'),Sum('built_up_area'),Sum('fruit_trees_area'),Sum('irrigated_agricultural_land_area'),Sum('permanent_snow_area'),Sum('rainfed_agricultural_land_area'),Sum('rangeland_area'),Sum('sandcover_area'),Sum('vineyards_area'),Sum('forest_area'), Sum('sand_dunes_area'), \
		#             Sum('settlements_at_risk'), Sum('settlements'), Sum('Population'), Sum('Area'), Sum('ava_forecast_low_pop'), Sum('ava_forecast_med_pop'), Sum('ava_forecast_high_pop'), Sum('total_ava_forecast_pop'),
		#             Sum('total_buildings'), Sum('total_risk_buildings'), Sum('high_ava_buildings'), Sum('med_ava_buildings'), Sum('total_ava_buildings') )
		
		response_tree = dict_ext(merge_dict(response_tree, getShortCutDataFormatter(px)))

	# # Avalanche Forecasted
	# sql = ""
	# if flag=='entireAfg':
	#     # cursor = connections['geodb'].cursor()
	#     sql = "select forcastedvalue.riskstate, \
	#         sum(afg_avsa.avalanche_pop) as pop, \
	#         sum(afg_avsa.area_buildings) as building \
	#         FROM afg_avsa \
	#         INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#         INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#         INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#         WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#         AND forcastedvalue.datadate = '%s-%s-%s' \
	#         AND forcastedvalue.forecasttype = 'snowwater' ) \
	#         GROUP BY forcastedvalue.riskstate" %(YEAR,MONTH,DAY)
	#     # cursor.execute("select forcastedvalue.riskstate, \
	#     #     sum(afg_avsa.avalanche_pop) as pop, \
	#     #     sum(afg_avsa.area_buildings) as building \
	#     #     FROM afg_avsa \
	#     #     INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#     #     INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#     #     INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#     #     WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#     #     AND forcastedvalue.datadate = '%s-%s-%s' \
	#     #     AND forcastedvalue.forecasttype = 'snowwater' ) \
	#     #     GROUP BY forcastedvalue.riskstate" %(YEAR,MONTH,DAY))  
	#     # row = cursor.fetchall()
	#     # cursor.close()
	# elif flag=='currentProvince':
	#     # cursor = connections['geodb'].cursor()
	#     if len(str(code)) > 2:
	#         ff0001 =  "dist_code  = '"+str(code)+"'"
	#     else :
	#         ff0001 =  "prov_code  = '"+str(code)+"'"

	#     sql = "select forcastedvalue.riskstate, \
	#         sum(afg_avsa.avalanche_pop) as pop, \
	#         sum(afg_avsa.area_buildings) as building \
	#         FROM afg_avsa \
	#         INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#         INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#         INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#         WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#         AND forcastedvalue.datadate = '%s-%s-%s' \
	#         AND forcastedvalue.forecasttype = 'snowwater' ) \
	#         and afg_avsa.%s \
	#         GROUP BY forcastedvalue.riskstate" %(YEAR,MONTH,DAY,ff0001)
	#     # cursor.execute("select forcastedvalue.riskstate, \
	#     #     sum(afg_avsa.avalanche_pop) as pop, \
	#     #     sum(afg_avsa.area_buildings) as building \
	#     #     FROM afg_avsa \
	#     #     INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#     #     INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#     #     INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#     #     WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#     #     AND forcastedvalue.datadate = '%s-%s-%s' \
	#     #     AND forcastedvalue.forecasttype = 'snowwater' ) \
	#     #     and afg_avsa.%s \
	#     #     GROUP BY forcastedvalue.riskstate" %(YEAR,MONTH,DAY,ff0001)) 
	#     # row = cursor.fetchall()
	#     # cursor.close()
	# elif flag=='drawArea':
	#     # cursor = connections['geodb'].cursor()
	#     sql = "select forcastedvalue.riskstate, \
	#         sum(case \
	#             when ST_CoveredBy(afg_avsa.wkb_geometry , %s) then afg_avsa.avalanche_pop \
	#             else st_area(st_intersection(afg_avsa.wkb_geometry, %s)) / st_area(afg_avsa.wkb_geometry)* avalanche_pop end \
	#         ) as pop, \
	#         sum(case \
	#             when ST_CoveredBy(afg_avsa.wkb_geometry , %s) then afg_avsa.area_buildings \
	#             else st_area(st_intersection(afg_avsa.wkb_geometry, %s)) / st_area(afg_avsa.wkb_geometry)* area_buildings end \
	#         ) as building \
	#         FROM afg_avsa \
	#         INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#         INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#         INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#         WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#         AND forcastedvalue.datadate = '%s-%s-%s' \
	#         AND forcastedvalue.forecasttype = 'snowwater' ) \
	#         GROUP BY forcastedvalue.riskstate" %(filterLock,filterLock, filterLock,filterLock,YEAR,MONTH,DAY)
	#     # cursor.execute("select forcastedvalue.riskstate, \
	#     #     sum(case \
	#     #         when ST_CoveredBy(afg_avsa.wkb_geometry , %s) then afg_avsa.avalanche_pop \
	#     #         else st_area(st_intersection(afg_avsa.wkb_geometry, %s)) / st_area(afg_avsa.wkb_geometry)* avalanche_pop end \
	#     #     ) as pop, \
	#     #     sum(case \
	#     #         when ST_CoveredBy(afg_avsa.wkb_geometry , %s) then afg_avsa.area_buildings \
	#     #         else st_area(st_intersection(afg_avsa.wkb_geometry, %s)) / st_area(afg_avsa.wkb_geometry)* area_buildings end \
	#     #     ) as building \
	#     #     FROM afg_avsa \
	#     #     INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#     #     INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#     #     INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#     #     WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#     #     AND forcastedvalue.datadate = '%s-%s-%s' \
	#     #     AND forcastedvalue.forecasttype = 'snowwater' ) \
	#     #     GROUP BY forcastedvalue.riskstate" %(filterLock,filterLock,YEAR,MONTH,DAY)) 
	#     # row = cursor.fetchall()
	#     # cursor.close()
	# else:
	#     # cursor = connections['geodb'].cursor()
	#     sql = "select forcastedvalue.riskstate, \
	#         sum(afg_avsa.avalanche_pop) as pop, \
	#         sum(afg_avsa.area_buildings) as building \
	#         FROM afg_avsa \
	#         INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#         INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#         INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#         WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#         AND forcastedvalue.datadate = '%s-%s-%s' \
	#         AND forcastedvalue.forecasttype = 'snowwater' ) \
	#         AND ST_Within(afg_avsa.wkb_geometry, %s) \
	#         GROUP BY forcastedvalue.riskstate" %(YEAR,MONTH,DAY,filterLock)
	#     # cursor.execute("select forcastedvalue.riskstate, \
	#     #     sum(afg_avsa.avalanche_pop) as pop, \
	#     #     sum(afg_avsa.area_buildings) as building \
	#     #     FROM afg_avsa \
	#     #     INNER JOIN current_sc_basins ON (ST_WITHIN(ST_Centroid(afg_avsa.wkb_geometry), current_sc_basins.wkb_geometry)) \
	#     #     INNER JOIN afg_sheda_lvl4 ON ( afg_avsa.basinmember_id = afg_sheda_lvl4.ogc_fid ) \
	#     #     INNER JOIN forcastedvalue ON ( afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id ) \
	#     #     WHERE (NOT (afg_avsa.basinmember_id IN (SELECT U1.ogc_fid FROM afg_sheda_lvl4 U1 LEFT OUTER JOIN forcastedvalue U2 ON ( U1.ogc_fid = U2.basin_id ) WHERE U2.riskstate IS NULL)) \
	#     #     AND forcastedvalue.datadate = '%s-%s-%s' \
	#     #     AND forcastedvalue.forecasttype = 'snowwater' ) \
	#     #     AND ST_Within(afg_avsa.wkb_geometry, %s) \
	#     #     GROUP BY forcastedvalue.riskstate" %(YEAR,MONTH,DAY,filterLock))  
	#     # row = cursor.fetchall()
	#     # cursor.close()    
	# cursor = connections['geodb'].cursor()
	# row = query_to_dicts(cursor, sql)
	# counts = []
	# for i in row:
	#     counts.append(i)
	# cursor.close()

	# temp = dict([(c['riskstate'], c['pop']) for c in counts])
	# # response['ava_forecast_low_pop']=round(dict(row).get(1, 0) or 0,0) 
	# # response['ava_forecast_med_pop']=round(dict(row).get(2, 0) or 0,0) 
	# # response['ava_forecast_high_pop']=round(dict(row).get(3, 0) or 0,0) 
	# response['ava_forecast_low_pop']=round(temp.get(1, 0) or 0,0) 
	# response['ava_forecast_med_pop']=round(temp.get(2, 0) or 0,0) 
	# response['ava_forecast_high_pop']=round(temp.get(3, 0) or 0,0) 
	# response['total_ava_forecast_pop']=response['ava_forecast_low_pop'] + response['ava_forecast_med_pop'] + response['ava_forecast_high_pop']

	# # avalanche forecast buildings
	# temp = dict([(c['riskstate'], c['building']) for c in counts])
	# # response['ava_forecast_low_buildings']=round(dict(row).get(1, 0) or 0,0) 
	# # response['ava_forecast_med_buildings']=round(dict(row).get(2, 0) or 0,0) 
	# # response['ava_forecast_high_buildings']=round(dict(row).get(3, 0) or 0,0)
	# response['ava_forecast_low_buildings']=round(temp.get(1, 0) or 0,0) 
	# response['ava_forecast_med_buildings']=round(temp.get(2, 0) or 0,0) 
	# response['ava_forecast_high_buildings']=round(temp.get(3, 0) or 0,0) 
	# response['total_ava_forecast_buildings']=response['ava_forecast_low_buildings'] + response['ava_forecast_med_buildings'] + response['ava_forecast_high_buildings']


	# counts =  getRiskNumber(targetRisk.exclude(mitigated_pop=0), filterLock, 'deeperthan', 'mitigated_pop', 'fldarea_sqm', 'area_buildings', flag, code, None)
	# temp = dict([(c['deeperthan'], c['count']) for c in counts])
	# response['high_risk_mitigated_population']=round(temp.get('271 cm', 0) or 0,0)
	# response['med_risk_mitigated_population']=round(temp.get('121 cm', 0) or 0, 0)
	# response['low_risk_mitigated_population']=round(temp.get('029 cm', 0) or 0,0)
	# response['total_risk_mitigated_population']=response['high_risk_mitigated_population']+response['med_risk_mitigated_population']+response['low_risk_mitigated_population']


	# # River Flood Forecasted
	# if rf_type == 'GFMS only':
	#     bring = filterLock    
	# temp_result = getFloodForecastBySource(rf_type, targetRisk, bring, flag, code, YEAR, MONTH, DAY)
	# for item in temp_result:
	#     response[item]=temp_result[item]


	# # Flash Flood Forecasted
	# # AfgFldzonea100KRiskLandcoverPop.objects.all().select_related("basinmembers").values_list("agg_simplified_description","basinmember__basins__riskstate")
	# counts =  getRiskNumber(targetRisk.exclude(mitigated_pop__gt=0).select_related("basinmembers").defer('basinmember__wkb_geometry').exclude(basinmember__basins__riskstate=None).filter(basinmember__basins__forecasttype='flashflood',basinmember__basins__datadate='%s-%s-%s' %(YEAR,MONTH,DAY)), filterLock, 'basinmember__basins__riskstate', 'fldarea_population', 'fldarea_sqm', 'area_buildings', flag, code, 'afg_fldzonea_100k_risk_landcover_pop')
	
	# temp = dict([(c['basinmember__basins__riskstate'], c['count']) for c in counts])
	# response['flashflood_forecast_verylow_pop']=round(temp.get(1, 0) or 0,0) 
	# response['flashflood_forecast_low_pop']=round(temp.get(2, 0) or 0,0) 
	# response['flashflood_forecast_med_pop']=round(temp.get(3, 0) or 0,0) 
	# response['flashflood_forecast_high_pop']=round(temp.get(4, 0) or 0,0) 
	# response['flashflood_forecast_veryhigh_pop']=round(temp.get(5, 0) or 0,0) 
	# response['flashflood_forecast_extreme_pop']=round(temp.get(6, 0) or 0,0) 
	# response['total_flashflood_forecast_pop']=response['flashflood_forecast_verylow_pop'] + response['flashflood_forecast_low_pop'] + response['flashflood_forecast_med_pop'] + response['flashflood_forecast_high_pop'] + response['flashflood_forecast_veryhigh_pop'] + response['flashflood_forecast_extreme_pop']

	# temp = dict([(c['basinmember__basins__riskstate'], c['areaatrisk']) for c in counts])
	# response['flashflood_forecast_verylow_area']=round((temp.get(1, 0) or 0)/1000000,0) 
	# response['flashflood_forecast_low_area']=round((temp.get(2, 0) or 0)/1000000,0) 
	# response['flashflood_forecast_med_area']=round((temp.get(3, 0) or 0)/1000000,0) 
	# response['flashflood_forecast_high_area']=round((temp.get(4, 0) or 0)/1000000,0) 
	# response['flashflood_forecast_veryhigh_area']=round((temp.get(5, 0) or 0)/1000000,0) 
	# response['flashflood_forecast_extreme_area']=round((temp.get(6, 0) or 0)/1000000,0) 
	# response['total_flashflood_forecast_area']=response['flashflood_forecast_verylow_area'] + response['flashflood_forecast_low_area'] + response['flashflood_forecast_med_area'] + response['flashflood_forecast_high_area'] + response['flashflood_forecast_veryhigh_area'] + response['flashflood_forecast_extreme_area']

	# # number of building on flahsflood forecasted
	# temp = dict([(c['basinmember__basins__riskstate'], c['houseatrisk']) for c in counts])
	# response['flashflood_forecast_verylow_buildings']=round(temp.get(1, 0) or 0,0) 
	# response['flashflood_forecast_low_buildings']=round(temp.get(2, 0) or 0,0) 
	# response['flashflood_forecast_med_buildings']=round(temp.get(3, 0) or 0,0) 
	# response['flashflood_forecast_high_buildings']=round(temp.get(4, 0) or 0,0) 
	# response['flashflood_forecast_veryhigh_buildings']=round(temp.get(5, 0) or 0,0) 
	# response['flashflood_forecast_extreme_buildings']=round(temp.get(6, 0) or 0,0) 
	# response['total_flashflood_forecast_buildings']=response['flashflood_forecast_verylow_buildings'] + response['flashflood_forecast_low_buildings'] + response['flashflood_forecast_med_buildings'] + response['flashflood_forecast_high_buildings'] + response['flashflood_forecast_veryhigh_buildings'] + response['flashflood_forecast_extreme_buildings']


	# response['total_flood_forecast_pop'] = response['total_riverflood_forecast_pop'] + response['total_flashflood_forecast_pop']
	# response['total_flood_forecast_area'] = response['total_riverflood_forecast_area'] + response['total_flashflood_forecast_area']

	response_tree = none_to_zero(response_tree)

	# # flood risk and flashflood forecast matrix
	# px = targetRisk.exclude(mitigated_pop__gt=0).select_related("basinmembers").defer('basinmember__wkb_geometry').exclude(basinmember__basins__riskstate=None).filter(basinmember__basins__forecasttype='flashflood',basinmember__basins__datadate='%s-%s-%s' %(YEAR,MONTH,DAY))
	# # px = px.values('basinmember__basins__riskstate','deeperthan').annotate(counter=Count('ogc_fid')).extra(
	# #     select={
	# #         'pop' : 'SUM(fldarea_population)'
	# #     }).values('basinmember__basins__riskstate','deeperthan', 'pop') 
	# if flag=='entireAfg': 
	#     px = px.\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(pop=Sum('fldarea_population')).\
	#         annotate(building=Sum('area_buildings')).\
	#         values('basinmember__basins__riskstate','deeperthan', 'pop', 'building')
	# elif flag=='currentProvince':
	#     if len(str(code)) > 2:
	#         ff0001 =  "dist_code  = '"+str(code)+"'"
	#     else :
	#         if len(str(code))==1:
	#             ff0001 =  "left(cast(dist_code as text),1)  = '"+str(code)+"'"
	#         else:
	#             ff0001 =  "left(cast(dist_code as text),2)  = '"+str(code)+"'"   
	#     px = px.\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(pop=Sum('fldarea_population')).\
	#         annotate(building=Sum('area_buildings')).\
	#         extra(
	#             where={
	#                 ff0001
	#             }).\
	#         values('basinmember__basins__riskstate','deeperthan', 'pop', 'building')
	# elif flag=='drawArea':
	#     px = px.\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(pop=RawSQL_nogroupby('SUM(  \
	#                         case \
	#                             when ST_CoveredBy(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry ,'+filterLock+') then fldarea_population \
	#                             else st_area(st_intersection(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry,'+filterLock+')) / st_area(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry)* fldarea_population end \
	#                     )')).\
	#         annotate(building=RawSQL_nogroupby('SUM(  \
	#                         case \
	#                             when ST_CoveredBy(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry ,'+filterLock+') then area_buildings \
	#                             else st_area(st_intersection(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry,'+filterLock+')) / st_area(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry)* area_buildings end \
	#                     )')).\
	#         extra(
	#             where = {
	#                 'ST_Intersects(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry, '+filterLock+')'
	#             }).\
	#         values('basinmember__basins__riskstate','deeperthan', 'pop', 'building')  
	# else:
	#     px = px.\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(pop=Sum('fldarea_population')).\
	#         annotate(building=Sum('area_buildings')).\
	#         extra(
	#             where = {
	#                 'ST_Within(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry, '+filterLock+')'
	#             }).\
	#         values('basinmember__basins__riskstate','deeperthan', 'pop', 'building')     

	# px = none_to_zero(px)

	# tempD = [ num for num in px if num['basinmember__basins__riskstate'] == 1 ]
	# temp = dict([(c['deeperthan'], c['pop']) for c in tempD])
	# response['flashflood_forecast_verylow_risk_low_pop']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_verylow_risk_med_pop']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_verylow_risk_high_pop']=round(temp.get('271 cm', 0) or 0,0)
	# temp = dict([(c['deeperthan'], c['building']) for c in tempD])
	# response['flashflood_forecast_verylow_risk_low_buildings']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_verylow_risk_med_buildings']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_verylow_risk_high_buildings']=round(temp.get('271 cm', 0) or 0,0)

	# tempD = [ num for num in px if num['basinmember__basins__riskstate'] == 2 ]
	# temp = dict([(c['deeperthan'], c['pop']) for c in tempD])
	# response['flashflood_forecast_low_risk_low_pop']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_low_risk_med_pop']=round(temp.get('121 cm', 0) or 0, 0) 
	# response['flashflood_forecast_low_risk_high_pop']=round(temp.get('271 cm', 0) or 0,0)
	# temp = dict([(c['deeperthan'], c['building']) for c in tempD])
	# response['flashflood_forecast_low_risk_low_buildings']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_low_risk_med_buildings']=round(temp.get('121 cm', 0) or 0, 0) 
	# response['flashflood_forecast_low_risk_high_buildings']=round(temp.get('271 cm', 0) or 0,0)

	# tempD = [ num for num in px if num['basinmember__basins__riskstate'] == 3 ]
	# temp = dict([(c['deeperthan'], c['pop']) for c in tempD])
	# response['flashflood_forecast_med_risk_low_pop']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_med_risk_med_pop']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_med_risk_high_pop']=round(temp.get('271 cm', 0) or 0,0) 
	# temp = dict([(c['deeperthan'], c['building']) for c in tempD])
	# response['flashflood_forecast_med_risk_low_buildings']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_med_risk_med_buildings']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_med_risk_high_buildings']=round(temp.get('271 cm', 0) or 0,0)

	# tempD = [ num for num in px if num['basinmember__basins__riskstate'] == 4 ]
	# temp = dict([(c['deeperthan'], c['pop']) for c in tempD])
	# response['flashflood_forecast_high_risk_low_pop']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_high_risk_med_pop']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_high_risk_high_pop']=round(temp.get('271 cm', 0) or 0,0)
	# temp = dict([(c['deeperthan'], c['building']) for c in tempD])
	# response['flashflood_forecast_high_risk_low_buildings']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_high_risk_med_buildings']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_high_risk_high_buildings']=round(temp.get('271 cm', 0) or 0,0)

	# tempD = [ num for num in px if num['basinmember__basins__riskstate'] == 5 ]
	# temp = dict([(c['deeperthan'], c['pop']) for c in tempD])
	# response['flashflood_forecast_veryhigh_risk_low_pop']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_veryhigh_risk_med_pop']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_veryhigh_risk_high_pop']=round(temp.get('271 cm', 0) or 0,0)
	# temp = dict([(c['deeperthan'], c['building']) for c in tempD])
	# response['flashflood_forecast_veryhigh_risk_low_buildings']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_veryhigh_risk_med_buildings']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_veryhigh_risk_high_buildings']=round(temp.get('271 cm', 0) or 0,0)

	# tempD = [ num for num in px if num['basinmember__basins__riskstate'] == 6 ]
	# temp = dict([(c['deeperthan'], c['pop']) for c in tempD])
	# response['flashflood_forecast_extreme_risk_low_pop']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_extreme_risk_med_pop']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_extreme_risk_high_pop']=round(temp.get('271 cm', 0) or 0,0)
	# temp = dict([(c['deeperthan'], c['building']) for c in tempD])
	# response['flashflood_forecast_extreme_risk_low_buildings']=round(temp.get('029 cm', 0) or 0,0)
	# response['flashflood_forecast_extreme_risk_med_buildings']=round(temp.get('121 cm', 0) or 0, 0)
	# response['flashflood_forecast_extreme_risk_high_buildings']=round(temp.get('271 cm', 0) or 0,0)
	

	# try:
	#     response['percent_total_risk_population'] = round((response['total_risk_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_total_risk_population'] = 0
		
	# try:
	#     response['percent_high_risk_population'] = round((response['high_risk_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_high_risk_population'] = 0

	# try:
	#     response['percent_med_risk_population'] = round((response['med_risk_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_med_risk_population'] = 0

	# try:
	#     response['percent_low_risk_population'] = round((response['low_risk_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_low_risk_population'] = 0

	# try:
	#     response['percent_total_risk_area'] = round((response['total_risk_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_total_risk_area'] = 0

	# try:
	#     response['percent_high_risk_area'] = round((response['high_risk_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_high_risk_area'] = 0

	# try:
	#     response['percent_med_risk_area'] = round((response['med_risk_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_med_risk_area'] = 0
	
	# try:
	#     response['percent_low_risk_area'] = round((response['low_risk_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_low_risk_area'] = 0

	# try:
	#     response['percent_total_ava_population'] = round((response['total_ava_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_total_ava_population'] = 0
	
	# try:
	#     response['percent_high_ava_population'] = round((response['high_ava_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_high_ava_population'] = 0    
	
	# try:
	#     response['percent_med_ava_population'] = round((response['med_ava_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_med_ava_population'] = 0

	# try:
	#     response['percent_low_ava_population'] = round((response['low_ava_population']/response['Population'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_low_ava_population'] = 0

	# try:
	#     response['percent_total_ava_area'] = round((response['total_ava_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_total_ava_area'] = 0

	# try:
	#     response['percent_high_ava_area'] = round((response['high_ava_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_high_ava_area'] = 0

	# try:
	#     response['percent_med_ava_area'] = round((response['med_ava_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_med_ava_area'] = 0
	# try:
	#     response['percent_low_ava_area'] = round((response['low_ava_area']/response['Area'])*100,0)
	# except ZeroDivisionError:
	#     response['percent_low_ava_area'] = 0    

	# # Population percentage
	# try:
	#     response['precent_barren_land_pop_risk'] = round((response['barren_land_pop_risk']/response['barren_land_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_barren_land_pop_risk'] = 0
	# try:
	#     response['precent_built_up_pop_risk'] = round((response['built_up_pop_risk']/response['built_up_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_built_up_pop_risk'] = 0       
	# try:
	#     response['precent_fruit_trees_pop_risk'] = round((response['fruit_trees_pop_risk']/response['fruit_trees_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_fruit_trees_pop_risk'] = 0
	# try:
	#     response['precent_irrigated_agricultural_land_pop_risk'] = round((response['irrigated_agricultural_land_pop_risk']/response['irrigated_agricultural_land_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_irrigated_agricultural_land_pop_risk'] = 0     
	# try:
	#     response['precent_permanent_snow_pop_risk'] = round((response['permanent_snow_pop_risk']/response['permanent_snow_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_permanent_snow_pop_risk'] = 0 
	# try:
	#     response['precent_rainfed_agricultural_land_pop_risk'] = round((response['rainfed_agricultural_land_pop_risk']/response['rainfed_agricultural_land_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_rainfed_agricultural_land_pop_risk'] = 0  
	# try:
	#     response['precent_rangeland_pop_risk'] = round((response['rangeland_pop_risk']/response['rangeland_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_rangeland_pop_risk'] = 0  
	# try:
	#     response['precent_sandcover_pop_risk'] = round((response['sandcover_pop_risk']/response['sandcover_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_sandcover_pop_risk'] = 0  
	# try:
	#     response['precent_vineyards_pop_risk'] = round((response['vineyards_pop_risk']/response['vineyards_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_vineyards_pop_risk'] = 0  
	# try:
	#     response['precent_water_body_pop_risk'] = round((response['water_body_pop_risk']/response['water_body_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_water_body_pop_risk'] = 0     
	# try:
	#     response['precent_forest_pop_risk'] = round((response['forest_pop_risk']/response['forest_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_forest_pop_risk'] = 0    
	# try:
	#     response['precent_sand_dunes_pop_risk'] = round((response['sand_dunes_pop_risk']/response['sand_dunes_pop'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_sand_dunes_pop_risk'] = 0                          


	# # Area percentage
	# try:
	#     response['precent_barren_land_area_risk'] = round((response['barren_land_area_risk']/response['barren_land_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_barren_land_area_risk'] = 0
	# try:        
	#     response['precent_built_up_area_risk'] = round((response['built_up_area_risk']/response['built_up_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_built_up_area_risk'] = 0    
	# try:
	#     response['precent_fruit_trees_area_risk'] = round((response['fruit_trees_area_risk']/response['fruit_trees_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_fruit_trees_area_risk'] = 0        
	# try:
	#     response['precent_irrigated_agricultural_land_area_risk'] = round((response['irrigated_agricultural_land_area_risk']/response['irrigated_agricultural_land_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_irrigated_agricultural_land_area_risk'] = 0 
	# try:
	#     response['precent_permanent_snow_area_risk'] = round((response['permanent_snow_area_risk']/response['permanent_snow_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_permanent_snow_area_risk'] = 0 
	# try:
	#     response['precent_rainfed_agricultural_land_area_risk'] = round((response['rainfed_agricultural_land_area_risk']/response['rainfed_agricultural_land_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_rainfed_agricultural_land_area_risk'] = 0  
	# try:
	#     response['precent_rangeland_area_risk'] = round((response['rangeland_area_risk']/response['rangeland_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_rangeland_area_risk'] = 0  
	# try:
	#     response['precent_sandcover_area_risk'] = round((response['sandcover_area_risk']/response['sandcover_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_sandcover_area_risk'] = 0  
	# try:
	#     response['precent_vineyards_area_risk'] = round((response['vineyards_area_risk']/response['vineyards_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_vineyards_area_risk'] = 0  
	# try:
	#     response['precent_water_body_area_risk'] = round((response['water_body_area_risk']/response['water_body_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_water_body_area_risk'] = 0     
	# try:
	#     response['precent_forest_area_risk'] = round((response['forest_area_risk']/response['forest_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_forest_area_risk'] = 0 
	# try:
	#     response['precent_sand_dunes_area_risk'] = round((response['sand_dunes_area_risk']/response['sand_dunes_area'])*100,0)
	# except ZeroDivisionError:
	#     response['precent_sand_dunes_area_risk'] = 0 

	# # Roads 
	# if flag=='drawArea':
	#     countsRoadBase = AfgRdsl.objects.all().\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length=RawSQL_nogroupby('SUM(  \
	#                     case \
	#                         when ST_CoveredBy(wkb_geometry'+','+filterLock+') then road_length \
	#                         else ST_Length(st_intersection(wkb_geometry::geography'+','+filterLock+')) / road_length end \
	#                 )/1000',())).\
	#         extra(
	#         where = {
	#             'ST_Intersects(wkb_geometry'+', '+filterLock+')'
	#         }).\
	#         values('type_update','road_length') 

	#     countsHLTBase = AfgHltfac.objects.all().filter(activestatus='Y').\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(numberhospital=Count('ogc_fid')).\
	#         extra(
	#             where = {
	#                 'ST_Intersects(wkb_geometry'+', '+filterLock+')'
	#             }).\
	#         values('facility_types_description', 'numberhospital')

	# elif flag=='entireAfg':    
	#     # countsRoadBase = AfgRdsl.objects.all().values('type_update').annotate(counter=Count('ogc_fid')).extra(
	#     #         select={
	#     #             'road_length' : 'SUM(road_length)/1000'
	#     #         }).values('type_update', 'road_length')
	#     countsRoadBase = AfgRdsl.objects.all().\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length__sum=Sum('road_length')/1000).\
	#         values('type_update', 'road_length__sum')

	#     # Health Facilities
	#     # countsHLTBase = AfgHltfac.objects.all().filter(activestatus='Y').values('facility_types_description').annotate(counter=Count('ogc_fid')).extra(
	#     #         select={
	#     #             'numberhospital' : 'count(*)'
	#     #         }).values('facility_types_description', 'numberhospital')
	#     countsHLTBase = AfgHltfac.objects.all().filter(activestatus='Y').\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(numberhospital=Count('ogc_fid')).\
	#         values('facility_types_description', 'numberhospital')
		
	# elif flag=='currentProvince':
	#     if len(str(code)) > 2:
	#         ff0001 =  "dist_code  = '"+str(code)+"'"
	#     else :
	#         if len(str(code))==1:
	#             ff0001 =  "left(cast(dist_code as text),1)  = '"+str(code)+"'"
	#         else:
	#             ff0001 =  "left(cast(dist_code as text),2)  = '"+str(code)+"'"    
				
	#     countsRoadBase = AfgRdsl.objects.all().\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length__sum=Sum('road_length')/1000).\
	#         extra(
	#             where = {
	#                 ff0001
	#             }).\
	#         values('type_update','road_length__sum') 

	#     countsHLTBase = AfgHltfac.objects.all().filter(activestatus='Y').\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(numberhospital=Count('ogc_fid')).\
	#         extra(
	#             where = {
	#                 ff0001
	#             }).\
	#         values('facility_types_description', 'numberhospital')

	# elif flag=='currentBasin':
	#     print 'currentBasin'
	# else:
	#     countsRoadBase = AfgRdsl.objects.all().\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(road_length__sum=Sum('road_length')/1000).\
	#         extra(
	#             where = {
	#                 'ST_Within(wkb_geometry'+', '+filterLock+')'
	#             }).\
	#         values('type_update','road_length__sum') 

	#     countsHLTBase = AfgHltfac.objects.all().filter(activestatus='Y').\
	#         annotate(counter=Count('ogc_fid')).\
	#         annotate(numberhospital=Count('ogc_fid')).\
	#         extra(
	#             where = {
	#                 'ST_Within(wkb_geometry'+', '+filterLock+')'
	#             }).\
	#         values('facility_types_description', 'numberhospital')


	# tempRoadBase = dict([(c['type_update'], c['road_length__sum']) for c in countsRoadBase])
	# tempHLTBase = dict([(c['facility_types_description'], c['numberhospital']) for c in countsHLTBase])

	roadParentData = getParentRoadNetworkRecap(filterLock, flag, code)
	sliced = {['type_update']: c['road_length__sum'] for c in roadParentData}
	response_tree.path('baseline')['road'] = {t:round(sliced.get(ROAD_TYPES[t]) or 0) for t in ROAD_TYPES}
	response_tree.path('baseline')['road_total'] = sum(response_tree.path('baseline')['road'].values())

	# response["highway_road_base"]=round(tempRoadBase.get("highway", 0),1)
	# response["primary_road_base"]=round(tempRoadBase.get("primary", 0),1)
	# response["secondary_road_base"]=round(tempRoadBase.get("secondary", 0),1)
	# response["tertiary_road_base"]=round(tempRoadBase.get("tertiary", 0),1)
	# response["residential_road_base"]=round(tempRoadBase.get("residential", 0),1)
	# response["track_road_base"]=round(tempRoadBase.get("track", 0),1)
	# response["path_road_base"]=round(tempRoadBase.get("path", 0),1)
	# response["river_crossing_road_base"]=round(tempRoadBase.get("river crossing", 0),1)
	# response["bridge_road_base"]=round(tempRoadBase.get("bridge", 0),1)
	# response["total_road_base"]=response["highway_road_base"]+response["primary_road_base"]+response["secondary_road_base"]+response["tertiary_road_base"]+response["residential_road_base"]+response["track_road_base"]+response["path_road_base"]+response["river_crossing_road_base"]+response["bridge_road_base"]

	hltParentData = getParentHltFacRecap(filterLock, flag, code)
	sliced = {c['facility_types_description']: c['numberhospital'] for c in hltParentData}
	response_tree.path('baseline')['healthfacility'] = {t:round(sliced.get(HEALTHFAC_TYPES[t]) or 0) for t in HEALTHFAC_TYPES}
	response_tree.path('baseline')['healthfacility_total'] = sum(response_tree.path('baseline')['healthfacility'].values())
	# response = response_tree.path('baseline','healthfacility')
	# for hftype in HEALTHFAC_TYPES:
	#     response.path('table')[hftype] = round(tempHLTBase.get(HEALTHFAC_TYPES[hftype], 0))
	# response['total'] = sum(response['table'].values())
	
	# response["h1_health_base"]=round(tempHLTBase.get("Regional / National Hospital (H1)", 0))
	# response["h2_health_base"]=round(tempHLTBase.get("Provincial Hospital (H2)", 0))    
	# response["h3_health_base"]=round(tempHLTBase.get("District Hospital (H3)", 0))
	# response["sh_health_base"]=round(tempHLTBase.get("Special Hospital (SH)", 0))
	# response["rh_health_base"]=round(tempHLTBase.get("Rehabilitation Center (RH)", 0))               
	# response["mh_health_base"]=round(tempHLTBase.get("Maternity Home (MH)", 0))
	# response["datc_health_base"]=round(tempHLTBase.get("Drug Addicted Treatment Center", 0))
	# response["tbc_health_base"]=round(tempHLTBase.get("TB Control Center (TBC)", 0))
	# response["mntc_health_base"]=round(tempHLTBase.get("Mental Clinic / Hospital", 0))
	# response["chc_health_base"]=round(tempHLTBase.get("Comprehensive Health Center (CHC)", 0))
	# response["bhc_health_base"]=round(tempHLTBase.get("Basic Health Center (BHC)", 0))
	# response["dcf_health_base"]=round(tempHLTBase.get("Day Care Feeding", 0))
	# response["mch_health_base"]=round(tempHLTBase.get("MCH Clinic M1 or M2 (MCH)", 0))
	# response["shc_health_base"]=round(tempHLTBase.get("Sub Health Center (SHC)", 0))
	# response["ec_health_base"]=round(tempHLTBase.get("Eye Clinic / Hospital", 0))
	# response["pyc_health_base"]=round(tempHLTBase.get("Physiotherapy Center", 0))
	# response["pic_health_base"]=round(tempHLTBase.get("Private Clinic", 0))        
	# response["mc_health_base"]=round(tempHLTBase.get("Malaria Center (MC)", 0))
	# response["moph_health_base"]=round(tempHLTBase.get("MoPH National", 0))
	# response["epi_health_base"]=round(tempHLTBase.get("EPI Fixed Center (EPI)", 0))
	# response["sfc_health_base"]=round(tempHLTBase.get("Supplementary Feeding Center (SFC)", 0))
	# response["mht_health_base"]=round(tempHLTBase.get("Mobile Health Team (MHT)", 0))
	# response["other_health_base"]=round(tempHLTBase.get("Other", 0))
	# response["total_health_base"] = response["bhc_health_base"]+response["dcf_health_base"]+response["mch_health_base"]+response["rh_health_base"]+response["h3_health_base"]+response["sh_health_base"]+response["mh_health_base"]+response["datc_health_base"]+response["h1_health_base"]+response["shc_health_base"]+response["ec_health_base"]+response["pyc_health_base"]+response["pic_health_base"]+response["tbc_health_base"]+response["mntc_health_base"]+response["chc_health_base"]+response["other_health_base"]+response["h2_health_base"]+response["mc_health_base"]+response["moph_health_base"]+response["epi_health_base"]+response["sfc_health_base"]+response["mht_health_base"]
	
	# try:
	#     rf = forecastedLastUpdate.objects.filter(forecasttype='riverflood').latest('datadate')
	# except forecastedLastUpdate.DoesNotExist:
	#     response["riverflood_lastupdated"] = None
	# else:
	#     tempRF = rf.datadate + datetime.timedelta(hours=4.5)
	#     response["riverflood_lastupdated"] = timeago.format(tempRF, datetime.datetime.utcnow()+ datetime.timedelta(hours=4.5))  #tempRF.strftime("%d-%m-%Y %H:%M")

	# try:
	#     sw = forecastedLastUpdate.objects.filter(forecasttype='snowwater').latest('datadate')
	# except forecastedLastUpdate.DoesNotExist:
	#     response["snowwater_lastupdated"] = None
	# else:
	#     tempSW = sw.datadate + datetime.timedelta(hours=4.5)
	#     response["snowwater_lastupdated"] =  timeago.format(tempSW, datetime.datetime.utcnow()+ datetime.timedelta(hours=4.5))   #tempSW.strftime("%d-%m-%Y %H:%M")

	# # print rf.datadate
	# tz = timezone('Asia/Kabul')
	# stdSC = datetime.datetime.utcnow()
	# stdSC = stdSC.replace(hour=3, minute=00, second=00)

	# tempSC = datetime.datetime.utcnow()

	# if stdSC > tempSC:
	#     tempSC = tempSC - datetime.timedelta(days=1)
	
	# tempSC = tempSC.replace(hour=3, minute=00, second=00)
	# tempSC = tempSC + datetime.timedelta(hours=4.5)
	# # tempSC = tempSC.replace(tzinfo=tz) 
	# print tempSC
	# response["glofas_lastupdated"] = timeago.format(tempSC, datetime.datetime.utcnow()+ datetime.timedelta(hours=4.5))     #tempSC.strftime("%d-%m-%Y %H:%M")
	
	# add response from optional modules
	for modulename in settings.GETRISKEXECUTEEXTERNAL_MODULES:
		module = importlib.import_module(modulename+'.views')
		response_add = module.getRiskExecuteExternal(filterLock, flag, code, yy, mm, dd, rf_type, bring, init_response=response_tree)
		response_tree = merge_dict(response_tree, response_add)

	return response_tree

class getVillages(ModelResource):
	"""villages api"""

	class Meta:
		authorization = DjangoAuthorization()
		resource_name = 'get_villages'
		allowed_methods = ['get']
		detail_allowed_methods = ['get']
		always_return_data = True
		object_class=None

	def get_list(self, request, **kwargs):
		self.method_check(request, allowed=['get'])

		if request.GET['type']=='VUID':
			response = self.getVillageFromVUID(request) 
		else:    
			response = self.getStats(request)
		
		# return self.create_response(request, response)   
		return HttpResponse(response, content_type='application/json')

	def getVillageFromVUID(self, request):
		resource = AfgPplp.objects.all().values('vil_uid','name_en','type_settlement','wkb_geometry')
		resource = resource.filter(vuid__icontains=request.GET['search'])
		response = GeoJSONSerializer().serialize(resource, use_natural_keys=True, with_modelname=False, geometry_field='wkb_geometry', srid=3857)
		data = json.loads(response)
		for i in range(len(data['features'])):
			data['features'][i]['properties']['number']=i+1
			if 'name_en' in data['features'][i]['properties']:
				data['features'][i]['properties']['fromlayer'] = 'glyphicon glyphicon-home'
		return json.dumps(data)

	def fuzzyLookup(self, request):
		f = AfgPplp.objects.all().values('name_en','dist_na_en','prov_na_en','vil_uid','type_settlement','wkb_geometry')

		if request.GET['provname'] != '':
			f = f.filter(prov_na_en=request.GET['provname'])
		if request.GET['distname'] != '':
			f = f.filter(dist_na_en=request.GET['distname'])

		choices = []
		for i in f:
			prov_na_en = ''
			dist_na_en = ''
			if request.GET['provname'] != '':
				prov_na_en = i['prov_na_en']
			if request.GET['distname'] != '':
				dist_na_en = i['dist_na_en']
			# choices.append(i['name_en'].lstrip()+';'+dist_na_en+';'+prov_na_en)
			choices.append(i['name_en'])

		# print choices
		# x = process.extract(request.GET['search']+";"+request.GET['distname']+";"+request.GET['provname'], choices, scorer=fuzz.token_sort_ratio, limit=10)

		# x = process.extract(request.GET['search'], choices, scorer=fuzz.token_sort_ratio, limit=25)
		x = process.extractWithoutOrder(request.GET['search'], choices, scorer=fuzz.token_sort_ratio, score_cutoff=50)
		# print x[0][0], request.GET['provname']+";"+request.GET['distname']+";"+request.GET['search']

		scoreKeeper = {}
		settlements = []

		for i in x:
			# print i[0]
			scoreKeeper[i[0]]=i[1]
			settlements.append(i[0])

		f = f.filter(name_en__in=settlements)
		# f = f.extra(where=["name_en+';'+dist_na_en+';'+prov_na_en in "])
		return {'result':f, 'scoreKeeper':scoreKeeper}



	def getStats(self, request):
		# print request.GET['fuzzy']
		fuzzy = False
		if request.GET['fuzzy']== 'true' and request.GET['search'] != '' and (request.GET['type']=='settlements' or request.GET['type']=='s_oasis'):
				dt = self.fuzzyLookup(request)
				resource = dt['result']
				fuzzy = True

		else:        
			# resource = .transform(900913, field_name='wkb_geometry') string__icontains
			if request.GET['type']=='settlements':
				resource = AfgPplp.objects.all().values('vil_uid','name_en','type_settlement','wkb_geometry')
			elif request.GET['type']=='healthfacility':    
				resource = AfgHltfac.objects.all()
			elif request.GET['type']=='airport':    
				resource = AfgAirdrmp.objects.all()
			else :    
				resource = OasisSettlements.objects.all().values('vil_uid','name_en','type_settlement','wkb_geometry')        

			# print request.GET['dist_code']
			if request.GET['dist_code'] != '':
				resource = resource.filter(dist_code=request.GET['dist_code'])     

			if request.GET['prov_code'] != '':
				if request.GET['type']=='settlements':
					resource = resource.filter(prov_code_1=request.GET['prov_code'])
				else:
					resource = resource.filter(prov_code=request.GET['prov_code'])    

			if request.GET['search'] != '':
				if request.GET['type']=='settlements':
					resource = resource.filter(name_en__icontains=request.GET['search'])
				elif request.GET['type']=='healthfacility':  
					resource = resource.filter(facility_name__icontains=request.GET['search'])    
				elif request.GET['type']=='airport':  
					resource = resource.filter(namelong__icontains=request.GET['search'])    
				else:
					resource = resource.filter(name_en__icontains=request.GET['search'])    

		response = GeoJSONSerializer().serialize(resource, use_natural_keys=True, with_modelname=False, geometry_field='wkb_geometry', srid=3857)

		data = json.loads(response)
		for i in range(len(data['features'])):
			if fuzzy:
				tmp_set = data['features'][i]['properties']['name_en']         
				data['features'][i]['properties']['score']=dt['scoreKeeper'][tmp_set]

			data['features'][i]['properties']['number']=i+1
			if 'name_en' in data['features'][i]['properties']:
				data['features'][i]['properties']['fromlayer'] = 'glyphicon glyphicon-home'
			elif 'namelong' in data['features'][i]['properties']:
				data['features'][i]['properties']['fromlayer'] = 'glyphicon glyphicon-plane'
			elif 'facility_name' in data['features'][i]['properties']:
				data['features'][i]['properties']['fromlayer'] = 'glyphicon glyphicon-header'


		# return response
		return json.dumps(data)

# get last update values
class getLastUpdatedStatus(ModelResource):
	"""last updated status api"""

	class Meta:
		resource_name = 'lastUpdated'
		allowed_methods = ['get']
		detail_allowed_methods = ['get'] 
		object_class=None

	def getUpdatedValues(self, request):
		response = {}
		tz = timezone('Asia/Kabul')

		try:
			rf = forecastedLastUpdate.objects.filter(forecasttype='riverflood').latest('datadate')
		except forecastedLastUpdate.DoesNotExist:
			response["flood_forecast_last_updated"] = None
		else:
			tempRF = rf.datadate + datetime.timedelta(hours=4.5)
			tempRF = tempRF.replace(tzinfo=tz)
			response["flood_forecast_last_updated"] = tempRF

		try:
			sw = forecastedLastUpdate.objects.filter(forecasttype='snowwater').latest('datadate')
		except forecastedLastUpdate.DoesNotExist:
			response["avalanche_forecast_last_updated"] = None
		else:
			tempSW = sw.datadate + datetime.timedelta(hours=4.5)
			tempSW = tempSW.replace(tzinfo=tz)
			response["avalanche_forecast_last_updated"] =  tempSW

		# sw = forecastedLastUpdate.objects.filter(forecasttype='snowwater').latest('datadate')
		# rf = forecastedLastUpdate.objects.filter(forecasttype='riverflood').latest('datadate')

		# # print rf.datadate
		# tempRF = rf.datadate + datetime.timedelta(hours=4.5)
		# tempSW = sw.datadate + datetime.timedelta(hours=4.5)

		# tz = timezone('Asia/Kabul')
		# tempRF = tempRF.replace(tzinfo=tz)
		# tempSW = tempSW.replace(tzinfo=tz)

		stdSC = datetime.datetime.utcnow()
		stdSC = stdSC.replace(hour=10, minute=00, second=00)

		tempSC = datetime.datetime.utcnow()
		# tempSC = tempSC.replace(hour=10, minute=00, second=00)

		if stdSC > tempSC:
			tempSC = tempSC - datetime.timedelta(days=1)
		#     tempSC = tempSC.replace(hour=10, minute=00, second=00)
		# else: 
		#     tempSC = tempSC.replace(hour=10, minute=00, second=00)  
		
		tempSC = tempSC.replace(hour=10, minute=00, second=00)
		tempSC = tempSC + datetime.timedelta(hours=4.5)
		tempSC = tempSC.replace(tzinfo=tz)    

		# print tempSC
		# print stdSC 

		# response["riverflood_lastupdated"] = tempRF.strftime("%d-%m-%Y %H:%M")
		# response["snowwater_lastupdated"] =  tempSW.strftime("%d-%m-%Y %H:%M")

		# response['flood_forecast_last_updated']=tempRF
		# response['avalanche_forecast_last_updated']=tempSW
		response['snow_cover_forecast_last_updated']=tempSC
		return response

	def get_list(self, request, **kwargs):
		self.method_check(request, allowed=['get'])
		response = self.getUpdatedValues(request)
		return self.create_response(request, response)  

	