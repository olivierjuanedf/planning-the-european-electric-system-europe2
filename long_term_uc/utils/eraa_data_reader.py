import os
from typing import Dict, List, Tuple
import pandas as pd
from datetime import datetime

from long_term_uc.common.constants_datatypes import DATATYPE_NAMES
from long_term_uc.common.error_msgs import print_out_msg
from long_term_uc.common.long_term_uc_io import INPUT_ERAA_FOLDER, DT_SUBFOLDERS, DT_FILE_PREFIX, COLUMN_NAMES, \
    FILES_FORMAT, DATE_FORMAT, GEN_CAPA_SUBDT_COLS
from long_term_uc.common.uc_run_params import UCRunParams
from long_term_uc.utils.basic_utils import str_sanitizer
from long_term_uc.utils.df_utils import cast_df_col_as_date, concatenate_dfs, selec_in_df_based_on_list, \
    set_aggreg_col_based_on_corresp, get_subdf_from_date_range, create_dict_from_cols_in_df



def filter_input_data(df: pd.DataFrame, date_col: str, climatic_year_col: str, period_start: datetime, 
                      period_end: datetime, climatic_year: int) -> pd.DataFrame:
    # ERAA date format not automatically cast by pd
    df = cast_df_col_as_date(df=df, date_col=date_col, date_format=DATE_FORMAT)
    # keep only wanted date range
    df_filtered = get_subdf_from_date_range(df=df, date_col=date_col, date_min=period_start, date_max=period_end)
    # then selected climatic year
    df_filtered = selec_in_df_based_on_list(df=df_filtered, selec_col=climatic_year_col, 
                                            selec_vals=[climatic_year])
    return df_filtered


def set_aggreg_cf_prod_types_data(df_cf_list: List[pd.DataFrame], pt_agg_col: str, date_col: str, val_col: str) -> pd.DataFrame:
    # concatenate, aggreg. over prod type of same aggreg. type and avg
    df_cf_agg = concatenate_dfs(dfs=df_cf_list)
    df_cf_agg = df_cf_agg.groupby([pt_agg_col, date_col]).agg({val_col: "mean"}).reset_index()
    return df_cf_agg


def gen_capa_pt_str_sanitizer(gen_capa_prod_type: str) -> str:
    # very ad-hoc operation
    sanitized_gen_capa_pt = gen_capa_prod_type.replace(" - ", " ")
    sanitized_gen_capa_pt = str_sanitizer(raw_str=sanitized_gen_capa_pt, 
                                          ad_hoc_replacements={"gas_": "gas", "(": "", ")": ""})
    return sanitized_gen_capa_pt


def select_interco_capas(df_intercos_capa: pd.DataFrame, countries: List[str]) -> pd.DataFrame:
    selection_col = "selected"
    # add selection column
    origin_col = COLUMN_NAMES.zone_origin
    destination_col = COLUMN_NAMES.zone_destination
    df_intercos_capa[selection_col] = \
        df_intercos_capa.apply(lambda col: 1 if (col[origin_col] in countries 
                                                 and col[destination_col] in countries) else 0, axis=1)
    # keep only lines with both origin and destination zones in the list of available countries
    df_intercos_capa = df_intercos_capa[df_intercos_capa[selection_col] == 1]
    # remove selection column
    all_cols = list(df_intercos_capa.columns)
    all_cols.remove(selection_col)
    df_intercos_capa = df_intercos_capa[all_cols]
    return df_intercos_capa


