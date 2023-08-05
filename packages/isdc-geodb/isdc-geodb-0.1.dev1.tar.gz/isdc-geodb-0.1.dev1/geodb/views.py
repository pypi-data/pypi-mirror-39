from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import csv, os
from geodb.models import (
    # AfgFldzonea100KRiskLandcoverPop,
    AfgLndcrva,
    AfgAdmbndaAdm1,
    AfgAdmbndaAdm2,
    # AfgFldzonea100KRiskMitigatedAreas,
    # AfgAvsa,
    Forcastedvalue,
    AfgShedaLvl4,
    districtsummary,
    provincesummary,
    basinsummary,
    AfgPpla,
    tempCurrentSC,
    # earthquake_events,
    # earthquake_shakemap,
    # villagesummaryEQ,
    AfgPplp,
    # AfgSnowaAverageExtent,
    AfgCaptPpl,
    AfgAirdrmp,
    AfgHltfac,
    forecastedLastUpdate,
    AfgCaptGmscvr,
    # AfgEqtUnkPplEqHzd,
    # Glofasintegrated,
    AfgBasinLvl4GlofasPoint,
    AfgPpltDemographics,
    AfgLspAffpplp,
    # AfgMettClim1KmChelsaBioclim,
    # AfgMettClim1KmWorldclimBioclim2050Rpc26,
    # AfgMettClim1KmWorldclimBioclim2050Rpc45,
    # AfgMettClim1KmWorldclimBioclim2050Rpc85,
    # AfgMettClim1KmWorldclimBioclim2070Rpc26,
    # AfgMettClim1KmWorldclimBioclim2070Rpc45,
    # AfgMettClim1KmWorldclimBioclim2070Rpc85,
    # AfgMettClimperc1KmChelsaPrec,
    # AfgMettClimtemp1KmChelsaTempavg,
    # AfgMettClimtemp1KmChelsaTempmax,
    # AfgMettClimtemp1KmChelsaTempmin
)
import requests
from django.core.files.base import ContentFile
import urllib2, base64
import urllib
from PIL import Image
from StringIO import StringIO
from django.db.models import Count, Sum, F
import time, sys
import subprocess
from django.template import RequestContext

from urlparse import urlparse
from geonode.maps.models import Map
from geonode.maps.views import _resolve_map, _PERMISSION_MSG_VIEW

from geodb.geoapi import getRiskExecuteExternal

# addded by boedy
from matrix.models import matrix
import datetime, re
from django.conf import settings
from ftplib import FTP

import gzip
import glob
from django.contrib.gis.gdal import DataSource
from django.db import connection, connections
from django.contrib.gis.geos import fromstr
from django.contrib.gis.utils import LayerMapping

# from geodb.usgs_comcat import getContents,getUTCTimeStamp
from django.contrib.gis.geos import Point

from zipfile import ZipFile
from urllib import urlretrieve
from tempfile import mktemp

from graphos.sources.model import ModelDataSource
from graphos.renderers import flot, gchart
from graphos.sources.simple import SimpleDataSource
from math import degrees, atan2

from django.utils.translation import ugettext as _

from netCDF4 import Dataset, num2date
import numpy as np

# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt, mpld3
# import matplotlib.ticker as ticker
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json

GS_TMP_DIR = getattr(settings, 'GS_TMP_DIR', '/tmp')

# initial_data_path = "/home/ubuntu/DRR-datacenter/geodb/initialdata/" # Production
# gdal_path = '/usr/bin/' # production

current_path = os.path.dirname(os.path.realpath(__file__))
initial_data_path = os.path.join(current_path, 'initialdata') # Production
gdal_path = '/usr/bin/' # production

# initial_data_path = "/Users/budi/Documents/iMMAP/DRR-datacenter/geodb/initialdata/" # in developement
# gdal_path = '/usr/local/bin/' # development



def cleantmpfile(filepattern):

    tmpfilelist = glob.glob("{}*.*".format(
        os.path.join(GS_TMP_DIR, filepattern)))
    for f in tmpfilelist:
        os.remove(f)

