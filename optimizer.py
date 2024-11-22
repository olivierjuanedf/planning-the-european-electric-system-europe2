"""
Optimization Framework for Complex Simulation Problems

This module implements a framework for optimizing simulation parameters using various
optimization algorithms. It handles the interaction between the optimizer, configuration
files, and external simulation scripts.

The framework follows these steps:
1. Update configuration parameters
2. Run external simulation
3. Evaluate results
4. Repeat until convergence

Author: [Your Name]
Date: [Current Date]
"""

import json
import subprocess
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from typing import List, Tuple, Dict, Union, Optional

class OptimizationProblem:
    """
    A class to handle the optimization of simulation parameters.
    
    This class manages the interaction between the optimization algorithm,
    configuration files, and simulation execution.
    
    Attributes:
        config_path (str): Path to the JSON configuration file
        script_path (str): Path to the simulation script
        iteration (int): Current iteration counter
    """
    
    def __init__(self, config_path: str, script_path: str):
        """
        Initialize the optimization problem.
        
        Args:
            config_path (str): Path to the JSON configuration file
            script_path (str): Path to the simulation script
        """
        self.config_path = config_path
        self.script_path = script_path
        self.iteration = 0
        
    def update_config(self, x: List[float]) -> None:
        """
        Update JSON configuration with new parameters.
        
        Args:
            x (List[float]): List of parameter values to optimize
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            JSONDecodeError: If config file is not valid JSON
        """
        try:
            # Read the existing config file
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            # Map optimization variables to config parameters
            # Structure matches testjson.json format
            param_index = 0
            
            # Update Scandinavia parameters
            config['updated_capacities_prod_types']['scandinavia']['wind_offshore'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['gas'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['others_fatal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['dsr'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['coal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['oil'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['wind_onshore'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['biofuel'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['scandinavia']['nuclear'] = x[param_index]; param_index += 1

            # Update Poland parameters
            config['updated_capacities_prod_types']['poland']['gas'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['poland']['others_fatal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['poland']['coal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['poland']['wind_onshore'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['poland']['biofuel'] = x[param_index]; param_index += 1

            # Update Benelux parameters
            config['updated_capacities_prod_types']['benelux']['wind_offshore'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['gas'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['others_fatal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['dsr'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['batteries'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['coal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['oil'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['wind_onshore'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['biofuel'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['benelux']['nuclear'] = x[param_index]; param_index += 1

            # Update France parameters
            config['updated_capacities_prod_types']['france']['wind_offshore'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['france']['gas'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['france']['others_fatal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['france']['coal'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['france']['dsr'] = x[param_index]; param_index += 1
            config['updated_capacities_prod_types']['france']['nuclear'] = x[param_index]; param_index += 1

            # Update interconnection parameters
            config['interco_capas_updated_values']['benelux2france'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['benelux2germany'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['benelux2scandinavia'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['france2benelux'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['france2germany'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['france2italy'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['germany2scandinavia'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['iberian_peninsula2france'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['poland2germany'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['poland2scandinavia'] = x[param_index]; param_index += 1
            config['interco_capas_updated_values']['scandinavia2germany'] = x[param_index]

            # Write updated config back to file
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

        except FileNotFoundError:
            print(f"Configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError:
            print(f"Invalid JSON in configuration file: {self.config_path}")
            raise
    
    def run_simulation(self) -> bool:
        """
        Execute the external simulation script.
        
        Returns:
            bool: True if simulation successful, False otherwise
            
        Raises:
            subprocess.CalledProcessError: If simulation fails
        """
        try:
            subprocess.run(['python', self.script_path], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running simulation: {e}")
            return False
    
    def calculate_fitness(self) -> float:
        """
        Calculate fitness from simulation results.
        
        Reads the simulation results from output.csv and calculates
        the total cost based on multiple factors.
        
        Returns:
            float: Total cost (lower is better), or infinity if calculation fails
            
        Notes:
            Cost components:
            - Operational cost: Sum of all operational values
            - Penalty cost: Sum of violations multiplied by penalty factor
            - Maintenance cost: Mean of maintenance values
        """
        try:
            # Read simulation results
            results = pd.read_csv('/home/maximilian/Projects/ATHENS_EU2/output/long_term_uc/data/marginal_prices_europe_2025_cy1989_1900-01-01.csv')
            
            # Calculate various costs
            operational_cost_ben = results['ben'].sum()
            operational_cost_fr = results['fra'].sum()
            operational_cost_ger = results['ger'].sum()
            operational_cost_ita = results['ita'].sum()
            operational_cost_pol = results['pol'].sum()
            operational_cost_sc = results['sca'].sum()
            #maintenance_cost = results['maintenance'].mean()
            
            # Combine costs
            total_cost = operational_cost_ben + operational_cost_fr + operational_cost_ger + operational_cost_ita + operational_cost_pol + operational_cost_sc
            
            print(f"Iteration {self.iteration}: Cost = {total_cost}")
            self.iteration += 1
            
            return total_cost
            
        except Exception as e:
            print(f"Error calculating fitness: {e}")
            return float('inf')  # Return high cost for failed runs
    
    def objective_function(self, x: List[float]) -> float:
        """
        Main objective function for optimization.
        
        This function:
        1. Updates the configuration with new parameters
        2. Runs the simulation
        3. Calculates and returns the fitness
        
        Args:
            x (List[float]): List of parameter values to optimize
            
        Returns:
            float: Fitness value (lower is better)
        """
        # Update configuration
        self.update_config(x)
        #print(x)
        
        # Run simulation
        if not self.run_simulation():
            return float('inf')
        
        # Calculate and return fitness
        return self.calculate_fitness()

def main():
    """
    Main function to run the optimization process.
    
    This function:
    1. Sets up the optimization problem
    2. Defines bounds and initial values
    3. Runs the optimization
    4. Prints results
    """
    # Initialize optimization problem
    # Set up optimization problem to find optimal parameters
    #
    # The optimization process involves:
    # 1. Parameter space exploration using Nelder-Mead algorithm
    # 2. Simulation runs with different parameter combinations
    # 3. Cost evaluation based on:
    #    - Operational costs (fuel, maintenance etc.)
    #    - Penalty costs for constraint violations
    #    - Maintenance scheduling costs
    #
    # The optimization aims to:
    # - Minimize total system costs
    # - Find feasible solutions within operational constraints
    # - Balance between different cost components
    #
    # Key parameters being optimized:
    # - x[0]: Production capacity scaling factor (0-100%)
    # - x[1]: Maintenance window duration (0-50 hours)
    # 
    # The optimization uses:
    # - Nelder-Mead simplex algorithm for derivative-free optimization
    # - Bounded parameter ranges to ensure feasible solutions
    # - Maximum 100 iterations to find optimal solution
    #
    # Returns OptimizationProblem instance configured with:
    # - Specified config file path
    # - Script path for simulation runs
    # - Initial parameter setup
    opt_problem = OptimizationProblem(
        #config_path='testjson-json',
        config_path='/home/maximilian/Projects/ATHENS_EU2/input/long_term_uc/countries/scandinavia.json',
        script_path='my_little_europe_lt_uc.py'
        #script_path='temp.py'
    )
    
    # Define bounds for variables
    # Define bounds based on all country capacities from scandinavia.json
    bounds_dict = {
        # Scandinavia
        'scandinavia_wind_offshore': (0, 100000),
        'scandinavia_gas': (0, 100000),
        'scandinavia_others_fatal': (0, 100000), 
        'scandinavia_dsr': (0, 100000),
        'scandinavia_hydro_reservoir': (0, 100000),
        'scandinavia_batteries': (0, 100000),
        'scandinavia_coal': (0, 100000),
        'scandinavia_oil': (0, 100000),
        'scandinavia_wind_onshore': (0, 100000),
        'scandinavia_biofuel': (0, 100000),
        'scandinavia_nuclear': (0, 100000),

        # Italy
        'italy_wind_offshore': (0, 100000),
        'italy_gas': (0, 100000),
        'italy_others_fatal': (0, 100000),
        'italy_dsr': (0, 100000),
        'italy_batteries': (0, 100000),
        'italy_coal': (0, 100000),
        'italy_oil': (0, 100000),
        'italy_wind_onshore': (0, 100000),
        'italy_solar_pv': (0, 100000),
        'italy_nuclear': (0, 100000),

        # Iberian Peninsula
        'iberian_peninsula_wind_offshore': (0, 100000),
        'iberian_peninsula_gas': (0, 100000),
        'iberian_peninsula_others_fatal': (0, 100000),
        'iberian_peninsula_dsr': (0, 100000),
        'iberian_peninsula_batteries': (0, 100000),
        'iberian_peninsula_coal': (0, 100000),
        'iberian_peninsula_oil': (0, 100000),
        'iberian_peninsula_wind_onshore': (0, 100000),
        'iberian_peninsula_nuclear': (0, 100000),

        # Poland
        'poland_gas': (0, 100000),
        'poland_others_fatal': (0, 100000),
        'poland_coal': (0, 100000),
        'poland_wind_onshore': (0, 100000),
        'poland_biofuel': (0, 100000),

        # Benelux
        'benelux_wind_offshore': (0, 100000),
        'benelux_gas': (0, 100000),
        'benelux_others_fatal': (0, 100000),
        'benelux_dsr': (0, 100000),
        'benelux_batteries': (0, 100000),
        'benelux_coal': (0, 100000),
        'benelux_oil': (0, 100000),
        'benelux_wind_onshore': (0, 100000),
        'benelux_biofuel': (0, 100000),
        'benelux_nuclear': (0, 100000),

        # France
        'france_wind_offshore': (0, 100000),
        'france_gas': (0, 100000),
        'france_others_fatal': (0, 100000),
        'france_coal': (0, 100000),
        'france_dsr': (0, 100000),
        'france_nuclear': (0, 100000),

        # Interconnection capacities
        'benelux2france': (0, 100000),
        'benelux2germany': (0, 100000),
        'benelux2scandinavia': (0, 100000),
        'france2benelux': (0, 100000),
        'france2germany': (0, 100000),
        'france2italy': (0, 100000),
        'germany2scandinavia': (0, 100000),
        'iberian_peninsula2france': (0, 100000),
        'poland2germany': (0, 100000),
        'poland2scandinavia': (0, 100000),
        'scandinavia2germany': (0, 100000)
    }

    # Convert bounds_dict to list of tuples
    bounds: List[Tuple[float, float]] = [entry for entry in bounds_dict.values()]
    
    # Initial guess
    x0: List[float] = [(upper + lower)/2 for lower, upper in bounds]
    
    # Run optimization
    result = minimize(
        opt_problem.objective_function,
        x0,
        method='Nelder-Mead',  # or 'SLSQP', 'COBYLA', etc.
        bounds=bounds,
        options={
            'maxiter': 100,  # Maximum number of iterations for the optimization algorithm
            'disp': True     # Display optimization progress/results during execution
        }
    )
    
    print("\nOptimization Results:")
    print(f"Best solution: {result.x}")
    print(f"Best fitness: {result.fun}")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")

if __name__ == "__main__":
    main()