def get_countries_data(uc_run_params: UCRunParams, agg_prod_types_with_cf_data: List[str],
                       aggreg_prod_types_def: Dict[str, List[str]]) \
                        -> (Dict[str, pd.DataFrame], Dict[str, pd.DataFrame], 
                            Dict[str, pd.DataFrame], Dict[Tuple[str, str], float]):
    """
    Get ERAA data necessary for the selected countries
    :param uc_run_params: UC run parameters, from which main reading infos will be obtained
    :param agg_prod_types_with_cf_data: aggreg. production types for which CF data must be read
    :param aggreg_prod_types_def: per-datatype definition of aggreg. to indiv. production types
    :returns: {country: df with demand of this country}, {country: df with - per aggreg. prod type CF}, 
    {country: df with installed generation capas}, df with all interconnection capas (for considered 
    countries and year)
    """
    # set shorter names for simplicity
    countries = uc_run_params.selected_countries
    year = uc_run_params.selected_target_year
    climatic_year = uc_run_params.selected_climatic_year
    selec_agg_prod_types = uc_run_params.selected_prod_types
    power_capacities = uc_run_params.updated_capacities_prod_types
    period_start = uc_run_params.uc_period_start
    period_end = uc_run_params.uc_period_end
    # get - per datatype - folder names
    demand_folder = os.path.join(INPUT_ERAA_FOLDER, DT_SUBFOLDERS.demand)
    res_cf_folder = os.path.join(INPUT_ERAA_FOLDER, DT_SUBFOLDERS.res_capa_factors)
    gen_capas_folder = os.path.join(INPUT_ERAA_FOLDER, DT_SUBFOLDERS.generation_capas)
    interco_capas_folder = os.path.join(INPUT_ERAA_FOLDER, DT_SUBFOLDERS.interco_capas)
    # file prefix
    demand_prefix = DT_FILE_PREFIX.demand
    res_cf_prefix = DT_FILE_PREFIX.res_capa_factors
    gen_capas_prefix = DT_FILE_PREFIX.generation_capas
    interco_capas_prefix = DT_FILE_PREFIX.interco_capas
    # column names
    date_col = COLUMN_NAMES.date
    climatic_year_col = COLUMN_NAMES.climatic_year
    prod_type_col = COLUMN_NAMES.production_type
    prod_type_agg_col = f"{prod_type_col}_agg"
    value_col = COLUMN_NAMES.value
    # separators for csv reader
    column_sep = FILES_FORMAT.column_sep
    decimal_sep = FILES_FORMAT.decimal_sep

    demand = {}
    agg_cf_data = {}
    agg_gen_capa_data = {}

    n_spaces_msg = 2

    aggreg_pt_cf_def = aggreg_prod_types_def[DATATYPE_NAMES.capa_factor]
    aggreg_pt_gen_capa_def = aggreg_prod_types_def[DATATYPE_NAMES.installed_capa]

    for country in countries:
        print(f"For country: {country}")
        # read csv files
        # [Coding trick] f"{year}_{country}" directly fullfill string with value of year 
        # and country variables (f-string completion)
        current_suffix = f"{year}_{country}"  # common suffix to all ERAA data files
        # get demand
        print("Get demand")
        current_df_demand = pd.read_csv(f"{demand_folder}/{demand_prefix}_{current_suffix}.csv",
                                        sep=column_sep, decimal=decimal_sep)
        # then keep only selected period date range and climatic year
        demand[country] = filter_input_data(df=current_df_demand, date_col=date_col, 
                                            climatic_year_col=climatic_year_col, period_start=period_start,
                                            period_end=period_end, climatic_year=climatic_year)

        # get RES capacity factor data
        print("Get RES capacity factors")
        agg_cf_data[country] = {}
        df_res_cf_list = []
        for agg_prod_type in selec_agg_prod_types[country]:
            # if prod type with CF data
            if agg_prod_type in agg_prod_types_with_cf_data:
                print(n_spaces_msg * " " + f"- For aggreg. prod. type: {agg_prod_type}")
                current_agg_pt_df_res_cf_list = []
                for prod_type in aggreg_pt_cf_def[agg_prod_type]:
                    cf_data_file = f"{res_cf_folder}/{res_cf_prefix}_{prod_type}_{current_suffix}.csv"
                    if os.path.exists(cf_data_file) is False:
                        print(2*n_spaces_msg * " " + f"[WARNING] RES capa. factor data file does not exist: {prod_type} not accounted for here")
                    else:
                        print(2*n_spaces_msg * " " + f"* Prod. type: {prod_type}")
                        current_df_res_cf = pd.read_csv(cf_data_file, sep=column_sep, decimal=decimal_sep) 
                        current_df_res_cf = \
                            filter_input_data(df=current_df_res_cf, date_col=date_col,
                                              climatic_year_col=climatic_year_col, 
                                              period_start=period_start, period_end=period_end, 
                                              climatic_year=climatic_year)
                        if len(current_df_res_cf) == 0:
                            print(2*n_spaces_msg * " " + f"[WARNING] No RES capa. factor data for prod. type {prod_type} and climatic year {climatic_year}")
                        else:
                            # add column with production type (for later aggreg.)
                            current_df_res_cf[prod_type_agg_col] = agg_prod_type
                            current_agg_pt_df_res_cf_list.append(current_df_res_cf)
                if len(current_agg_pt_df_res_cf_list) == 0:
                    print(n_spaces_msg * " " + f"[WARNING] No data available for aggregate RES prod. type {agg_prod_type} -> not accounted for in UC model here")
                else:
                    df_res_cf_list.extend(current_agg_pt_df_res_cf_list)

        # concatenate, aggreg. over prod type of same aggreg. type and avg
        if len(df_res_cf_list) == 0:
            print(n_spaces_msg * " " + f"[WARNING] No RES data available for country {country} -> not accounted for in UC model here")
        else:
            agg_cf_data[country] = \
                set_aggreg_cf_prod_types_data(df_cf_list=df_res_cf_list, pt_agg_col=prod_type_agg_col, date_col=date_col,
                                              val_col=value_col)
        
        # get installed generation capacity data
        print("Get installed generation capacities (unique file per country and year, with all prod. types in it)")
        gen_capa_data_file = f"{gen_capas_folder}/{gen_capas_prefix}_{current_suffix}.csv"
        if os.path.exists(gen_capa_data_file) is False:
            print_out_msg(msg_level="warning", msg=f"Generation capas data file does not exist: {country} not accounted for here")
        else:
            current_df_gen_capa = pd.read_csv(gen_capa_data_file, sep=column_sep, decimal=decimal_sep)
            # Keep sanitize prod. types col values
            current_df_gen_capa[prod_type_col] = current_df_gen_capa[prod_type_col].apply(gen_capa_pt_str_sanitizer)
            # Keep only selected aggreg. prod. types
            current_df_gen_capa = \
                set_aggreg_col_based_on_corresp(df=current_df_gen_capa, col_name=prod_type_col,
                                                created_agg_col_name=prod_type_agg_col, val_cols=GEN_CAPA_SUBDT_COLS, 
                                                agg_corresp=aggreg_pt_gen_capa_def, common_aggreg_ope="sum")
            current_df_gen_capa = \
                selec_in_df_based_on_list(df=current_df_gen_capa, selec_col=prod_type_agg_col,
                                          selec_vals=selec_agg_prod_types[country])
            if country in power_capacities:
                for k, v in power_capacities[country].items():
                    current_df_gen_capa.loc[current_df_gen_capa['production_type_agg']==k, 'power_capacity'] = v
            
            if 'failure' in selec_agg_prod_types[country]:
                failure_df = pd.DataFrame.from_dict({
                    'production_type_agg': ['failure'],
                    'power_capacity': [uc_run_params.failure_power_capa],
                    'power_capacity_turbine': [0.0],
                    'power_capacity_pumping': [0.0],
                    'power_capacity_injection': [0.0],
                    'power_capacity_offtake': [0.0]
                })
                current_df_gen_capa = pd.concat([current_df_gen_capa, failure_df], ignore_index=True)
            
            if country in power_capacities:
                for k, v in power_capacities[country].items():
                    current_df_gen_capa.loc[current_df_gen_capa['production_type_agg']==k, 'power_capacity'] = v
            agg_gen_capa_data[country] = current_df_gen_capa
            print('#'*100)
            print(current_df_gen_capa)
            print('#'*100)

    # read interconnection capas file
    print("Get interconnection capacities, with unique file for all nodes (zones=countries) and year")
    interco_capas_data_file = f"{interco_capas_folder}/{interco_capas_prefix}_{year}.csv"
    if os.path.exists(interco_capas_data_file) is False:
        print_out_msg(msg_level="warning", msg=f"Generation capas data file does not exist: {country} not accounted for here")
    else:
        df_interco_capas = pd.read_csv(interco_capas_data_file, sep=column_sep, decimal=decimal_sep)
    # and select information needed for selected countries
    df_interco_capas = select_interco_capas(df_intercos_capa=df_interco_capas, countries=countries)
    # set as dictionary
    origin_col = COLUMN_NAMES.zone_origin
    destination_col = COLUMN_NAMES.zone_destination
    tuple_key_col = "tuple_key"
    df_interco_capas[tuple_key_col] = \
        df_interco_capas.apply(lambda col: (col[origin_col], col[destination_col]),
                               axis=1)
    interco_capas = create_dict_from_cols_in_df(df=df_interco_capas, key_col=tuple_key_col, val_col=value_col)
    # add interco capas values set by user
    interco_capas |= uc_run_params.interco_capas_updated_values

    return demand, agg_cf_data, agg_gen_capa_data, interco_capas
    