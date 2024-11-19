from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, Optional, Literal

from long_term_uc.common.error_msgs import print_errors_list
from long_term_uc.utils.basic_utils import is_str_bool
from long_term_uc.utils.eraa_utils import set_interco_to_tuples
from long_term_uc.utils.type_checker import apply_data_type_check


INTERCO_STR_SEP = "2"
USAGE_PARAMS_SHORT_NAMES = {
    "allow_adding_interco_capas": "adding_interco_capas",
    "allow_overwriting_eraa_interco_capa_vals": "overwriting_eraa_interco_capa_vals",
    "allow_manually_adding_demand": "manually_adding_demand",
    "allow_manually_adding_generators": "manually_adding_generators",
    "apply_cf_techno_breakthrough": "apply_cf_techno_breakthrough",
    "res_cf_stress_test_folder": "res_cf_stress_test_folder",
    "res_cf_stress_test_cy": "res_cf_stress_test_cy", 
    "mode": "mode",
    "team": "team"
}


type Mode = Literal['solo', 'europe']


def apply_params_type_check(param_obj_dict: dict, types_for_check: Dict[str, str], param_name: str):
    check_errors = []
    for attr_tb_checked, type_for_check in types_for_check.items():
        check_result = apply_data_type_check(data_type=type_for_check, data_val=param_obj_dict[attr_tb_checked])
        if check_result is False:
            check_errors.append(attr_tb_checked)
    if len(check_errors) > 0:
        print_errors_list(error_name=f"{param_name} JSON data with erroneous types", 
                            errors_list=check_errors)


# raw types (just after reading) of the following attributes 
# -> for "direct" check to stop asap if erroneous values
# TODO: define complex types in a dataclass (centralized)
RAW_TYPES_FOR_CHECK = {"eraa_dataset_descr": 
                       {"aggreg_prod_types_def": "two_level_dict_str_str_list-of-str",
                        "agg_prod_types_with_cf_data": "list_of_str",
                        "available_climatic_years": "list_of_int",
                        "available_countries": "list_of_str",
                        "available_aggreg_prod_types": "two_level_dict_str_str_list-of-str",
                        "available_intercos": "list_of_str",
                        "available_target_years": "list_of_int",
                        "eraa_edition": "str",
                        "gps_coordinates": "dict_str_list_of_float",
                        "per_agg_prod_type_color": "dict_str_str",
                        "per_zone_color": "dict_str_str",
                        "pypsa_unit_params_per_agg_pt": "dict_str_dict",
                        "units_complem_params_per_agg_pt": "two_level_dict_str_str_str"
                        },
                        "pypsa_static_params":
                        {
                            "min_unit_params_per_agg_pt": "dict_str_list_of_str"
                        }
}


@dataclass
class UsageParameters:
    adding_interco_capas: bool = False
    overwriting_eraa_interco_capa_vals: bool = False 
    manually_adding_demand: bool = False
    manually_adding_generators: bool = False
    mode: Mode = "solo"
    team: Optional[str] = None
    # parameters for climate-based "sensitivity" tests
    apply_cf_techno_breakthrough: bool = False
    res_cf_stress_test_folder: str = None
    res_cf_stress_test_cy: int = None

    def check_types(self):
        """
        Check coherence of types
        """
        # TODO: code it


# TODO: "failure" as global constant
FAILURE_ASSET = "failure"
        

@dataclass
class ERAADatasetDescr:
    # {datatype: {aggreg. prod. type: list of ERAA prod types}}
    aggreg_prod_types_def: Dict[str, Dict[str, List[str]]]
    agg_prod_types_with_cf_data: List[str]  # list of aggreg. prod types with CF (to be read)
    available_climatic_years: List[int]
    available_countries: List[str]
    available_aggreg_prod_types: Union[Dict[str, Dict[str, List[str]]], Dict[str, Dict[int, List[str]]]]
    available_intercos: Union[List[str], List[Tuple[str, str]]]
    available_target_years: List[int]  # N.B. "target year" is a "year" in ERAA terminology
    eraa_edition: str
    # per (meta-)country GPS coordinates - only for network plot
    gps_coordinates: Union[Dict[str, List[float]], Dict[str, Tuple[float, float]]]
    per_zone_color: Dict[str, str]
    per_agg_prod_type_color: Dict[str, str]
    pypsa_unit_params_per_agg_pt: Dict[str, dict]  # dict of per aggreg. prod type main Pypsa params
    # for each aggreg. prod type, a dict. {complem. param name: source - "from_json_tb_modif"/"from_eraa_data"}
    units_complem_params_per_agg_pt: Dict[str, Dict[str, str]]

    def check_types(self):
        """
        Check coherence of types
        """
        apply_params_type_check(param_obj_dict=self.__dict__, 
                                types_for_check=RAW_TYPES_FOR_CHECK["eraa_dataset_descr"], 
                                param_name="ERAA description data - fixed ones -")

    # TODO: get auto_add_failure_pu from global usage params
    def process(self, auto_add_failure_pu: bool = True):
        # convert str bool to boolean
        for agg_pt, pypsa_params in self.pypsa_unit_params_per_agg_pt.items():
            for param_name, param_val in pypsa_params.items():
                if is_str_bool(bool_str=param_val) is True:
                    self.pypsa_unit_params_per_agg_pt[agg_pt][param_name] = bool(param_val)
        for country in self.gps_coordinates:
            self.gps_coordinates[country] = tuple(self.gps_coordinates[country])
        # from "{zone_origin}{INTERCO_STR_SEP}{zone_dest}" format of interco names to tuples (zone_origin, zone_dest)
        self.available_intercos = set_interco_to_tuples(interco_names=self.available_intercos)
        # convert str year values to int
        new_avail_aggreg_pt_dict = {}
        for country, all_years_dict in self.available_aggreg_prod_types.items():
            new_avail_aggreg_pt_dict[country] = {int(elt_year): all_years_dict[elt_year] for elt_year in all_years_dict}
            # and add failure - fictive - asset
            if auto_add_failure_pu is True:
                for elt_year in new_avail_aggreg_pt_dict[country]:
                    if FAILURE_ASSET not in new_avail_aggreg_pt_dict[country][elt_year]:
                        new_avail_aggreg_pt_dict[country][elt_year].append(FAILURE_ASSET)
             
        self.available_aggreg_prod_types = new_avail_aggreg_pt_dict

ALL_UNITS_KEY = "all_units"


@dataclass
class PypsaStaticParams:
    # per aggreg. prod. unit list of minimal parameters for PyPSA generators to be built
    min_unit_params_per_agg_pt: Dict[str, List[str]]

    def check_types(self):
        """
        Check coherence of types
        """
        apply_params_type_check(param_obj_dict=self.__dict__, 
                                types_for_check=RAW_TYPES_FOR_CHECK["pypsa_static_params"], 
                                param_name="PyPSA static params - to set objects main infos")

    def process(self):
        # add common static params to all agg. prod type
        if ALL_UNITS_KEY in self.min_unit_params_per_agg_pt:
            common_min_params = self.min_unit_params_per_agg_pt[ALL_UNITS_KEY]
            self.min_unit_params_per_agg_pt.pop(ALL_UNITS_KEY)
            for agg_pt in self.min_unit_params_per_agg_pt:
                self.min_unit_params_per_agg_pt[agg_pt].extend(common_min_params)
                