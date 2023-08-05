# RESPONSE_TREE_TEMPLATE = {}
 
PANEL_TITLES = {
    'pop': 'Population',
    'area': 'Area (km2)',
    'settlement': 'Settlements',
    'building': 'Buildings',
    'road': 'Road (km)',
    'healthfacility': 'Health Facilities',
}

HEALTHFAC_INDEX = {
    1: "h1",
    2: "h2",
    3: "h3",
    4: "sh",
    5: "rh",
    6: "mh",
    7: "datc",
    8: "tbc",
    9: "mntc",
    10: "chc",
    11: "bhc",
    12: "dcf",
    13: "mch",
    14: "shc",
    15: "ec",
    16: "pyc",
    17: "pic",
    18: "mc",
    19: "moph",
    20: "epi",
    21: "sfc",
    22: "mht",
    23: "other",
}

HEALTHFAC_TYPES = {
    "h1": "Regional / National Hospital (H1)",
    "h2": "Provincial Hospital (H2)",
    "h3": "District Hospital (H3)",
    "sh": "Special Hospital (SH)",
    "rh": "Rehabilitation Center (RH)",
    "mh": "Maternity Home (MH)",
    "datc": "Drug Addicted Treatment Center",
    "tbc": "TB Control Center (TBC)",
    "mntc": "Mental Clinic / Hospital",
    "chc": "Comprehensive Health Center (CHC)",
    "bhc": "Basic Health Center (BHC)",
    "dcf": "Day Care Feeding",
    "mch": "MCH Clinic M1 or M2 (MCH)",
    "shc": "Sub Health Center (SHC)",
    "ec": "Eye Clinic / Hospital",
    "pyc": "Physiotherapy Center",
    "pic": "Private Clinic",
    "mc": "Malaria Center (MC)",
    "moph": "MoPH National",
    "epi": "EPI Fixed Center (EPI)",
    "sfc": "Supplementary Feeding Center (SFC)",
    "mht": "Mobile Health Team (MHT)",
    "other": "Other",
}

HEALTHFAC_TYPES_INVERSE = {v: k for k, v in HEALTHFAC_TYPES.items()}
HEALTHFAC_GROUP7 = ['h1','h2','h3','chc','bhc','shc','other']
HEALTHFAC_GROUP14 = ['h1','h2','h3','sh','rh','mh','datc','chc','bhc','shc','pic','mc','mht','other']

ROAD_INDEX = {
    1: "highway",
    2: "primary",
    3: "secondary",
    4: "tertiary",
    5: "residential",
    6: "track",
    7: "path",
    8: "river_crossing",
    9: "bridge",
}

ROAD_TYPES = {
    "highway": "Highway",
    "primary": "Primary",
    "secondary": "Secondary",
    "tertiary": "Tertiary",
    "residential": "Residential",
    "track": "Track",
    "path": "Path",
    "river_crossing": "River Crossing",
    "bridge": "Bridge",
}

ROAD_TYPES_INVERSE = {v: k for k, v in ROAD_TYPES.items()}

LANDCOVER_INDEX = {
    1: 'water_body',
    2: 'barren_land',
    3: 'built_up',
    4: 'fruit_trees',
    5: 'irrigated_agricultural_land',
    6: 'snow',
    7: 'rainfed',
    8: 'rangeland',
    9: 'sandcover',
    10: 'vineyards',
    11: 'forest',
    12: 'sand_dunes',
}

LANDCOVER_TYPES = {
    'water_body': 'Water body and Marshland',
    'barren_land': 'Barren land',
    'built_up': 'Build Up',
    'fruit_trees': 'Fruit Trees',
    'irrigated_agricultural_land': 'Irrigated Agricultural Land',
    'snow': 'Snow',
    'rainfed': 'Rainfed',
    'rangeland': 'Rangeland',
    'sandcover': 'Sand Covered Areas',
    'vineyards': 'Vineyards',
    'forest': 'Forest & Shrub',
    'sand_dunes': 'Sand Dunes',
}

PROVINCESUMMARY_LANDCOVER_TYPES = {
    'water_body': 'water_body',
    'barren_land': 'barren_land',
    'built_up': 'built_up',
    'fruit_trees': 'fruit_trees',
    'irrigated_agricultural_land': 'irrigated_agricultural_land',
    'permanent_snow': 'snow',
    'rainfed_agricultural_land': 'rainfed',
    'rangeland': 'rangeland',
    'sandcover': 'sandcover',
    'vineyards': 'vineyards',
    'forest': 'forest',
    'sand_dunes': 'sand_dunes',
}

LANDCOVER_TYPES_INVERSE = {v: k for k, v in LANDCOVER_TYPES.items()}

LANDCOVER_TYPES_GROUP = {
    'built_up': ['built_up'],
    'cultivated': ['fruit_trees','irrigated_agricultural_land','rainfed','vineyards'],
    'barren': ['water_body','barren_land','snow','rangeland','sandcover','forest','sand_dunes'],
}

LANDCOVER_TYPES_GROUP_INVERSE = {l:g  for l in LANDCOVER_TYPES for g in LANDCOVER_TYPES_GROUP if l in LANDCOVER_TYPES_GROUP[g]}

LIKELIHOOD_INDEX = {
    1: 'verylow',
    2: 'low',
    3: 'med',
    4: 'high',
    5: 'veryhigh',
    6: 'extreme',
}

LIKELIHOOD_TYPES = {
    'verylow': 'Very Low',
    'low': 'Low',
    'med': 'Med',
    'high': 'High',
    'veryhigh': 'Very High',
    'extreme': 'Extreme',
}

LIKELIHOOD_INDEX_INVERSE = {v: k for k, v in LIKELIHOOD_INDEX.items()}

DEPTH_INDEX = {
    1: 'low',
    2: 'med',
    3: 'high',
}

DEPTH_TYPES = {
    'low': '029 cm',
    'med': '121 cm',
    'high': '271 cm',
}

DEPTH_TYPES_SIMPLE = {
    'low': 'Low',
    'med': 'Medium',
    'high': 'High',
}

DEPTH_TYPES_INVERSE = {v: k for k, v in DEPTH_TYPES.items()}

AVA_LIKELIHOOD_INDEX = {1:'low', 2:'med', 3:'high'}
AVA_LIKELIHOOD_TYPES = {'high':'High','med':'Medium','low':'Low'}
AVA_LIKELIHOOD_INVERSE = {v: k for k, v in AVA_LIKELIHOOD_TYPES.items()}

TIME_DISTANCE_TYPES = ['l1','l2','l3','l4','l5','l6','l7','l8','g8']
TIME_DISTANCE_TITLES = {'l1':'1>','l2':'2>','l3':'3>','l4':'4>','l5':'5>','l6':'6>','l7':'7>','l8':'8>','g8':'8<'}

EARTHQUAKE_TYPES = {
    'weak': 'Weak',
    'light': 'Light',
    'moderate': 'Moderate',
    'strong': 'Strong',
    'verystrong': 'Very Strong',
    'severe': 'Severe',
    'violent': 'Violent',
    'extreme': 'Extreme',    
}
EARTHQUAKE_TYPES_ORDER = ['weak','light','moderate','strong','verystrong','severe','violent','extreme']

LANDSLIDE_TYPES = {
    'very_low': 'Very Low',  
    'low': 'Low',
    'moderate': 'Moderate',
    'high': 'High',
    'very_high': 'Very High',
}
LANDSLIDE_TYPES_ORDER = ['very_low','low','moderate','high','very_high']
