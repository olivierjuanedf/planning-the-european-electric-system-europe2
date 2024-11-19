from pypsa import Network
import numpy as np
from typing import Dict


def get_generators_opt_p(network: Network) -> Dict[str, np.array]:
    generator_names = list(network.generators_t.p.columns)
    return {name: np.array(network.generators_t.p["Hard-Coal_ita"]) for name in generator_names}


def generators_opt_p_to_csv():
    return None
    