def getForecastedDisaster():
    username = 'wmo'
    password = 'SAsia:14-ffg'
    auth_encoded = base64.encodestring('%s:%s' % (username, password))[:-1]

    currentdate = datetime.datetime.utcnow()

    try:
        year = currentdate.strftime("%Y")
        month = currentdate.strftime("%m")
        day = currentdate.strftime("%d")
        hh = currentdate.strftime("%H")
        req = urllib2.Request('https://sasiaffg.hrcwater.org/CONSOLE/EXPORTS/AFGHANISTAN/'+year+'/'+month+'/'+day+'/COMPOSITE_CSV/')
        req.add_header('Authorization', 'Basic %s' % auth_encoded)
        response = urllib2.urlopen(req)

    except urllib2.HTTPError, err:
        currentdate = currentdate - datetime.timedelta(days=1)
        year = currentdate.strftime("%Y")
        month = currentdate.strftime("%m")
        day = currentdate.strftime("%d")
        hh = currentdate.strftime("%H")

        req = urllib2.Request('https://sasiaffg.hrcwater.org/CONSOLE/EXPORTS/AFGHANISTAN/'+year+'/'+month+'/'+day+'/COMPOSITE_CSV/')
        req.add_header('Authorization', 'Basic %s' % auth_encoded)
        response = urllib2.urlopen(req)
        # print response

    string = response.read().decode('utf-8')
    pattern = '<a href="*?.*?00_ffgs_prod_composite_table_01hr_afghanistan.csv">(.*?)</a>'
    for filename in re.findall(pattern, string):
        selectedFile = filename


    url = 'https://sasiaffg.hrcwater.org/CONSOLE/EXPORTS/AFGHANISTAN/'+year+'/'+month+'/'+day+'/COMPOSITE_CSV/'+selectedFile
    print url

    req = urllib2.Request(url)
    req.add_header('Authorization', 'Basic %s' % auth_encoded)
    response = urllib2.urlopen(req)

    csv_f = csv.reader(response)
    Forcastedvalue.objects.all()
    pertama=True

    # put the date back to the current date for storing data
    # it will stored the latest data from yesterday in case no result it on today
    currentdate = datetime.datetime.utcnow()
    year = currentdate.strftime("%Y")
    month = currentdate.strftime("%m")
    day = currentdate.strftime("%d")
    hh = currentdate.strftime("%H")
    minute = currentdate.strftime("%M")

    for row in csv_f:
        print row
        if not pertama:
            try:
                flashfloodArray = [float(row[21]),float(row[24]),float(row[27])]
                flashflood = max(flashfloodArray)
            except:
                flashflood = 0

            try:
                snowWater  = float(row[29])
            except:
                snowWater = 0

            flashFloodState = 0
            if flashflood > 0 and flashflood <= 5:
                flashFloodState = 1 # very low
            elif flashflood > 5 and flashflood <= 10:
                flashFloodState = 2 # low
            elif flashflood > 10 and flashflood <= 25:
                flashFloodState = 3 # moderate
            elif flashflood > 25 and flashflood <= 60:
                flashFloodState = 4 # high
            elif flashflood > 60 and flashflood <= 100:
                flashFloodState = 5 # very high
            elif flashflood > 100:
                flashFloodState = 6 # Extreme


            snowWaterState = 0
            if snowWater > 60 and snowWater <= 100:
                snowWaterState = 1 #low
            elif snowWater > 100 and snowWater <= 140:
                snowWaterState = 2 #moderate
            elif snowWater > 140:
                snowWaterState = 3 #high

            basin = AfgShedaLvl4.objects.get(value=row[0])
            if flashFloodState>0:
                # basin = AfgShedaLvl4.objects.get(value=row[0])
                recordExists = Forcastedvalue.objects.all().filter(datadate=year+'-'+month+'-'+day,forecasttype='flashflood',basin=basin)
                if recordExists.count() > 0:
                    if recordExists[0].riskstate < flashFloodState:
                        c = Forcastedvalue(pk=recordExists[0].pk,basin=basin)
                        c.riskstate = flashFloodState
                        c.datadate = recordExists[0].datadate
                        c.forecasttype = recordExists[0].forecasttype
                        c.save()
                    #     print 'flashflood modified'
                    # print 'flashflood skip'
                else:
                    c = Forcastedvalue(basin=basin)
                    c.datadate = year+'-'+month+'-'+day
                    c.forecasttype = 'flashflood'
                    c.riskstate = flashFloodState
                    c.save()
                    # print 'flashflood added'

            if snowWaterState>0:
                # basin = AfgShedaLvl4.objects.get(value=row[0])
                recordExists = Forcastedvalue.objects.all().filter(datadate=year+'-'+month+'-'+day,forecasttype='snowwater',basin=basin)
                if recordExists.count() > 0:
                    if recordExists[0].riskstate < snowWaterState:
                        c = Forcastedvalue(pk=recordExists[0].pk,basin=basin)
                        c.riskstate = snowWaterState
                        c.datadate = recordExists[0].datadate
                        c.forecasttype = recordExists[0].forecasttype
                        c.save()
                    #     print 'snowwater modified'
                    # print 'snowwater skip'
                else:
                    c = Forcastedvalue(basin=basin)
                    c.datadate = year+'-'+month+'-'+day
                    c.forecasttype = 'snowwater'
                    c.riskstate = snowWaterState
                    c.save()
                    # print 'snowwater added'

            if snowWater>0:
                # basin = AfgShedaLvl4.objects.get(value=row[0])
                recordExists = Forcastedvalue.objects.all().filter(datadate=year+'-'+month+'-'+day,forecasttype='snowwaterreal',basin=basin)
                if recordExists.count() > 0:
                    if recordExists[0].riskstate < snowWater:
                        c = Forcastedvalue(pk=recordExists[0].pk,basin=basin)
                        c.riskstate = snowWater
                        c.datadate = recordExists[0].datadate
                        c.forecasttype = recordExists[0].forecasttype
                        c.save()
                    #     print 'snowwaterreal modified'
                    # print 'snowwaterreal skip'
                else:
                    c = Forcastedvalue(basin=basin)
                    c.datadate = year+'-'+month+'-'+day
                    c.forecasttype = 'snowwaterreal'
                    c.riskstate = snowWater
                    c.save()
                    # print 'snowwaterreal added'



        pertama=False
    ff = forecastedLastUpdate(datadate=year+'-'+month+'-'+day+' '+hh+':'+minute,forecasttype='flashflood')
    ff.save()
    ff = forecastedLastUpdate(datadate=year+'-'+month+'-'+day+' '+hh+':'+minute,forecasttype='snowwater')
    ff.save()
    ff = forecastedLastUpdate(datadate=year+'-'+month+'-'+day+' '+hh+':'+minute,forecasttype='snowwaterreal')
    ff.save()

