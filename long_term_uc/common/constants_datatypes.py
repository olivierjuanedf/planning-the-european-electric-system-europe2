from dataclasses import dataclass


@dataclass
class DatatypesNames:
    demand: str = "demand"
    capa_factor: str = "res_capa-factors"
    installed_capa: str = "generation_capas"


DATATYPE_NAMES = DatatypesNames()
PROD_TYPES_PER_DT = {DATATYPE_NAMES.capa_factor: ["csp_nostorage", "lfsolarpv", "wind_offshore", "wind_onshore"],
                     DATATYPE_NAMES.installed_capa: ["batteries", "biofuel", "coal", "hard_coal", 
                                                     "lignite", "demand_side_response_capacity", "gas",
                                                     "hydro_pondage", "hydro_pump_storage_closed_loop", 
                                                     "hydro_pump_storage_open_loop", "hydro_reservoir", 
                                                     "hydro_run_of_river", "nuclear", "oil", 
                                                     "solar_(photovoltaic)", "solar_(thermal)", 
                                                     "wind_offshore", "wind_onshore"]
                                                     }
