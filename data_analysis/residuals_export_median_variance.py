import os
import numpy as np
import pandas as pd

# Directory containing the data files
data_dir = '/Users/josephtrevorrow/Documents/GitHub/Hierarchical-Consensus-Value-Aggregation/data/results/normalised_residuals/country-residuals'

# List of filenames to process
filenames = os.listdir(data_dir)

# Iterate over the list of filenames
for filename in filenames:
    file_path = os.path.join(data_dir, filename)
    
    # Read in the data
    data = pd.read_csv(file_path)
    
    # Calculate the median and variance for each column
    median = data.median()
    variance = data.var()
    
    # Combine the results into a DataFrame
    results = pd.DataFrame({'Median': median, 'Variance': variance})
    
    # Export the results to a new file
    output_filename = f"{os.path.splitext(filename)[0]}_median_variance.csv"
    output_path = os.path.join(data_dir, output_filename)
    results.to_csv(output_path, index_label='Column')

    print(f"Processed {filename} and saved results to {output_filename}")