def getOverviewMaps(request):
    selectedBox = request.GET['send']

    map_obj = _resolve_map(request, request.GET['mapID'], 'base.view_resourcebase', _PERMISSION_MSG_VIEW)
    queryset = matrix(user=request.user,resourceid=map_obj,action='Interactive Map Download')
    queryset.save()

    response = HttpResponse(content_type="image/png")
    url = 'http://asdc.immap.org/geoserver/geonode/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=geonode%3Aafg_admbnda_adm2%2Cgeonode%3Aafg_admbnda_adm1&STYLES=overview_adm2,overview_adm1&SRS=EPSG%3A4326&WIDTH=292&HEIGHT=221&BBOX=59.150390625%2C28.135986328125%2C76.025390625%2C38.792724609375'
    # url2='http://asdc.immap.org/geoserver/geonode/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&SRS=EPSG%3A4326&WIDTH=768&HEIGHT=485&BBOX=59.150390625%2C28.135986328125%2C76.025390625%2C38.792724609375&SLD_BODY='+selectedBox
    url2='http://asdc.immap.org/geoserver/geonode/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&SRS=EPSG%3A4326&WIDTH=292&HEIGHT=221&BBOX=59.150390625%2C28.135986328125%2C76.025390625%2C38.792724609375'
    template = '<sld:StyledLayerDescriptor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">'
    template +='<sld:UserLayer>'
    template +=     '<sld:Name>Inline</sld:Name>'
    template +=      '<sld:InlineFeature>'
    template +=         '<sld:FeatureCollection>'
    template +=             '<gml:featureMember>'
    template +=                 '<feature>'
    template +=                     '<polygonProperty>'
    template +=                         '<gml:Polygon  srsName="4326">'
    template +=                             '<gml:outerBoundaryIs>'
    template +=                                 '<gml:LinearRing>'
    template +=                                     '<gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">'+selectedBox
    template +=                                     '</gml:coordinates>'
    template +=                                 '</gml:LinearRing>'
    template +=                             '</gml:outerBoundaryIs>'
    template +=                         '</gml:Polygon>'
    template +=                      '</polygonProperty>'
    template +=                      '<title>Pacific NW</title>'
    template +=                 '</feature>'
    template +=             '</gml:featureMember>'
    template +=         '</sld:FeatureCollection>'
    template +=     '</sld:InlineFeature>'
    template +=     '<sld:UserStyle>'
    template +=         '<sld:FeatureTypeStyle>'
    template +=             '<sld:Rule>'
    template +=                 '<sld:PolygonSymbolizer>'
    template +=                     '<sld:Stroke>'
    template +=                         '<sld:CssParameter name="stroke">#FF0000</sld:CssParameter>'
    template +=                         '<sld:CssParameter name="stroke-width">1</sld:CssParameter>'
    template +=                     '</sld:Stroke>'
    template +=                 '</sld:PolygonSymbolizer>'
    template +=             '</sld:Rule>'
    template +=         '</sld:FeatureTypeStyle>'
    template +=     '</sld:UserStyle>'
    template += '</sld:UserLayer>'
    template +='</sld:StyledLayerDescriptor>'

    header = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.encodestring("boedy1996:kontol").replace('\n', '')
    }

    request1 = urllib2.Request(url, None, header)

    input_file = StringIO(urllib2.urlopen(request1).read())


    background = Image.open(input_file)

    values = {'SLD_BODY' : template}
    data = urllib.urlencode(values)


    request2 = urllib2.Request(url2, data)
    request2.add_header('Authorization', "Basic " + base64.encodestring("boedy1996:kontol").replace('\n', ''))
    response2 = urllib2.urlopen(request2)

    input_file2 = StringIO(response2.read())
    # input_file = StringIO(urllib2.urlopen(request2,data).read())

    overlay = Image.open(input_file2)

    new_img = Image.blend(background, overlay, 0.5)  #background.paste(overlay, overlay.size, overlay)

    new_img.save(response, 'PNG', quality=300)
    background.save(response, 'PNG', quality=300)

    return response

# Create your views here.
def update_progress(progress, msg, proctime):
    barLength = 100 # Modify this to change the length of the progress bar
    status = ""
    # print float(progress)
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float"
    if progress < 0:
        progress = 0
        status = "Halt..."
    if progress >= 1:
        progress = 1
        status = "Done..."
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2} {3} {4}s \r".format( "#"*block + "-"*(barLength-block), progress*100, status, msg, proctime)
    sys.stdout.write(text)
    sys.stdout.flush()

def updateForecastSummary():
    print 'def updateForecastSummary()'
    # targetRisk.select_related("basinmembers").defer('basinmember__wkb_geometry').exclude(basinmember__basins__riskstate=None).filter(basinmember__basins__forecasttype='riverflood',basinmember__basins__datadate='%s-%s-%s' %(YEAR,MONTH,DAY)
    # counts =  getRiskNumber(), filterLock, 'basinmember__basins__riskstate', 'fldarea_population', 'fldarea_sqm', flag, code, 'afg_fldzonea_100k_risk_landcover_pop')
    # temp = dict([(c['basinmember__basins__riskstate'], c['count']) for c in counts])
    # response['riverflood_forecast_verylow_pop']=round(temp.get(1, 0),0)
    # response['riverflood_forecast_low_pop']=round(temp.get(2, 0),0)
    # response['riverflood_forecast_med_pop']=round(temp.get(3, 0),0)
    # response['riverflood_forecast_high_pop']=round(temp.get(4, 0),0)
    # response['riverflood_forecast_veryhigh_pop']=round(temp.get(5, 0),0)
    # response['riverflood_forecast_extreme_pop']=round(temp.get(6, 0),0)
    # response['total_riverflood_forecast_pop']=response['riverflood_forecast_verylow_pop'] + response['riverflood_forecast_low_pop'] + response['riverflood_forecast_med_pop'] + response['riverflood_forecast_high_pop'] + response['riverflood_forecast_veryhigh_pop'] + response['riverflood_forecast_extreme_pop']


