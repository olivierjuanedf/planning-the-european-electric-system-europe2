from dataclasses import dataclass

"""
**[Optional, for better parametrization of assets]**
"""

# [Coding trick] dataclass is a simple way to define object to store multiple attributes
@dataclass
class FuelSources:
    name: str
    co2_emissions: float
    committable: bool
    min_up_time: float
    min_down_time: float
    energy_density_per_ton: float  # in MWh / ton
    cost_per_ton: float
    primary_cost: float = None  # € / MWh (multiply this by the efficiency of your power plant to get the marginal cost)
# [Coding trick] this function will be applied automatically at initialization of an object of this class
    def __post_init__(self):
      if self.energy_density_per_ton != 0:
          self.primary_cost = self.cost_per_ton / self.energy_density_per_ton
      else:
          self.primary_cost = 0

FUEL_SOURCES = {
    "Coal": FuelSources("Coal", 760, True, 4, 4, 8, 128),
    "Gas": FuelSources("Gas", 370, True, 2, 2, 14.89, 134.34),
    "Oil": FuelSources("Oil", 406, True, 1, 1, 11.63, 555.78),
    "Uranium": FuelSources("Uranium", 0, True, 10, 10, 22394, 150000.84),
    "Solar": FuelSources("Solar", 0, False, 1, 1, 0, 0),
    "Wind": FuelSources("Wind", 0, False, 1, 1, 0, 0),
    "Hydro": FuelSources("Hydro", 0, True, 2, 2, 0, 0),
    "Biomass": FuelSources("Biomass", 0, True, 2, 2, 5, 30)
}
