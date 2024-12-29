import pandas as pd
import glob

# Match all files with the specified pattern
file_pattern = "*.csv"  # Adjust the pattern if needed
csv_files = glob.glob(file_pattern)

# Check if files were found
if not csv_files:
    print("No files matched the pattern.")
else:
    # Sort the files by their date in the filename
    # Extract the numeric part of the filename and sort by it
    csv_files.sort(key=lambda x: int(x.split('.')[0]))  # Assumes filenames are like '2412.csv'

    # List to store DataFrames
    dfs = []

    for file in csv_files:
        # Read the CSV file, specifying the decimal separator as ','
        df = pd.read_csv(file, decimal=',')
        dfs.append(df)

    # Concatenate all DataFrames, ignoring the index to reindex the combined data
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv("combined_output.csv", index=False, decimal=',')
    print(f"Combined {len(csv_files)} files into 'combined_output.csv' in date order.")

