from typing import Dict, List

from long_term_uc.common.fuel_sources import FuelSources


gps_coords = (400, 40)  # Your choice!

def get_generators(country_trigram: str, fuel_sources: Dict[str, FuelSources],
                   wind_on_shore_data, wind_off_shore_data, solar_pv_data) -> List[dict]:
    """
    Get list of generators to be set on a given node of a PyPSA model
    :param country_trigram: name of considered country, as a trigram (ex: "ben", "fra", etc.)
    :param fuel_sources
    """
    generators = [
        {"name": f"Hard-Coal_{country_trigram}", "carrier": "Coal", "p_nom": 13181.55,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Coal"].primary_cost * 0.37,
        "efficiency": 0.37, "committable": False},
        {"name": f"Gas_{country_trigram}", "carrier": "Gas", "p_nom": 3728.2,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Gas"].primary_cost * 0.5,
        "efficiency": 0.5, "committable": False},
        {"name": f"Oil_{country_trigram}", "carrier": "Oil", "p_nom": 0,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Gas"].primary_cost * 0.4,
        "efficiency": 0.4, "committable": False},
        {"name": f"Other-non-renewables_{country_trigram}",
        "carrier": "Other-non-renewables", "p_nom": 6485.96, "p_min_pu": 0,
        "p_max_pu": 1, "marginal_cost": fuel_sources["Gas"].primary_cost * 0.4,
        "efficiency": 0.4, "committable": False},
        {"name": f"Wind-on-shore_{country_trigram}", "carrier": "Wind",
        "p_nom": 10930.32, "p_min_pu": 0, "p_max_pu": wind_on_shore_data["value"].values,
        "marginal_cost": fuel_sources["Wind"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Wind-off-shore_{country_trigram}", "carrier": "Wind",
        "p_nom": 0, "p_min_pu": 0, "p_max_pu": wind_off_shore_data["value"].values,
        "marginal_cost": fuel_sources["Wind"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Solar-pv_{country_trigram}", "carrier": "Solar", "p_nom": 16049,
        "p_min_pu": 0, "p_max_pu": solar_pv_data["value"].values,
        "marginal_cost": fuel_sources["Solar"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Other-renewables_{country_trigram}", "carrier": "Other-renewables",
        "p_nom": 1331.65, "p_min_pu": 0, "p_max_pu": 1, "marginal_cost": 0,
        "efficiency": 1, "committable": False},
        {"name": f"Biofuel_{country_trigram}", "carrier": "Biofuel",
        "p_nom": 664.84, "p_min_pu": 0, "p_max_pu": 1, "marginal_cost": 0,
        "efficiency": 1, "committable": False},
        
        # QUESTION: what is this - very necessary - last fictive asset?
        {"name": f"Failure_{country_trigram}", "carrier": "Failure",
        "p_nom": 1e10, "p_min_pu": 0, "p_max_pu": 1, "marginal_cost": 1e5,
        "efficiency": 1, "committable": False}
    ]
    return generators