def updateSummaryTable():   # for district
    YEAR = datetime.datetime.utcnow().strftime("%Y")
    MONTH = datetime.datetime.utcnow().strftime("%m")
    DAY = datetime.datetime.utcnow().strftime("%d")
    resourcesProvinces = AfgAdmbndaAdm1.objects.all().order_by('prov_code')
    resourcesDistricts = AfgAdmbndaAdm2.objects.all().order_by('dist_code')
    resourcesBasin = AfgPpla.objects.all()

    header = []

    print '----- Process Provinces Statistics ------\n'
    ppp = resourcesProvinces.count()
    xxx = 0
    update_progress(float(xxx/ppp), 'start', 0)

    databaseFields = provincesummary._meta.get_all_field_names()
    databaseFields.remove('id')
    databaseFields.remove('province')
    for aoi in resourcesProvinces:
        start = time.time()
        riskNumber = getRiskExecuteExternal('ST_GeomFromText(\''+aoi.wkb_geometry.wkt+'\',4326)', 'currentProvince', aoi.prov_code, YEAR, MONTH, DAY)
        px = provincesummary.objects.filter(province=aoi.prov_code)

        if px.count()>0:
            a = provincesummary(id=px[0].id,province=aoi.prov_code)
        else:
            a = provincesummary(province=aoi.prov_code)

        for i in databaseFields:
            setattr(a, i, riskNumber[i])
        a.save()
        loadingtime = time.time() - start
        xxx=xxx+1
        update_progress(float(float(xxx)/float(ppp)), aoi.prov_code, loadingtime)

    print '----- Process Districts Statistics ------\n'
    ppp = resourcesDistricts.count()
    xxx = 0
    update_progress(float(xxx/ppp), 'start', 0)

    databaseFields = districtsummary._meta.get_all_field_names()
    databaseFields.remove('id')
    databaseFields.remove('district')
    for aoi in resourcesDistricts:
        start = time.time()
        riskNumber = getRiskExecuteExternal('ST_GeomFromText(\''+aoi.wkb_geometry.wkt+'\',4326)', 'currentProvince', aoi.dist_code, YEAR, MONTH, DAY)
        px = districtsummary.objects.filter(district=aoi.dist_code)

        if px.count()>0:
            a = districtsummary(id=px[0].id,district=aoi.dist_code)
        else:
            a = districtsummary(district=aoi.dist_code)

        for i in databaseFields:
            setattr(a, i, riskNumber[i])
        a.save()
        loadingtime = time.time() - start
        xxx=xxx+1
        update_progress(float(float(xxx)/float(ppp)), aoi.dist_code, loadingtime)

    print '----- Process Villages Statistics ------\n'
    cursor = connections['geodb'].cursor()
    cursor.execute('\
        update "villagesummary" \
            set \
            riverflood_forecast_verylow_pop = 0,\
            riverflood_forecast_low_pop = 0,\
            riverflood_forecast_med_pop = 0,\
            riverflood_forecast_high_pop = 0,\
            riverflood_forecast_veryhigh_pop = 0,\
            riverflood_forecast_extreme_pop = 0,\
            total_riverflood_forecast_pop = 0,\
            \
            riverflood_forecast_verylow_area = 0,\
            riverflood_forecast_low_area = 0,\
            riverflood_forecast_med_area = 0,\
            riverflood_forecast_high_area = 0,\
            riverflood_forecast_veryhigh_area = 0,\
            riverflood_forecast_extreme_area = 0,\
            total_riverflood_forecast_area = 0,\
            \
            flashflood_forecast_verylow_pop = 0,\
            flashflood_forecast_low_pop = 0,\
            flashflood_forecast_med_pop = 0,\
            flashflood_forecast_high_pop = 0,\
            flashflood_forecast_veryhigh_pop = 0,\
            flashflood_forecast_extreme_pop = 0,\
            total_flashflood_forecast_pop = 0,\
            \
            flashflood_forecast_verylow_area = 0,\
            flashflood_forecast_low_area = 0,\
            flashflood_forecast_med_area = 0,\
            flashflood_forecast_high_area = 0,\
            flashflood_forecast_veryhigh_area = 0,\
            flashflood_forecast_extreme_area = 0,\
            total_flashflood_forecast_area = 0,\
            \
            ava_forecast_low_pop = 0,\
            ava_forecast_med_pop = 0,\
            ava_forecast_high_pop = 0,\
            total_ava_forecast_pop = 0;\
            \
            update "villagesummary"\
            set\
            riverflood_forecast_verylow_pop = p.riverflood_forecast_verylow_pop,\
            riverflood_forecast_low_pop = p.riverflood_forecast_low_pop,\
            riverflood_forecast_med_pop = p.riverflood_forecast_med_pop,\
            riverflood_forecast_high_pop = p.riverflood_forecast_high_pop,\
            riverflood_forecast_veryhigh_pop = p.riverflood_forecast_veryhigh_pop,\
            riverflood_forecast_extreme_pop = p.riverflood_forecast_extreme_pop,\
            \
            riverflood_forecast_verylow_area = p.riverflood_forecast_verylow_area,\
            riverflood_forecast_low_area = p.riverflood_forecast_low_area,\
            riverflood_forecast_med_area = p.riverflood_forecast_med_area,\
            riverflood_forecast_high_area = p.riverflood_forecast_high_area,\
            riverflood_forecast_veryhigh_area = p.riverflood_forecast_veryhigh_area,\
            riverflood_forecast_extreme_area = p.riverflood_forecast_extreme_area\
            from (\
            SELECT \
            "afg_fldzonea_100k_risk_landcover_pop"."vuid", \
            "afg_fldzonea_100k_risk_landcover_pop"."basin_id", \
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 1 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as riverflood_forecast_verylow_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 2 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as riverflood_forecast_low_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 3 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as riverflood_forecast_med_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 4 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as riverflood_forecast_high_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 5 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as riverflood_forecast_veryhigh_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 6 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as riverflood_forecast_extreme_pop,\
            \
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 1 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as riverflood_forecast_verylow_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 2 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as riverflood_forecast_low_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 3 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as riverflood_forecast_med_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 4 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as riverflood_forecast_high_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 5 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as riverflood_forecast_veryhigh_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 6 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as riverflood_forecast_extreme_area\
            FROM "afg_fldzonea_100k_risk_landcover_pop" \
            INNER JOIN "afg_sheda_lvl4" ON ( "afg_fldzonea_100k_risk_landcover_pop"."basinmember_id" = "afg_sheda_lvl4"."ogc_fid" ) \
            INNER JOIN "forcastedvalue" ON ( "afg_sheda_lvl4"."ogc_fid" = "forcastedvalue"."basin_id" ) \
            WHERE (NOT ("afg_fldzonea_100k_risk_landcover_pop"."agg_simplified_description" = \'Water body and marshland\' ) \
            AND NOT ("afg_fldzonea_100k_risk_landcover_pop"."basinmember_id" IN (SELECT U1."ogc_fid" FROM "afg_sheda_lvl4" U1 LEFT OUTER JOIN "forcastedvalue" U2 ON ( U1."ogc_fid" = U2."basin_id" ) WHERE U2."riskstate" IS NULL)) \
            AND "forcastedvalue"."datadate" = \''+YEAR+'-'+MONTH+'-'+DAY+' 00:00:00\'  \
            AND "forcastedvalue"."forecasttype" = \'riverflood\' ) \
            GROUP BY \
            "afg_fldzonea_100k_risk_landcover_pop"."vuid", \
            "afg_fldzonea_100k_risk_landcover_pop"."basin_id") as p \
            WHERE p.vuid = "villagesummary".vuid and p.basin_id = cast("villagesummary".basin as float);\
            \
            update "villagesummary"\
            set\
            flashflood_forecast_verylow_pop = p.flashflood_forecast_verylow_pop,\
            flashflood_forecast_low_pop = p.flashflood_forecast_low_pop,\
            flashflood_forecast_med_pop = p.flashflood_forecast_med_pop,\
            flashflood_forecast_high_pop = p.flashflood_forecast_high_pop,\
            flashflood_forecast_veryhigh_pop = p.flashflood_forecast_veryhigh_pop,\
            flashflood_forecast_extreme_pop = p.flashflood_forecast_extreme_pop,\
            \
            flashflood_forecast_verylow_area = p.flashflood_forecast_verylow_area,\
            flashflood_forecast_low_area = p.flashflood_forecast_low_area,\
            flashflood_forecast_med_area = p.flashflood_forecast_med_area,\
            flashflood_forecast_high_area = p.flashflood_forecast_high_area,\
            flashflood_forecast_veryhigh_area = p.flashflood_forecast_veryhigh_area,\
            flashflood_forecast_extreme_area = p.flashflood_forecast_extreme_area\
            from (\
            SELECT \
            "afg_fldzonea_100k_risk_landcover_pop"."vuid", \
            "afg_fldzonea_100k_risk_landcover_pop"."basin_id", \
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 1 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as flashflood_forecast_verylow_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 2 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as flashflood_forecast_low_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 3 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as flashflood_forecast_med_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 4 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as flashflood_forecast_high_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 5 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as flashflood_forecast_veryhigh_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 6 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_population"\
             else 0\
            end\
            )) as flashflood_forecast_extreme_pop,\
            \
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 1 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as flashflood_forecast_verylow_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 2 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as flashflood_forecast_low_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 3 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as flashflood_forecast_med_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 4 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as flashflood_forecast_high_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 5 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as flashflood_forecast_veryhigh_area,\
            SUM(\
            case\
             when "forcastedvalue"."riskstate" = 6 then "afg_fldzonea_100k_risk_landcover_pop"."fldarea_sqm"\
             else 0\
            end\
            )/1000000 as flashflood_forecast_extreme_area\
            FROM "afg_fldzonea_100k_risk_landcover_pop" \
            INNER JOIN "afg_sheda_lvl4" ON ( "afg_fldzonea_100k_risk_landcover_pop"."basinmember_id" = "afg_sheda_lvl4"."ogc_fid" ) \
            INNER JOIN "forcastedvalue" ON ( "afg_sheda_lvl4"."ogc_fid" = "forcastedvalue"."basin_id" ) \
            WHERE (NOT ("afg_fldzonea_100k_risk_landcover_pop"."agg_simplified_description" = \'Water body and marshland\' ) \
            AND NOT ("afg_fldzonea_100k_risk_landcover_pop"."basinmember_id" IN (SELECT U1."ogc_fid" FROM "afg_sheda_lvl4" U1 LEFT OUTER JOIN "forcastedvalue" U2 ON ( U1."ogc_fid" = U2."basin_id" ) WHERE U2."riskstate" IS NULL)) \
            AND "forcastedvalue"."datadate" = \''+YEAR+'-'+MONTH+'-'+DAY+' 00:00:00\'  \
            AND "forcastedvalue"."forecasttype" = \'flashflood\' ) \
            GROUP BY \
            "afg_fldzonea_100k_risk_landcover_pop"."vuid", \
            "afg_fldzonea_100k_risk_landcover_pop"."basin_id") as p \
            WHERE p.vuid = "villagesummary".vuid and p.basin_id = cast("villagesummary".basin as float);\
            \
            update "villagesummary"\
            set\
            ava_forecast_low_pop = p.ava_forecast_low_pop,\
            ava_forecast_med_pop = p.ava_forecast_med_pop,\
            ava_forecast_high_pop = p.ava_forecast_high_pop\
            From (SELECT \
            "afg_avsa"."vuid", \
            "afg_avsa"."basin_id",\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 1 then "afg_avsa"."avalanche_pop"\
             else 0\
            end\
            )) as ava_forecast_low_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 2 then "afg_avsa"."avalanche_pop"\
             else 0\
            end\
            )) as ava_forecast_med_pop,\
            round(SUM(\
            case\
             when "forcastedvalue"."riskstate" = 3 then "afg_avsa"."avalanche_pop"\
             else 0\
            end\
            )) as ava_forecast_high_pop\
            FROM "afg_avsa" \
            INNER JOIN "afg_sheda_lvl4" ON ( "afg_avsa"."basinmember_id" = "afg_sheda_lvl4"."ogc_fid" ) \
            INNER JOIN "forcastedvalue" ON ( "afg_sheda_lvl4"."ogc_fid" = "forcastedvalue"."basin_id" ) \
            WHERE (NOT ("afg_avsa"."basinmember_id" IN (SELECT U1."ogc_fid" FROM "afg_sheda_lvl4" U1 LEFT OUTER JOIN "forcastedvalue" U2 ON ( U1."ogc_fid" = U2."basin_id" ) WHERE U2."riskstate" IS NULL)) \
            AND "forcastedvalue"."datadate" = \''+YEAR+'-'+MONTH+'-'+DAY+' 00:00:00\'  \
            AND "forcastedvalue"."forecasttype" = \'snowwater\' )\
            GROUP BY  \
            "afg_avsa"."vuid", \
            "afg_avsa"."basin_id") as p\
            WHERE p.vuid = "villagesummary".vuid and p.basin_id = cast("villagesummary".basin as float);\
            \
            update "villagesummary"\
            set\
            total_riverflood_forecast_pop = riverflood_forecast_verylow_pop + riverflood_forecast_low_pop + riverflood_forecast_med_pop + riverflood_forecast_high_pop + riverflood_forecast_veryhigh_pop + riverflood_forecast_extreme_pop,\
            total_riverflood_forecast_area = riverflood_forecast_verylow_area + riverflood_forecast_low_area + riverflood_forecast_med_area + riverflood_forecast_high_area + riverflood_forecast_veryhigh_area + riverflood_forecast_extreme_area,\
            total_flashflood_forecast_pop = flashflood_forecast_verylow_pop + flashflood_forecast_low_pop + flashflood_forecast_med_pop + flashflood_forecast_high_pop + flashflood_forecast_veryhigh_pop + flashflood_forecast_extreme_pop,\
            total_flashflood_forecast_area = flashflood_forecast_verylow_area + flashflood_forecast_low_area + flashflood_forecast_med_area + flashflood_forecast_high_area + flashflood_forecast_veryhigh_area + flashflood_forecast_extreme_area,\
            total_ava_forecast_pop = ava_forecast_low_pop+ava_forecast_med_pop+ava_forecast_high_pop;\
    ')
    cursor.close()
    print 'done'
    # ppp = resourcesBasin.count()
    # xxx = 0
    # update_progress(float(xxx/ppp), 'start', 0)

    # databaseFields = basinsummary._meta.get_all_field_names()
    # databaseFields.remove('id')
    # databaseFields.remove('basin')
    # for aoi in resourcesBasin:
    #     start = time.time()
    #     riskNumber = getRiskExecuteExternal('ST_GeomFromText(\''+aoi.wkb_geometry.wkt+'\',4326)', 'currentBasin', aoi.vuid)
    #     px = basinsummary.objects.filter(basin=aoi.vuid)
    #     if px.count()>0:
    #         a = basinsummary(id=px[0].id,basin=aoi.vuid)
    #     else:
    #         a = basinsummary(basin=aoi.vuid)

    #     for i in databaseFields:
    #         setattr(a, i, riskNumber[i])
    #     a.save()
    #     loadingtime = time.time() - start
    #     xxx=xxx+1
    #     update_progress(float(float(xxx)/float(ppp)), aoi.vuid, loadingtime)


    return

