# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = True` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.contrib.gis.db import models

class AfgAdmbndaAdm1(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    prov_na_dar = models.CharField(max_length=255, blank=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    reg_unama_na_dar = models.CharField(max_length=255, blank=True)
    reg_code = models.IntegerField(blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_admbnda_adm1'
    def __unicode__(self):
        return self.prov_na_en    

class AfgAdmbndaAdm2(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    unit_type = models.CharField(max_length=255, blank=True)
    dist_na_dar = models.CharField(max_length=255, blank=True)
    prov_na_dar = models.CharField(max_length=255, blank=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    dist_na_ps = models.CharField(max_length=255, blank=True)
    reg_unama_na_dar = models.CharField(max_length=255, blank=True)
    test2 = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_admbnda_adm2'
    def __unicode__(self):
        return self.dist_na_en     

class AfgAdmbndaInt(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True)
    name_en_short = models.CharField(max_length=255, blank=True)
    names_ps = models.CharField(max_length=255, blank=True)
    name_prs = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_admbnda_int'
    def __unicode__(self):
        return self.name_en      

class AfgAdmbndlAdm1(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    fid_afg_admbnda_adm1_50000_agcho = models.IntegerField(blank=True, null=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    prov_na_dar = models.CharField(max_length=255, blank=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    reg_unama_na_dar = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_admbndl_adm1'
    def __unicode__(self):
        return self.prov_na_en        

class AfgAdmbndlAdm2(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    unit_type = models.CharField(max_length=255, blank=True)
    dist_na_dar = models.CharField(max_length=255, blank=True)
    prov_na_dar = models.CharField(max_length=255, blank=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    dist_na_ps = models.CharField(max_length=255, blank=True)
    reg_unama_na_dar = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_admbndl_adm2'
    def __unicode__(self):
        return self.dist_na_en     

class AfgAdmbndlInt(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_admbndl_int'
    def __unicode__(self):
        return self.name    

class AfgAirdrma(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(dim=3, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    nameshort = models.CharField(max_length=255, blank=True)
    namelong = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    icao = models.CharField(max_length=255, blank=True)
    iata = models.CharField(max_length=255, blank=True)
    apttype = models.CharField(max_length=255, blank=True)
    aptclass = models.CharField(max_length=255, blank=True)
    authority = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    rwpaved = models.CharField(max_length=255, blank=True)
    rwlengthm = models.IntegerField(blank=True, null=True)
    elevm = models.IntegerField(blank=True, null=True)
    humuse = models.CharField(max_length=255, blank=True)
    humoperate = models.CharField(max_length=255, blank=True)
    locprecisi = models.CharField(max_length=255, blank=True)
    iso3 = models.CharField(max_length=255, blank=True)
    lastcheckd = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True)
    createdate = models.DateTimeField(blank=True, null=True)
    updatedate = models.DateTimeField(blank=True, null=True)
    adjusted_by = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_airdrma'
    def __unicode__(self):
        return self.name      

class AfgAirdrmp(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(dim=3, blank=True, null=True)
    nameshort = models.CharField(max_length=255, blank=True)
    namelong = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    icao = models.CharField(max_length=255, blank=True)
    iata = models.CharField(max_length=255, blank=True)
    apttype = models.CharField(max_length=255, blank=True)
    aptclass = models.CharField(max_length=255, blank=True)
    authority = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    rwpaved = models.CharField(max_length=255, blank=True)
    rwlengthm = models.IntegerField(blank=True, null=True)
    rwlengthf = models.IntegerField(blank=True, null=True)
    elevm = models.IntegerField(blank=True, null=True)
    humuse = models.CharField(max_length=255, blank=True)
    humoperate = models.CharField(max_length=255, blank=True)
    locprecisi = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    iso3 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    lastcheckd = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    createdate = models.DateTimeField(blank=True, null=True)
    updatedate = models.DateTimeField(blank=True, null=True)
    geonameid = models.IntegerField(blank=True, null=True)
    adjusted_by = models.CharField(max_length=255, blank=True)
    prov_code = models.CharField(max_length=20, blank=True)
    dist_code = models.CharField(max_length=20, blank=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_airdrmp'
    def __unicode__(self):
        return self.namelong      

class AfgShedaLvl4(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_sheda_lvl4'

class AfgBasinLvl4GlofasPoint(models.Model):
    gid = models.IntegerField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    wcmwf_lat = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    wcmwf_lon = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    shape_leng = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_basin_lvl4_glofas_point'

class AfgCapaAdm1ItsProvc(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_adm1_its_provc'

class AfgCapaAdm1NearestProvc(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_adm1_nearest_provc'

class AfgCapaAdm2NearestDistrictc(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_adm2_nearest_districtc'

class AfgCapaAirdrm(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_airdrm'

class AfgCapaGsmcvr(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    gsm_coverage = models.CharField(max_length=255, blank=True)
    gsm_coverage_population = models.FloatField(blank=True, null=True)
    gsm_coverage_area_sqm = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_gsmcvr'

class AfgCapaHltfacTier1(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_hltfac_tier1'

class AfgCapaHltfacTier2(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_hltfac_tier2'

class AfgCapaHltfacTier3(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_hltfac_tier3'

class AfgCapaHltfacTierall(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    facilities_name = models.CharField(max_length=255, blank=True)
    time = models.CharField(max_length=255, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_capa_hltfac_tierall'

class AfgCaptAdm1ItsProvcImmap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_adm1_its_provc_immap'

class AfgCaptAdm1NearestProvcImmap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_adm1_nearest_provc_immap'

class AfgCaptAdm2NearestDistrictcImmap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_adm2_nearest_districtc_immap'

class AfgCaptAirdrmImmap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_airdrm_immap'

class AfgCaptGmscvr(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    vuid = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    gsm_coverage = models.CharField(max_length=255, blank=True)
    frequency = models.IntegerField(blank=True, null=True)
    gsm_coverage_population = models.FloatField(blank=True, null=True)
    gsm_coverage_area_sqm = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_gmscvr'

class AfgCaptHltfacTier1Immap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_hltfac_tier1_immap'

class AfgCaptHltfacTier2Immap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_hltfac_tier2_immap'

class AfgCaptHltfacTier3Immap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_hltfac_tier3_immap'

class AfgCaptHltfacTierallImmap(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    facilities_name = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    area_sqm = models.FloatField(blank=True, null=True)
    sum_area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_hltfac_tierall_immap'

class AfgCaptPpl(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    vil_uid = models.CharField(max_length=50, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    distance_to_road = models.IntegerField(blank=True, null=True)
    time_to_road = models.IntegerField(blank=True, null=True)
    airdrm_id = models.IntegerField(blank=True, null=True)
    airdrm_dist = models.IntegerField(blank=True, null=True)
    airdrm_time = models.IntegerField(blank=True, null=True)
    ppl_provc_vuid = models.CharField(max_length=50, blank=True)
    ppl_provc_dist = models.IntegerField(blank=True, null=True)
    ppl_provc_time = models.IntegerField(blank=True, null=True)
    ppl_provc_its_vuid = models.CharField(max_length=50, blank=True)
    ppl_provc_its_dist = models.IntegerField(blank=True, null=True)
    ppl_provc_its_time = models.IntegerField(blank=True, null=True)
    ppl_distc_vuid = models.CharField(max_length=50, blank=True)
    ppl_distc_dist = models.IntegerField(blank=True, null=True)
    ppl_distc_time = models.IntegerField(blank=True, null=True)
    ppl_distc_its_vuid = models.CharField(max_length=50, blank=True)
    ppl_distc_its_dist = models.IntegerField(blank=True, null=True)
    ppl_distc_its_time = models.IntegerField(blank=True, null=True)
    hltfac_tier1_id = models.IntegerField(blank=True, null=True)
    hltfac_tier1_dist = models.IntegerField(blank=True, null=True)
    hltfac_tier1_time = models.IntegerField(blank=True, null=True)
    hltfac_tier2_id = models.IntegerField(blank=True, null=True)
    hltfac_tier2_dist = models.IntegerField(blank=True, null=True)
    hltfac_tier2_time = models.IntegerField(blank=True, null=True)
    hltfac_tier3_id = models.IntegerField(blank=True, null=True)
    hltfac_tier3_dist = models.IntegerField(blank=True, null=True)
    hltfac_tier3_time = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_capt_ppl'

class AfgFaultslUnkCafd(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    faultid = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_faultsl_unk_cafd'

class AfgFaultslUnkUsgs(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    data = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_faultsl_unk_usgs'

class AfgGeologyTecta(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_geology_tecta'

class AfgHltfac(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    facility_id = models.FloatField(blank=True, null=True)
    vilicode = models.CharField(max_length=50, blank=True)
    facility_name = models.CharField(max_length=255, blank=True)
    facility_name_dari = models.CharField(max_length=255, blank=True)
    facility_name_pashto = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    location_dari = models.CharField(max_length=255, blank=True)
    location_pashto = models.CharField(max_length=255, blank=True)
    facilitytype = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    activestatus = models.CharField(max_length=255, blank=True)
    date_established = models.DateTimeField(blank=True, null=True)
    subimplementer = models.CharField(max_length=255, blank=True)
    locationsource = models.CharField(max_length=255, blank=True)
    moph = models.CharField(max_length=250, blank=True)
    hproreply = models.CharField(max_length=250, blank=True)
    facility_types_description = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=250, blank=True)
    prov_na_en = models.CharField(max_length=250, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    hpro_facilitytypes_description = models.CharField(max_length=250, blank=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_hltfac'

class AfgLndcrva(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    lccsuslb = models.CharField(max_length=255, blank=True)
    lccsperc = models.CharField(max_length=255, blank=True)
    basin_id = models.FloatField(blank=True, null=True)
    area_sqm = models.FloatField(blank=True, null=True)
    aggcode_simplified = models.CharField(max_length=255, blank=True)
    agg_simplified_description = models.CharField(max_length=255, blank=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.IntegerField(blank=True, null=True)
    area_buildup_assoc = models.CharField(max_length=255, blank=True)
    vuid = models.CharField(max_length=255, blank=True)
    lccs_main_description = models.CharField(max_length=255, blank=True)
    lccs_sub_description = models.CharField(max_length=255, blank=True)
    lccsuslb_simplified = models.CharField(max_length=255, blank=True)
    lccs_aggregated = models.CharField(max_length=255, blank=True)
    aggcode = models.CharField(max_length=255, blank=True)
    vuid_buildings = models.FloatField(blank=True, null=True)
    vuid_population = models.FloatField(blank=True, null=True)
    vuid_pop_per_building = models.FloatField(blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True)
    type_settlement = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_lndcrva'

class AfgLndcrvaCity(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    osm_id = models.CharField(max_length=255, blank=True)
    code = models.IntegerField(blank=True, null=True)
    fclass = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_lndcrva_city'

class AfgLndcrvaSimplified(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    lccsperc = models.CharField(max_length=255, blank=True)
    aggcode = models.CharField(max_length=255, blank=True)
    aggcode_simplified = models.CharField(max_length=255, blank=True)
    agg_simplified_description = models.CharField(max_length=255, blank=True)
    vuid = models.CharField(max_length=255, blank=True)
    vuid_population_landscan = models.IntegerField(blank=True, null=True)
    vuid_area_sqm = models.FloatField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_sqm = models.FloatField(blank=True, null=True)
    population_misti = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)
    edited_by = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    type_settlement = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    unit_type = models.CharField(max_length=255, blank=True)
    dist_na_dar = models.CharField(max_length=255, blank=True)
    prov_na_dar = models.CharField(max_length=255, blank=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    dist_na_ps = models.CharField(max_length=255, blank=True)
    reg_unama_na_dar = models.CharField(max_length=255, blank=True)
    basin_id = models.FloatField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_lndcrva_simplified'

class AfgLspAffpplp(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=50, blank=True)
    lsi_ku = models.IntegerField(blank=True, null=True)
    ls_s1_wb = models.IntegerField(blank=True, null=True)
    ls_s2_wb = models.IntegerField(blank=True, null=True)
    ls_s3_wb = models.IntegerField(blank=True, null=True)
    lsi_immap = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_lsp_affpplp'

class AfgPoiaBuildings(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    osm_id = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_poia_buildings'

class AfgPoip(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    osm_id = models.FloatField(blank=True, null=True)
    timestamp = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    category_style = models.CharField(max_length=255, blank=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_poip'

class AfgPpla(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    vuidnear = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    vuid_buildings = models.FloatField(blank=True, null=True)
    vuid_population = models.FloatField(blank=True, null=True)
    vuid_pop_per_building = models.FloatField(blank=True, null=True)
    name_local = models.CharField(max_length=255, blank=True)
    name_alternative_en = models.CharField(max_length=255, blank=True)
    name_local_confidence = models.CharField(max_length=255, blank=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    area_sqm = models.FloatField(blank=True, null=True)
    type_settlement = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    pplp_point_x = models.FloatField(blank=True, null=True)
    pplp_point_y = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_ppla'

class AfgPplaBasin(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    vuidnear = models.CharField(max_length=50, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    area_population = models.FloatField(blank=True, null=True)
    area_buildings = models.FloatField(blank=True, null=True)
    area_sqm = models.IntegerField(blank=True, null=True)
    basin_id = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    vuid_buildings = models.FloatField(blank=True, null=True)
    vuid_population = models.FloatField(blank=True, null=True)
    vuid_pop_per_building = models.FloatField(blank=True, null=True)
    name_local = models.CharField(max_length=255, blank=True)
    name_alternative_en = models.CharField(max_length=255, blank=True)
    name_local_confidence = models.CharField(max_length=255, blank=True)
    type_settlement = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    basinmember_id = models.IntegerField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_ppla_basin'

class AfgPplp(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True)
    vil_uid = models.CharField(max_length=255, blank=True)
    cntr_code = models.IntegerField(blank=True, null=True)
    afg_uid = models.CharField(max_length=255, blank=True)
    language_field = models.CharField(db_column='language_', max_length=255, blank=True) # Field renamed because it ended with '_'.
    lang_code = models.IntegerField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    lat_y = models.FloatField(blank=True, null=True)
    lon_x = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)
    edited_by = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    type_settlement = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code_1 = models.IntegerField(blank=True, null=True)
    unit_type = models.CharField(max_length=255, blank=True)
    dist_na_dar = models.CharField(max_length=255, blank=True)
    prov_na_dar = models.CharField(max_length=255, blank=True)
    reg_unama_na_en = models.CharField(max_length=255, blank=True)
    dist_na_ps = models.CharField(max_length=255, blank=True)
    reg_unama_na_dar = models.CharField(max_length=255, blank=True)
    vuid_area_sqm = models.FloatField(blank=True, null=True)
    vuidnear = models.CharField(max_length=255, blank=True)
    vuid_buildings = models.FloatField(blank=True, null=True)
    vuid_population = models.FloatField(blank=True, null=True)
    vuid_pop_per_building = models.FloatField(blank=True, null=True)
    vuid = models.CharField(max_length=255, blank=True)
    name_local = models.CharField(max_length=255, blank=True)
    name_local_confidence = models.CharField(max_length=255, blank=True)
    name_alternative_en = models.CharField(max_length=255, blank=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_pplp'

class AfgPpltDemographics(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    vuidnear = models.CharField(max_length=50, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=100, blank=True)
    prov_na_en = models.CharField(max_length=100, blank=True)
    prov_code_field = models.IntegerField(db_column='prov_code_', blank=True, null=True) # Field renamed because it ended with '_'.
    partofbuil = models.CharField(max_length=100, blank=True)
    vuid_buildings = models.IntegerField(blank=True, null=True)
    vuid_population = models.IntegerField(blank=True, null=True)
    vuid_male_perc = models.FloatField(blank=True, null=True)
    vuid_female_perc = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True)
    vuid_pop_per_building = models.FloatField(blank=True, null=True)
    m_perc_yrs_0_4 = models.FloatField(blank=True, null=True)
    m_perc_yrs_5_9 = models.FloatField(blank=True, null=True)
    m_perc_yrs_10_14 = models.FloatField(blank=True, null=True)
    m_perc_yrs_15_19 = models.FloatField(blank=True, null=True)
    m_perc_yrs_20_24 = models.FloatField(blank=True, null=True)
    m_perc_yrs_25_29 = models.FloatField(blank=True, null=True)
    m_perc_yrs_30_34 = models.FloatField(blank=True, null=True)
    m_perc_yrs_35_39 = models.FloatField(blank=True, null=True)
    m_perc_yrs_40_44 = models.FloatField(blank=True, null=True)
    m_perc_yrs_45_49 = models.FloatField(blank=True, null=True)
    m_perc_yrs_50_54 = models.FloatField(blank=True, null=True)
    m_perc_yrs_55_59 = models.FloatField(blank=True, null=True)
    m_perc_yrs_60_64 = models.FloatField(blank=True, null=True)
    m_perc_yrs_65_69 = models.FloatField(blank=True, null=True)
    m_perc_yrs_70_74 = models.FloatField(blank=True, null=True)
    m_perc_yrs_75_79 = models.FloatField(blank=True, null=True)
    m_perc_yrs_80pls = models.FloatField(blank=True, null=True)
    f_perc_yrs_0_4 = models.FloatField(blank=True, null=True)
    f_perc_yrs_5_9 = models.FloatField(blank=True, null=True)
    f_perc_yrs_10_14 = models.FloatField(blank=True, null=True)
    f_perc_yrs_15_19 = models.FloatField(blank=True, null=True)
    f_perc_yrs_20_24 = models.FloatField(db_column='f_perc_yrs__20_24', blank=True, null=True) # Field renamed because it contained more than one '_' in a row.
    f_perc_yrs_25_29 = models.FloatField(blank=True, null=True)
    f_perc_yrs_30_34 = models.FloatField(blank=True, null=True)
    f_perc_yrs_35_39 = models.FloatField(blank=True, null=True)
    f_perc_yrs_40_44 = models.FloatField(blank=True, null=True)
    f_perc_yrs_45_49 = models.FloatField(blank=True, null=True)
    f_perc_yrs_50_54 = models.FloatField(blank=True, null=True)
    f_perc_yrs_55_59 = models.FloatField(blank=True, null=True)
    f_perc_yrs_60_64 = models.FloatField(blank=True, null=True)
    f_perc_yrs_65_69 = models.FloatField(blank=True, null=True)
    f_perc_yrs_70_74 = models.FloatField(blank=True, null=True)
    f_perc_yrs_75_79 = models.FloatField(blank=True, null=True)
    f_perc_yrs_80pls = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'afg_pplt_demographics'

class AfgRafUnkIom(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    no = models.IntegerField(blank=True, null=True)
    incident_date = models.DateTimeField(blank=True, null=True)
    disaster_type = models.CharField(max_length=255, blank=True)
    rafno = models.CharField(max_length=255, blank=True)
    assessment_date = models.DateTimeField(blank=True, null=True)
    msraf_status = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    village_or_nahya = models.CharField(max_length=255, blank=True)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    numberofhouseholds = models.IntegerField(blank=True, null=True)
    numberoffamilies = models.IntegerField(blank=True, null=True)
    numberofidps = models.IntegerField(blank=True, null=True)
    totalpopulation = models.IntegerField(blank=True, null=True)
    affectedfamilies = models.IntegerField(blank=True, null=True)
    province_1 = models.CharField(max_length=255, blank=True)
    district_1 = models.CharField(max_length=255, blank=True)
    village = models.CharField(max_length=255, blank=True)
    nodamaged = models.CharField(max_length=255, blank=True)
    moderatelydamaged = models.IntegerField(blank=True, null=True)
    severelydamaged = models.IntegerField(blank=True, null=True)
    completelydestroyed = models.IntegerField(blank=True, null=True)
    affected_individuals = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    injuried = models.IntegerField(blank=True, null=True)
    missing = models.IntegerField(blank=True, null=True)
    long_1 = models.FloatField(blank=True, null=True)
    lat_1 = models.FloatField(blank=True, null=True)
    alternativevillagenamemisti = models.CharField(max_length=255, blank=True)
    alternativedistrictname = models.CharField(max_length=255, blank=True)
    misti_vuid = models.CharField(max_length=255, blank=True)
    disastertype = models.CharField(max_length=255, blank=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_raf_unk_iom'

class AfgRdsl(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    avg_slope = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    speedkmh = models.IntegerField(blank=True, null=True)
    type_update = models.CharField(max_length=255, blank=True)
    adjusted_kmh = models.IntegerField(blank=True, null=True)
    priority_class = models.IntegerField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    bridge = models.CharField(max_length=255, blank=True)
    tunnel = models.CharField(max_length=255, blank=True)
    road_length = models.IntegerField(blank=True, null=True)
    builduparea = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_rdsl'

class AfgRiv(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    join_count = models.IntegerField(blank=True, null=True)
    join_cou_1 = models.IntegerField(blank=True, null=True)
    join_cou_2 = models.IntegerField(blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    arcid = models.IntegerField(blank=True, null=True)
    grid_code = models.IntegerField(blank=True, null=True)
    from_node = models.IntegerField(blank=True, null=True)
    to_node = models.IntegerField(blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    idcode = models.IntegerField(blank=True, null=True)
    fnode = models.IntegerField(blank=True, null=True)
    tnode = models.IntegerField(blank=True, null=True)
    strahler = models.IntegerField(blank=True, null=True)
    segment = models.IntegerField(blank=True, null=True)
    shreve = models.IntegerField(blank=True, null=True)
    us_accum = models.FloatField(blank=True, null=True)
    link_type = models.CharField(max_length=255, blank=True)
    riverwidth = models.IntegerField(blank=True, null=True)
    landcover = models.CharField(max_length=255, blank=True)
    vertices = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    flooddepth = models.FloatField(blank=True, null=True)
    riverwid_1 = models.FloatField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_riv'

class AfgShedaLvl2(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(dim=3, blank=True, null=True)
    basinnumbe = models.IntegerField(blank=True, null=True)
    basinname = models.CharField(max_length=255, blank=True)
    area = models.IntegerField(blank=True, null=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_sheda_lvl2'

class AfgShedaLvl3(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(dim=3, blank=True, null=True)
    basinnumbe = models.IntegerField(blank=True, null=True)
    basinname = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_sheda_lvl3'

class AfgUtilWell(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    serial_number = models.FloatField(blank=True, null=True)
    implementing_agency = models.CharField(max_length=255, blank=True)
    donor_name = models.CharField(max_length=255, blank=True)
    date_visited = models.DateTimeField(blank=True, null=True)
    district_name = models.CharField(max_length=255, blank=True)
    village_name = models.CharField(max_length=255, blank=True)
    care_taker_name = models.CharField(max_length=255, blank=True)
    longitude_degree = models.FloatField(blank=True, null=True)
    latitude_degree = models.FloatField(blank=True, null=True)
    water_point_code = models.FloatField(blank=True, null=True)
    year_implented = models.FloatField(blank=True, null=True)
    ec_micros_cm = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    t_c = models.FloatField(blank=True, null=True)
    beneficiaries_families = models.FloatField(blank=True, null=True)
    well_depth_m = models.FloatField(blank=True, null=True)
    well_diameter_cm = models.FloatField(blank=True, null=True)
    static_water_level_m = models.FloatField(blank=True, null=True)
    type_of_system = models.CharField(max_length=255, blank=True)
    maintenance_system_existing = models.CharField(max_length=255, blank=True)
    maintenance_agreement_signed = models.CharField(max_length=255, blank=True)
    mechanic_valveman_trained = models.CharField(max_length=255, blank=True)
    wage_of_mechanic_valveman_paid = models.CharField(max_length=255, blank=True)
    water_user_group_established = models.CharField(max_length=255, blank=True)
    care_taker_selected_trained = models.CharField(max_length=255, blank=True)
    water_management_committee_established = models.FloatField(blank=True, null=True)
    pipe_scheme_conditions = models.CharField(max_length=255, blank=True)
    pipe_scheme_problem = models.CharField(max_length=255, blank=True)
    water_point_working = models.CharField(max_length=255, blank=True)
    water_point_working_with_bucket = models.CharField(max_length=255, blank=True)
    water_point_dry_drawdown = models.CharField(max_length=255, blank=True)
    water_point_collapsed_destroyed = models.CharField(max_length=255, blank=True)
    water_point_plugged_abandoned = models.CharField(max_length=255, blank=True)
    water_point_enclosed = models.CharField(max_length=255, blank=True)
    water_point_concrete_problem = models.CharField(max_length=255, blank=True)
    water_point_pump_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_tap_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_pipeline_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_catchment_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_reservoir_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_solar_pump_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_solar_panel_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_submersible_pump_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_generator_problem = models.CharField(max_length=255, blank=True)
    pipe_scheme_generator_room_problem = models.CharField(max_length=255, blank=True)
    wp_type = models.CharField(max_length=255, blank=True)
    no_maintenance_problem = models.CharField(max_length=255, blank=True)
    community_problem = models.CharField(max_length=255, blank=True)
    mechanic_valveman_problem = models.CharField(max_length=255, blank=True)
    spare_parts_availlability_problem = models.CharField(max_length=255, blank=True)
    original_hp_present = models.CharField(max_length=255, blank=True)
    no_new_hp = models.CharField(max_length=255, blank=True)
    new_hp_from_community = models.CharField(max_length=255, blank=True)
    new_hp_from_ngo_government = models.CharField(max_length=255, blank=True)
    hp_condition = models.CharField(max_length=255, blank=True)
    hp_problem_fixible = models.CharField(max_length=255, blank=True)
    hp_problem_not_fixible = models.CharField(max_length=255, blank=True)
    hp_raising_main_problem = models.CharField(max_length=255, blank=True)
    hp_removed_vandalized = models.CharField(max_length=255, blank=True)
    pump_manufacturer = models.CharField(max_length=255, blank=True)
    pump_code = models.FloatField(blank=True, null=True)
    solar_panel_manufacturer = models.CharField(max_length=255, blank=True)
    pump_type = models.CharField(max_length=255, blank=True)
    flood_risk = models.CharField(max_length=255, blank=True)
    avalanche_risk = models.CharField(max_length=255, blank=True)
    data_source = models.CharField(max_length=255, blank=True)
    basin_id = models.FloatField(blank=True, null=True)
    landcover_description = models.CharField(max_length=255, blank=True)
    vuid = models.CharField(max_length=255, blank=True)
    name_en = models.CharField(max_length=255, blank=True)
    type_settlement = models.CharField(max_length=255, blank=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'afg_util_well'

class AndmaOffice(models.Model):
    gid = models.IntegerField(primary_key=True)
    objectid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    vil_uid = models.CharField(max_length=10, blank=True)
    note = models.CharField(max_length=50, blank=True)
    name_en = models.CharField(max_length=50, blank=True)
    dist_na_en = models.CharField(max_length=50, blank=True)
    prov_na_en = models.CharField(max_length=50, blank=True)
    dist_na_da = models.CharField(max_length=254, blank=True)
    prov_na_da = models.CharField(max_length=254, blank=True)
    dist_na_ps = models.CharField(max_length=254, blank=True)
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'andma_office'

class basinsummary(models.Model):
    basin                                      = models.CharField(max_length=255, blank=False)
    
    # total
    Population                                  = models.FloatField(blank=True, null=True)
    Area                                        = models.FloatField(blank=True, null=True)
    settlements                                 = models.FloatField(blank=True, null=True) 
    
    # landcover total population
    water_body_pop                              = models.FloatField(blank=True, null=True) 
    barren_land_pop                             = models.FloatField(blank=True, null=True)
    built_up_pop                                = models.FloatField(blank=True, null=True)
    fruit_trees_pop                             = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_pop             = models.FloatField(blank=True, null=True)  
    permanent_snow_pop                          = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_pop               = models.FloatField(blank=True, null=True)
    rangeland_pop                               = models.FloatField(blank=True, null=True)
    sandcover_pop                               = models.FloatField(blank=True, null=True)
    vineyards_pop                               = models.FloatField(blank=True, null=True)
    forest_pop                                  = models.FloatField(blank=True, null=True)
    
    # landcover total area
    water_body_area                             = models.FloatField(blank=True, null=True)
    barren_land_area                            = models.FloatField(blank=True, null=True)
    built_up_area                               = models.FloatField(blank=True, null=True) 
    fruit_trees_area                            = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_area            = models.FloatField(blank=True, null=True)
    permanent_snow_area                         = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_area              = models.FloatField(blank=True, null=True)
    rangeland_area                              = models.FloatField(blank=True, null=True) 
    sandcover_area                              = models.FloatField(blank=True, null=True)
    vineyards_area                              = models.FloatField(blank=True, null=True)
    forest_area                                 = models.FloatField(blank=True, null=True)
    
    # Flood Risk Population
    high_risk_population                        = models.FloatField(blank=True, null=True)
    med_risk_population                         = models.FloatField(blank=True, null=True)
    low_risk_population                         = models.FloatField(blank=True, null=True)
    total_risk_population                       = models.FloatField(blank=True, null=True) 
    settlements_at_risk                         = models.FloatField(blank=True, null=True)
    
    # Flood Risk Area
    high_risk_area                              = models.FloatField(blank=True, null=True) 
    med_risk_area                               = models.FloatField(blank=True, null=True)
    low_risk_area                               = models.FloatField(blank=True, null=True)  
    total_risk_area                             = models.FloatField(blank=True, null=True)
    
    # landcover flood risk population
    water_body_pop_risk                         = models.FloatField(blank=True, null=True)
    barren_land_pop_risk                        = models.FloatField(blank=True, null=True) 
    built_up_pop_risk                           = models.FloatField(blank=True, null=True)
    fruit_trees_pop_risk                        = models.FloatField(blank=True, null=True)
    irrigated_agricultural_land_pop_risk        = models.FloatField(blank=True, null=True)    
    permanent_snow_pop_risk                     = models.FloatField(blank=True, null=True) 
    rainfed_agricultural_land_pop_risk          = models.FloatField(blank=True, null=True)
    rangeland_pop_risk                          = models.FloatField(blank=True, null=True) 
    sandcover_pop_risk                          = models.FloatField(blank=True, null=True)
    vineyards_pop_risk                          = models.FloatField(blank=True, null=True)
    forest_pop_risk                             = models.FloatField(blank=True, null=True) 

    # landcover flood risk area
    water_body_area_risk                        = models.FloatField(blank=True, null=True)
    barren_land_area_risk                       = models.FloatField(blank=True, null=True)
    built_up_area_risk                          = models.FloatField(blank=True, null=True)
    fruit_trees_area_risk                       = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_area_risk       = models.FloatField(blank=True, null=True) 
    permanent_snow_area_risk                    = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_area_risk         = models.FloatField(blank=True, null=True)
    rangeland_area_risk                         = models.FloatField(blank=True, null=True)
    sandcover_area_risk                         = models.FloatField(blank=True, null=True)
    vineyards_area_risk                         = models.FloatField(blank=True, null=True)
    forest_area_risk                            = models.FloatField(blank=True, null=True)

    # Avalanche Risk Population
    high_ava_population                         = models.FloatField(blank=True, null=True)
    med_ava_population                          = models.FloatField(blank=True, null=True)
    low_ava_population                          = models.FloatField(blank=True, null=True)    
    total_ava_population                        = models.FloatField(blank=True, null=True)

    # Avalanche Risk Area
    high_ava_area                               = models.FloatField(blank=True, null=True)
    med_ava_area                                = models.FloatField(blank=True, null=True) 
    low_ava_area                                = models.FloatField(blank=True, null=True)
    total_ava_area                              = models.FloatField(blank=True, null=True)

    ### Forecasting Sections  ###
    # --- This section values will be updated every 3 hours --- #

    # River Flood Forecasted Population 
    riverflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    riverflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_pop               = models.FloatField(blank=True, null=True)
    
    # River Flood Forecasted Area
    riverflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_area               = models.FloatField(blank=True, null=True) 
    riverflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_area            = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Flash Flood Forecasted Population
    flashflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True) 
    flashflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)     
    flashflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_flashflood_forecast_pop               = models.FloatField(blank=True, null=True)

    # Flash Flood Forecasted Area
    flashflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    flashflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_area               = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_area            = models.FloatField(blank=True, null=True) 
    total_flashflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Avalanche Forecasted Population
    ava_forecast_low_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_med_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_high_pop                       = models.FloatField(blank=True, null=True)
    total_ava_forecast_pop                      = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'basinsummary'

class CurrentScBasins(models.Model):
    basin = models.FloatField(blank=True, null=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'current_sc_basins'

class DistrictAddSummary(models.Model):
    dist_code = models.CharField(max_length=255)
    hlt_h1 = models.FloatField(blank=True, null=True)
    hlt_h2 = models.FloatField(blank=True, null=True)
    hlt_h3 = models.FloatField(blank=True, null=True)
    hlt_special_hospital = models.FloatField(blank=True, null=True)
    hlt_rehabilitation_center = models.FloatField(blank=True, null=True)
    hlt_maternity_home = models.FloatField(blank=True, null=True)
    hlt_drug_addicted_treatment_center = models.FloatField(blank=True, null=True)
    hlt_chc = models.FloatField(blank=True, null=True)
    hlt_bhc = models.FloatField(blank=True, null=True)
    hlt_shc = models.FloatField(blank=True, null=True)
    hlt_private_clinic = models.FloatField(blank=True, null=True)
    hlt_malaria_center = models.FloatField(blank=True, null=True)
    hlt_mobile_health_team = models.FloatField(blank=True, null=True)
    hlt_other = models.FloatField(blank=True, null=True)
    road_highway = models.FloatField(blank=True, null=True)
    road_primary = models.FloatField(blank=True, null=True)
    road_secondary = models.FloatField(blank=True, null=True)
    road_tertiary = models.FloatField(blank=True, null=True)
    road_residential = models.FloatField(blank=True, null=True)
    road_track = models.FloatField(blank=True, null=True)
    road_path = models.FloatField(blank=True, null=True)
    road_river_crossing = models.FloatField(blank=True, null=True)
    road_bridge = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'district_add_summary'

class districtsummary(models.Model):
    district                                    = models.CharField(max_length=255, blank=False)
    
    # total
    Population                                  = models.FloatField(blank=True, null=True)
    Area                                        = models.FloatField(blank=True, null=True)
    settlements                                 = models.FloatField(blank=True, null=True) 
    
    # landcover total population
    water_body_pop                              = models.FloatField(blank=True, null=True) 
    barren_land_pop                             = models.FloatField(blank=True, null=True)
    built_up_pop                                = models.FloatField(blank=True, null=True)
    fruit_trees_pop                             = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_pop             = models.FloatField(blank=True, null=True)  
    permanent_snow_pop                          = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_pop               = models.FloatField(blank=True, null=True)
    rangeland_pop                               = models.FloatField(blank=True, null=True)
    sandcover_pop                               = models.FloatField(blank=True, null=True)
    vineyards_pop                               = models.FloatField(blank=True, null=True)
    forest_pop                                  = models.FloatField(blank=True, null=True)
    
    # landcover total area
    water_body_area                             = models.FloatField(blank=True, null=True)
    barren_land_area                            = models.FloatField(blank=True, null=True)
    built_up_area                               = models.FloatField(blank=True, null=True) 
    fruit_trees_area                            = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_area            = models.FloatField(blank=True, null=True)
    permanent_snow_area                         = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_area              = models.FloatField(blank=True, null=True)
    rangeland_area                              = models.FloatField(blank=True, null=True) 
    sandcover_area                              = models.FloatField(blank=True, null=True)
    vineyards_area                              = models.FloatField(blank=True, null=True)
    forest_area                                 = models.FloatField(blank=True, null=True)
    
    # Flood Risk Population
    high_risk_population                        = models.FloatField(blank=True, null=True)
    med_risk_population                         = models.FloatField(blank=True, null=True)
    low_risk_population                         = models.FloatField(blank=True, null=True)
    total_risk_population                       = models.FloatField(blank=True, null=True) 
    settlements_at_risk                         = models.FloatField(blank=True, null=True)
    
    # Flood Risk Area
    high_risk_area                              = models.FloatField(blank=True, null=True) 
    med_risk_area                               = models.FloatField(blank=True, null=True)
    low_risk_area                               = models.FloatField(blank=True, null=True)  
    total_risk_area                             = models.FloatField(blank=True, null=True)
    
    # landcover flood risk population
    water_body_pop_risk                         = models.FloatField(blank=True, null=True)
    barren_land_pop_risk                        = models.FloatField(blank=True, null=True) 
    built_up_pop_risk                           = models.FloatField(blank=True, null=True)
    fruit_trees_pop_risk                        = models.FloatField(blank=True, null=True)
    irrigated_agricultural_land_pop_risk        = models.FloatField(blank=True, null=True)    
    permanent_snow_pop_risk                     = models.FloatField(blank=True, null=True) 
    rainfed_agricultural_land_pop_risk          = models.FloatField(blank=True, null=True)
    rangeland_pop_risk                          = models.FloatField(blank=True, null=True) 
    sandcover_pop_risk                          = models.FloatField(blank=True, null=True)
    vineyards_pop_risk                          = models.FloatField(blank=True, null=True)
    forest_pop_risk                             = models.FloatField(blank=True, null=True) 

    # landcover flood risk area
    water_body_area_risk                        = models.FloatField(blank=True, null=True)
    barren_land_area_risk                       = models.FloatField(blank=True, null=True)
    built_up_area_risk                          = models.FloatField(blank=True, null=True)
    fruit_trees_area_risk                       = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_area_risk       = models.FloatField(blank=True, null=True) 
    permanent_snow_area_risk                    = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_area_risk         = models.FloatField(blank=True, null=True)
    rangeland_area_risk                         = models.FloatField(blank=True, null=True)
    sandcover_area_risk                         = models.FloatField(blank=True, null=True)
    vineyards_area_risk                         = models.FloatField(blank=True, null=True)
    forest_area_risk                            = models.FloatField(blank=True, null=True)

    # Avalanche Risk Population
    high_ava_population                         = models.FloatField(blank=True, null=True)
    med_ava_population                          = models.FloatField(blank=True, null=True)
    low_ava_population                          = models.FloatField(blank=True, null=True)    
    total_ava_population                        = models.FloatField(blank=True, null=True)

    # Avalanche Risk Area
    high_ava_area                               = models.FloatField(blank=True, null=True)
    med_ava_area                                = models.FloatField(blank=True, null=True) 
    low_ava_area                                = models.FloatField(blank=True, null=True)
    total_ava_area                              = models.FloatField(blank=True, null=True)

    ### Forecasting Sections  ###
    # --- This section values will be updated every 3 hours --- #

    # River Flood Forecasted Population 
    riverflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    riverflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_pop               = models.FloatField(blank=True, null=True)
    
    # River Flood Forecasted Area
    riverflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_area               = models.FloatField(blank=True, null=True) 
    riverflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_area            = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Flash Flood Forecasted Population
    flashflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True) 
    flashflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)     
    flashflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_flashflood_forecast_pop               = models.FloatField(blank=True, null=True)

    # Flash Flood Forecasted Area
    flashflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    flashflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_area               = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_area            = models.FloatField(blank=True, null=True) 
    total_flashflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Avalanche Forecasted Population
    ava_forecast_low_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_med_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_high_pop                       = models.FloatField(blank=True, null=True)
    total_ava_forecast_pop                      = models.FloatField(blank=True, null=True)

    sand_dunes_pop                              = models.FloatField(blank=True, null=True)
    sand_dunes_pop_risk                         = models.FloatField(blank=True, null=True)
    sand_dunes_area                             = models.FloatField(blank=True, null=True)
    sand_dunes_area_risk                        = models.FloatField(blank=True, null=True)

    total_buildings                             = models.FloatField(blank=True, null=True)
    total_risk_buildings                        = models.FloatField(blank=True, null=True)

    high_ava_buildings                          = models.FloatField(blank=True, null=True)
    med_ava_buildings                           = models.FloatField(blank=True, null=True)
    total_ava_buildings                         = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'districtsummary'
        
class EventdataHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    api = models.CharField(max_length=255, blank=True)
    eventdata = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = True
        db_table = 'eventdata_history'

class forecastedLastUpdate(models.Model):
    datadate = models.DateTimeField(blank=False, null=False)
    forecasttype = models.CharField(max_length=50, blank=False) 
    class Meta:
        managed = True
        db_table = 'forecastedlastupdate'

class Forcastedvalue(models.Model):
    basin = models.ForeignKey(AfgShedaLvl4, related_name='basins')
    datadate = models.DateTimeField(blank=False, null=False)
    forecasttype = models.CharField(max_length=50, blank=False)
    riskstate = models.IntegerField(blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'forcastedvalue'

class LandcoverDescription(models.Model):
    code = models.CharField(max_length=255, blank=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = True
        db_table = 'landcover_description'

class OasisSettlements(models.Model):
    gid = models.IntegerField(primary_key=True)
    type_settlement = models.CharField(max_length=20, blank=True)
    source = models.CharField(max_length=50, blank=True)
    x = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    y = models.DecimalField(max_digits=30, decimal_places=20, blank=True, null=True)
    prov_na_en = models.CharField(max_length=50, blank=True)
    dist_na_en = models.CharField(max_length=50, blank=True)
    un_reg = models.CharField(max_length=50, blank=True)
    isaf_rc = models.CharField(max_length=50, blank=True)
    name_en = models.CharField(max_length=200, blank=True)
    vil_uid = models.IntegerField(blank=True, null=True)
    anso_reg = models.CharField(max_length=50, blank=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    prov_code = models.IntegerField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'oasis_settlements'

class ProvinceAddSummary(models.Model):
    prov_code = models.CharField(max_length=255)
    hlt_h1 = models.FloatField(blank=True, null=True)
    hlt_h2 = models.FloatField(blank=True, null=True)
    hlt_h3 = models.FloatField(blank=True, null=True)
    hlt_special_hospital = models.FloatField(blank=True, null=True)
    hlt_rehabilitation_center = models.FloatField(blank=True, null=True)
    hlt_maternity_home = models.FloatField(blank=True, null=True)
    hlt_drug_addicted_treatment_center = models.FloatField(blank=True, null=True)
    hlt_chc = models.FloatField(blank=True, null=True)
    hlt_bhc = models.FloatField(blank=True, null=True)
    hlt_shc = models.FloatField(blank=True, null=True)
    hlt_private_clinic = models.FloatField(blank=True, null=True)
    hlt_malaria_center = models.FloatField(blank=True, null=True)
    hlt_mobile_health_team = models.FloatField(blank=True, null=True)
    hlt_other = models.FloatField(blank=True, null=True)
    road_highway = models.FloatField(blank=True, null=True)
    road_primary = models.FloatField(blank=True, null=True)
    road_secondary = models.FloatField(blank=True, null=True)
    road_tertiary = models.FloatField(blank=True, null=True)
    road_residential = models.FloatField(blank=True, null=True)
    road_track = models.FloatField(blank=True, null=True)
    road_path = models.FloatField(blank=True, null=True)
    road_river_crossing = models.FloatField(blank=True, null=True)
    road_bridge = models.FloatField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'province_add_summary'

class provincesummary(models.Model):
    id = models.IntegerField(primary_key=True)
    province                                    = models.CharField(max_length=255, blank=False)
    
    # total
    Population                                  = models.FloatField(blank=True, null=True)
    Area                                        = models.FloatField(blank=True, null=True)
    settlements                                 = models.FloatField(blank=True, null=True) 
    
    # landcover total population
    water_body_pop                              = models.FloatField(blank=True, null=True) 
    barren_land_pop                             = models.FloatField(blank=True, null=True)
    built_up_pop                                = models.FloatField(blank=True, null=True)
    fruit_trees_pop                             = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_pop             = models.FloatField(blank=True, null=True)  
    permanent_snow_pop                          = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_pop               = models.FloatField(blank=True, null=True)
    rangeland_pop                               = models.FloatField(blank=True, null=True)
    sandcover_pop                               = models.FloatField(blank=True, null=True)
    vineyards_pop                               = models.FloatField(blank=True, null=True)
    forest_pop                                  = models.FloatField(blank=True, null=True)
    
    # landcover total area
    water_body_area                             = models.FloatField(blank=True, null=True)
    barren_land_area                            = models.FloatField(blank=True, null=True)
    built_up_area                               = models.FloatField(blank=True, null=True) 
    fruit_trees_area                            = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_area            = models.FloatField(blank=True, null=True)
    permanent_snow_area                         = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_area              = models.FloatField(blank=True, null=True)
    rangeland_area                              = models.FloatField(blank=True, null=True) 
    sandcover_area                              = models.FloatField(blank=True, null=True)
    vineyards_area                              = models.FloatField(blank=True, null=True)
    forest_area                                 = models.FloatField(blank=True, null=True)
    
    # Flood Risk Population
    high_risk_population                        = models.FloatField(blank=True, null=True)
    med_risk_population                         = models.FloatField(blank=True, null=True)
    low_risk_population                         = models.FloatField(blank=True, null=True)
    total_risk_population                       = models.FloatField(blank=True, null=True) 
    settlements_at_risk                         = models.FloatField(blank=True, null=True)
    
    # Flood Risk Area
    high_risk_area                              = models.FloatField(blank=True, null=True) 
    med_risk_area                               = models.FloatField(blank=True, null=True)
    low_risk_area                               = models.FloatField(blank=True, null=True)  
    total_risk_area                             = models.FloatField(blank=True, null=True)
    
    # landcover flood risk population
    water_body_pop_risk                         = models.FloatField(blank=True, null=True)
    barren_land_pop_risk                        = models.FloatField(blank=True, null=True) 
    built_up_pop_risk                           = models.FloatField(blank=True, null=True)
    fruit_trees_pop_risk                        = models.FloatField(blank=True, null=True)
    irrigated_agricultural_land_pop_risk        = models.FloatField(blank=True, null=True)    
    permanent_snow_pop_risk                     = models.FloatField(blank=True, null=True) 
    rainfed_agricultural_land_pop_risk          = models.FloatField(blank=True, null=True)
    rangeland_pop_risk                          = models.FloatField(blank=True, null=True) 
    sandcover_pop_risk                          = models.FloatField(blank=True, null=True)
    vineyards_pop_risk                          = models.FloatField(blank=True, null=True)
    forest_pop_risk                             = models.FloatField(blank=True, null=True) 

    # landcover flood risk area
    water_body_area_risk                        = models.FloatField(blank=True, null=True)
    barren_land_area_risk                       = models.FloatField(blank=True, null=True)
    built_up_area_risk                          = models.FloatField(blank=True, null=True)
    fruit_trees_area_risk                       = models.FloatField(blank=True, null=True) 
    irrigated_agricultural_land_area_risk       = models.FloatField(blank=True, null=True) 
    permanent_snow_area_risk                    = models.FloatField(blank=True, null=True)
    rainfed_agricultural_land_area_risk         = models.FloatField(blank=True, null=True)
    rangeland_area_risk                         = models.FloatField(blank=True, null=True)
    sandcover_area_risk                         = models.FloatField(blank=True, null=True)
    vineyards_area_risk                         = models.FloatField(blank=True, null=True)
    forest_area_risk                            = models.FloatField(blank=True, null=True)

    # Avalanche Risk Population
    high_ava_population                         = models.FloatField(blank=True, null=True)
    med_ava_population                          = models.FloatField(blank=True, null=True)
    low_ava_population                          = models.FloatField(blank=True, null=True)    
    total_ava_population                        = models.FloatField(blank=True, null=True)

    # Avalanche Risk Area
    high_ava_area                               = models.FloatField(blank=True, null=True)
    med_ava_area                                = models.FloatField(blank=True, null=True) 
    low_ava_area                                = models.FloatField(blank=True, null=True)
    total_ava_area                              = models.FloatField(blank=True, null=True)

    ### Forecasting Sections  ###
    # --- This section values will be updated every 3 hours --- #

    # River Flood Forecasted Population 
    riverflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    riverflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_pop               = models.FloatField(blank=True, null=True)
    
    # River Flood Forecasted Area
    riverflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_area               = models.FloatField(blank=True, null=True) 
    riverflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_area            = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Flash Flood Forecasted Population
    flashflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True) 
    flashflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)     
    flashflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_flashflood_forecast_pop               = models.FloatField(blank=True, null=True)

    # Flash Flood Forecasted Area
    flashflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    flashflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_area               = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_area            = models.FloatField(blank=True, null=True) 
    total_flashflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Avalanche Forecasted Population
    ava_forecast_low_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_med_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_high_pop                       = models.FloatField(blank=True, null=True)
    total_ava_forecast_pop                      = models.FloatField(blank=True, null=True)

    sand_dunes_pop                              = models.FloatField(blank=True, null=True)
    sand_dunes_pop_risk                         = models.FloatField(blank=True, null=True)
    sand_dunes_area                             = models.FloatField(blank=True, null=True)
    sand_dunes_area_risk                        = models.FloatField(blank=True, null=True)

    total_buildings                             = models.FloatField(blank=True, null=True)
    total_risk_buildings                        = models.FloatField(blank=True, null=True)

    high_ava_buildings                          = models.FloatField(blank=True, null=True)
    med_ava_buildings                           = models.FloatField(blank=True, null=True)
    total_ava_buildings                         = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'provincesummary'

class SlopeHospLndcvrNofldNoavaNouxo4KmsqGonogo(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    dist_code = models.IntegerField(blank=True, null=True)
    dist_na_en = models.CharField(max_length=255, blank=True)
    prov_na_en = models.CharField(max_length=255, blank=True)
    prov_code = models.IntegerField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    buff_dist = models.FloatField(blank=True, null=True)
    orig_fid = models.IntegerField(blank=True, null=True)
    gonogo = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'slope_hosp_lndcvr_nofld_noava_nouxo__4kmsq_gonogo'

class tempCurrentSC(models.Model):
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'temp_current_sc'

class villagesummary(models.Model):
    id = models.IntegerField(primary_key=True)
    vuid                                       = models.CharField(max_length=255, blank=False)
    basin                                      = models.CharField(max_length=255, blank=False)
    ### Forecasting Sections  ###
    # --- This section values will be updated every 3 hours --- #

    # River Flood Forecasted Population 
    riverflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    riverflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_pop               = models.FloatField(blank=True, null=True)
    
    # River Flood Forecasted Area
    riverflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    riverflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    riverflood_forecast_high_area               = models.FloatField(blank=True, null=True) 
    riverflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True) 
    riverflood_forecast_extreme_area            = models.FloatField(blank=True, null=True)
    total_riverflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Flash Flood Forecasted Population
    flashflood_forecast_verylow_pop             = models.FloatField(blank=True, null=True) 
    flashflood_forecast_low_pop                 = models.FloatField(blank=True, null=True)     
    flashflood_forecast_med_pop                 = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_pop                = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_pop            = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_pop             = models.FloatField(blank=True, null=True)
    total_flashflood_forecast_pop               = models.FloatField(blank=True, null=True)

    # Flash Flood Forecasted Area
    flashflood_forecast_verylow_area            = models.FloatField(blank=True, null=True)
    flashflood_forecast_low_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_med_area                = models.FloatField(blank=True, null=True)
    flashflood_forecast_high_area               = models.FloatField(blank=True, null=True)
    flashflood_forecast_veryhigh_area           = models.FloatField(blank=True, null=True)
    flashflood_forecast_extreme_area            = models.FloatField(blank=True, null=True) 
    total_flashflood_forecast_area              = models.FloatField(blank=True, null=True) 

    # Avalanche Forecasted Population
    ava_forecast_low_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_med_pop                        = models.FloatField(blank=True, null=True) 
    ava_forecast_high_pop                       = models.FloatField(blank=True, null=True)
    total_ava_forecast_pop                      = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'villagesummary'

class WrlAdmbndaInt(models.Model):
    ogc_fid = models.IntegerField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True)
    continent = models.CharField(max_length=255, blank=True)
    name_prs = models.CharField(max_length=255, blank=True)
    name_ps = models.CharField(max_length=255, blank=True)
    shape_length = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    objects = models.GeoManager()
    class Meta:
        managed = True
        db_table = 'wrl_admbnda_int'
