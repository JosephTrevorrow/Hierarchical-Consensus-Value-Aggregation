import os
import pandas as pd
import numpy as np

def calculate_boxplot_stats(data):
    stats = {}
    stats['mean'] = np.mean(data)
    stats['median'] = np.median(data)
    stats['q1'] = np.percentile(data, 25)
    stats['q3'] = np.percentile(data, 75)
    stats['iqr'] = stats['q3'] - stats['q1']
    stats['lower_whisker'] = stats['q1'] - 1.5 * stats['iqr']
    stats['upper_whisker'] = stats['q3'] + 1.5 * stats['iqr']
    #stats = {k: round(v, 4) if isinstance(v, (int, float)) else v for k, v in stats.items()}
    return stats

def process_csv_files(directory,output_directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path)
            data.drop_duplicates(subset=['residual'], inplace=True)
            data.reset_index(drop=True, inplace=True)
            for column in data.columns:
                column_data = data[column].dropna()
                #column_data = column_data.drop_duplicates()
                stats = calculate_boxplot_stats(column_data)
                print(f"File: {filename}, Column: {column}")
                print(stats)
                output_filename = f"boxplot-{filename}"
                output_path = os.path.join(output_directory, output_filename)
                stats_df = pd.DataFrame([stats])
                stats_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    directory = '/data/results/normalised_residuals/individual_residuals'
    output_directory = '/'
    process_csv_files(directory, output_directory)