def exportdata():
    outfile_path = '/Users/budi/Documents/iMMAP/out.csv' # for local
    # outfile_path = '/home/ubuntu/DRR-datacenter/geonode/static_root/intersection_stats.csv' # for server

    csvFile = open(outfile_path, 'w')

    # resources = AfgAdmbndaAdm2.objects.all().filter(dist_code__in=['1205']).order_by('dist_code')  # ingat nanti ganti
    resources = AfgAdmbndaAdm2.objects.all().order_by('dist_code')  # ingat nanti ganti

    writer = csv.writer(csvFile)
    header = []
    headerTemp = []
    ppp = resources.count()
    xxx = 0
    update_progress(float(xxx/ppp), 'start', 0)
    for aoi in resources:
        start = time.time()
        row = []
        # test = getRiskExecuteExternal('ST_GeomFromText(\''+aoi.wkb_geometry.wkt+'\',4326)', 'drawArea', None) # real calculation
        test = getRiskExecuteExternal('ST_GeomFromText(\''+aoi.wkb_geometry.wkt+'\',4326)', 'currentProvince', aoi.dist_code)

        if len(header) == 0:
            headerTemp.append('aoi_id')
            for i in test:
                header.append(i)
                headerTemp.append(i)
            writer.writerow(headerTemp)

        row.append(aoi.dist_code)
    	for i in header:
            row.append(test[i])

        writer.writerow(row)

        loadingtime = time.time() - start
        xxx=xxx+1
        update_progress(float(float(xxx)/float(ppp)), aoi.dist_code, loadingtime)
    return


