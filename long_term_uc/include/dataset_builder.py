from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import pypsa

from long_term_uc.common.error_msgs import print_errors_list, print_out_msg
from long_term_uc.common.long_term_uc_io import COMPLEM_DATA_SOURCES, COLUMN_NAMES
from long_term_uc.common.fuel_sources import FuelSources
from long_term_uc.common.uc_run_params import UCRunParams
from long_term_uc.utils.basic_utils import lexico_compar_str


@dataclass
class GenUnitsPypsaParams:
    capa_factors: str = "p_max_pu" 
    power_capa: str = "p_nom"
    energy_capa: str = None
    marginal_cost: str = "marginal_cost"
    co2_emissions: str = "co2_emissions"  # TODO: check that aligned on PyPSA generators attribute names


GEN_UNITS_PYPSA_PARAMS = GenUnitsPypsaParams()


@dataclass
class GenerationUnitData:
    name: str
    type: str
    carrier: str = None
    p_nom: float = None
    p_min_pu: float = None
    p_max_pu: float = None
    efficiency: float = None
    marginal_cost: float = None
    committable: bool = False
    max_hours: float = None
    cyclic_state_of_charge: bool = None

    def get_non_none_attr_names(self):
        return [key for key, val in self.__dict__.items() if val is not None]


def get_val_of_agg_pt_in_df(df_data: pd.DataFrame, prod_type_agg_col: str, 
                            agg_prod_type: str, value_col: str, static_val: bool) \
                                -> Union[np.ndarray, float]:
    if static_val is True:
        return df_data[df_data[prod_type_agg_col] == agg_prod_type][value_col].iloc[0]
    else:
        return np.array(df_data[df_data[prod_type_agg_col] == agg_prod_type][value_col])


UNIT_NAME_SEP = "_"


def set_country_trigram(country: str) -> str:
    return f"{country[:3].lower()}"


def get_prod_type_from_unit_name(prod_unit_name: str) -> str:
    len_country_suffix = 3 + len(UNIT_NAME_SEP)
    return prod_unit_name[len_country_suffix:]


def set_gen_unit_name(country: str, agg_prod_type: str) -> str:
    country_trigram = set_country_trigram(country=country)
    return f"{country_trigram}{UNIT_NAME_SEP}{agg_prod_type}"


GEN_UNITS_DATA_TYPE = Dict[str, List[GenerationUnitData]]


