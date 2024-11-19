# -*- coding: utf-8 -*-
"""
First very simple toy Unit Commitment model of Benelux zone - alone -> with PyPSA and ERAA data
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

"""
# I) Set global parameters for the case simulated
"""
# unique country modeled in this example -> some comments are provided 
# below to explain how PyPSA model could be extended to a multiple countries case
# -> look at "[Multiple-countries ext.]" tags
country = "benelux"
# select first ERAA year available, as an example 
# -> see values in input/long_term_uc/elec-europe_eraa-available-values.json
year = 2025
# and a given "climatic year" (to possibly test different climatic*weather conditions)
# -> idem
# N.B. Ask Boutheina OUESLATI on Wednesday to get an idea of the 'climatic' versus 'weather' conditions 
climatic_year = 1989
# TODO: used?
agg_prod_types_selec = ["wind_onshore", "wind_offshore", "solar_pv"]

"""
II) Initialize a UCRunParams object 
"""
# N.B. UC = Unit Commitment, i.e. supply-demand equilibrium problem 
# - for given electricity generation capacities
from datetime import datetime, timedelta
from long_term_uc.common.uc_run_params import UCRunParams
# Set start and end date corresponding to the period to be simulated
# ATTENTION: uc_period_end not included -> here period {1900/1/1 00:00, 1900/1/1 01:00, ..., 1900/1/13 23:00}
# N.B. Calendar of year 1900 used here, to make explicit the fact that ERAA data are 'projected' 
# on a fictive calendar; as made of 52 full weeks
uc_period_start = datetime(year=1900, month=1, day=1)
uc_period_end = uc_period_start + timedelta(days=14)
selected_countries = [country]  # [Multiple-countries ext.] List with multiple country names
uc_run_params = UCRunParams(selected_countries=selected_countries, selected_target_year=year, 
                            selected_climatic_year=climatic_year, 
                            selected_prod_types={"benelux": agg_prod_types_selec},
                            uc_period_start=uc_period_start,
                            uc_period_end=uc_period_end)

"""
III) Get needed data - from ERAA csv files in data\\ERAA_2023-2
"""
from long_term_uc.utils.eraa_data_reader import get_countries_data

# III.1) Get data for Italy... just for test -> data used when writing PyPSA model will be re-obtained afterwards
demand, agg_cf_data, agg_gen_capa_data, interco_capas = \
    get_countries_data(uc_run_params=uc_run_params, agg_prod_types_with_cf_data=agg_prod_types_selec,
                       aggreg_prod_types_def=AGG_PROD_TYPES_DEF)

# III.2) In this case, decompose aggreg. CF data into three sub-dicts (for following ex. to be more explicit)
from long_term_uc.utils.df_utils import selec_in_df_based_on_list
solar_pv = {
    country: selec_in_df_based_on_list(df=agg_cf_data[country], selec_col="production_type_agg",
                                       selec_vals=["solar_pv"], rm_selec_col=True)
}
wind_on_shore = {
    country: selec_in_df_based_on_list(df=agg_cf_data[country], selec_col="production_type_agg",
                                       selec_vals=["wind_onshore"], rm_selec_col=True)
}
wind_off_shore = {
    country: selec_in_df_based_on_list(df=agg_cf_data[country], selec_col="production_type_agg",
                                       selec_vals=["wind_offshore"], rm_selec_col=True)
}

nuclear = {
    country: selec_in_df_based_on_list(df=agg_cf_data[country], selec_col="production_type_agg",
                                       selec_vals=["nuclear"], rm_selec_col=True)
}


"""
IV) Build PyPSA model - with unique country (benelux here)
"""
# IV.1) Initialize PyPSA Network (basis of all your simulations this week!). 
import pypsa
print("Initialize PyPSA network")
# Here snapshots is used to defined the temporal period associated to considered UC model
# -> for ex. as a list of indices (other formats; like data ranges can be used instead) 
network = pypsa.Network(snapshots=demand[country].index)
# And print it to check that for now it is... empty
print(network)

#################################################
# KEY POINT: main parameters needed for Italy description in PyPSA are set in script
# long_term_uc.toy_model_params.italy_parameters.py
# To get the meaning and format of main PyPSA objects/attributes look 
# at file doc/toy-model_tutorial.md
#################################################

# IV.2) Add bus for considered country
# N.B. Italy coordinates set randomly! (not useful in the calculation that will be done this week)
from long_term_uc.toy_model_params.italy_parameters import gps_coords
coordinates = {"benelux": gps_coords}
# IV.2.1) For brevity, set country trigram as the "id" of this zone in following model definition (and observed outputs)
from long_term_uc.include.dataset_builder import set_country_trigram
country_trigram = set_country_trigram(country=country)
# N.B. Multiple bus would be added if multiple countries were considered
network.add("Bus", name=country_trigram, x=coordinates[country][0], y=coordinates[country][1])
# [Multiple-count. ext., start] Loop over the different countries to add an associated bus
# for country in modeled_countries:
#    network.add("Bus", name=country_trigram, x=coordinates[country][0], y=coordinates[country][1])
# [Multiple-count. ext., end]

# IV.4) [VERY KEY STAGE] Generators definition, beginning with only simple parameters. 
# Almost "real Italy"... excepting hydraulic storage and Demand-Side Response capacity 
# (we will come back on this later)
# Thanks to Tim WALTER - student of last year ATHENS course, detailed parameter values associated 
# to different fuel sources are available in following dictionary. You can use it or search/define 
# fictive alternative values instead -> plenty infos on Internet on this... sometimes of "varying" quality! 
# (keeping format of dataclass - sort of enriched dictionary -, just change values in 
# file long_term_uc/common/fuel_sources.py)
from long_term_uc.common.fuel_sources import FUEL_SOURCES
from long_term_uc.toy_model_params.italy_parameters import get_generators
# IV.4.1) get generators to be set on the unique considered bus here 
# -> from long_term_uc.toy_model_params.italy_parameters.py script
generators = get_generators(country_trigram=country_trigram, fuel_sources=FUEL_SOURCES, 
                            wind_on_shore_data=wind_on_shore[country], wind_off_shore_data=wind_off_shore[country],
                            solar_pv_data=solar_pv[country])

# IV.4.2) Loop over previous list of dictionaries to add each of the generators to PyPSA network
# [Coding trick] ** used to "unpack" the dictionary as named parameters
for generator in generators:
    network.add("Generator", bus=country_trigram, **generator, )
# [Multiple-count. ext., start] Idem but adding the different generators to the bus (country) they are connected to
# -> a correspondence (for ex. with a dictionary) between bus names and list of associated 
# generators is then needed
# [Multiple-count. ext., end]

# IV.5) Add load
# N.B. "carrier" here just to explicit that an AC current network is considered
# IV.5.1) Setting attribute values in a dictionary
loads = [
    {
        "name": f"{country_trigram}-load", "bus": country_trigram,
        "carrier": "AC", "p_set": demand[country]["value"].values
    }
]
# [Coding trick] f"{my_var} is associated to {my_country}" is a f-string or formatted-string (https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
# [Multiple-count. ext., start] Multiple dictionaries in previous list, 
# each of them corresponding to a given bus (country)
# [Multiple-count. ext., end]

# IV.5.2) Then adding Load objects to PyPSA model
for load in loads:
    network.add("Load", **load)

# IV.6) A few prints to check/observe that created PyPSA model be coherent 
# IV.6.1) Print the network after having completed it
print(network)
# IV.6.2) And plot it. Surely better when having multiple buses (countries)!!
network.plot(
    title="Mixed AC (blue) - DC (red) network - DC (cyan)",
    color_geomap=True,
    jitter=0.3,
)
# IV.6.3) Print out list of generators
print(network.generators)

# IV.7) "Optimize network" i.e., solve the associated Unit-Commitment problem
# IV.7.1) Solve and print result
result = network.optimize(solver_name="highs")
print(result)
print(f"Total cost at optimum: {network.objective:.2f}")
# IV.7.2) [Optional] For those who want to get a standard .lp file containing 
# the equations associated to the solved problem
# -> will be saved in output folder output/long_term_uc/data
from pathlib import Path
import pypsa.optimization as opt
from long_term_uc.common.long_term_uc_io import OUTPUT_DATA_FOLDER
m = opt.create_model(network)
m.to_file(Path(f'{OUTPUT_DATA_FOLDER}/model_{country_trigram}.lp'))

# IV.8) Plot a few info/results
import matplotlib.pyplot as plt
print("Plot generation and prices figures")
# IV.8.1) Plot generation units capacities
# N.B. p_nom_opt is the optimized capacity (that can be also a variable in PyPSA but here... 
# not optimized - only UC problem -> values plotted correspond to the ones that can be found in input data)
network.generators.p_nom_opt.drop(f"Failure_{country_trigram}").div(1e3).plot.bar(ylabel="GW", figsize=(8, 3))
# [Coding trick] Matplotlib can directly adapt size of figure to fit with values plotted
plt.tight_layout()

# IV.8.2) And "stack" of optimized production profiles -> key graph to interpret UC solution -> will be 
# saved in file output/long_term_uc/figures/prod_italy_{year}_{period start, under format %Y-%m-%d}.png
network.generators_t.p.div(1e3).plot.area(subplots=False, ylabel="GW")
from long_term_uc.common.long_term_uc_io import get_prod_figure, get_price_figure
plt.tight_layout()
plt.savefig(get_prod_figure(country=country, year=year, start_horizon=uc_run_params.uc_period_start))

# IV.8.3) Finally, "marginal prices" -> QUESTION: meaning? 
# -> saved in file output/long_term_uc/figures/prices_italy_{year}_{period start, under format %Y-%m-%d}.png
# QUESTION: how can you interpret the very constant value plotted?
network.buses_t.marginal_price.mean(1).plot.area(figsize=(8, 3), ylabel="Euro per MWh")
plt.tight_layout()
plt.savefig(get_price_figure(country=country, year=year, start_horizon=uc_run_params.uc_period_start))
