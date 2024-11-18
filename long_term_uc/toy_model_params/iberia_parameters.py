from typing import Dict, List

from long_term_uc.common.fuel_sources import FuelSources


gps_coords = (0, 0)  # Your choice!


def get_generators(country_trigram: str, fuel_sources: Dict[str, FuelSources],
                   wind_on_shore_data, wind_off_shore_data, solar_pv_data) -> List[dict]:
    """
    Get list of generators to be set on a given node of a PyPSA model
    :param country_trigram: name of considered country, as a trigram (ex: "ben", "fra", etc.)
    :param fuel_sources
    """
    # List to be completed
    generators = [
        {"name": f"Hard-Coal_{country_trigram}", "carrier": "Coal", "p_nom": 561.80,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Coal"].primary_cost * 0.37,
        "efficiency": 0.37, "committable": False},
        {"name": f"Gas_{country_trigram}", "carrier": "Gas", "p_nom": 28327.56,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Gas"].primary_cost * 0.5,
        "efficiency": 0.5, "committable": False},
        {"name": f"Oil_{country_trigram}", "carrier": "Oil", "p_nom": 0,
        "p_min_pu": 0, "p_max_pu": 0,
        "marginal_cost": fuel_sources["Gas"].primary_cost * 0.4,
        "efficiency": 0.4, "committable": False},
        {"name": f"Other-non-renewables_{country_trigram}",
        "carrier": "Other-non-renewables", "p_nom": 5018.49, "p_min_pu": 0,
        "p_max_pu": 1, "marginal_cost": fuel_sources["Gas"].primary_cost * 0.4,
        "efficiency": 0.4, "committable": False},
        {"name": f"Wind-on-shore_{country_trigram}", "carrier": "Wind",
        "p_nom": 14512, "p_min_pu": 0, "p_max_pu": wind_on_shore_data["value"].values,
        "marginal_cost": fuel_sources["Wind"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Wind-off-shore_{country_trigram}", "carrier": "Wind",
        "p_nom": 41216.73, "p_min_pu": 0, "p_max_pu": wind_off_shore_data["value"].values,
        "marginal_cost": fuel_sources["Wind"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Solar-pv_{country_trigram}", "carrier": "Solar", "p_nom": 40177.08,
        "p_min_pu": 0, "p_max_pu": solar_pv_data["value"].values,
        "marginal_cost": fuel_sources["Solar"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Solar-thermal_{country_trigram}", "carrier": "Solar", "p_nom": 2364.50,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Solar"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Hydro-pondage_{country_trigram}", "carrier": "Hydro", "p_nom": 266.00,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": 0.1, "efficiency": 1,
        "committable": False},
        {"name": f"Hydro-pump-storage-open-loop_{country_trigram}", "carrier": "Hydro", "p_nom": 6522.72,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": 0.1, "efficiency": 1,
        "committable": False},
        {"name": f"Hydro-pump-storage-closed-loop_{country_trigram}", "carrier": "Hydro", "p_nom": 3331.40,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": fuel_sources["Hydro"].primary_cost, "efficiency": 1,
        "committable": False},
        {"name": f"Hydro-reservoir_{country_trigram}", "carrier": "Hydro", "p_nom": 15179.69,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": 0, "efficiency": 1,
        "committable": False},
        {"name": f"Hydro-run-of-river_{country_trigram}", "carrier": "Hydro", "p_nom": 3679.44,
        "p_min_pu": 0, "p_max_pu": 1,
        "marginal_cost": 0, "efficiency": 1,
        "committable": False},
        {"name": f"Other-renewables_{country_trigram}", "carrier": "Other-renewables",
        "p_nom": 2033.40, "p_min_pu": 0, "p_max_pu": 1, "marginal_cost": 0,
        "efficiency": 0.4, "committable": False},
        # QUESTION: what is this - very necessary - last fictive asset?
        {"name": f"Failure_{country_trigram}", "carrier": "Failure",
        "p_nom": 1e10, "p_min_pu": 0, "p_max_pu": 1, "marginal_cost": 1e5,
        "efficiency": 1, "committable": False},
        {
        "name": f"Batteries_{country_trigram}",
        "carrier": "flexibility","p_nom":100.00,"marginal_cost":0,
        "p_min_pu": -1,
        "p_max_pu": 1,
        "efficiency":1,"committable":False
        },
        {"name": f"Nuclear_{country_trigram}", "carrier": "nuclear",
        "p_nom": 7117.36, "p_min_pu": 0, "p_max_pu": 1, 
        "marginal_cost": fuel_sources["Uranium"].primary_cost*0.33,
        "efficiency": 0.33, "committable": False},
        {"name":f"Demand-side-response-capacity_{country_trigram}","p_nom":500.00,"p_min_pu":0,"p_max_pu":1,
        "efficiency":1,"marginal_cost": 0,"committable":False}
    ]
    return generators
