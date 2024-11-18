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
    generators = []
    return generators
