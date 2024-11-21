import pandas as pd
import matplotlib.pyplot as plt

# Replace with your actual CSV file paths
demand_csv = 'demand_2025_scandinavia.csv'
generation_csv = ('capa_factor_wind_onshore_2025_scandinavia.csv')


# Read the CSV files with the correct delimiter
demand_data = pd.read_csv(demand_csv, delimiter=';')
generation_data = pd.read_csv(generation_csv, delimiter=';')

# Filter demand data to include only entries where climatic_year = 1986
demand_data = demand_data[demand_data['climatic_year'] == 1986]
generation_data = generation_data[generation_data['climatic_year'] == 1989]

# Drop the 'climatic_year' column from generation data as it's not used
generation_data = generation_data.drop(columns=['climatic_year'])
demand_data = demand_data.drop(columns=['climatic_year'])

# Extract the value columns for demand and generation
demand_values = demand_data['value']
generation_values = generation_data['value']

# Calculate rolling averages with a window size of 7*24 (7 days)
rolling_window = 7 * 24  # 7 days × 24 hours
demand_rolling_avg = demand_values.rolling(window=rolling_window).mean()
generation_rolling_avg = generation_values.rolling(window=rolling_window).mean()

# Plot the rolling averages
plt.figure(figsize=(14, 8))
plt.plot(demand_rolling_avg, label='Demand (7-day Rolling Avg, 1986)', linestyle='-', linewidth=2)
plt.plot(generation_rolling_avg, label='Generation (7-day Rolling Avg)', linestyle='--', linewidth=2)

# Add labels, title, legend, and grid
plt.title('7-Day Rolling Average of Demand (1986) and Generation', fontsize=16)
plt.xlabel('Time (Hours)', fontsize=14)
plt.ylabel('Power (MW)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
