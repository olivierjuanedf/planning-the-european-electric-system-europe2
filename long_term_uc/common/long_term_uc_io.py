import os
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DtSubfolders:
    demand: str = "demand"
    res_capa_factors: str = "res_capa-factors"
    generation_capas: str = "generation_capas"
    interco_capas: str = "interco_capas"


@dataclass
class DtFilePrefix:
    demand: str = "demand"
    res_capa_factors: str = "capa_factor"
    generation_capas: str = "generation-capa"
    interco_capas: str = "interco-capas"


@dataclass
class ColumnNames:
    date: str = "date"
    target_year: str = "year"
    climatic_year: str = "climatic_year"
    production_type: str = "production_type"
    value: str = "value"
    zone_origin: str = "zone_origin"
    zone_destination: str = "zone_destination"


@dataclass
class FilesFormat:
    column_sep: str = ";"
    decimal_sep: str = "."


@dataclass
class ComplemDataSources:
    from_json_tb_modif: str = "from_json_tb_modif"
    from_eraa_data: str = "from_eraa_data"


LT_UC_COMMON_FOLDER = "long_term_uc/common"
COLUMN_NAMES = ColumnNames()
COMPLEM_DATA_SOURCES = ComplemDataSources()
DATE_FORMAT_FILE = "%Y-%m-%d"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_PRINT = "%Y/%m/%d"
DT_FILE_PREFIX = DtFilePrefix()
DT_SUBFOLDERS = DtSubfolders()
FILES_FORMAT = FilesFormat()
GEN_CAPA_SUBDT_COLS = ["power_capacity", "power_capacity_turbine", "power_capacity_pumping", 
                       "power_capacity_injection", "power_capacity_offtake"]
INPUT_ERAA_FOLDER = "data/ERAA_2023-2"
INPUT_FOLDER = "input"
INPUT_LT_UC_SUBFOLDER = f"{INPUT_FOLDER}/long_term_uc"
INPUT_LT_UC_COUNTRY_SUBFOLDER = f"{INPUT_LT_UC_SUBFOLDER}/countries"
INPUT_FUNC_PARAMS_SUBFOLDER = f"{INPUT_FOLDER}/functional_params"
INTERCO_STR_SEP = "2"
# first date in ERAA data (fictive 364 days calendar)
MIN_DATE_IN_DATA = datetime(year=1900, month=1, day=1)
# first date NOT in ERAA data (fictive 364 days calendar)
MAX_DATE_IN_DATA = datetime(year=1901, month=1, day=1)
OUTPUT_DATA_FOLDER = "output/long_term_uc/data"
OUTPUT_FIG_FOLDER = "output/long_term_uc/figures"


def get_json_usage_params_file() -> str:
    return os.path.join(INPUT_FUNC_PARAMS_SUBFOLDER, "usage_params.json")


def get_json_fixed_params_file() -> str:
    return os.path.join(INPUT_LT_UC_SUBFOLDER, "elec-europe_params_fixed.json")


def get_json_eraa_avail_values_file() -> str:
    return os.path.join(INPUT_LT_UC_SUBFOLDER, "elec-europe_eraa-available-values.json")


def get_json_params_tb_modif_file() -> str:
    return os.path.join(INPUT_LT_UC_SUBFOLDER, "elec-europe_params_to-be-modif.json")


def get_json_fuel_sources_tb_modif_file() -> str:
    return os.path.join(INPUT_LT_UC_SUBFOLDER, "fuel_sources_to-be_modif.json")


def get_json_params_modif_country_files() -> List[str]:
    return map(
        lambda x: os.path.join(INPUT_LT_UC_COUNTRY_SUBFOLDER, x),
        filter(lambda x: x.endswith('.json'),
               os.listdir(INPUT_LT_UC_COUNTRY_SUBFOLDER)))


def get_json_pypsa_static_params_file() -> str:
    return os.path.join(INPUT_LT_UC_SUBFOLDER, "pypsa_static_params.json") 


def get_network_figure() -> str:
    return f"{OUTPUT_FIG_FOLDER}/network.png"


def get_output_file_suffix(country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return f"{country}_{year}_cy{climatic_year}_{start_horizon.strftime(DATE_FORMAT_FILE)}"


def get_output_file_named(name: str, extension:str, output_dir:str, country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    file_suffix = get_output_file_suffix(country=country, year=year, climatic_year=climatic_year,
                                         start_horizon=start_horizon)
    return f"{output_dir}/{name}_{file_suffix}.{extension}"

def get_figure_file_named(name: str, country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return get_output_file_named(name, 'png', OUTPUT_FIG_FOLDER, country, year, climatic_year, start_horizon)

def get_prod_figure(country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return get_figure_file_named('prod', country, year, climatic_year, start_horizon)

def get_price_figure(country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return get_figure_file_named('prices', country, year, climatic_year, start_horizon)

def get_csv_file_named(name:str, country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return get_output_file_named(name, 'csv', OUTPUT_DATA_FOLDER, country, year, climatic_year, start_horizon)

def get_opt_power_file(country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return get_csv_file_named('opt_power', country, year, climatic_year, start_horizon)

def get_marginal_prices_file(country: str, year: int, climatic_year: int, start_horizon: datetime) -> str:
    return get_csv_file_named('marginal_prices', country, year, climatic_year, start_horizon)