def get_generation_units_data(uc_run_params: UCRunParams,
                              pypsa_unit_params_per_agg_pt: Dict[str, dict], 
                              units_complem_params_per_agg_pt: Dict[str, Dict[str, str]], 
                              agg_res_cf_data: Dict[str, pd.DataFrame], 
                              agg_gen_capa_data: Dict[str, pd.DataFrame]) -> GEN_UNITS_DATA_TYPE:
    """
    Get generation units data to create them hereafter
    :param pypsa_unit_params_per_agg_pt: dict of per aggreg. prod type main Pypsa params
    :param units_complem_params_per_agg_pt: # for each aggreg. prod type, a dict. {complem. param name: source - "from_json_tb_modif"/"from_eraa_data"}
    :param agg_res_cf_data: {country: df with per aggreg. prod type RES capa factor data}
    :param agg_gen_capa_data: {country: df with per aggreg. prod type (installed) generation capa. data}
    """
    countries = list(agg_gen_capa_data)
    prod_type_col = COLUMN_NAMES.production_type
    prod_type_agg_col = f"{prod_type_col}_agg"
    value_col = COLUMN_NAMES.value
    # TODO: set as global constants/unify...
    power_capa_key = "power_capa"
    capa_factor_key = "capa_factors"

    n_spaces_msg = 2

    generation_units_data = {}
    for country in countries:
        print_out_msg(msg_level="info", msg=f"- for country {country}")
        generation_units_data[country] = []
        current_capa_data = agg_gen_capa_data[country]
        current_res_cf_data = agg_res_cf_data[country]
        # get list of assets to be treated from capa. data
        agg_prod_types = list(set(current_capa_data[prod_type_agg_col]))
        # initialize set of params for each unit by using pypsa default values
        current_assets_data = {agg_pt: pypsa_unit_params_per_agg_pt[agg_pt] for agg_pt in agg_prod_types}
        # and loop over pt to add complementary params
        for agg_pt in agg_prod_types:
            print_out_msg(msg_level="info", msg=n_spaces_msg * " " + f"* for aggreg. prod. type {agg_pt}")
            # set and add asset name
            gen_unit_name = set_gen_unit_name(country=country, agg_prod_type=agg_pt)
            current_assets_data[agg_pt]["name"] = gen_unit_name
            # and "type" (the aggreg. prod types used here, with a direct corresp. to PyPSA generators; 
            # made explicit in JSON fixed params files)
            current_assets_data[agg_pt]["type"] = agg_pt
            if agg_pt in units_complem_params_per_agg_pt and len(units_complem_params_per_agg_pt[agg_pt]) > 0:
                # add pnom attribute if needed
                if power_capa_key in units_complem_params_per_agg_pt[agg_pt]:
                    print_out_msg(msg_level="info", msg=2*n_spaces_msg * " " + f"-> add {power_capa_key}")
                    current_power_capa = \
                        get_val_of_agg_pt_in_df(df_data=current_capa_data, prod_type_agg_col=prod_type_agg_col,
                                                agg_prod_type=agg_pt, value_col="power_capacity",
                                                static_val=True)
                    current_assets_data[agg_pt][GEN_UNITS_PYPSA_PARAMS.power_capa] = int(current_power_capa)
                        
                # add pmax_pu when variable for RES/fatal units
                if capa_factor_key in units_complem_params_per_agg_pt[agg_pt]:
                    print_out_msg(msg_level="info", msg=2*n_spaces_msg * " " + f"-> add {capa_factor_key}")
                    current_assets_data[agg_pt][GEN_UNITS_PYPSA_PARAMS.capa_factors] = \
                        get_val_of_agg_pt_in_df(df_data=current_res_cf_data, prod_type_agg_col=prod_type_agg_col,
                                                agg_prod_type=agg_pt, value_col=value_col, static_val=False)
                # max hours for storage-like assets (energy capa/power capa)

                # marginal costs/efficiency, from FuelSources
            elif agg_pt == 'failure':
                current_assets_data[agg_pt]['p_nom'] = agg_gen_capa_data[country].loc[agg_gen_capa_data[country]['production_type_agg']=='failure', 'power_capacity'].iloc[0]
                current_assets_data[agg_pt]['marginal_cost'] = uc_run_params.failure_penalty
                current_assets_data[agg_pt]['committable'] = False
            current_assets_data[agg_pt]['p_nom'] = agg_gen_capa_data[country].loc[agg_gen_capa_data[country]['production_type_agg']==agg_pt, 'power_capacity'].iloc[0]
            generation_units_data[country].append(GenerationUnitData(**current_assets_data[agg_pt]))
    return generation_units_data


def overwrite_gen_units_fuel_src_params(generation_units_data: GEN_UNITS_DATA_TYPE, updated_fuel_sources_params: Dict[str, Dict[str, float]]) -> GEN_UNITS_DATA_TYPE:
    for _, units_data in generation_units_data.items():
        # loop over all units in current country
        for indiv_unit_data in units_data:
            current_prod_type = get_prod_type_from_unit_name(prod_unit_name=indiv_unit_data.name)
            if current_prod_type in updated_fuel_sources_params:
                # TODO: add CO2 emissions, and merge both case? Q2OJ: how-to properly?
                if GEN_UNITS_PYPSA_PARAMS.marginal_cost in updated_fuel_sources_params[current_prod_type]:
                    indiv_unit_data.marginal_cost = updated_fuel_sources_params[current_prod_type][GEN_UNITS_PYPSA_PARAMS.marginal_cost]

        # TODO: from units data info on fuel source extract and apply updated params values
        updated_fuel_sources_params = None


