from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union

from long_term_uc.common.constants_extract_eraa_data import ERAADatasetDescr
from long_term_uc.common.error_msgs import print_errors_list, print_out_msg
from long_term_uc.common.long_term_uc_io import MIN_DATE_IN_DATA, MAX_DATE_IN_DATA
from long_term_uc.utils.basic_utils import get_period_str, are_lists_eq
from long_term_uc.utils.eraa_utils import set_interco_to_tuples


DATE_FORMAT = "%Y/%m/%d"
N_DAYS_UC_DEFAULT = 9


def uncoherent_param_stop(param_errors: List[str]):
    print_errors_list(error_name="in JSON params to be modif. file", errors_list=param_errors)


def check_unique_int_value(param_name: str, param_value) -> Optional[str]:
    if not isinstance(param_value, int):
        f"Unique {param_name} to be provided; must be an int"
    else:
        return None
    

@dataclass
class UCRunParams:
    selected_climatic_year: int
    selected_countries: List[str]
    selected_target_year: int
    selected_prod_types: Dict[str, Optional[List[str]]]
    uc_period_start: Union[str, datetime]
    uc_period_end: Union[str, datetime] = None
    failure_power_capa: float = None
    failure_penalty: float = None
    interco_capas_updated_values: Union[Dict[str, float], Dict[Tuple[str, str], float]] = field(default_factory=dict)
    updated_capacities_prod_types: Dict[str, Optional[Dict[str, float]]] = field(default_factory=dict)
    updated_fuel_sources_params: Dict[str, Dict[str, Optional[float]]] = None

    def __repr__(self):
        repr_str = "UC long-term model run with params:"
        n_countries = len(self.selected_countries)
        repr_str += f"\n- {n_countries} country(ies): {self.selected_countries}"
        period_str = get_period_str(period_start=self.uc_period_start, period_end=self.uc_period_end)
        repr_str += f"\n- year: {self.selected_target_year}, on period {period_str}"
        repr_str += f"\n- climatic year: {self.selected_climatic_year}"
        return repr_str

    def process(self, available_countries: List[str]):
        print('*'*30)
        print(self.updated_capacities_prod_types)
        print('*'*30)
        # if dates in str format, cast them as datetime
        # - setting end of period to default value if not provided
        if isinstance(self.uc_period_start, str):
            self.uc_period_start = datetime.strptime(self.uc_period_start, DATE_FORMAT)
        if self.uc_period_end is None:
            self.uc_period_end = min(MAX_DATE_IN_DATA, self.uc_period_start + timedelta(days=N_DAYS_UC_DEFAULT))
            print(f"End of period set to default value: {self.uc_period_end:%Y/%m/%d} (period of {N_DAYS_UC_DEFAULT} days; with bound on 1900, Dec. 31th)")
        elif isinstance(self.uc_period_end, str):
            self.uc_period_end = datetime.strptime(self.uc_period_end, DATE_FORMAT)
        # replace None and missing countries in dict of aggreg. prod. types
        for country in available_countries:
            if country not in self.selected_prod_types \
                or self.selected_prod_types[country] is None:
                self.selected_prod_types[country] = []
        # empty dict if interco. added values is empty
        if self.interco_capas_updated_values is None:
            self.interco_capas_updated_values = {}
        else:  # set interco. from {zone_origin}2{zone_destination} names to tuples
            interco_tuples = set_interco_to_tuples(interco_names=self.interco_capas_updated_values,
                                                   return_corresp=True)
            self.interco_capas_updated_values = {interco_tuples[key]: val
                                               for key, val in self.interco_capas_updated_values.items()}
        print('*'*30)
        print(self.selected_prod_types)
        print('*'*30)
        # keep only updated source params values that are non None
        new_updated_fuel_source_params = {}
        for source, params in self.updated_fuel_sources_params.items():
            new_params = {name: val for name, val in params.items() if val is not None}
            if len(new_params) > 0:
                new_updated_fuel_source_params[source] = new_params
        self.updated_fuel_sources_params = new_updated_fuel_source_params

    def coherence_check(self, eraa_data_descr: ERAADatasetDescr, year: int):
        errors_list = []
        # check that there is no repetition of countries
        countries_set = set(self.selected_countries)
        if len(countries_set) < len(self.selected_countries):
            errors_list.append("Repetition in selected countries") 

        # check coherence of values with fixed params
        # for selected countries
        unknown_countries = list(countries_set - set(eraa_data_descr.available_countries))
        if len(unknown_countries) > 0:
            errors_list.append(f"Unknown selected country(ies): {unknown_countries}")

        # for selected target and climatic years
        # check that unique value provided
        target_yr_msg = check_unique_int_value(param_name="target year", param_value=self.selected_target_year)
        if target_yr_msg is not None:
            errors_list.append(target_yr_msg)
        climatic_yr_msg = check_unique_int_value(param_name="climatic year", param_value=self.selected_climatic_year)
        if climatic_yr_msg is not None:
            errors_list.append(climatic_yr_msg)
        if isinstance(self.selected_target_year, int) \
            and self.selected_target_year not in eraa_data_descr.available_target_years:
            errors_list.append(f"Unknown target year {self.selected_target_year}")
        if isinstance(self.selected_climatic_year, int) \
            and self.selected_climatic_year not in eraa_data_descr.available_climatic_years:
            errors_list.append(f"Unknown climatic year {self.selected_climatic_year}")

        for elt_country, current_agg_pt in self.selected_prod_types.items():
            if current_agg_pt == ['all']:
                self.selected_prod_types[elt_country] = eraa_data_descr.available_aggreg_prod_types[elt_country][year]
        
        # check that countries in aggreg. prod. types are not repeated, and known
        agg_pt_countries = list(self.selected_prod_types)
        agg_pt_countries_set = set(agg_pt_countries)
        msg_suffix = "in keys of dict. of aggreg. prod. types selection"
        if len(agg_pt_countries_set) < len(agg_pt_countries):
            errors_list.append(f"Repetition of countries {msg_suffix}")
        unknown_agg_pt_countries = list(agg_pt_countries_set - set(eraa_data_descr.available_countries))
        if len(unknown_agg_pt_countries) > 0:
            errors_list.append(f"Unknown countrie(s) {msg_suffix}: {unknown_agg_pt_countries}")
 
         # check coherence of prod types in all different params
        agg_pt_countries_with_val = [elt_country for elt_country in agg_pt_countries 
                                     if len(self.selected_prod_types[elt_country]) > 0]
        countries_lists = [self.selected_countries, agg_pt_countries_with_val]
        if are_lists_eq(list_of_lists=countries_lists) is False:
            errors_list.append(f"Countries are different in selection list ({self.selected_countries}) versus keys of aggreg. prod. types selection dict. - wo None value ({agg_pt_countries_with_val})")

        # check that aggreg. prod types are not repeated, and known
        msg_suffix = "in values of dict. of aggreg. prod. types selection, for country"
        for elt_country, current_agg_pt in self.selected_prod_types.items():
            current_avail_aggreg_pt_set = set(eraa_data_descr.available_aggreg_prod_types[elt_country][year])
            current_agg_pt_set = set(current_agg_pt)
            if len(current_agg_pt_set) < len(current_agg_pt):
                errors_list.append(f"Repetition of aggreg. prod. types {msg_suffix} {elt_country}")
            unknown_agg_prod_types = list(current_agg_pt_set - current_avail_aggreg_pt_set)
            if len(unknown_agg_prod_types) > 0:
                errors_list.append(f"Unknown/not available aggreg. prod. types {msg_suffix} {elt_country}: {unknown_agg_prod_types}")

        # check that both dates are in allowed period
        allowed_period_msg = f"[{MIN_DATE_IN_DATA.strftime(DATE_FORMAT)}, {MAX_DATE_IN_DATA.strftime(DATE_FORMAT)}]"
        if not (MIN_DATE_IN_DATA <= self.uc_period_start <= MAX_DATE_IN_DATA):
            errors_list.append(f"UC period start {self.uc_period_start.strftime(DATE_FORMAT)} not in allowed period {allowed_period_msg}")
        if not (MIN_DATE_IN_DATA <= self.uc_period_end <= MAX_DATE_IN_DATA):
            errors_list.append(f"UC period end {self.uc_period_end.strftime(DATE_FORMAT)} not in allowed period {allowed_period_msg}")

        # updated fuel sources params -> check non-negative marginal cost and CO2 emission values
        for source, params in self.updated_fuel_sources_params.items():
            for name, val in params.items():
                if val < 0:
                    errors_list.append(f"Updated fuel source {source} param {name} must be non-negative; but value read {val}")

        # stop if any error
        if len(errors_list) > 0:
            uncoherent_param_stop(param_errors=errors_list)
        else:
            print_out_msg(msg_level="info", msg="Modified LONG-TERM UC PARAMETERS ARE COHERENT!")
            print_out_msg(msg_level="info", msg=f"RUN CAN START with parameters: {str(self)}")
