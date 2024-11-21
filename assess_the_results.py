import pandas as pd
import os
import matplotlib.pyplot as plt

def load_result_data(directory):
    """Load all relevant CSV files from the specified directory"""
    data = {}
    csv_path = os.path.expanduser('~/Projects/ATHENS_EU2/output/long_term_uc/data')
    
    for file in os.listdir(csv_path):
        if file.endswith('.csv'):
            file_path = os.path.join(csv_path, file)
            data[file.replace('.csv', '')] = pd.read_csv(file_path)
    
    return data

def analyze_results(data):
    """Perform basic analysis on the optimization results"""
    results = {}
    
    # Add analysis for each dataframe
    for name, df in data.items():
        print(f"\nAnalyzing {name}:")
        print("-" * 50)
        print(f"Shape: {df.shape}")
        print("\nColumns:", df.columns.tolist())
        print("\nSample data:")
        print(df.head())
        print("\nBasic statistics:")
        print(df.describe())

def plot_results(data):
    """Create visualizations of the optimization results"""
    plt.style.use('ggplot')
    
    # Create plots based on the available data
    # This is a placeholder - we can customize based on your specific needs
    for name, df in data.items():
        if len(df.select_dtypes(include=['float64', 'int64']).columns) > 0:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            plt.figure(figsize=(12, 6))
            df[numeric_cols].plot()
            plt.title(f'Time Series Plot - {name}')
            plt.xlabel('Index')
            plt.ylabel('Value')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()

def main():
    # Load the data
    data = load_result_data('~/Projects/ATHENS_EU2/output/long_term_uc/data')
    
    # Analyze the results
    analyze_results(data)
    
    # Plot the results
    plot_results(data)

if __name__ == "__main__":
    main() 