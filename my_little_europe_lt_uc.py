"""
Read JSON parametrization files... and check coherence of them
"""
import warnings
#deactivate some annoying and useless warnings in pypsa/pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
import matplotlib.pyplot as plt

from long_term_uc.common.long_term_uc_io import get_marginal_prices_file, get_opt_power_file, get_price_figure, get_prod_figure, get_network_figure
from long_term_uc.utils.read import read_and_check_uc_run_params
from long_term_uc.utils.eraa_data_reader import get_countries_data
from long_term_uc.utils.basic_utils import get_period_str
from long_term_uc.include.dataset_builder import get_generation_units_data, control_min_pypsa_params_per_gen_units
from long_term_uc.utils.read import read_and_check_pypsa_static_params
from long_term_uc.include.dataset_builder import init_pypsa_network, add_gps_coordinates, add_energy_carrier, \
  add_generators, add_loads, add_interco_links, save_lp_model, overwrite_gen_units_fuel_src_params
from long_term_uc.common.fuel_sources import FUEL_SOURCES

usage_params, eraa_data_descr, uc_run_params = read_and_check_uc_run_params()

"""
Get needed data (demand, RES Capa. Factors, installed generation capacities)
"""
uc_period_msg = get_period_str(period_start=uc_run_params.uc_period_start, 
                               period_end=uc_run_params.uc_period_end)

print(f"Read needed ERAA ({eraa_data_descr.eraa_edition}) data for period {uc_period_msg}")
demand, agg_cf_data, agg_gen_capa_data, interco_capas = \
  get_countries_data(uc_run_params=uc_run_params,
                     agg_prod_types_with_cf_data=eraa_data_descr.agg_prod_types_with_cf_data,
                     aggreg_prod_types_def=eraa_data_descr.aggreg_prod_types_def
                     )

print("Get generation units data, from both ERAA data - read just before - and JSON parameter file")
generation_units_data = \
  get_generation_units_data(uc_run_params=uc_run_params, pypsa_unit_params_per_agg_pt=eraa_data_descr.pypsa_unit_params_per_agg_pt,
                            units_complem_params_per_agg_pt=eraa_data_descr.units_complem_params_per_agg_pt, 
                            agg_res_cf_data=agg_cf_data, agg_gen_capa_data=agg_gen_capa_data)
for country, val in generation_units_data.items():
    for i in range(len(val)):
        val[i].committable = False
# TODO: connect this properly
#if len(uc_run_params.updated_fuel_sources_params) > 0:
#   generation_units_data = overwrite_gen_units_fuel_src_params(generation_units_data=generation_units_data, 
#                                                               updated_fuel_sources_params=uc_run_params.updated_fuel_sources_params)

print("Check that 'minimal' PyPSA parameters for unit creation have been provided (in JSON files)/read (from ERAA data)")
pypsa_static_params = read_and_check_pypsa_static_params()
control_min_pypsa_params_per_gen_units(generation_units_data=generation_units_data,
                                       pypsa_min_unit_params_per_agg_pt=pypsa_static_params.min_unit_params_per_agg_pt)

# create PyPSA network
network = init_pypsa_network(df_demand_first_country=demand[uc_run_params.selected_countries[0]])
import pandas as pd
horizon = pd.date_range(
    start = uc_run_params.uc_period_start.replace(year=uc_run_params.selected_target_year),
    end = uc_run_params.uc_period_end.replace(year=uc_run_params.selected_target_year),
    freq = 'h'
)
network.set_snapshots(horizon[:-1])
# add GPS coordinates
selec_countries_gps_coords = \
  {country: gps_coords for country, gps_coords in eraa_data_descr.gps_coordinates.items() 
   if country in uc_run_params.selected_countries}
network = add_gps_coordinates(network=network, countries_gps_coords=selec_countries_gps_coords)
network = add_energy_carrier(network=network, fuel_sources=FUEL_SOURCES)
network = add_generators(network=network, generators_data=generation_units_data)
network = add_loads(network=network, demand=demand)
network = add_interco_links(network, countries=uc_run_params.selected_countries, 
                            interco_capas=interco_capas)
print("PyPSA network main properties:", network)
plt.close()
network.plot(title="My little elec. Europe network", color_geomap=True, jitter=0.3)
plt.savefig(get_network_figure())
print("Optimize 'network' - i.e. solve associated UC problem")
result = network.optimize(solver_name="highs")
print(result)
save_lp_model(network, year=uc_run_params.selected_target_year, 
              n_countries=len(uc_run_params.selected_countries), 
              period_start=uc_run_params.uc_period_start)
print("THE END of European PyPSA-ERAA UC simulation... now you can hack it!")

from long_term_uc.utils.pypsa_utils import OPTIM_RESOL_STATUS, get_network_obj_value
pypsa_opt_resol_status = OPTIM_RESOL_STATUS.optimal
if result[1] == pypsa_opt_resol_status:
  objective_value = get_network_obj_value(network=network)
  print(f"Optimisation resolution status is {pypsa_opt_resol_status} with objective value (cost) = {objective_value:.2f} -> output data (resp. figures) can be generated")

  network.buses_t.marginal_price.plot.line(figsize=(8, 3), ylabel="Euro per MWh")
  plt.tight_layout()
  plt.show()
  plt.savefig(get_price_figure(country='europe', year=uc_run_params.selected_target_year, climatic_year=uc_run_params.selected_climatic_year,
                             start_horizon=uc_run_params.uc_period_start)
                             )
  plt.close()

  # IV.9) Save optimal decision to an output file
  print("Save optimal dispatch decisions to .csv file")
  opt_p_csv_file = get_opt_power_file(country='europe', year=uc_run_params.selected_target_year, climatic_year=uc_run_params.selected_climatic_year,
                                      start_horizon=uc_run_params.uc_period_start)
  network.generators_t.p.to_csv(opt_p_csv_file)

  # IV.10) Save marginal prices to an output file
  print("Save marginal prices decisions to .csv file")
  marginal_prices_csv_file = get_marginal_prices_file(country='europe', year=uc_run_params.selected_target_year, climatic_year=uc_run_params.selected_climatic_year,
                                                      start_horizon=uc_run_params.uc_period_start)
  network.buses_t.marginal_price.to_csv(marginal_prices_csv_file)
else:
   print(f"Optimisation resolution status is not {pypsa_opt_resol_status} -> output data (resp. figures) cannot be saved (resp. plotted)")
   