def getKeyCustom(dt, idx):
    result = 0
    if len(dt)>0:
        result = round(dt[0][idx] or 0,0)
    return result

def getGeneralInfoVillages(request):
    template = './generalInfo.html'
    village = request.GET["v"]

    context_dict = getCommonVillageData(village)
    px = AfgLndcrva.objects.all().filter(vuid=village).values('agg_simplified_description').annotate(totalpop=Sum('area_population'), totalarea=Sum('area_sqm')).values('agg_simplified_description','totalpop', 'totalarea')
    data1 = []
    data2 = []
    data1.append(['agg_simplified_description','area_population'])
    data2.append(['agg_simplified_description','area_sqm'])
    for i in px:
        data1.append([i['agg_simplified_description'],round(i['totalpop'] or 0,0)])
        data2.append([i['agg_simplified_description'],round(i['totalarea']/1000000,1)])

    context_dict['landcover_pop_chart'] = gchart.PieChart(SimpleDataSource(data=data1), html_id="pie_chart1", options={'title': _("# of Population"), 'width': 225,'height': 225, 'pieSliceText': _('percentage'),'legend': {'position': 'top', 'maxLines':3}})
    context_dict['landcover_area_chart'] = gchart.PieChart(SimpleDataSource(data=data2), html_id="pie_chart2", options={'title': _("# of Area (KM2)"), 'width': 225,'height': 225, 'pieSliceText': _('percentage'),'legend': {'position': 'top', 'maxLines':3}})
    context_dict['longitude'] = context_dict['position'].x
    context_dict['latitude'] = context_dict['position'].y
    context_dict.pop('position')
    return render_to_response(template,
                                  RequestContext(request, context_dict))

