import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_demand_by_year_more_input_files(file_paths:list):
    # Read CSV file
    df1 = pd.read_csv(file_paths[0], sep=';')
    df2 = pd.read_csv(file_paths[1], sep=';')

    df = pd.concat([df1, df2], ignore_index=True)
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Group by climatic_year
    grouped = df.groupby('climatic_year')
    
    # Print available climatic years
    years = list(grouped.groups.keys())
    years.sort()  # Sort years for better readability
    print("\nAvailable climatic years:")
    print(years)
    print(f"Total number of years: {len(years)}")
    
    return grouped

def plot_demand_comparison_sorted(grouped_df1, grouped_df2, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    df_sorted_1 = grouped_df1.sort_values(by='value', ascending=False)
    df_sorted_2 = grouped_df2.sort_values(by='value', ascending=False)
    # Create the plot
    plt.figure(figsize=(15, 6))
    x_values = range(len(df_sorted_1))
    plt.plot(df_sorted_1.index, df_sorted_1['value'], label='Dataset 1')
    plt.plot(df_sorted_2.index, df_sorted_2['value'], label='Dataset 2')
    
    # Customize the plot
    plt.title('Sorted Demand Values Comparison')
    plt.xlabel('Index (Sorted by Value)')
    plt.ylabel('Demand (MW)')
    plt.grid(True)
    plt.legend()
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'demand_comparison_sorted.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Comparison plot saved: {output_path}")

    
   

def plot_demand_for_year(grouped_df, year, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get data for specific year
    year_data = grouped_df.get_group(year)
    
    # Create the plot
    plt.figure(figsize=(15, 6))
    plt.plot(year_data['date'], year_data['value'])
    
    # Customize the plot
    plt.title(f'Demand Values for Climatic Year {year}')
    plt.xlabel('Date')
    plt.ylabel('Demand (MW)')
    plt.grid(True)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, f'demand_plot_{year}.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    print(f"Plot saved: {output_path}")



def main():
    file_paths = [
        "/home/maximilian/Projects/ATHENS_EU2/data/ERAA_2023-2/demand/demand_2025_scandinavia.csv",
        "/home/maximilian/Projects/ATHENS_EU2/data/ERAA_2023-2/demand/cy_stress-test/demand_2025_scandinavia.csv"
    ]
    output_dir = "output/demand_plots"
    
    # Get grouped data
    grouped = analyze_demand_by_year_more_input_files(file_paths)
    
    # Alternative ways to see the keys
    #print("\nAlternative ways to view years:")
    #print("Method 1:", grouped.groups.keys())
    #print("Method 2:", grouped.groups.items())  # This shows years and corresponding indices
    """
    for year in list(grouped.groups.keys()):
        plot_demand_for_year(grouped, year, output_dir)
    """
    #print(grouped.get_group(1987))
    grouped_df1 = grouped.get_group(1987)
    print(grouped_df1.keys())
    grouped_df2 = grouped.get_group(2003)
    plot_demand_comparison_sorted(grouped_df1, grouped_df2, output_dir)


    

if __name__ == "__main__":
    main()
