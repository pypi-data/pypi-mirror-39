-- put drop function sql here

DROP FUNCTION IF EXISTS public.get_merge_glofas_gfms(date, character varying, integer, character varying);

DROP FUNCTION IF EXISTS public.get_gfms_detail(date);

DROP FUNCTION IF EXISTS public.get_gfms_layer(date);

DROP FUNCTION IF EXISTS public.get_gfms_layer(date, boolean);

DROP FUNCTION IF EXISTS public.get_gfms_query(date, character varying, integer, character varying);

DROP FUNCTION IF EXISTS public.get_glofas(date, character varying, integer, character varying);

DROP FUNCTION IF EXISTS public.get_glofas_detail(date);

DROP FUNCTION IF EXISTS public.get_glofas_layer(date);

DROP FUNCTION IF EXISTS public.get_glofas_query(date, character varying, integer, character varying);

DROP FUNCTION IF EXISTS public.get_glofas_rl20_layer(date, boolean);

DROP FUNCTION IF EXISTS public.get_glofas_rl20_layer(date);

DROP FUNCTION IF EXISTS public.get_merge_glofas_gfms_detail(date);