def getCommonVillageData(village):
    databaseFields = AfgPpla._meta.get_all_field_names()
    databaseFields.remove('ogc_fid')
    databaseFields.remove('wkb_geometry')
    databaseFields.remove('shape_length')
    databaseFields.remove('shape_area')
    px = get_object_or_404(AfgPpla, vuid=village)
    context_dict = {}
    for i in databaseFields:
        context_dict[i] = getattr(px, i)

    px = get_object_or_404(AfgPplp, vil_uid=village)
    context_dict['language_field'] = px.language_field
    context_dict['elevation'] = round(px.elevation,1)
    context_dict['position'] = px.wkb_geometry
    return context_dict

def getConvertedTime(t):
    if t>120 and t<3600:
        m, s = divmod(t, 60)
        return str(m)+' minutes'
        # return str(round(t/60,0))+' minutes'
    elif t>3600:
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        return "%d hours %d minutes" % (h, m)
        # return str(round(t/3600,1))+' hour(s)'
    else :
        return str(t)+' second(s)'

def getConvertedDistance(d):
    if d>1000:
        km, m = divmod(d, 1000)
        return str(km)+' km'
        # return str(round(d/1000))+' km'
    else:
        return str(d)+' m'

def getAngle(x, y, center_x, center_y):
    angle = degrees(atan2(y - center_y, x - center_x))
    bearing1 = (angle + 360) % 360
    bearing2 = (90 - angle) % 360
    if angle < 0:
        angle = 360 + angle
    angle = -(angle)
    return {'angle':angle,'bearing1':bearing1,'bearing2':bearing2}

def getDirectionLabel(angle):
    angle = -(angle)
    if angle == 0:
       return 'E'
    elif angle == 90:
        return 'N'
    elif angle == 180:
        return 'W'
    elif angle == 270:
        return 'S'
    elif angle == 360:
        return 'E'
    elif angle > 0 and angle<45:
        return 'EN'
    elif angle > 45 and angle<90:
        return 'NE'
    elif angle > 90 and angle<135:
        return 'NW'
    elif angle > 135 and angle<180:
        return 'WN'
    elif angle > 180 and angle<225:
        return 'WS'
    elif angle > 225 and angle<270:
        return 'SW'
    elif angle > 270 and angle<315:
        return 'SE'
    elif angle > 315 and angle<360:
        return 'ES'

def databasevacumm():
    cursor = connections['geodb'].cursor()
    cursor.execute("VACUUM (VERBOSE, ANALYZE);")
    cursor.close()

def getWMS(request):

    # print request
    req = urllib2.Request('http://asdc.immap.org/geoserver/wms?'+request.META['QUERY_STRING'])
    # print request.META['QUERY_STRING']
    # print request.GET.get('request')
    # print request.GET.get('bbox')

    if request.GET.get('request') == 'GetLegendGraphic' or request.GET.get('bbox') == '60.4720890240001,29.3771715570001,74.889451148,38.4907374680001':
        base64string = base64.encodestring('%s:%s' % ('boedy1996', 'kontol'))[:-1]
        authheader =  "Basic %s" % base64string
        req.add_header('Authorization', authheader)
        req.add_header('Content-Type', 'image/png')
        response = urllib2.urlopen(req).read()
        # print response

        return HttpResponse(response, content_type='image/png' )
    else:
        base64string = base64.encodestring('%s:%s' % ('boedy1996', 'kontol'))[:-1]
        authheader =  "Basic %s" % base64string
        req.add_header('Authorization', authheader)
        req.add_header('Content-Type', 'image/png')
        response = urllib2.urlopen(req).read()
        return HttpResponse(response, content_type='image/png' )

def get_month_name(monthNo):
    if monthNo==1:
        return 'January'
    elif monthNo==2:
        return 'February'
    elif monthNo==3:
        return 'March'
    elif monthNo==4:
        return 'April'
    elif monthNo==5:
        return 'May'
    elif monthNo==6:
        return 'June'
    elif monthNo==7:
        return 'July'
    elif monthNo==8:
        return 'August'
    elif monthNo==9:
        return 'September'
    elif monthNo==10:
        return 'October'
    elif monthNo==11:
        return 'November'
    elif monthNo==12:
        return 'December'


def getRefactorData():
    # f_IN = open("/Users/budi/Documents/iMMAP/DRR-datacenter/scripts/misc-boedy1996/Glofas_Baseline_Output_Adjustment_factor.csv", 'rU')
    f_IN = open("/home/ubuntu/Glofas_Baseline_Output_Adjustment_factor.csv", 'rU')
    reader = csv.reader(f_IN)
    first = True
    data = {}

    for row in reader:
        if first:
            first = False
        else:
            lon = row[2]
            lat = row[1]

            # data[lat][lon]['rl2_factor']=row[8]
            data[lat]={lon:{'rl2_factor':row[8],'rl5_factor':row[9],'rl20_factor':row[10]}}

    f_IN.close()
    return data


def get_nc_file_from_ftp(date):
    # print getattr(settings, 'GLOFAS_FTP_UNAME')
    # print getattr(settings, 'GLOFAS_FTP_UPASS')
    # print Glofasintegrated.objects.latest('datadate').date
    date_arr = date.split('-')
    base_url = 'ftp.ecmwf.int'
    # filelist=[]

    server = FTP()
    server.connect('data-portal.ecmwf.int')
    server.login(getattr(settings, 'GLOFAS_FTP_UNAME'),getattr(settings, 'GLOFAS_FTP_UPASS'))

    server.cwd("/for_IMMAP/")

    try:
        print server.size("glofas_arealist_for_IMMAP_in_Afghanistan_"+date_arr[0]+date_arr[1]+date_arr[2]+"00.nc")
        print getattr(settings, 'GLOFAS_NC_FILES')+date_arr[0]+date_arr[1]+date_arr[2]+"00.nc"
        server.retrbinary("RETR " + "glofas_arealist_for_IMMAP_in_Afghanistan_"+date_arr[0]+date_arr[1]+date_arr[2]+"00.nc", open(getattr(settings, 'GLOFAS_NC_FILES')+date_arr[0]+date_arr[1]+date_arr[2]+"00.nc","wb").write)
        server.close()
        return True
    except:
        server.close()
        return False