def control_min_pypsa_params_per_gen_units(generation_units_data: Dict[str, List[GenerationUnitData]],
                                           pypsa_min_unit_params_per_agg_pt: Dict[str, List[str]]):
    """
    Control that minimal PyPSA parameter infos has been provided before creating generation units
    """
    pypsa_params_errors_list = []
    # loop over countries
    for country, gen_units_data in generation_units_data.items():
        # and unit in them
        for elt_unit_data in gen_units_data:
            current_unit_type = elt_unit_data.type
            pypsa_min_unit_params_set = set(pypsa_min_unit_params_per_agg_pt[current_unit_type])
            params_with_init_val_set = set(elt_unit_data.get_non_none_attr_names())
            missing_pypsa_params = list(pypsa_min_unit_params_set - params_with_init_val_set)
            if len(missing_pypsa_params) > 0:
                current_unit_name = elt_unit_data.name
                current_msg = f"country {country}, unit name {current_unit_name} and type {current_unit_type} -> {missing_pypsa_params}"
                pypsa_params_errors_list.append(current_msg)
    if len(pypsa_params_errors_list) > 0:
        print_errors_list(error_name="on 'minimal' PyPSA gen. units parameters; missing ones for", 
                        errors_list=pypsa_params_errors_list)     
    else:
        print_out_msg(msg_level="info", msg="PyPSA NEEDED PARAMETERS FOR GENERATION UNITS CREATION HAVE BEEN LOADED!")


def get_country_bus_name(country: str) -> str:
    return country.lower()[:3]


def init_pypsa_network(df_demand_first_country: pd.DataFrame):
    print("Initialize PyPSA network")
    network = pypsa.Network(snapshots=df_demand_first_country.index)
    return network


def add_gps_coordinates(network, countries_gps_coords: Dict[str, Tuple[float, float]]):
    print("Add GPS coordinates") 
    for country, gps_coords in countries_gps_coords.items():
        country_bus_name = get_country_bus_name(country=country)
        network.add("Bus", name=f"{country_bus_name}", x=gps_coords[0], y=gps_coords[1])
    return network


def add_energy_carrier(network, fuel_sources: Dict[str, FuelSources]):
    print("Add energy carriers")
    for carrier in list(fuel_sources.keys()):
        network.add("Carrier", name=carrier, co2_emissions=fuel_sources[carrier].co2_emissions/1000)
    return network


STORAGE_LIKE_UNITS = ["batteries"]


def add_generators(network, generators_data: Dict[str, List[GenerationUnitData]]):
    print("Add generators - associated to their respective buses")
    for country, gen_units_data in generators_data.items():
        country_bus_name = get_country_bus_name(country=country)
        for gen_unit_data in gen_units_data:
            pypsa_gen_unit_dict = gen_unit_data.__dict__
            if gen_unit_data.type in STORAGE_LIKE_UNITS:
                network.add("StorageUnit", bus=f"{country_bus_name}", **pypsa_gen_unit_dict)
            else:
                network.add("Generator", bus=f"{country_bus_name}", **pypsa_gen_unit_dict)
    print("Considered generators", network.generators)
    return network


def add_loads(network, demand: Dict[str, pd.DataFrame]):
    print("Add loads - associated to their respective buses")
    for country in demand:
        country_bus_name = get_country_bus_name(country=country)
        load_data = {"name": f"{country_bus_name}-load", "bus": f"{country_bus_name}",
                     "carrier": "AC", "p_set": demand[country]["value"].values}
        network.add("Load", **load_data)
    return network


from itertools import product


def get_current_interco_capa(interco_capas: Dict[Tuple[str, str], float], country_origin: str, 
                             country_dest: str) -> (Optional[float], Optional[bool]):
    link_tuple = (country_origin, country_dest)
    reverse_link_tuple = (country_dest, country_origin)
    if link_tuple in interco_capas:
        current_interco_capa = interco_capas[link_tuple]
        is_sym_interco = reverse_link_tuple not in interco_capas
    elif reverse_link_tuple in interco_capas:
        current_interco_capa = interco_capas[reverse_link_tuple]
        is_sym_interco = True
    else:
        current_interco_capa = None
        is_sym_interco = None
    return current_interco_capa, is_sym_interco


