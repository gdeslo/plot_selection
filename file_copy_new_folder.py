import os
import shutil
import pandas as pd

# Paths (modify these)
csv_path = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\trees_within_plot.csv"
source_folder = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\Extraction_output\extracted_trees_20m_buffer"
destination_folder = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\trees_within_plot"

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Read the CSV file
df = pd.read_csv(csv_path)

# Make sure the column is named 'filename'
if 'filename' not in df.columns:
    raise ValueError("CSV file must contain a column named 'filename'")

# Iterate over filenames in the CSV
for file_name in df['filename']:
    source_path = os.path.join(source_folder, file_name)
    dest_path = os.path.join(destination_folder, file_name)

    # Check if the file exists in the source folder
    if os.path.isfile(source_path):
        shutil.copy2(source_path, dest_path)  # Copy file with metadata
        print(f"Copied: {file_name}")
    else:
        print(f"File not found: {file_name}")
