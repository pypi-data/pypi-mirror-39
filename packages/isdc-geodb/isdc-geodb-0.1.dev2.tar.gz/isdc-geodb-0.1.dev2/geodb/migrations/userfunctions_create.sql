-- Function: public.get_merge_glofas_gfms(date, character varying, integer, character varying)

-- DROP FUNCTION public.get_merge_glofas_gfms(date, character varying, integer, character varying);

CREATE OR REPLACE FUNCTION public.get_merge_glofas_gfms(IN p_date date, IN p_filter character varying, IN p_code integer, IN p_spatial character varying)
  RETURNS TABLE(basin_id bigint, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision, extreme_high double precision, extreme_med double precision, extreme_low double precision, veryhigh_high double precision, veryhigh_med double precision, veryhigh_low double precision, high_high double precision, high_med double precision, high_low double precision, moderate_high double precision, moderate_med double precision, moderate_low double precision, low_high double precision, low_med double precision, low_low double precision, verylow_high double precision, verylow_med double precision, verylow_low double precision, extreme_area double precision, veryhigh_area double precision, high_area double precision, moderate_area double precision, low_area double precision, verylow_area double precision, extreme_buildings double precision, veryhigh_buildings double precision, high_buildings double precision, moderate_buildings double precision, low_buildings double precision, verylow_buildings double precision, extreme_high_buildings double precision, extreme_med_buildings double precision, extreme_low_buildings double precision, veryhigh_high_buildings double precision, veryhigh_med_buildings double precision, veryhigh_low_buildings double precision, high_high_buildings double precision, high_med_buildings double precision, high_low_buildings double precision, moderate_high_buildings double precision, moderate_med_buildings double precision, moderate_low_buildings double precision, low_high_buildings double precision, low_med_buildings double precision, low_low_buildings double precision, verylow_high_buildings double precision, verylow_med_buildings double precision, verylow_low_buildings double precision) AS
$BODY$
DECLARE 
    var_r record;
DECLARE temp double precision;

BEGIN

   FOR var_r IN(select 
	a.*,
	b.basin_id as gfms_basin_id,
	b.gfms_verylow_pop,
	b.gfms_low_pop,
	b.gfms_med_pop,
	b.gfms_high_pop,
	b.gfms_veryhigh_pop,
	b.gfms_extreme_pop,
	b.gfms_verylow_area,
	b.gfms_low_area,
	b.gfms_med_area,
	b.gfms_high_area,
	b.gfms_veryhigh_area,
	b.gfms_extreme_area,
	b.gfms_verylow_buildings,
	b.gfms_low_buildings,
	b.gfms_med_buildings,
	b.gfms_high_buildings,
	b.gfms_veryhigh_buildings,
	b.gfms_extreme_buildings,
	
	b.gfms_verylow_low_pop,
	b.gfms_verylow_med_pop,
	b.gfms_verylow_high_pop,
	b.gfms_low_low_pop,
	b.gfms_low_med_pop,
	b.gfms_low_high_pop,
	b.gfms_med_low_pop,
	b.gfms_med_med_pop,
	b.gfms_med_high_pop,
	b.gfms_high_low_pop,
	b.gfms_high_med_pop,
	b.gfms_high_high_pop,
	b.gfms_veryhigh_low_pop,
	b.gfms_veryhigh_med_pop,
	b.gfms_veryhigh_high_pop,
	b.gfms_extreme_low_pop,
	b.gfms_extreme_med_pop,
	b.gfms_extreme_high_pop,

	b.gfms_verylow_low_buildings,
	b.gfms_verylow_med_buildings,
	b.gfms_verylow_high_buildings,
	b.gfms_low_low_buildings,
	b.gfms_low_med_buildings,
	b.gfms_low_high_buildings,
	b.gfms_med_low_buildings,
	b.gfms_med_med_buildings,
	b.gfms_med_high_buildings,
	b.gfms_high_low_buildings,
	b.gfms_high_med_buildings,
	b.gfms_high_high_buildings,
	b.gfms_veryhigh_low_buildings,
	b.gfms_veryhigh_med_buildings,
	b.gfms_veryhigh_high_buildings,
	b.gfms_extreme_low_buildings,
	b.gfms_extreme_med_buildings,
	b.gfms_extreme_high_buildings
	
	from afg_sheda_lvl4 c
	left join get_gfms_query(p_date,p_filter,p_code,p_spatial) b on b.basin_id=c.value
	left join get_glofas(p_date-1,p_filter,p_code,p_spatial) a on a.basin_id=c.value)  
     LOOP
	IF var_r.basin_id IS NOT NULL THEN
		basin_id := var_r.basin_id; 

		extreme := var_r.extreme;
		veryhigh := var_r.veryhigh;
		high := var_r.high;
		moderate := var_r.moderate;
		low := var_r.low;
		verylow := var_r.verylow;

		extreme_high := var_r.extreme_high;
		extreme_med := var_r.extreme_med;
		extreme_low := var_r.extreme_low;
		veryhigh_high := var_r.veryhigh_high;
		veryhigh_med := var_r.veryhigh_med;
		veryhigh_low := var_r.veryhigh_low;
		high_high := var_r.high_high;
		high_med := var_r.high_med;
		high_low := var_r.high_low;
		moderate_high := var_r.moderate_high;
		moderate_med := var_r.moderate_med;
		moderate_low := var_r.moderate_low;
		low_high := var_r.low_high;
		low_med := var_r.low_med;
		low_low := var_r.low_low;
		verylow_high := var_r.verylow_high;
		verylow_med := var_r.verylow_med;
		verylow_low := var_r.verylow_low;

		extreme_area := var_r.extreme_area;
		veryhigh_area := var_r.veryhigh_area;
		high_area := var_r.high_area;
		moderate_area := var_r.moderate_area;
		low_area := var_r.low_area;
		verylow_area := var_r.verylow_area;

		extreme_buildings := var_r.extreme_buildings;
		veryhigh_buildings := var_r.veryhigh_buildings;
		high_buildings := var_r.high_buildings;
		moderate_buildings := var_r.moderate_buildings;
		low_buildings := var_r.low_buildings;
		verylow_buildings := var_r.verylow_buildings;

		extreme_high_buildings := var_r.extreme_high_buildings;
		extreme_med_buildings := var_r.extreme_med_buildings;
		extreme_low_buildings := var_r.extreme_low_buildings;
		veryhigh_high_buildings := var_r.veryhigh_high_buildings;
		veryhigh_med_buildings := var_r.veryhigh_med_buildings;
		veryhigh_low_buildings := var_r.veryhigh_low_buildings;
		high_high_buildings := var_r.high_high_buildings;
		high_med_buildings := var_r.high_med_buildings;
		high_low_buildings := var_r.high_low_buildings;
		moderate_high_buildings := var_r.moderate_high_buildings;
		moderate_med_buildings := var_r.moderate_med_buildings;
		moderate_low_buildings := var_r.moderate_low_buildings;
		low_high_buildings := var_r.low_high_buildings;
		low_med_buildings := var_r.low_med_buildings;
		low_low_buildings := var_r.low_low_buildings;
		verylow_high_buildings := var_r.verylow_high_buildings;
		verylow_med_buildings := var_r.verylow_med_buildings;
		verylow_low_buildings := var_r.verylow_low_buildings;

	ELSE
		basin_id := var_r.gfms_basin_id; 

		extreme := var_r.gfms_extreme_pop;
		veryhigh := var_r.gfms_veryhigh_pop;
		high := var_r.gfms_high_pop;
		moderate := var_r.gfms_med_pop;
		low := var_r.gfms_low_pop;
		verylow := var_r.gfms_verylow_pop;

		extreme_high := var_r.gfms_extreme_high_pop;
		extreme_med := var_r.gfms_extreme_med_pop;
		extreme_low := var_r.gfms_extreme_low_pop;
		veryhigh_high := var_r.gfms_veryhigh_high_pop;
		veryhigh_med := var_r.gfms_veryhigh_med_pop;
		veryhigh_low := var_r.gfms_veryhigh_low_pop;
		high_high := var_r.gfms_high_high_pop;
		high_med := var_r.gfms_high_med_pop;
		high_low := var_r.gfms_high_low_pop;
		moderate_high := var_r.gfms_med_high_pop;
		moderate_med := var_r.gfms_med_med_pop;
		moderate_low := var_r.gfms_med_low_pop;
		low_high := var_r.gfms_low_high_pop;
		low_med := var_r.gfms_low_med_pop;
		low_low := var_r.gfms_low_low_pop;
		verylow_high := var_r.gfms_verylow_high_pop;
		verylow_med := var_r.gfms_verylow_med_pop;
		verylow_low := var_r.gfms_verylow_low_pop;

		extreme_area := var_r.gfms_extreme_area;
		veryhigh_area := var_r.gfms_veryhigh_area;
		high_area := var_r.gfms_high_area;
		moderate_area := var_r.gfms_med_area;
		low_area := var_r.gfms_low_area;
		verylow_area := var_r.gfms_verylow_area;

		extreme_buildings := var_r.gfms_extreme_buildings;
		veryhigh_buildings := var_r.gfms_veryhigh_buildings;
		high_buildings := var_r.gfms_high_buildings;
		moderate_buildings := var_r.gfms_med_buildings;
		low_buildings := var_r.gfms_low_buildings;
		verylow_buildings := var_r.gfms_verylow_buildings;

		extreme_high_buildings := var_r.gfms_extreme_high_buildings;
		extreme_med_buildings := var_r.gfms_extreme_med_buildings;
		extreme_low_buildings := var_r.gfms_extreme_low_buildings;
		veryhigh_high_buildings := var_r.gfms_veryhigh_high_buildings;
		veryhigh_med_buildings := var_r.gfms_veryhigh_med_buildings;
		veryhigh_low_buildings := var_r.gfms_veryhigh_low_buildings;
		high_high_buildings := var_r.gfms_high_high_buildings;
		high_med_buildings := var_r.gfms_high_med_buildings;
		high_low_buildings := var_r.gfms_high_low_buildings;
		moderate_high_buildings := var_r.gfms_med_high_buildings;
		moderate_med_buildings := var_r.gfms_med_med_buildings;
		moderate_low_buildings := var_r.gfms_med_low_buildings;
		low_high_buildings := var_r.gfms_low_high_buildings;
		low_med_buildings := var_r.gfms_low_med_buildings;
		low_low_buildings := var_r.gfms_low_low_buildings;
		verylow_high_buildings := var_r.gfms_verylow_high_buildings;
		verylow_med_buildings := var_r.gfms_verylow_med_buildings;
		verylow_low_buildings := var_r.gfms_verylow_low_buildings;
	END IF;	

        

        RETURN NEXT;
     END LOOP;
END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_merge_glofas_gfms(date, character varying, integer, character varying)
--   OWNER TO postgres;

-- Function: public.get_gfms_detail(date)

-- DROP FUNCTION public.get_gfms_detail(date);

CREATE OR REPLACE FUNCTION public.get_gfms_detail(IN p_date date)
  RETURNS TABLE(prov_code integer, dist_code integer, basin_id double precision, gfms_verylow_pop double precision, gfms_low_pop double precision, gfms_med_pop double precision, gfms_high_pop double precision, gfms_veryhigh_pop double precision, gfms_extreme_pop double precision) AS
$BODY$
  BEGIN

	   RETURN QUERY
		SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.prov_code,
		    afg_fldzonea_100k_risk_landcover_pop.dist_code,
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.prov_code, afg_fldzonea_100k_risk_landcover_pop.dist_code, afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.prov_code, afg_fldzonea_100k_risk_landcover_pop.dist_code, afg_fldzonea_100k_risk_landcover_pop.basin_id;
   
 END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_gfms_detail(date)
--   OWNER TO postgres;

-- Function: public.get_gfms_layer(date)

-- DROP FUNCTION public.get_gfms_layer(date);

CREATE OR REPLACE FUNCTION public.get_gfms_layer(IN p_date date)
  RETURNS TABLE(vuid character varying, basin_id double precision, gfms_verylow_pop double precision, gfms_low_pop double precision, gfms_med_pop double precision, gfms_high_pop double precision, gfms_veryhigh_pop double precision, gfms_extreme_pop double precision) AS
$BODY$
  BEGIN

	   RETURN QUERY
		SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.vuid,
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.vuid, afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.vuid, afg_fldzonea_100k_risk_landcover_pop.basin_id;
   
 END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_gfms_layer(date)