def add_interco_links(network, countries: List[str], interco_capas: Dict[Tuple[str, str], float]):
    print(f"Add interco. links - between the selected countries: {countries}")
    links = []
    symmetric_links = []
    links_wo_capa_msg = []
    for country_origin, country_dest in product(countries, countries):
        link_tuple = (country_origin, country_dest)
        # do not add link for (country, country); neither for symmetric links already treated 
        # (as bidirectional setting p_min_pu=-1)
        if not country_origin == country_dest and link_tuple not in symmetric_links:
            # TODO: fix AC/DC.... all AC here in names but not true (cf. CS students data)
            current_interco_capa, is_sym_interco = \
                get_current_interco_capa(interco_capas=interco_capas, country_origin=country_origin,
                                         country_dest=country_dest)
            if current_interco_capa is None:
                # if symmetrical interco order lexicographically to fit with input data format
                if is_sym_interco is True:
                    link_wo_capa = lexico_compar_str(string1=country_origin,
                                                     string2=country_dest, return_tuple=True)
                else:
                    link_wo_capa = link_tuple
                link_wo_capa_msg = f"({link_wo_capa[0]}, {link_wo_capa[1]})"
                if link_wo_capa_msg not in links_wo_capa_msg:
                    links_wo_capa_msg.append(f"({link_wo_capa[0]}, {link_wo_capa[1]})")
            else:
                country_origin_bus_name = get_country_bus_name(country=country_origin)
                country_dest_bus_name = get_country_bus_name(country=country_dest)
                if is_sym_interco is True:
                    p_min_pu, p_max_pu = -1, 1
                    symmetric_links.append(link_tuple)
                else:
                    p_min_pu, p_max_pu = 0, 1
                links.append({"name": f"{country_origin_bus_name}-{country_dest_bus_name}_ac", 
                            "bus0": f"{country_origin_bus_name}", "bus1": f"{country_dest_bus_name}", 
                            "p_nom": current_interco_capa, "p_min_pu": p_min_pu, "p_max_pu" : p_max_pu}
                            )
    if len(links_wo_capa_msg) > 0:
        print_errors_list(error_name="-> interco. links without capacity data", 
                          errors_list=links_wo_capa_msg)
    
    # add to PyPSA network
    for link in links:
        if link['p_nom'] > 0:
            network.add("Link", **link)

    return network


def set_period_start_file(year: int, period_start: datetime) -> str:
    return datetime(year=year, month=period_start.month, day=period_start.day).strftime("%Y-%m-%d")


def save_lp_model(network, year: int, n_countries: int, period_start: datetime):
    print("Save lp model")
    import pypsa.optimization as opt
    from long_term_uc.common.long_term_uc_io import OUTPUT_DATA_FOLDER

    m = opt.create_model(network)
    # to avoid suppressing previous runs results
    run_id = np.random.randint(99)
    period_start_file = set_period_start_file(year=year, period_start=period_start)
    file_suffix = f"{n_countries}-countries_{period_start_file}_{run_id}"
    m.to_file(Path(f'{OUTPUT_DATA_FOLDER}/model_{file_suffix}.lp'))


def get_stationary_batt_opt_dec(network, countries: List[str]):
    stationary_batt_opt_dec = {}
    # for all but storages
    # network.generators_t.p
    # for storages
    # network.storage_units_t.p_dispatch
    # network.generators.loc["fra_coal"] -> info given asset
    # network.generators_t.p_set
    for generator in network.generators:
        if generator.carrier == "flexibility":
            bus_name = generator.bus
            current_country = [country for country in countries if country.startswith(bus_name)][0]
            stationary_batt_opt_dec[current_country] = generator.p_nom_opt


def plot_uc_run_figs(network, countries: List[str]):
    import matplotlib.pyplot as plt
    print("Plot generation and prices figures")

    # p_nom_opt is the optimized capacity (that can be also a variable in PyPSA...
    # but here not optimized -> values in input data plotted)
    for country in countries:
        country_bus_name = get_country_bus_name(country=country)
        network.generators.p_nom_opt.drop(f"Failure_{country_bus_name}").div(1e3).plot.bar(ylabel="GW", figsize=(8, 3))
    # [Coding trick] Matplotlib can directly adapt size of figure to fit with values plotted
    plt.tight_layout()

    # And "stack" of optimized production profiles
    network.generators_t.p.div(1e3).plot.area(subplots=False, ylabel="GW")
    from long_term_uc.common.long_term_uc_io import get_prod_figure, get_price_figure
    plt.savefig(get_prod_figure(country=country, year=year, start_horizon=uc_run_params.uc_period_start))
    plt.tight_layout()

    # Finally, "marginal prices" -> meaning? How can you interpret the very constant value plotted?
    network.buses_t.marginal_price.mean(1).plot.area(figsize=(8, 3), ylabel="Euro per MWh")
    plt.savefig(get_price_figure(country=country, year=year, start_horizon=uc_run_params.uc_period_start))
    plt.tight_layout()