def getDemographicInfo(request):
    template = './demographic.html'
    village = request.GET["v"]

    context_dict = getCommonVillageData(village)

    rowsgenderpercent = AfgPpltDemographics.objects.all().filter(vuidnear=village).values()
    i = rowsgenderpercent[0]

    data3 = []
    data3.append(['Gender','Percent'])
    data3.append(['Male', i['vuid_male_perc']])
    data3.append(['Female', i['vuid_female_perc']])

    data4 = []
    data4.append(['Age','Male','Female'])
    data4options={'title': _("Gender Ratio by Age Group (in %)"), 'width': 510, 'isStacked': True, 'hAxis': {'format': ';','title': _('in percent of total population')}, 'vAxis': {'title': _('age group in years'),'direction': -1}, 'legend': {'position': 'top', 'maxLines':3}}
    if context_dict['vuid_population'] > 200:
        data4.append(['0-4',   -i['m_perc_yrs_0_4'],    i['f_perc_yrs_0_4']])
        data4.append(['5-9',   -i['m_perc_yrs_5_9'],    i['f_perc_yrs_5_9']])
        data4.append(['10-14', -i['m_perc_yrs_10_14'],  i['f_perc_yrs_10_14']])
        data4.append(['15-19', -i['m_perc_yrs_15_19'],  i['f_perc_yrs_15_19']])
        data4.append(['20-24', -i['m_perc_yrs_20_24'],  i['f_perc_yrs_20_24']])
        data4.append(['25-29', -i['m_perc_yrs_25_29'],  i['f_perc_yrs_25_29']])
        data4.append(['30-34', -i['m_perc_yrs_30_34'],  i['f_perc_yrs_30_34']])
        data4.append(['35-39', -i['m_perc_yrs_35_39'],  i['f_perc_yrs_35_39']])
        data4.append(['40-44', -i['m_perc_yrs_40_44'],  i['f_perc_yrs_40_44']])
        data4.append(['45-49', -i['m_perc_yrs_45_49'],  i['f_perc_yrs_45_49']])
        data4.append(['50-54', -i['m_perc_yrs_50_54'],  i['f_perc_yrs_50_54']])
        data4.append(['55-59', -i['m_perc_yrs_55_59'],  i['f_perc_yrs_55_59']])
        data4.append(['60-64', -i['m_perc_yrs_60_64'],  i['f_perc_yrs_60_64']])
        data4.append(['65-69', -i['m_perc_yrs_65_69'],  i['f_perc_yrs_65_69']])
        data4.append(['70-74', -i['m_perc_yrs_70_74'],  i['f_perc_yrs_70_74']])
        data4.append(['75-79', -i['m_perc_yrs_75_79'],  i['f_perc_yrs_75_79']])
        data4.append(['80+',   -i['m_perc_yrs_80pls'],  i['f_perc_yrs_80pls']])

        data4options['height'] = 450
        data4options['vAxis']['textStyle'] = {'fontSize': 11}
    else:
        data4.append(['0-9',   -i['m_perc_yrs_0_4']  -i['m_perc_yrs_5_9'],    i['f_perc_yrs_0_4']  +i['f_perc_yrs_5_9']])
        data4.append(['10-19', -i['m_perc_yrs_10_14']-i['m_perc_yrs_15_19'],  i['f_perc_yrs_10_14']+i['f_perc_yrs_15_19']])
        data4.append(['20-29', -i['m_perc_yrs_20_24']-i['m_perc_yrs_25_29'],  i['f_perc_yrs_20_24']+i['f_perc_yrs_25_29']])
        data4.append(['30-39', -i['m_perc_yrs_30_34']-i['m_perc_yrs_35_39'],  i['f_perc_yrs_30_34']+i['f_perc_yrs_35_39']])
        data4.append(['40-49', -i['m_perc_yrs_40_44']-i['m_perc_yrs_45_49'],  i['f_perc_yrs_40_44']+i['f_perc_yrs_45_49']])
        data4.append(['50-59', -i['m_perc_yrs_50_54']-i['m_perc_yrs_55_59'],  i['f_perc_yrs_50_54']+i['f_perc_yrs_55_59']])
        data4.append(['60-69', -i['m_perc_yrs_60_64']-i['m_perc_yrs_65_69'],  i['f_perc_yrs_60_64']+i['f_perc_yrs_65_69']])
        data4.append(['70-79', -i['m_perc_yrs_70_74']-i['m_perc_yrs_75_79'],  i['f_perc_yrs_70_74']+i['f_perc_yrs_75_79']])
        data4.append(['80+',   -i['m_perc_yrs_80pls'],                        i['f_perc_yrs_80pls']])

    for i, v in enumerate(data3):
        if i > 0:
            v[1] = {'v':v[1], 'f':str(abs(round(v[1], 1)))+' %'}

    for i, v in enumerate(data4):
        if i > 0:
            v[1] = {'v':v[1], 'f':str(abs(round(v[1], 1)))+' %'}
            v[2] = {'v':v[2], 'f':str(abs(round(v[2], 1)))+' %'}

    context_dict['gender_ratio_chart'] = gchart.PieChart(SimpleDataSource(data=data3), html_id="pie_chart3", width=510, options={'title': _("Gender Ratio (in %)"), 'width': 510, 'pieSliceText': _('value'),'pieHole':0.5,'legend': {'position': 'top', 'maxLines':3},'tooltip': {'text': 'value'}})
    context_dict['gender_ratio_by_age_chart'] = gchart.BarChart(SimpleDataSource(data=data4), html_id="bar_chart1", width=510, options=data4options)

    context_dict.pop('position')
    return render_to_response(template,
                                  RequestContext(request, context_dict))
