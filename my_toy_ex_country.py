# -*- coding: utf-8 -*-
"""
First very simple toy Unit Commitment model of... YOUR COUNTRY zone - alone -> with PyPSA and ERAA data
-> 
(i) copy/paste/rename this file according to your country name
(ii) copy/paste pieces of code from my_toy_ex_italy.py to this created file
(iii) Also, set the parameters of your country electricity generators in file {your country}_parameters.py,
following/adapting model of long_term_uc/toy_model_params/italy_parameters.py
"""
import warnings
#deactivate some annoying and useless warnings in pypsa/pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

AGG_PROD_TYPES_DEF = {
    "res_capa-factors": {
        "solar_pv": ["lfsolarpv"],
        "solar_thermal": ["csp_nostorage"],
        "wind_offshore": ["wind_offshore"],
        "wind_onshore": ["wind_onshore"]
    },
    "generation_capas": {
        "batteries": ["batteries"],
        "biofuel": ["biofuel"],
        "coal": ["coal", "hard_coal", "lignite"],
        "dsr": ["demand_side_response_capacity"],
        "gas": ["gas"],
        "hydro_pondage": ["hydro_pondage"],
        "hydro_pump_storage_closed_loop": ["hydro_pump_storage_closed_loop"],
        "hydro_pump_storage_open_loop": ["hydro_pump_storage_open_loop"],
        "hydro_reservoir": ["hydro_reservoir"],
        "hydro_run_of_river": ["hydro_run_of_river"],
        "nuclear": ["nuclear"], "oil": ["oil"],
        "others_fatal": ["others_non-renewable", "others_renewable"],
        "solar_pv": ["solar_photovoltaic"],
        "solar_thermal": ["solar_thermal"],
        "wind_offshore": ["wind_offshore"], "wind_onshore": ["wind_onshore"]
    }
}