--   OWNER TO postgres;

-- Function: public.get_gfms_layer(date, boolean)

-- DROP FUNCTION public.get_gfms_layer(date, boolean);

CREATE OR REPLACE FUNCTION public.get_gfms_layer(IN p_date date, IN include boolean)
  RETURNS TABLE(vuid character varying, basin_id double precision, gfms_verylow_pop double precision, gfms_low_pop double precision, gfms_med_pop double precision, gfms_high_pop double precision, gfms_veryhigh_pop double precision, gfms_extreme_pop double precision) AS
$BODY$
  BEGIN
	IF not include THEN 
		p_date = date('0001-01-01');
	END IF;

	   RETURN QUERY
		SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.vuid,
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.vuid, afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.vuid, afg_fldzonea_100k_risk_landcover_pop.basin_id;
   
 END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_gfms_layer(date, boolean)
--   OWNER TO postgres;

-- Function: public.get_gfms_query(date, character varying, integer, character varying)

-- DROP FUNCTION public.get_gfms_query(date, character varying, integer, character varying);

CREATE OR REPLACE FUNCTION public.get_gfms_query(IN p_date date, IN p_filter character varying, IN p_code integer, IN p_spt_filter character varying)
  RETURNS TABLE(basin_id double precision, gfms_verylow_pop double precision, gfms_low_pop double precision, gfms_med_pop double precision, gfms_high_pop double precision, gfms_veryhigh_pop double precision, gfms_extreme_pop double precision, gfms_verylow_area double precision, gfms_low_area double precision, gfms_med_area double precision, gfms_high_area double precision, gfms_veryhigh_area double precision, gfms_extreme_area double precision, gfms_verylow_buildings double precision, gfms_low_buildings double precision, gfms_med_buildings double precision, gfms_high_buildings double precision, gfms_veryhigh_buildings double precision, gfms_extreme_buildings double precision, gfms_verylow_low_pop double precision, gfms_verylow_med_pop double precision, gfms_verylow_high_pop double precision, gfms_low_low_pop double precision, gfms_low_med_pop double precision, gfms_low_high_pop double precision, gfms_med_low_pop double precision, gfms_med_med_pop double precision, gfms_med_high_pop double precision, gfms_high_low_pop double precision, gfms_high_med_pop double precision, gfms_high_high_pop double precision, gfms_veryhigh_low_pop double precision, gfms_veryhigh_med_pop double precision, gfms_veryhigh_high_pop double precision, gfms_extreme_low_pop double precision, gfms_extreme_med_pop double precision, gfms_extreme_high_pop double precision, gfms_verylow_low_buildings double precision, gfms_verylow_med_buildings double precision, gfms_verylow_high_buildings double precision, gfms_low_low_buildings double precision, gfms_low_med_buildings double precision, gfms_low_high_buildings double precision, gfms_med_low_buildings double precision, gfms_med_med_buildings double precision, gfms_med_high_buildings double precision, gfms_high_low_buildings double precision, gfms_high_med_buildings double precision, gfms_high_high_buildings double precision, gfms_veryhigh_low_buildings double precision, gfms_veryhigh_med_buildings double precision, gfms_veryhigh_high_buildings double precision, gfms_extreme_low_buildings double precision, gfms_extreme_med_buildings double precision, gfms_extreme_high_buildings double precision) AS
$BODY$
  BEGIN
   IF p_filter='entireAfg' THEN
	   RETURN QUERY
		SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_verylow_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_low_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_med_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_high_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_veryhigh_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_extreme_area,

		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_buildings,
		----------------- matrix start for population
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_pop,
		----------------- matrix start for buildings
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_buildings
			
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.basin_id;
    ELSEIF p_filter='currentProvince' THEN
	IF length(p_code::text)>2 THEN
		RETURN QUERY
			SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_verylow_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_low_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_med_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_high_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_veryhigh_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_extreme_area,

		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_buildings,
		----------------- matrix start for population
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_pop,
		----------------- matrix start for buildings
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_buildings
			
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date AND afg_fldzonea_100k_risk_landcover_pop.dist_code = p_code
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.basin_id;
			
	ELSE
		RETURN QUERY
			SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_verylow_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_low_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_med_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_high_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_veryhigh_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_extreme_area,

		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_buildings,
		----------------- matrix start for population
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_pop,
		----------------- matrix start for buildings
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_buildings
			
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date AND afg_fldzonea_100k_risk_landcover_pop.prov_code = p_code
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.basin_id;
	END IF;
    ELSE
		RETURN QUERY
			SELECT 
		    afg_fldzonea_100k_risk_landcover_pop.basin_id,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_pop,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_pop,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_verylow_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_low_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_med_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_high_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_veryhigh_area,
		    sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_sqm
			    ELSE 0::double precision
			END) / 1000000::double precision AS gfms_extreme_area,

		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_buildings,
		    round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_buildings,
		----------------- matrix start for population
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_low_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_med_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_high_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_pop,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.fldarea_population
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_pop,
		----------------- matrix start for buildings
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 1 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_verylow_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 2 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_low_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 3 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_med_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 4 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_high_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 5 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_veryhigh_high_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '029 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_low_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '121 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_med_buildings,
		   round(sum(
			CASE
			    WHEN forcastedvalue.riskstate = 6 AND afg_fldzonea_100k_risk_landcover_pop.deeperthan = '271 cm' THEN afg_fldzonea_100k_risk_landcover_pop.area_buildings
			    ELSE 0::double precision
			END)) AS gfms_extreme_high_buildings
			
		   FROM afg_fldzonea_100k_risk_landcover_pop
		     JOIN afg_sheda_lvl4 ON afg_fldzonea_100k_risk_landcover_pop.basinmember_id = afg_sheda_lvl4.ogc_fid
		     JOIN forcastedvalue ON afg_sheda_lvl4.ogc_fid = forcastedvalue.basin_id
		  WHERE NOT afg_fldzonea_100k_risk_landcover_pop.agg_simplified_description::text = 'Water body and marshland'::text AND NOT (afg_fldzonea_100k_risk_landcover_pop.basinmember_id IN ( SELECT u1.ogc_fid
			   FROM afg_sheda_lvl4 u1
			     LEFT JOIN forcastedvalue u2 ON u1.ogc_fid = u2.basin_id
			  WHERE u2.riskstate IS NULL)) AND forcastedvalue.forecasttype::text = 'riverflood'::text
				AND forcastedvalue.datadate = p_date AND ST_Within(afg_fldzonea_100k_risk_landcover_pop.wkb_geometry, ST_GeometryFromText(p_spt_filter, 4326))
		  GROUP BY afg_fldzonea_100k_risk_landcover_pop.basin_id
		  ORDER BY afg_fldzonea_100k_risk_landcover_pop.basin_id;
	
    END IF;
 END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_gfms_query(date, character varying, integer, character varying)
--   OWNER TO postgres;

-- Function: public.get_glofas(date, character varying, integer, character varying)

-- DROP FUNCTION public.get_glofas(date, character varying, integer, character varying);

CREATE OR REPLACE FUNCTION public.get_glofas(IN p_date date, IN p_filter character varying, IN p_code integer, IN p_spatial character varying)
  RETURNS TABLE(basin_id bigint, rl2 double precision, rl5 double precision, rl20 double precision, rl2_dis_percent integer, rl2_avg_dis_percent integer, rl5_dis_percent integer, rl5_avg_dis_percent integer, rl20_dis_percent integer, rl20_avg_dis_percent integer, rl100_pop double precision, rl100_buildings integer, rl100_area double precision, rl100_low_risk double precision, rl100_med_risk double precision, rl100_high_risk double precision, rl100_low_risk_buildings double precision, rl100_med_risk_buildings double precision, rl100_high_risk_buildings double precision, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision, extreme_buildings double precision, veryhigh_buildings double precision, high_buildings double precision, moderate_buildings double precision, low_buildings double precision, verylow_buildings double precision, extreme_high double precision, extreme_med double precision, extreme_low double precision, veryhigh_high double precision, veryhigh_med double precision, veryhigh_low double precision, high_high double precision, high_med double precision, high_low double precision, moderate_high double precision, moderate_med double precision, moderate_low double precision, low_high double precision, low_med double precision, low_low double precision, verylow_high double precision, verylow_med double precision, verylow_low double precision, extreme_high_buildings double precision, extreme_med_buildings double precision, extreme_low_buildings double precision, veryhigh_high_buildings double precision, veryhigh_med_buildings double precision, veryhigh_low_buildings double precision, high_high_buildings double precision, high_med_buildings double precision, high_low_buildings double precision, moderate_high_buildings double precision, moderate_med_buildings double precision, moderate_low_buildings double precision, low_high_buildings double precision, low_med_buildings double precision, low_low_buildings double precision, verylow_high_buildings double precision, verylow_med_buildings double precision, verylow_low_buildings double precision, extreme_area double precision, veryhigh_area double precision, high_area double precision, moderate_area double precision, low_area double precision, verylow_area double precision) AS
$BODY$
DECLARE 
    var_r record;
DECLARE temp double precision;
DECLARE temp_buildings double precision;
DECLARE temp_area double precision;
DECLARE temp_rl20 double precision;   
DECLARE temp_dis_percent double precision;  
DECLARE temp_low_risk  double precision; 
DECLARE temp_med_risk  double precision;
DECLARE temp_high_risk  double precision;
DECLARE temp_buildings_low_risk  double precision; 
DECLARE temp_buildings_med_risk  double precision;
DECLARE temp_buildings_high_risk  double precision;

