from pypsa import Network
import numpy as np
from typing import Dict
from dataclasses import dataclass


@dataclass
class OptimResolStatus:
    optimal: str = "optimal"
    infeasible: str = "infeasible"
    

OPTIM_RESOL_STATUS = OptimResolStatus()


def get_generators_opt_p(network: Network) -> Dict[str, np.array]:
    generator_names = list(network.generators_t.p.columns)
    return {name: np.array(network.generators_t.p["Hard-Coal_ita"]) for name in generator_names}


def generators_opt_p_to_csv():
    return None


def get_network_obj_value(network: Network) -> float:
    return network.objective