DECLARE constant_rl2  double precision;
DECLARE constant_rl5  double precision;
DECLARE constant_rl20  double precision;
BEGIN
   constant_rl2 := 0.02;
   constant_rl5 := 0.02;
   constant_rl20:= 0.18;
   FOR var_r IN(select * from get_glofas_query(p_date,p_filter,p_code,p_spatial))  
     LOOP
        basin_id := var_r.basin_id; 
	rl2 := var_r.rl2;
	rl5 := var_r.rl5;
	rl20 := var_r.rl20;
	---rl2_dis_percent := var_r.rl2_dis_percent;
	rl2_dis_percent := 0;
	rl2_avg_dis_percent := var_r.rl2_avg_dis_percent;
	rl5_dis_percent := var_r.rl5_dis_percent;
	rl5_avg_dis_percent := var_r.rl5_avg_dis_percent;
	rl20_dis_percent := var_r.rl20_dis_percent;
	rl20_avg_dis_percent := var_r.rl20_avg_dis_percent;
	RL100_pop := var_r.RL100_pop;
	rl100_buildings := var_r.rl100_buildings;
	RL100_area := var_r.RL100_area/1000000;
	rl100_low_risk := var_r.rl100_low_risk;
	rl100_med_risk := var_r.rl100_med_risk;
	rl100_high_risk := var_r.rl100_high_risk;

	rl100_low_risk_buildings := var_r.rl100_low_risk_buildings;
	rl100_med_risk_buildings := var_r.rl100_med_risk_buildings;
	rl100_high_risk_buildings := var_r.rl100_high_risk_buildings;
	
	temp := var_r.RL100_pop;
	temp_buildings := var_r.RL100_buildings;
	temp_area := var_r.RL100_area/1000000;
	extreme := 0;
        veryhigh := 0;
        high := 0;
        moderate := 0;
        low := 0;
        verylow := 0;

        extreme_buildings := 0;
        veryhigh_buildings := 0;
        high_buildings := 0;
        moderate_buildings := 0;
        low_buildings := 0;
        verylow_buildings := 0;

        extreme_high := 0;
	extreme_med := 0;
	extreme_low := 0;
	veryhigh_high := 0;
	veryhigh_med := 0;
	veryhigh_low := 0;
	high_high := 0;
	high_med := 0;
	high_low := 0;
	moderate_high := 0;
	moderate_med := 0;
	moderate_low := 0;
	low_high := 0;
	low_med := 0;
	low_low := 0;
	verylow_high := 0;
	verylow_med := 0;
	verylow_low := 0;

	extreme_high_buildings := 0;
	extreme_med_buildings := 0;
	extreme_low_buildings := 0;
	veryhigh_high_buildings := 0;
	veryhigh_med_buildings := 0;
	veryhigh_low_buildings := 0;
	high_high_buildings := 0;
	high_med_buildings := 0;
	high_low_buildings := 0;
	moderate_high_buildings := 0;
	moderate_med_buildings := 0;
	moderate_low_buildings := 0;
	low_high_buildings := 0;
	low_med_buildings := 0;
	low_low_buildings := 0;
	verylow_high_buildings := 0;
	verylow_med_buildings := 0;
	verylow_low_buildings := 0;

	extreme_area := 0;
	veryhigh_area := 0;
	high_area := 0;
	moderate_area := 0;
	low_area := 0;
	verylow_area := 0;

        temp_low_risk := rl100_low_risk;
        temp_med_risk := rl100_med_risk;
        temp_high_risk := rl100_high_risk;
	
        temp_buildings_low_risk := rl100_low_risk_buildings;
        temp_buildings_med_risk := rl100_med_risk_buildings;
        temp_buildings_high_risk := rl100_high_risk_buildings;

		temp_dis_percent := 0;
		IF rl2_dis_percent >= 100 THEN
			temp_dis_percent := rl2_avg_dis_percent;
		ELSE
			temp_dis_percent := rl2_dis_percent;
		END IF;	
		
		IF temp_dis_percent>400 THEN
			extreme := extreme + constant_rl2*temp;
			extreme_buildings := extreme_buildings + constant_rl2*temp_buildings;
			extreme_area := extreme_area + constant_rl2*temp_area;
			IF temp_high_risk-(constant_rl2*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl2*temp);
				extreme_high := extreme_high + (constant_rl2*temp);
			ELSEIF temp_high_risk-(constant_rl2*temp) < 0 AND temp_high_risk>0 THEN
				extreme_high := extreme_high + temp_high_risk;
				extreme_med := extreme_med + ((temp_high_risk-(constant_rl2*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl2*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl2*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl2*temp);
				extreme_med := extreme_med + (constant_rl2*temp);
			ELSEIF temp_med_risk-(constant_rl2*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				extreme_med:= extreme_med + temp_med_risk;
				extreme_low := extreme_low + ((temp_med_risk-(constant_rl2*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl2*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl2*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl2*temp);
				extreme_low := extreme_low + (constant_rl2*temp);
			END IF;
			
			IF temp_buildings_high_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl2*temp_buildings);
				extreme_high_buildings := extreme_high_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				extreme_high_buildings := extreme_high_buildings + temp_buildings_high_risk;
				extreme_med_buildings := extreme_med_buildings + ((temp_buildings_high_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl2*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl2*temp_buildings);
				extreme_med_buildings := extreme_med_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				extreme_med_buildings:= extreme_med_buildings + temp_buildings_med_risk;
				extreme_low_buildings := extreme_low_buildings + ((temp_buildings_med_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl2*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl2*temp_buildings);
				extreme_low_buildings := extreme_low_buildings + (constant_rl2*temp_buildings);
			END IF;
			temp := temp - constant_rl2*temp;
			temp_area := temp_area - constant_rl2*temp_area;
			temp_buildings := temp_buildings - constant_rl2*temp_buildings;
		ELSEIF temp_dis_percent>160 AND temp_dis_percent<=400 THEN
			veryhigh := veryhigh + constant_rl2*temp;
			veryhigh_buildings := veryhigh_buildings + constant_rl2*temp_buildings;
			veryhigh_area := veryhigh_area + constant_rl2*temp_area;
			IF temp_high_risk-(constant_rl2*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl2*temp);
				veryhigh_high := veryhigh_high + (constant_rl2*temp);
			ELSEIF temp_high_risk-(constant_rl2*temp) < 0 AND temp_high_risk>0 THEN
				veryhigh_high := veryhigh_high + temp_high_risk;
				veryhigh_med := veryhigh_med + ((temp_high_risk-(constant_rl2*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl2*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl2*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl2*temp);
				veryhigh_med := veryhigh_med + (constant_rl2*temp);
			ELSEIF temp_med_risk-(constant_rl2*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				veryhigh_med:= veryhigh_med + temp_med_risk;
				veryhigh_low := veryhigh_low + ((temp_med_risk-(constant_rl2*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl2*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl2*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl2*temp);
				veryhigh_low := veryhigh_low + (constant_rl2*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl2*temp_buildings);
				veryhigh_high_buildings := veryhigh_high_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				veryhigh_high_buildings := veryhigh_high_buildings + temp_buildings_high_risk;
				veryhigh_med_buildings := veryhigh_med_buildings + ((temp_buildings_high_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl2*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl2*temp_buildings);
				veryhigh_med_buildings := veryhigh_med_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				veryhigh_med_buildings:= veryhigh_med_buildings + temp_buildings_med_risk;
				veryhigh_low_buildings := veryhigh_low_buildings + ((temp_buildings_med_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl2*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl2*temp_buildings);
				veryhigh_low_buildings := veryhigh_low_buildings + (constant_rl2*temp_buildings);
			END IF;
			
			temp := temp - constant_rl2*temp;
			temp_area := temp_area - constant_rl2*temp_area;
			temp_buildings := temp_buildings - constant_rl2*temp_buildings;
		ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
			high := high + constant_rl2*temp;
			high_buildings := high_buildings + constant_rl2*temp_buildings;
			high_area := high_area + constant_rl2*temp_area;
			IF temp_high_risk-(constant_rl2*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl2*temp);
				high_high := high_high + (constant_rl2*temp);
			ELSEIF temp_high_risk-(constant_rl2*temp) < 0 AND temp_high_risk>0 THEN
				high_high := high_high + temp_high_risk;
				high_med := high_med + ((temp_high_risk-(constant_rl2*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl2*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl2*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl2*temp);
				high_med := high_med + (constant_rl2*temp);
			ELSEIF temp_med_risk-(constant_rl2*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				high_med:= high_med + temp_med_risk;
				high_low := high_low + ((temp_med_risk-(constant_rl2*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl2*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl2*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl2*temp);
				high_low := high_low + (constant_rl2*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl2*temp_buildings);
				high_high_buildings := high_high_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				high_high_buildings := high_high_buildings + temp_buildings_high_risk;
				high_med_buildings := high_med_buildings + ((temp_buildings_high_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl2*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl2*temp_buildings);
				high_med_buildings := high_med_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				high_med_buildings:= high_med_buildings + temp_buildings_med_risk;
				high_low_buildings := high_low_buildings + ((temp_buildings_med_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl2*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl2*temp_buildings);
				high_low_buildings := high_low_buildings + (constant_rl2*temp_buildings);
			END IF;
			
			temp := temp - constant_rl2*temp;
			temp_area := temp_area - constant_rl2*temp_area;
			temp_buildings := temp_buildings - constant_rl2*temp_buildings;
		ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
			moderate := moderate + constant_rl2*temp;
			moderate_buildings := moderate_buildings + constant_rl2*temp_buildings;
			moderate_area := moderate_area + constant_rl2*temp_area;
			IF temp_high_risk-(constant_rl2*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl2*temp);
				moderate_high := moderate_high + (constant_rl2*temp);
			ELSEIF temp_high_risk-(constant_rl2*temp) < 0 AND temp_high_risk>0 THEN
				moderate_high := moderate_high + temp_high_risk;
				moderate_med := moderate_med + ((temp_high_risk-(constant_rl2*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl2*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl2*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl2*temp);
				moderate_med := moderate_med + (constant_rl2*temp);
			ELSEIF temp_med_risk-(constant_rl2*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				moderate_med:= moderate_med + temp_med_risk;
				moderate_low := moderate_low + ((temp_med_risk-(constant_rl2*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl2*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl2*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl2*temp);
				moderate_low := moderate_low + (constant_rl2*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl2*temp_buildings);
				moderate_high_buildings := moderate_high_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				moderate_high_buildings := moderate_high_buildings + temp_buildings_high_risk;
				moderate_med_buildings := moderate_med_buildings + ((temp_buildings_high_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl2*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl2*temp_buildings);
				moderate_med_buildings := moderate_med_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				moderate_med_buildings:= moderate_med_buildings + temp_buildings_med_risk;
				moderate_low_buildings := moderate_low_buildings + ((temp_buildings_med_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl2*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl2*temp_buildings);
				moderate_low_buildings := moderate_low_buildings + (constant_rl2*temp_buildings);
			END IF;
			
			temp := temp - constant_rl2*temp;
			temp_area := temp_area - constant_rl2*temp_area;
			temp_buildings := temp_buildings - constant_rl2*temp_buildings;
		ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
			low := low + constant_rl2*temp;
			low_buildings := low_buildings + constant_rl2*temp_buildings;
			low_area := low_area + constant_rl2*temp_area;
			IF temp_high_risk-(constant_rl2*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl2*temp);
				low_high := low_high + (constant_rl2*temp);
			ELSEIF temp_high_risk-(constant_rl2*temp) < 0 AND temp_high_risk>0 THEN
				low_high := low_high + temp_high_risk;
				low_med := low_med + ((temp_high_risk-(constant_rl2*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl2*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl2*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl2*temp);
				low_med := low_med + (constant_rl2*temp);
			ELSEIF temp_med_risk-(constant_rl2*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				low_med:= low_med + temp_med_risk;
				low_low := low_low + ((temp_med_risk-(constant_rl2*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl2*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl2*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl2*temp);
				low_low := low_low + (constant_rl2*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl2*temp_buildings);
				low_high_buildings := low_high_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				low_high_buildings := low_high_buildings + temp_buildings_high_risk;
				low_med_buildings := low_med_buildings + ((temp_buildings_high_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl2*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl2*temp_buildings);
				low_med_buildings := low_med_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				low_med_buildings:= low_med_buildings + temp_buildings_med_risk;
				low_low_buildings := low_low_buildings + ((temp_buildings_med_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl2*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl2*temp_buildings);
				low_low_buildings := low_low_buildings + (constant_rl2*temp_buildings);
			END IF;
			
			temp := temp - constant_rl2*temp;
			temp_area := temp_area - constant_rl2*temp_area;
			temp_buildings := temp_buildings - constant_rl2*temp_buildings;
		ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
			verylow := verylow + constant_rl2*temp;
			verylow_area := verylow_area + constant_rl2*temp_area;
			verylow_buildings := verylow_buildings + constant_rl2*temp_buildings;
			IF temp_high_risk-(constant_rl2*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl2*temp);
				verylow_high := verylow_high + (constant_rl2*temp);
			ELSEIF temp_high_risk-(constant_rl2*temp) < 0 AND temp_high_risk>0 THEN
				verylow_high := verylow_high + temp_high_risk;
				verylow_med := verylow_med + ((temp_high_risk-(constant_rl2*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl2*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl2*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl2*temp);
				verylow_med := verylow_med + (constant_rl2*temp);
			ELSEIF temp_med_risk-(constant_rl2*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				verylow_med:= verylow_med + temp_med_risk;
				verylow_low := verylow_low + ((temp_med_risk-(constant_rl2*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl2*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl2*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl2*temp);
				verylow_low := verylow_low + (constant_rl2*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl2*temp_buildings);
				verylow_high_buildings := verylow_high_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				verylow_high_buildings := verylow_high_buildings + temp_buildings_high_risk;
				verylow_med_buildings := verylow_med_buildings + ((temp_buildings_high_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl2*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl2*temp_buildings);
				verylow_med_buildings := verylow_med_buildings + (constant_rl2*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl2*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				verylow_med_buildings:= verylow_med_buildings + temp_buildings_med_risk;
				verylow_low_buildings := verylow_low_buildings + ((temp_buildings_med_risk-(constant_rl2*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl2*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl2*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl2*temp_buildings);
				verylow_low_buildings := verylow_low_buildings + (constant_rl2*temp_buildings);
			END IF;
			temp := temp - constant_rl2*temp;
			temp_area := temp_area - constant_rl2*temp_area;
			temp_buildings := temp_buildings - constant_rl2*temp_buildings;
		END IF;
		--temp := temp - extreme - veryhigh - high - moderate - low - verylow;

		temp_dis_percent := 0;
		IF rl5_dis_percent >= 100 THEN
			temp_dis_percent := rl5_avg_dis_percent;
		ELSE
			temp_dis_percent := rl5_dis_percent;
		END IF;	
		
		IF temp_dis_percent>160 THEN
			--extreme := extreme + constant_rl5*temp;
			--extreme_buildings := extreme_buildings + constant_rl5*temp_buildings;
			--extreme_area := extreme_area + constant_rl5*temp_area;
			IF temp_high_risk-(constant_rl5*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl5*temp);
				extreme_high := extreme_high + (constant_rl5*temp);
			ELSEIF temp_high_risk-(constant_rl5*temp) < 0 AND temp_high_risk>0 THEN
				extreme_high := extreme_high + temp_high_risk;
				--extreme_med := extreme_med + ((temp_high_risk-(constant_rl5*temp))*-1);
				--temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl5*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl5*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--temp_med_risk = temp_med_risk - (constant_rl5*temp);
				--extreme_med := extreme_med + (constant_rl5*temp);
			ELSEIF temp_med_risk-(constant_rl5*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--extreme_med:= extreme_med + temp_med_risk;
				--extreme_low := extreme_low + ((temp_med_risk-(constant_rl5*temp))*-1);
				--temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl5*temp));
				--temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl5*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				--temp_low_risk = temp_low_risk - (constant_rl5*temp);
				--extreme_low := extreme_low + (constant_rl5*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl5*temp_buildings);
				extreme_high_buildings := extreme_high_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				extreme_high_buildings := extreme_high_buildings + temp_buildings_high_risk;
				--extreme_med_buildings := extreme_med_buildings + ((temp_buildings_high_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl5*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl5*temp_buildings);
				--extreme_med_buildings := extreme_med_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--extreme_med_buildings:= extreme_med_buildings + temp_buildings_med_risk;
				--extreme_low_buildings := extreme_low_buildings + ((temp_buildings_med_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl5*temp_buildings));
				--temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				--temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl5*temp_buildings);
				--extreme_low_buildings := extreme_low_buildings + (constant_rl5*temp_buildings);
			END IF;
			
			IF constant_rl5*temp>temp_high_risk THEN
				extreme := extreme + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				extreme := extreme + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;

			IF constant_rl5*temp_buildings>temp_buildings_high_risk THEN
				extreme_buildings := extreme_buildings+ temp_buildings_high_risk;
				temp_buildings := temp_buildings - temp_buildings_high_risk;
			ELSE
				extreme_buildings := extreme_buildings + constant_rl5*temp_buildings;
				temp_buildings := temp_buildings - constant_rl5*temp_buildings;
			END IF;
			--temp := temp - constant_rl5*temp;
			--temp_area := temp_area - constant_rl5*temp_area;
			--temp_buildings := temp_buildings - constant_rl5*temp_buildings;
		ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
			--veryhigh := veryhigh + constant_rl5*temp;
			--veryhigh_buildings := veryhigh_buildings + constant_rl5*temp_buildings;
			--veryhigh_area := veryhigh_area + constant_rl5*temp_area;
			IF temp_high_risk-(constant_rl5*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl5*temp);
				veryhigh_high := veryhigh_high + (constant_rl5*temp);
			ELSEIF temp_high_risk-(constant_rl5*temp) < 0 AND temp_high_risk>0 THEN
				veryhigh_high := veryhigh_high + temp_high_risk;
				--veryhigh_med := veryhigh_med + ((temp_high_risk-(constant_rl5*temp))*-1);
				--temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl5*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl5*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--temp_med_risk = temp_med_risk - (constant_rl5*temp);
				--veryhigh_med := veryhigh_med + (constant_rl5*temp);
			ELSEIF temp_med_risk-(constant_rl5*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--veryhigh_med:= veryhigh_med + temp_med_risk;
				--veryhigh_low := veryhigh_low + ((temp_med_risk-(constant_rl5*temp))*-1);
				--temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl5*temp));
				--temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl5*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				--temp_low_risk = temp_low_risk - (constant_rl5*temp);
				--veryhigh_low := veryhigh_low + (constant_rl5*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl5*temp_buildings);
				veryhigh_high_buildings := veryhigh_high_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				veryhigh_high_buildings := veryhigh_high_buildings + temp_buildings_high_risk;
				--veryhigh_med _buildings:= veryhigh_med_buildings + ((temp_buildings_high_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl5*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl5*temp_buildings);
				--veryhigh_med_buildings := veryhigh_med_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--veryhigh_med_buildings:= veryhigh_med_buildings + temp_buildings_med_risk;
				--veryhigh_low_buildings := veryhigh_low_buildings + ((temp_buildings_med_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl5*temp_buildings));
				--temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				--temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl5*temp_buildings);
				--veryhigh_low_buildings := veryhigh_low_buildings + (constant_rl5*temp_buildings);
			END IF;
			
			IF constant_rl5*temp>temp_high_risk THEN
				veryhigh := veryhigh + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				veryhigh := veryhigh + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;

			IF constant_rl5*temp_buildings>temp_buildings_high_risk THEN
				veryhigh_buildings := veryhigh_buildings + temp_buildings_high_risk;
				temp_buildings := temp_buildings - temp_buildings_high_risk;
			ELSE
				veryhigh_buildings := veryhigh_buildings + constant_rl5*temp_buildings;
				temp_buildings := temp_buildings - constant_rl5*temp_buildings;
			END IF;
			
			--temp := temp - constant_rl5*temp;
			--temp_area := temp_area - constant_rl5*temp_area;
			--temp_buildings := temp_buildings - constant_rl5*temp_buildings;
		ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
			--high := high + constant_rl5*temp;
			--high_buildings := high_buildings + constant_rl5*temp_buildings;
			--high_area := high_area + constant_rl5*temp_area;
			IF temp_high_risk-(constant_rl5*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl5*temp);
				high_high := high_high + (constant_rl5*temp);
			ELSEIF temp_high_risk-(constant_rl5*temp) < 0 AND temp_high_risk>0 THEN
				high_high := high_high + temp_high_risk;
				--high_med := high_med + ((temp_high_risk-(constant_rl5*temp))*-1);
				--temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl5*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl5*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--temp_med_risk = temp_med_risk - (constant_rl5*temp);
				--high_med := high_med + (constant_rl5*temp);
			ELSEIF temp_med_risk-(constant_rl5*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--high_med:= high_med + temp_med_risk;
				--high_low := high_low + ((temp_med_risk-(constant_rl5*temp))*-1);
				--temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl5*temp));
				--temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl5*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				--temp_low_risk = temp_low_risk - (constant_rl5*temp);
				--high_low := high_low + (constant_rl5*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl5*temp_buildings);
				high_high_buildings := high_high_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				high_high_buildings := high_high_buildings + temp_buildings_high_risk;
				--high_med_buildings := high_med_buildings + ((temp_buildings_high_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl5*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl5*temp_buildings);
				--high_med_buildings := high_med_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--high_med_buildings:= high_med_buildings + temp_buildings_med_risk;
				--high_low_buildings := high_low_buildings + ((temp_buildings_med_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl5*temp_buildings));
				--temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				--temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl5*temp_buildings);
				--high_low_buildings := high_low_buildings + (constant_rl5*temp_buildings);
			END IF;
			
			IF constant_rl5*temp>temp_high_risk THEN
				high := high + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				high := high + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;

			IF constant_rl5*temp_buildings>temp_buildings_high_risk THEN
				high_buildings := high_buildings + temp_buildings_high_risk;
				temp_buildings := temp_buildings - temp_buildings_high_risk;
			ELSE
				high_buildings := high_buildings + constant_rl5*temp_buildings;
				temp_buildings := temp_buildings - constant_rl5*temp_buildings;
			END IF;
			--temp := temp - constant_rl5*temp;
			--temp_area := temp_area - constant_rl5*temp_area;
			--temp_buildings := temp_buildings - constant_rl5*temp_buildings;
		ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
			--moderate := moderate + constant_rl5*temp;
			--moderate_buildings := moderate_buildings + constant_rl5*temp_buildings;
			--moderate_area := moderate_area + constant_rl5*temp_area;
			IF temp_high_risk-(constant_rl5*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl5*temp);
				moderate_high := moderate_high + (constant_rl5*temp);
			ELSEIF temp_high_risk-(constant_rl5*temp) < 0 AND temp_high_risk>0 THEN
				moderate_high := moderate_high + temp_high_risk;
				--moderate_med := moderate_med + ((temp_high_risk-(constant_rl5*temp))*-1);
				--temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl5*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl5*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--temp_med_risk = temp_med_risk - (constant_rl5*temp);
				--moderate_med := moderate_med + (constant_rl5*temp);
			ELSEIF temp_med_risk-(constant_rl5*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--moderate_med:= moderate_med + temp_med_risk;
				--moderate_low := moderate_low + ((temp_med_risk-(constant_rl5*temp))*-1);
				--temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl5*temp));
				--temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl5*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				--temp_low_risk = temp_low_risk - (constant_rl5*temp);
				--moderate_low := moderate_low + (constant_rl5*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl5*temp_buildings);
				moderate_high_buildings := moderate_high_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				moderate_high_buildings := moderate_high_buildings + temp_buildings_high_risk;
				--moderate_med_buildings := moderate_med_buildings + ((temp_buildings_high_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl5*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl5*temp_buildings);
				--moderate_med_buildings := moderate_med_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--moderate_med_buildings:= moderate_med_buildings + temp_buildings_med_risk;
				--moderate_low_buildings := moderate_low_buildings + ((temp_buildings_med_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl5*temp_buildings));
				--temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				--temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl5*temp_buildings);
				--moderate_low_buildings := moderate_low_buildings + (constant_rl5*temp_buildings);
			END IF;
			
			IF constant_rl5*temp>temp_high_risk THEN
				moderate := moderate + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				moderate := moderate + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;

			IF constant_rl5*temp_buildings>temp_buildings_high_risk THEN
				moderate_buildings := moderate_buildings + temp_buildings_high_risk;
				temp_buildings := temp_buildings - temp_buildings_high_risk;
			ELSE
				moderate_buildings := moderate_buildings + constant_rl5*temp_buildings;
				temp_buildings := temp_buildings - constant_rl5*temp_buildings;
			END IF;
			--temp := temp - constant_rl5*temp;
			--temp_area := temp_area - constant_rl5*temp_area;
			--temp_buildings := temp_buildings - constant_rl5*temp_buildings;
		ELSEIF temp_dis_percent>50 AND temp_dis_percent<=70 THEN
			--low := low + constant_rl5*temp;
			--low_buildings := low_buildings + constant_rl5*temp_buildings;
			--low_area := low_area + constant_rl5*temp_area;
			IF temp_high_risk-(constant_rl5*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl5*temp);
				low_high := low_high + (constant_rl5*temp);
			ELSEIF temp_high_risk-(constant_rl5*temp) < 0 AND temp_high_risk>0 THEN
				low_high := low_high + temp_high_risk;
				--low_med := low_med + ((temp_high_risk-(constant_rl5*temp))*-1);
				--temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl5*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl5*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--temp_med_risk = temp_med_risk - (constant_rl5*temp);
				--low_med := low_med + (constant_rl5*temp);
			ELSEIF temp_med_risk-(constant_rl5*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--low_med:= low_med + temp_med_risk;
				--low_low := low_low + ((temp_med_risk-(constant_rl5*temp))*-1);
				--temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl5*temp));
				--temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl5*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				--temp_low_risk = temp_low_risk - (constant_rl5*temp);
				--low_low := low_low + (constant_rl5*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl5*temp_buildings);
				low_high_buildings := low_high_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				low_high_buildings := low_high_buildings + temp_buildings_high_risk;
				--low_med_buildings := low_med_buildings + ((temp_buildings_high_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl5*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl5*temp_buildings);
				--low_med_buildings := low_med_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--low_med_buildings:= low_med_buildings + temp_buildings_med_risk;
				--low_low_buildings := low_low_buildings + ((temp_buildings_med_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl5*temp_buildings));
				--temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				--temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl5*temp_buildings);
				--low_low_buildings := low_low_buildings + (constant_rl5*temp_buildings);
			END IF;
			
			IF constant_rl5*temp>temp_high_risk THEN
				 low :=  low + temp_high_risk;
				 temp := temp - temp_high_risk;
			ELSE
				low :=  low + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;

			IF constant_rl5*temp_buildings>temp_buildings_high_risk THEN
				 low_buildings :=  low_buildings + temp_buildings_high_risk;
				 temp_buildings := temp_buildings - temp_buildings_high_risk;
			ELSE
				low_buildings :=  low_buildings + constant_rl5*temp_buildings;
				temp_buildings := temp_buildings - constant_rl5*temp_buildings;
			END IF;
			--temp := temp - constant_rl5*temp;
			--temp_area := temp_area - constant_rl5*temp_area;
			--temp_buildings := temp_buildings - constant_rl5*temp_buildings;
		ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
			--verylow := verylow + constant_rl5*temp;
			--verylow_buildings := verylow_buildings + constant_rl5*temp_buildings;
			--verylow_area := verylow_area + constant_rl5*temp_area;
			IF temp_high_risk-(constant_rl5*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl5*temp);
				verylow_high := verylow_high + (constant_rl5*temp);
			ELSEIF temp_high_risk-(constant_rl5*temp) < 0 AND temp_high_risk>0 THEN
				verylow_high := verylow_high + temp_high_risk;
				--verylow_med := verylow_med + ((temp_high_risk-(constant_rl5*temp))*-1);
				--temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl5*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl5*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--temp_med_risk = temp_med_risk - (constant_rl5*temp);
				--verylow_med := verylow_med + (constant_rl5*temp);
			ELSEIF temp_med_risk-(constant_rl5*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				--verylow_med:= verylow_med + temp_med_risk;
				--verylow_low := verylow_low + ((temp_med_risk-(constant_rl5*temp))*-1);
				--temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl5*temp));
				--temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl5*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				--temp_low_risk = temp_low_risk - (constant_rl5*temp);
				--verylow_low := verylow_low + (constant_rl5*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl5*temp_buildings);
				verylow_high_buildings := verylow_high_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				verylow_high_buildings := verylow_high_buildings + temp_buildings_high_risk;
				--verylow_med_buildings := verylow_med_buildings + ((temp_buildings_high_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl5*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl5*temp_buildings);
				--verylow_med_buildings := verylow_med_buildings + (constant_rl5*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl5*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				--verylow_med_buildings:= verylow_med_buildings + temp_buildings_med_risk;
				--verylow_low_buildings := verylow_low_buildings + ((temp_buildings_med_risk-(constant_rl5*temp_buildings))*-1);
				--temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl5*temp_buildings));
				--temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl5*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				--temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl5*temp_buildings);
				--verylow_low_buildings := verylow_low_buildings + (constant_rl5*temp_buildings);
			END IF;
			
			IF constant_rl5*temp>temp_high_risk THEN
				verylow :=  verylow + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				verylow :=  verylow + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;

			IF constant_rl5*temp_buildings>temp_buildings_high_risk THEN
				verylow_buildings :=  verylow_buildings + temp_buildings_high_risk;
				temp_buildings := temp_buildings - temp_buildings_high_risk;
			ELSE
				verylow_buildings :=  verylow_buildings + constant_rl5*temp_buildings;
				temp_buildings := temp_buildings - constant_rl5*temp_buildings;
			END IF;
			--temp := temp - constant_rl5*temp;
			--temp_area := temp_area - constant_rl5*temp_area;
			--temp_buildings := temp_buildings - constant_rl5*temp_buildings;
		END IF;
		--temp := temp - extreme - veryhigh - high - moderate - low - verylow;

		temp_dis_percent := 0;
		IF rl20_dis_percent >= 100 THEN
			temp_dis_percent := rl20_avg_dis_percent;
		ELSE
			temp_dis_percent := rl20_dis_percent;
		END IF;	

		IF temp_dis_percent>125 THEN
			extreme := extreme + constant_rl20*temp;
			extreme_buildings := extreme_buildings + constant_rl20*temp_buildings;
			extreme_area := extreme_area + constant_rl20*temp_area;
			IF temp_high_risk-(constant_rl20*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl20*temp);
				extreme_high := extreme_high + (constant_rl20*temp);
			ELSEIF temp_high_risk-(constant_rl20*temp) < 0 AND temp_high_risk>0 THEN
				extreme_high := extreme_high + temp_high_risk;
				extreme_med := extreme_med + ((temp_high_risk-(constant_rl20*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl20*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl20*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl20*temp);
				extreme_med := extreme_med + (constant_rl20*temp);
			ELSEIF temp_med_risk-(constant_rl20*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				extreme_med:= extreme_med + temp_med_risk;
				extreme_low := extreme_low + ((temp_med_risk-(constant_rl20*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl20*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl20*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl20*temp);
				extreme_low := extreme_low + (constant_rl20*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl20*temp_buildings);
				extreme_high_buildings := extreme_high_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				extreme_high_buildings := extreme_high_buildings + temp_buildings_high_risk;
				extreme_med_buildings := extreme_med_buildings + ((temp_buildings_high_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl20*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl20*temp_buildings);
				extreme_med_buildings := extreme_med_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				extreme_med_buildings:= extreme_med_buildings + temp_buildings_med_risk;
				extreme_low_buildings := extreme_low_buildings + ((temp_buildings_med_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl20*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl20*temp_buildings);
				extreme_low_buildings := extreme_low_buildings + (constant_rl20*temp_buildings);
			END IF;
			
			temp := temp - constant_rl20*temp;
			temp_area := temp_area - constant_rl20*temp_area;
			temp_buildings := temp_buildings - constant_rl20*temp_buildings;
		ELSEIF temp_dis_percent>100 AND temp_dis_percent<=125 THEN
			veryhigh := veryhigh + constant_rl20*temp;
			veryhigh_buildings := veryhigh_buildings + constant_rl20*temp_buildings;
			veryhigh_area := veryhigh_area + constant_rl20*temp_area;
			IF temp_high_risk-(constant_rl20*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl20*temp);
				veryhigh_high := veryhigh_high + (constant_rl20*temp);
			ELSEIF temp_high_risk-(constant_rl20*temp) < 0 AND temp_high_risk>0 THEN
				veryhigh_high := veryhigh_high + temp_high_risk;
				veryhigh_med := veryhigh_med + ((temp_high_risk-(constant_rl20*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl20*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl20*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl20*temp);
				veryhigh_med := veryhigh_med + (constant_rl20*temp);
			ELSEIF temp_med_risk-(constant_rl20*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				veryhigh_med:= veryhigh_med + temp_med_risk;
				veryhigh_low := veryhigh_low + ((temp_med_risk-(constant_rl20*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl20*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl20*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl20*temp);
				veryhigh_low := veryhigh_low + (constant_rl20*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl20*temp_buildings);
				veryhigh_high_buildings := veryhigh_high_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				veryhigh_high_buildings := veryhigh_high_buildings + temp_buildings_high_risk;
				veryhigh_med_buildings := veryhigh_med_buildings + ((temp_buildings_high_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl20*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl20*temp_buildings);
				veryhigh_med_buildings := veryhigh_med_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				veryhigh_med_buildings:= veryhigh_med_buildings + temp_buildings_med_risk;
				veryhigh_low_buildings := veryhigh_low_buildings + ((temp_buildings_med_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl20*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl20*temp_buildings);
				veryhigh_low_buildings := veryhigh_low_buildings + (constant_rl20*temp_buildings);
			END IF;
			
			temp := temp - constant_rl20*temp;
			temp_area := temp_area - constant_rl20*temp_area;
			temp_buildings := temp_buildings - constant_rl20*temp_buildings;
		ELSEIF temp_dis_percent>75 AND temp_dis_percent<=100 THEN
			high := high + constant_rl20*temp;
			high_buildings := high_buildings + constant_rl20*temp_buildings;
			high_area := high_area + constant_rl20*temp_area;
			IF temp_high_risk-(constant_rl20*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl20*temp);
				high_high := high_high + (constant_rl20*temp);
			ELSEIF temp_high_risk-(constant_rl20*temp) < 0 AND temp_high_risk>0 THEN
				high_high := high_high + temp_high_risk;
				high_med := high_med + ((temp_high_risk-(constant_rl20*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl20*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl20*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl20*temp);
				high_med := high_med + (constant_rl20*temp);
			ELSEIF temp_med_risk-(constant_rl20*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				high_med:= high_med + temp_med_risk;
				high_low := high_low + ((temp_med_risk-(constant_rl20*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl20*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl20*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl20*temp);
				high_low := high_low + (constant_rl20*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl20*temp_buildings);
				high_high_buildings := high_high_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				high_high_buildings := high_high_buildings + temp_buildings_high_risk;
				high_med_buildings := high_med_buildings + ((temp_buildings_high_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl20*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl20*temp_buildings);
				high_med_buildings := high_med_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				high_med_buildings:= high_med_buildings + temp_buildings_med_risk;
				high_low_buildings := high_low_buildings + ((temp_buildings_med_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl20*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl20*temp_buildings);
				high_low_buildings := high_low_buildings + (constant_rl20*temp_buildings);
			END IF;
			temp := temp - constant_rl20*temp;
			temp_area := temp_area - constant_rl20*temp_area;
			temp_buildings := temp_buildings - constant_rl20*temp_buildings;
		ELSEIF temp_dis_percent>50 AND temp_dis_percent<=75 THEN
			moderate := moderate + constant_rl20*temp;
			moderate_buildings := moderate_buildings + constant_rl20*temp_buildings;
			moderate_area := moderate_area + constant_rl20*temp_area;
			IF temp_high_risk-(constant_rl20*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl20*temp);
				moderate_high := moderate_high + (constant_rl20*temp);
			ELSEIF temp_high_risk-(constant_rl20*temp) < 0 AND temp_high_risk>0 THEN
				moderate_high := moderate_high + temp_high_risk;
				moderate_med := moderate_med + ((temp_high_risk-(constant_rl20*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl20*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl20*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl20*temp);
				moderate_med := moderate_med + (constant_rl20*temp);
			ELSEIF temp_med_risk-(constant_rl20*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				moderate_med:= moderate_med + temp_med_risk;
				moderate_low := moderate_low + ((temp_med_risk-(constant_rl20*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl20*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl20*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl20*temp);
				moderate_low := moderate_low + (constant_rl20*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl20*temp_buildings);
				moderate_high_buildings := moderate_high_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				moderate_high_buildings := moderate_high_buildings + temp_buildings_high_risk;
				moderate_med_buildings := moderate_med_buildings + ((temp_buildings_high_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl20*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl20*temp_buildings);
				moderate_med_buildings := moderate_med_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				moderate_med_buildings:= moderate_med_buildings + temp_buildings_med_risk;
				moderate_low_buildings := moderate_low_buildings + ((temp_buildings_med_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl20*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl20*temp_buildings);
				moderate_low_buildings := moderate_low_buildings + (constant_rl20*temp_buildings);
			END IF;
			
			temp := temp - constant_rl20*temp;
			temp_area := temp_area - constant_rl20*temp_area;
			temp_buildings := temp_buildings - constant_rl20*temp_buildings;
		ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
			low := low + constant_rl20*temp;
			low_buildings := low_buildings + constant_rl20*temp_buildings;
			low_area := low_area + constant_rl20*temp_area;
			IF temp_high_risk-(constant_rl20*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl20*temp);
				low_high := low_high + (constant_rl20*temp);
			ELSEIF temp_high_risk-(constant_rl20*temp) < 0 AND temp_high_risk>0 THEN
				low_high := low_high + temp_high_risk;
				low_med := low_med + ((temp_high_risk-(constant_rl20*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl20*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl20*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl20*temp);
				low_med := low_med + (constant_rl20*temp);
			ELSEIF temp_med_risk-(constant_rl20*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				low_med:= low_med + temp_med_risk;
				low_low := low_low + ((temp_med_risk-(constant_rl20*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl20*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl20*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl20*temp);
				low_low := low_low + (constant_rl20*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl20*temp_buildings);
				low_high_buildings := low_high_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				low_high_buildings := low_high_buildings + temp_buildings_high_risk;
				low_med_buildings := low_med_buildings + ((temp_buildings_high_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl20*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl20*temp_buildings);
				low_med_buildings := low_med_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				low_med_buildings:= low_med_buildings + temp_buildings_med_risk;
				low_low_buildings := low_low_buildings + ((temp_buildings_med_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl20*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl20*temp_buildings);
				low_low_buildings := low_low_buildings + (constant_rl20*temp_buildings);
			END IF;
			
			temp := temp - constant_rl20*temp;
			temp_area := temp_area - constant_rl20*temp_area;
			temp_buildings := temp_buildings - constant_rl20*temp_buildings;
		ELSEIF temp_dis_percent>0 AND temp_dis_percent<=25 THEN
			verylow := verylow + constant_rl20*temp;
			verylow_buildings := verylow_buildings + constant_rl20*temp_buildings;
			verylow_area := verylow_area + constant_rl20*temp_area;
			IF temp_high_risk-(constant_rl20*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - (constant_rl20*temp);
				verylow_high := verylow_high + (constant_rl20*temp);
			ELSEIF temp_high_risk-(constant_rl20*temp) < 0 AND temp_high_risk>0 THEN
				verylow_high := verylow_high + temp_high_risk;
				verylow_med := verylow_med + ((temp_high_risk-(constant_rl20*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - (constant_rl20*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-(constant_rl20*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - (constant_rl20*temp);
				verylow_med := verylow_med + (constant_rl20*temp);
			ELSEIF temp_med_risk-(constant_rl20*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				verylow_med:= verylow_med + temp_med_risk;
				verylow_low := verylow_low + ((temp_med_risk-(constant_rl20*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - (constant_rl20*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-(constant_rl20*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - (constant_rl20*temp);
				verylow_low := verylow_low + (constant_rl20*temp);
			END IF;

			IF temp_buildings_high_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - (constant_rl20*temp_buildings);
				verylow_high_buildings := verylow_high_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_high_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				verylow_high_buildings := verylow_high_buildings + temp_buildings_high_risk;
				verylow_med_buildings := verylow_med_buildings + ((temp_buildings_high_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - (constant_rl20*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - (constant_rl20*temp_buildings);
				verylow_med_buildings := verylow_med_buildings + (constant_rl20*temp_buildings);
			ELSEIF temp_buildings_med_risk-(constant_rl20*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				verylow_med_buildings:= verylow_med_buildings + temp_buildings_med_risk;
				verylow_low_buildings := verylow_low_buildings + ((temp_buildings_med_risk-(constant_rl20*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - (constant_rl20*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-(constant_rl20*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - (constant_rl20*temp_buildings);
				verylow_low_buildings := verylow_low_buildings + (constant_rl20*temp_buildings);
			END IF;
			temp := temp - constant_rl20*temp;
			temp_area := temp_area - constant_rl20*temp_area;
			temp_buildings := temp_buildings - constant_rl20*temp_buildings;
		END IF;
		-- temp := temp - extreme - veryhigh - high - moderate - low - verylow;

		temp_rl20 := 0;
		IF temp_dis_percent>125 THEN
			temp_rl20 := temp_dis_percent - 100;
		END IF;
			
		IF temp_dis_percent>125 THEN
			veryhigh := veryhigh + (temp_rl20/100)*temp;
			veryhigh_buildings := veryhigh_buildings + (temp_rl20/100)*temp_buildings;
			veryhigh_area := veryhigh_area + (temp_rl20/100)*temp_area;
			IF temp_high_risk-((temp_rl20/100)*temp) >= 0 AND temp_high_risk>0 THEN
				temp_high_risk = temp_high_risk - ((temp_rl20/100)*temp);
				veryhigh_high := veryhigh_high + ((temp_rl20/100)*temp);
			ELSEIF temp_high_risk-((temp_rl20/100)*temp) < 0 AND temp_high_risk>0 THEN
				veryhigh_high := veryhigh_high + temp_high_risk;
				veryhigh_med := veryhigh_med + ((temp_high_risk-((temp_rl20/100)*temp))*-1);
				temp_med_risk = temp_med_risk + (temp_high_risk - ((temp_rl20/100)*temp));
				temp_high_risk = 0;
			ELSEIF temp_med_risk-((temp_rl20/100)*temp) >= 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				temp_med_risk = temp_med_risk - ((temp_rl20/100)*temp);
				veryhigh_med := veryhigh_med + ((temp_rl20/100)*temp);
			ELSEIF temp_med_risk-((temp_rl20/100)*temp) < 0 AND temp_med_risk>0 AND temp_high_risk<=0 THEN
				veryhigh_med := veryhigh_med + temp_med_risk;
				veryhigh_low := veryhigh_low + ((temp_med_risk-((temp_rl20/100)*temp))*-1);
				temp_low_risk = temp_low_risk + (temp_med_risk - ((temp_rl20/100)*temp));
				temp_med_risk = 0;
			ELSEIF temp_low_risk-((temp_rl20/100)*temp) >= 0 AND temp_low_risk>0 AND temp_high_risk<=0 AND temp_med_risk<=0 THEN
				temp_low_risk = temp_low_risk - ((temp_rl20/100)*temp);
				veryhigh_low := veryhigh_low + ((temp_rl20/100)*temp);
			END IF;

			IF temp_buildings_high_risk-((temp_rl20/100)*temp_buildings) >= 0 AND temp_buildings_high_risk>0 THEN
				temp_buildings_high_risk = temp_buildings_high_risk - ((temp_rl20/100)*temp_buildings);
				veryhigh_high_buildings := veryhigh_high_buildings + ((temp_rl20/100)*temp_buildings);
			ELSEIF temp_buildings_high_risk-((temp_rl20/100)*temp_buildings) < 0 AND temp_buildings_high_risk>0 THEN
				veryhigh_high_buildings := veryhigh_high_buildings + temp_buildings_high_risk;
				veryhigh_med_buildings := veryhigh_med_buildings + ((temp_buildings_high_risk-((temp_rl20/100)*temp_buildings))*-1);
				temp_buildings_med_risk = temp_buildings_med_risk + (temp_buildings_high_risk - ((temp_rl20/100)*temp_buildings));
				temp_buildings_high_risk = 0;
			ELSEIF temp_buildings_med_risk-((temp_rl20/100)*temp_buildings) >= 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				temp_buildings_med_risk = temp_buildings_med_risk - ((temp_rl20/100)*temp_buildings);
				veryhigh_med_buildings := veryhigh_med_buildings + ((temp_rl20/100)*temp_buildings);
			ELSEIF temp_buildings_med_risk-((temp_rl20/100)*temp_buildings) < 0 AND temp_buildings_med_risk>0 AND temp_buildings_high_risk<=0 THEN
				veryhigh_med_buildings := veryhigh_med_buildings + temp_buildings_med_risk;
				veryhigh_low_buildings := veryhigh_low_buildings + ((temp_buildings_med_risk-((temp_rl20/100)*temp_buildings))*-1);
				temp_buildings_low_risk = temp_buildings_low_risk + (temp_buildings_med_risk - ((temp_rl20/100)*temp_buildings));
				temp_buildings_med_risk = 0;
			ELSEIF temp_buildings_low_risk-((temp_rl20/100)*temp_buildings) >= 0 AND temp_buildings_low_risk>0 AND temp_buildings_high_risk<=0 AND temp_buildings_med_risk<=0 THEN
				temp_buildings_low_risk = temp_buildings_low_risk - ((temp_rl20/100)*temp_buildings);
				veryhigh_low_buildings := veryhigh_low_buildings + ((temp_rl20/100)*temp_buildings);
			END IF;
			temp := temp - ((temp_rl20/100)*temp);
			temp_area := temp_area - ((temp_rl20/100)*temp_area);
			temp_buildings := temp_buildings - ((temp_rl20/100)*temp_buildings);
		END IF;

	        RETURN NEXT;
	     END LOOP;
	END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_glofas(date, character varying, integer, character varying)
--   OWNER TO postgres;

-- Function: public.get_glofas_detail(date)

-- DROP FUNCTION public.get_glofas_detail(date);

CREATE OR REPLACE FUNCTION public.get_glofas_detail(IN p_date date)
  RETURNS TABLE(prov_code integer, dist_code integer, basin_id bigint, rl2 double precision, rl5 double precision, rl20 double precision, rl2_dis_percent integer, rl2_avg_dis_percent integer, rl5_dis_percent integer, rl5_avg_dis_percent integer, rl20_dis_percent integer, rl20_avg_dis_percent integer, rl100_pop double precision, rl100_area double precision, rl100_low_risk double precision, rl100_med_risk double precision, rl100_high_risk double precision, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision) AS
$BODY$
DECLARE var_r record;
DECLARE temp double precision;
DECLARE temp_rl20 double precision;   
DECLARE temp_dis_percent double precision;  

DECLARE constant_rl2  double precision;
DECLARE constant_rl5  double precision;
DECLARE constant_rl20  double precision;

DECLARE temp_high_risk  double precision;
BEGIN
   constant_rl2 := 0.02;
   constant_rl5 := 0.02;
   constant_rl20:= 0.18;
   
   FOR var_r IN(select 
		a.prov_code, a.dist_code, b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
		sum(a.fldarea_population) as RL100_pop,
		sum(a.fldarea_sqm) as RL100_area,
		sum(case
		  when a.deeperthan = '029 cm' then a.fldarea_population
		  else 0	 
		end) as rl100_low_risk,
		sum(case
		  when a.deeperthan = '121 cm' then a.fldarea_population
		  else 0	 
		end) as rl100_med_risk,
		sum(case
		  when a.deeperthan = '271 cm' then a.fldarea_population
		  else 0	 
		end) as rl100_high_risk
		from afg_fldzonea_100k_risk_landcover_pop a
		inner join glofasintegrated b on b.basin_id = a.basin_id
		where b.datadate = p_date and b.rl2>1
		group by a.prov_code, a.dist_code,b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent
		order by a.prov_code, a.dist_code,b.basin_id, rl100_high_risk asc)  
    LOOP
		prov_code := var_r.prov_code;
		dist_code := var_r.dist_code;
	        basin_id := var_r.basin_id; 
		rl2 := var_r.rl2;
		rl5 := var_r.rl5;
		rl20 := var_r.rl20;
		--rl2_dis_percent := var_r.rl2_dis_percent;
		rl2_dis_percent := 0;
		rl2_avg_dis_percent := var_r.rl2_avg_dis_percent;
		rl5_dis_percent := var_r.rl5_dis_percent;
		rl5_avg_dis_percent := var_r.rl5_avg_dis_percent;
		rl20_dis_percent := var_r.rl20_dis_percent;
		rl20_avg_dis_percent := var_r.rl20_avg_dis_percent;
		RL100_pop := var_r.RL100_pop;
		RL100_area := var_r.RL100_area/1000000;
		rl100_low_risk := var_r.rl100_low_risk;
		rl100_med_risk := var_r.rl100_med_risk;
		rl100_high_risk := var_r.rl100_high_risk;
		temp := var_r.RL100_pop;
		temp_high_risk := var_r.rl100_high_risk;
		extreme := 0;
	        veryhigh := 0;
	        high := 0;
	        moderate := 0;
	        low := 0;
	        verylow := 0;

		temp_dis_percent := 0;
		IF rl2_dis_percent >= 100 THEN
			temp_dis_percent := rl2_avg_dis_percent;
		ELSE
			temp_dis_percent := rl2_dis_percent;
		END IF;	
		
		IF temp_dis_percent>400 THEN
			extreme := extreme + constant_rl2*temp;
			temp := temp - constant_rl2*temp;
		ELSEIF temp_dis_percent>160 AND temp_dis_percent<=400 THEN
			veryhigh := veryhigh + constant_rl2*temp;
			temp := temp - constant_rl2*temp;
		ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
			high := high + constant_rl2*temp;
			temp := temp - constant_rl2*temp;
		ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
			moderate := moderate + constant_rl2*temp;
			temp := temp - constant_rl2*temp;
		ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
			low := low + constant_rl2*temp;
			temp := temp - constant_rl2*temp;
		ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
			verylow := verylow + constant_rl2*temp;
			temp := temp - constant_rl2*temp;
		END IF;
		--temp := temp - extreme - veryhigh - high - moderate - low - verylow;

		temp_dis_percent := 0;
		IF rl5_dis_percent >= 100 THEN
			temp_dis_percent := rl5_avg_dis_percent;
		ELSE
			temp_dis_percent := rl5_dis_percent;
		END IF;	
		
		IF temp_dis_percent>160 THEN
			IF constant_rl5*temp>temp_high_risk THEN
				extreme := extreme + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				extreme := extreme + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;
			--extreme := extreme + constant_rl5*temp;
			--temp := temp - constant_rl5*temp;
		ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
			IF constant_rl5*temp>temp_high_risk THEN
				veryhigh := veryhigh + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				veryhigh := veryhigh + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;
			--veryhigh := veryhigh + constant_rl5*temp;
			--temp := temp - constant_rl5*temp;
		ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
			IF constant_rl5*temp>temp_high_risk THEN
				high := high + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				high := high + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;
			--high := high + constant_rl5*temp;
			--temp := temp - constant_rl5*temp;
		ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
			IF constant_rl5*temp>temp_high_risk THEN
				moderate := moderate + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				moderate := moderate + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;
			--moderate := moderate + constant_rl5*temp;
			--temp := temp - constant_rl5*temp;
		ELSEIF temp_dis_percent>50 AND temp_dis_percent<=70 THEN
			IF constant_rl5*temp>temp_high_risk THEN
				low := low + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				low := low + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;
			--low := low + constant_rl5*temp;
			--temp := temp - constant_rl5*temp;
		ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
			IF constant_rl5*temp>temp_high_risk THEN
				verylow := verylow + temp_high_risk;
				temp := temp - temp_high_risk;
			ELSE
				verylow := verylow + constant_rl5*temp;
				temp := temp - constant_rl5*temp;
			END IF;
			--verylow := verylow + constant_rl5*temp;
			--temp := temp - constant_rl5*temp;
		END IF;
		--temp := temp - extreme - veryhigh - high - moderate - low - verylow;

		temp_dis_percent := 0;
		IF rl20_dis_percent >= 100 THEN
			temp_dis_percent := rl20_avg_dis_percent;
		ELSE
			temp_dis_percent := rl20_dis_percent;
		END IF;	

		IF temp_dis_percent>125 THEN
			extreme := extreme + constant_rl20*temp;
			temp := temp - constant_rl20*temp;
		ELSEIF temp_dis_percent>100 AND temp_dis_percent<=125 THEN
			veryhigh := veryhigh + constant_rl20*temp;
			temp := temp - constant_rl20*temp;
		ELSEIF temp_dis_percent>75 AND temp_dis_percent<=100 THEN
			high := high + constant_rl20*temp;
			temp := temp - constant_rl20*temp;
		ELSEIF temp_dis_percent>50 AND temp_dis_percent<=75 THEN
			moderate := moderate + constant_rl20*temp;
			temp := temp - constant_rl20*temp;
		ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
			low := low + constant_rl20*temp;
			temp := temp - constant_rl20*temp;
		ELSEIF temp_dis_percent>0 AND temp_dis_percent<=25 THEN
			verylow := verylow + constant_rl20*temp;
			temp := temp - constant_rl20*temp;
		END IF;
		-- temp := temp - extreme - veryhigh - high - moderate - low - verylow;

		temp_rl20 := 0;
		IF temp_dis_percent>125 THEN
			temp_rl20 := temp_dis_percent - 100;
		END IF;
			
		IF temp_dis_percent>125 THEN
			veryhigh := veryhigh + (temp_rl20/100)*temp;
			temp := temp - ((temp_rl20/100)*temp);
		END IF;

        RETURN NEXT;
     END LOOP;
END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_glofas_detail(date)
--   OWNER TO postgres;

-- Function: public.get_glofas_layer(date)

-- DROP FUNCTION public.get_glofas_layer(date);

CREATE OR REPLACE FUNCTION public.get_glofas_layer(IN p_date date)
  RETURNS TABLE(vuid character varying, basin_id bigint, rl2 double precision, rl5 double precision, rl20 double precision, rl2_dis_percent integer, rl2_avg_dis_percent integer, rl5_dis_percent integer, rl5_avg_dis_percent integer, rl20_dis_percent integer, rl20_avg_dis_percent integer, rl100_pop double precision, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision) AS
$BODY$
DECLARE 
    var_r record;
DECLARE temp double precision;
DECLARE temp_rl20 double precision;   
DECLARE temp_dis_percent double precision;  

DECLARE constant_rl2  double precision;
DECLARE constant_rl5  double precision;
DECLARE constant_rl20  double precision;

BEGIN
   constant_rl2 := 0.02;
   constant_rl5 := 0.02;
   constant_rl20:= 0.18;
   
   FOR var_r IN(select 
		a.vuid,
		b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
		sum(a.fldarea_population) as RL100_pop
		from afg_fldzonea_100k_risk_landcover_pop a
		inner join glofasintegrated b on b.basin_id = a.basin_id
		where b.datadate = p_date and b.rl2>1
		group by a.vuid, b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent)  
     LOOP
	vuid := var_r.vuid;
        basin_id := var_r.basin_id; 
	rl2 := var_r.rl2;
	rl5 := var_r.rl5;
	rl20 := var_r.rl20;
	rl2_dis_percent := var_r.rl2_dis_percent;
	--rl2_dis_percent := 0;
	rl2_avg_dis_percent := var_r.rl2_avg_dis_percent;
	rl5_dis_percent := var_r.rl5_dis_percent;
	rl5_avg_dis_percent := var_r.rl5_avg_dis_percent;
	rl20_dis_percent := var_r.rl20_dis_percent;
	rl20_avg_dis_percent := var_r.rl20_avg_dis_percent;
	RL100_pop := var_r.RL100_pop;
	temp := var_r.RL100_pop;
	extreme := 0;
        veryhigh := 0;
        high := 0;
        moderate := 0;
        low := 0;
        verylow := 0;

	temp_dis_percent := 0;
	IF rl2_dis_percent >= 100 THEN
		temp_dis_percent := rl2_avg_dis_percent;
	ELSE
		temp_dis_percent := rl2_dis_percent;
	END IF;	
	
	IF temp_dis_percent>400 THEN
		extreme := extreme + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>160 AND temp_dis_percent<=400 THEN
		veryhigh := veryhigh + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
		high := high + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
		moderate := moderate + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
		low := low + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=70 THEN
		verylow := verylow + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	END IF;

	temp_dis_percent := 0;
	IF rl5_dis_percent >= 100 THEN
		temp_dis_percent := rl5_avg_dis_percent;
	ELSE
		temp_dis_percent := rl5_dis_percent;
	END IF;	
	
	IF temp_dis_percent>160 THEN
		extreme := extreme + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
		veryhigh := veryhigh + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
		high := high + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
		moderate := moderate + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>50 AND temp_dis_percent<=70 THEN
		low := low + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
		verylow := verylow + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	END IF;

	temp_dis_percent := 0;
	IF rl20_dis_percent >= 100 THEN
		temp_dis_percent := rl20_avg_dis_percent;
	ELSE
		temp_dis_percent := rl20_dis_percent;
	END IF;	

	IF temp_dis_percent>125 THEN
		extreme := extreme + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>100 AND temp_dis_percent<=125 THEN
		veryhigh := veryhigh + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>75 AND temp_dis_percent<=100 THEN
		high := high + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>50 AND temp_dis_percent<=75 THEN
		moderate := moderate + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
		low := low + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>0 AND temp_dis_percent<=25 THEN
		verylow := verylow + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	END IF;

	temp_rl20 := 0;
	IF temp_dis_percent>125 THEN
		temp_rl20 := temp_dis_percent - 100;
	END IF;
		
	IF temp_rl20>125 THEN
		veryhigh := veryhigh + (temp_rl20/100)*temp;
		temp := temp - (temp_rl20/100)*temp;
	END IF;

        RETURN NEXT;
     END LOOP;
END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_glofas_layer(date)
--   OWNER TO postgres;

-- Function: public.get_glofas_query(date, character varying, integer, character varying)

-- DROP FUNCTION public.get_glofas_query(date, character varying, integer, character varying);

CREATE OR REPLACE FUNCTION public.get_glofas_query(IN p_date date, IN p_filter character varying, IN p_code integer, IN p_spt_filter character varying)
  RETURNS TABLE(basin_id bigint, rl2 double precision, rl5 double precision, rl20 double precision, rl2_dis_percent integer, rl2_avg_dis_percent integer, rl5_dis_percent integer, rl5_avg_dis_percent integer, rl20_dis_percent integer, rl20_avg_dis_percent integer, rl100_pop double precision, rl100_area double precision, rl100_buildings bigint, rl100_low_risk double precision, rl100_med_risk double precision, rl100_high_risk double precision, rl100_low_risk_buildings bigint, rl100_med_risk_buildings bigint, rl100_high_risk_buildings bigint) AS
$BODY$
  BEGIN
   IF p_filter='entireAfg' THEN
	   RETURN QUERY
		select 
		b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
		sum(coalesce(a.fldarea_population,0)) as RL100_pop,
		sum(coalesce(a.fldarea_sqm,0)) as RL100_area,
		sum(coalesce(a.area_buildings,0)) as RL100_buildings,
		sum(case
		  when a.deeperthan = '029 cm' then coalesce(a.fldarea_population,0)
		  else 0	 
		end) as rl100_low_risk,
		sum(case
		  when a.deeperthan = '121 cm' then coalesce(a.fldarea_population,0)
		  else 0	 
		end) as rl100_med_risk,
		sum(case
		  when a.deeperthan = '271 cm' then coalesce(a.fldarea_population,0)
		  else 0	 
		end) as rl100_high_risk,

		sum(case
		  when a.deeperthan = '029 cm' then coalesce(a.area_buildings,0)
		  else 0	 
		end) as rl100_low_risk_buildings,
		sum(case
		  when a.deeperthan = '121 cm' then coalesce(a.area_buildings,0)
		  else 0	 
		end) as rl100_med_risk_buildings,
		sum(case
		  when a.deeperthan = '271 cm' then coalesce(a.area_buildings,0)
		  else 0	 
		end) as rl100_high_risk_buildings
		
		from afg_fldzonea_100k_risk_landcover_pop a
		inner join glofasintegrated b on b.basin_id = a.basin_id
		where b.datadate = p_date and b.rl2>1
		group by b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent
		order by b.basin_id, rl100_high_risk asc;
    ELSEIF p_filter='currentProvince' THEN
	IF length(p_code::text)>2 THEN
		RETURN QUERY
			select 
			b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
			sum(coalesce(a.fldarea_population,0)) as RL100_pop,
			sum(coalesce(a.fldarea_sqm,0)) as RL100_area,
			sum(coalesce(a.area_buildings,0)) as RL100_buildings,
			sum(case
			  when a.deeperthan = '029 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_low_risk,
			sum(case
			  when a.deeperthan = '121 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_med_risk,
			sum(case
			  when a.deeperthan = '271 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_high_risk,

			sum(case
			  when a.deeperthan = '029 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_low_risk_buildings,
			sum(case
			  when a.deeperthan = '121 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_med_risk_buildings,
			sum(case
			  when a.deeperthan = '271 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_high_risk_buildings
			from afg_fldzonea_100k_risk_landcover_pop a
			inner join glofasintegrated b on b.basin_id = a.basin_id
			where b.datadate = p_date AND a.dist_code = p_code and b.rl2>1
			group by b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent
			order by b.basin_id, rl100_high_risk asc;
	ELSE
		RETURN QUERY
			select 
			b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
			sum(coalesce(a.fldarea_population,0)) as RL100_pop,
			sum(coalesce(a.fldarea_sqm,0)) as RL100_area,
			sum(coalesce(a.area_buildings,0)) as RL100_buildings,
			sum(case
			  when a.deeperthan = '029 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_low_risk,
			sum(case
			  when a.deeperthan = '121 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_med_risk,
			sum(case
			  when a.deeperthan = '271 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_high_risk,

			sum(case
			  when a.deeperthan = '029 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_low_risk_buildings,
			sum(case
			  when a.deeperthan = '121 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_med_risk_buildings,
			sum(case
			  when a.deeperthan = '271 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_high_risk_buildings
			from afg_fldzonea_100k_risk_landcover_pop a
			inner join glofasintegrated b on b.basin_id = a.basin_id
			where b.datadate = p_date AND a.prov_code = p_code and b.rl2>1
			group by b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent
			order by b.basin_id, rl100_high_risk asc;
	END IF;
    ELSE
		RETURN QUERY
			select 
			b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
			sum(coalesce(a.fldarea_population,0)) as RL100_pop,
			sum(coalesce(a.fldarea_sqm,0)) as RL100_area,
			sum(coalesce(a.area_buildings,0)) as RL100_buildings,
			sum(case
			  when a.deeperthan = '029 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_low_risk,
			sum(case
			  when a.deeperthan = '121 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_med_risk,
			sum(case
			  when a.deeperthan = '271 cm' then coalesce(a.fldarea_population,0)
			  else 0	 
			end) as rl100_high_risk,

			sum(case
			  when a.deeperthan = '029 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_low_risk_buildings,
			sum(case
			  when a.deeperthan = '121 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_med_risk_buildings,
			sum(case
			  when a.deeperthan = '271 cm' then coalesce(a.area_buildings,0)
			  else 0	 
			end) as rl100_high_risk_buildings
			from afg_fldzonea_100k_risk_landcover_pop a
			inner join glofasintegrated b on b.basin_id = a.basin_id
			where b.datadate = p_date AND ST_Within(a.wkb_geometry, ST_GeometryFromText(p_spt_filter, 4326)) and b.rl2>1
			group by b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent
			order by b.basin_id, rl100_high_risk asc;
    END IF;
 END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_glofas_query(date, character varying, integer, character varying)
--   OWNER TO postgres;

-- Function: public.get_glofas_rl20_layer(date, boolean)

-- DROP FUNCTION public.get_glofas_rl20_layer(date, boolean);

CREATE OR REPLACE FUNCTION public.get_glofas_rl20_layer(IN p_date date, IN include boolean)
  RETURNS TABLE(vuid character varying, basin_id bigint, rl2 double precision, rl5 double precision, rl20 double precision, rl2_dis_percent integer, rl2_avg_dis_percent integer, rl5_dis_percent integer, rl5_avg_dis_percent integer, rl20_dis_percent integer, rl20_avg_dis_percent integer, rl100_pop double precision, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision) AS
$BODY$
DECLARE 
    var_r record;
DECLARE temp double precision;
DECLARE temp_rl20 double precision;   
DECLARE temp_dis_percent double precision;  

DECLARE constant_rl2  double precision;
DECLARE constant_rl5  double precision;
DECLARE constant_rl20  double precision;

BEGIN
   constant_rl2 := 0.02;
   constant_rl5 := 0.02;
   constant_rl20:= 0.18;

   IF not include THEN 
	p_date = date('0001-01-01');
   END IF;
   
   FOR var_r IN(select 
		a.vuid,
		b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
		sum(a.fldarea_population) as RL100_pop
		from afg_fldzonea_100k_risk_landcover_pop a
		inner join glofasintegrated b on b.basin_id = a.basin_id
		where b.datadate = p_date and b.rl2>1
		group by a.vuid, b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent)  
     LOOP
	vuid := var_r.vuid;
        basin_id := var_r.basin_id; 
	rl2 := var_r.rl2;
	rl5 := var_r.rl5;
	rl20 := var_r.rl20;
	--rl2_dis_percent := var_r.rl2_dis_percent;
	rl2_dis_percent := 0;
	rl2_avg_dis_percent := var_r.rl2_avg_dis_percent;
	rl5_dis_percent := var_r.rl5_dis_percent;
	--rl5_dis_percent := 0;
	rl5_avg_dis_percent := var_r.rl5_avg_dis_percent;
	rl20_dis_percent := var_r.rl20_dis_percent;
	rl20_avg_dis_percent := var_r.rl20_avg_dis_percent;
	RL100_pop := var_r.RL100_pop;
	temp := var_r.RL100_pop;
	extreme := 0;
        veryhigh := 0;
        high := 0;
        moderate := 0;
        low := 0;
        verylow := 0;

	temp_dis_percent := 0;
	IF rl2_dis_percent >= 100 THEN
		temp_dis_percent := rl2_avg_dis_percent;
	ELSE
		temp_dis_percent := rl2_dis_percent;
	END IF;	
	
	IF temp_dis_percent>400 THEN
		extreme := extreme + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>160 AND temp_dis_percent<=400 THEN
		veryhigh := veryhigh + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
		high := high + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
		moderate := moderate + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
		low := low + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=70 THEN
		verylow := verylow + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	END IF;

	temp_dis_percent := 0;
	IF rl5_dis_percent >= 100 THEN
		temp_dis_percent := rl5_avg_dis_percent;
	ELSE
		temp_dis_percent := rl5_dis_percent;
	END IF;	
	
	IF temp_dis_percent>160 THEN
		extreme := extreme + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
		veryhigh := veryhigh + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
		high := high + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
		moderate := moderate + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>50 AND temp_dis_percent<=70 THEN
		low := low + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
		verylow := verylow + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	END IF;

	temp_dis_percent := 0;
	IF rl20_dis_percent >= 100 THEN
		temp_dis_percent := rl20_avg_dis_percent;
	ELSE
		temp_dis_percent := rl20_dis_percent;
	END IF;	

	IF temp_dis_percent>125 THEN
		extreme := extreme + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>100 AND temp_dis_percent<=125 THEN
		veryhigh := veryhigh + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>75 AND temp_dis_percent<=100 THEN
		high := high + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>50 AND temp_dis_percent<=75 THEN
		moderate := moderate + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
		low := low + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>0 AND temp_dis_percent<=25 THEN
		verylow := verylow + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	END IF;

	temp_rl20 := 0;
	IF temp_dis_percent>125 THEN
		temp_rl20 := temp_dis_percent - 100;
	END IF;
		
	IF temp_dis_percent>125 THEN
		veryhigh := veryhigh + (temp_rl20/100)*temp;
		temp := temp - (temp_rl20/100)*temp;
	END IF;

        RETURN NEXT;
     END LOOP;
END; 

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_glofas_rl20_layer(date, boolean)
--   OWNER TO postgres;

-- Function: public.get_glofas_rl20_layer(date)

-- DROP FUNCTION public.get_glofas_rl20_layer(date);

CREATE OR REPLACE FUNCTION public.get_glofas_rl20_layer(IN p_date date)
  RETURNS TABLE(vuid character varying, basin_id bigint, rl2 double precision, rl5 double precision, rl20 double precision, rl2_dis_percent integer, rl2_avg_dis_percent integer, rl5_dis_percent integer, rl5_avg_dis_percent integer, rl20_dis_percent integer, rl20_avg_dis_percent integer, rl100_pop double precision, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision) AS
$BODY$
DECLARE 
    var_r record;
DECLARE temp double precision;
DECLARE temp_rl20 double precision;   
DECLARE temp_dis_percent double precision;  

DECLARE constant_rl2  double precision;
DECLARE constant_rl5  double precision;
DECLARE constant_rl20  double precision;

BEGIN
   constant_rl2 := 0.02;
   constant_rl5 := 0.02;
   constant_rl20:= 0.18;
   
   FOR var_r IN(select 
		a.vuid,
		b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent,  
		sum(a.fldarea_population) as RL100_pop
		from afg_fldzonea_100k_risk_landcover_pop a
		inner join glofasintegrated b on b.basin_id = a.basin_id
		where b.datadate = p_date and b.rl2>1
		group by a.vuid, b.basin_id, b.rl2, b.rl5, b.rl20, b.rl2_dis_percent, b.rl2_avg_dis_percent, b.rl5_dis_percent, b.rl5_avg_dis_percent, b.rl20_dis_percent, b.rl20_avg_dis_percent)  
     LOOP
	vuid := var_r.vuid;
        basin_id := var_r.basin_id; 
	rl2 := var_r.rl2;
	rl5 := var_r.rl5;
	rl20 := var_r.rl20;
	--rl2_dis_percent := var_r.rl2_dis_percent;
	rl2_dis_percent := 0;
	rl2_avg_dis_percent := var_r.rl2_avg_dis_percent;
	rl5_dis_percent := var_r.rl5_dis_percent;
	--rl5_dis_percent := 0;
	rl5_avg_dis_percent := var_r.rl5_avg_dis_percent;
	rl20_dis_percent := var_r.rl20_dis_percent;
	rl20_avg_dis_percent := var_r.rl20_avg_dis_percent;
	RL100_pop := var_r.RL100_pop;
	temp := var_r.RL100_pop;
	extreme := 0;
        veryhigh := 0;
        high := 0;
        moderate := 0;
        low := 0;
        verylow := 0;

	temp_dis_percent := 0;
	IF rl2_dis_percent >= 100 THEN
		temp_dis_percent := rl2_avg_dis_percent;
	ELSE
		temp_dis_percent := rl2_dis_percent;
	END IF;	
	
	IF temp_dis_percent>400 THEN
		extreme := extreme + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>160 AND temp_dis_percent<=400 THEN
		veryhigh := veryhigh + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
		high := high + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
		moderate := moderate + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
		low := low + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=70 THEN
		verylow := verylow + constant_rl2*temp;
		temp := temp - constant_rl2*temp;
	END IF;

	temp_dis_percent := 0;
	IF rl5_dis_percent >= 100 THEN
		temp_dis_percent := rl5_avg_dis_percent;
	ELSE
		temp_dis_percent := rl5_dis_percent;
	END IF;	
	
	IF temp_dis_percent>160 THEN
		extreme := extreme + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>120 AND temp_dis_percent<=160 THEN
		veryhigh := veryhigh + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>90 AND temp_dis_percent<=120 THEN
		high := high + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>70 AND temp_dis_percent<=90 THEN
		moderate := moderate + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>50 AND temp_dis_percent<=70 THEN
		low := low + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
		verylow := verylow + constant_rl5*temp;
		temp := temp - constant_rl5*temp;
	END IF;

	temp_dis_percent := 0;
	IF rl20_dis_percent >= 100 THEN
		temp_dis_percent := rl20_avg_dis_percent;
	ELSE
		temp_dis_percent := rl20_dis_percent;
	END IF;	

	IF temp_dis_percent>125 THEN
		extreme := extreme + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>100 AND temp_dis_percent<=125 THEN
		veryhigh := veryhigh + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>75 AND temp_dis_percent<=100 THEN
		high := high + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>50 AND temp_dis_percent<=75 THEN
		moderate := moderate + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>25 AND temp_dis_percent<=50 THEN
		low := low + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	ELSEIF temp_dis_percent>0 AND temp_dis_percent<=25 THEN
		verylow := verylow + constant_rl20*temp;
		temp := temp - constant_rl20*temp;
	END IF;

	temp_rl20 := 0;
	IF temp_dis_percent>125 THEN
		temp_rl20 := temp_dis_percent - 100;
	END IF;
		
	IF temp_dis_percent>125 THEN
		veryhigh := veryhigh + (temp_rl20/100)*temp;
		temp := temp - (temp_rl20/100)*temp;
	END IF;

        RETURN NEXT;
     END LOOP;
END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_glofas_rl20_layer(date)
--   OWNER TO postgres;

-- Function: public.get_merge_glofas_gfms_detail(date)

-- DROP FUNCTION public.get_merge_glofas_gfms_detail(date);

CREATE OR REPLACE FUNCTION public.get_merge_glofas_gfms_detail(IN p_date date)
  RETURNS TABLE(basin_id bigint, dist_code integer, prov_code integer, extreme double precision, veryhigh double precision, high double precision, moderate double precision, low double precision, verylow double precision) AS
$BODY$
DECLARE 
    var_r record;
DECLARE temp double precision;

BEGIN

   FOR var_r IN(select distinct
	c.basin_id, c.dist_code, c.prov_code,
	a.basin_id as glofas_basin_id,
	a.extreme,
	a.veryhigh,
	a.high,
	a.moderate,
	a.low,
	a.verylow,
	b.basin_id as gfms_basin_id,
	b.gfms_verylow_pop,
	b.gfms_low_pop,
	b.gfms_med_pop,
	b.gfms_high_pop,
	b.gfms_veryhigh_pop,
	b.gfms_extreme_pop
	from afg_ppla_basin c
	left join get_gfms_detail(p_date) b on b.basin_id=c.basin_id and b.dist_code=c.dist_code
	left join get_glofas_detail(p_date-1) a on a.basin_id=c.basin_id and a.dist_code=c.dist_code
	where a.dist_code is not NULL or b.dist_code is not NULL
	order by c.basin_id, c.dist_code, c.prov_code)  
     LOOP
	IF var_r.glofas_basin_id IS NOT NULL THEN
		basin_id := var_r.basin_id; 
		dist_code := var_r.dist_code;
		prov_code := var_r.prov_code;
		extreme := var_r.extreme;
		veryhigh := var_r.veryhigh;
		high := var_r.high;
		moderate := var_r.moderate;
		low := var_r.low;
		verylow := var_r.verylow;

	ELSE
		basin_id := var_r.gfms_basin_id; 
		dist_code := var_r.dist_code;
		prov_code := var_r.prov_code;
		extreme := var_r.gfms_extreme_pop;
		veryhigh := var_r.gfms_veryhigh_pop;
		high := var_r.gfms_high_pop;
		moderate := var_r.gfms_med_pop;
		low := var_r.gfms_low_pop;
		verylow := var_r.gfms_verylow_pop;

		
	END IF;	

        

        RETURN NEXT;
     END LOOP;
END; $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
-- ALTER FUNCTION public.get_merge_glofas_gfms_detail(date)
--   OWNER TO postgres;
