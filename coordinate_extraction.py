import laspy
import numpy as np
import os
import csv

# Set directory containing LAZ files
folder_path = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\Extraction_output\extracted_trees_20m_buffer"

# Output CSV file with updated name
output_csv = os.path.join(r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\\" , "tree_locations.csv")

# Initialize CSV writing
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["filename", "center_x", "center_y"])  # Write header

    # Loop through all LAZ files ending in "_fixed.laz"
    for filename in os.listdir(folder_path):
        if filename.endswith(".las"):
            file_path = os.path.join(folder_path, filename)

            try:
                # Load LAZ file
                las = laspy.read(file_path, laz_backend=laspy.LazBackend.Lazrs)

                # Extract coordinates
                x = np.array(las.x)
                y = np.array(las.y)
                z = np.array(las.z)

                # Define cross-section range (e.g., bottom 0.5 meters)
                z_min = np.min(z)
                z_threshold = z_min + 0.5

                # Filter points in the cross-section
                mask = (z >= z_min) & (z <= z_threshold)
                x_section = x[mask]
                y_section = y[mask]

                if len(x_section) > 0:
                    # Compute centroid
                    center_x = np.mean(x_section)
                    center_y = np.mean(y_section)

                    # Write to CSV
                    writer.writerow([filename, center_x, center_y])

                    print(f"Processed {filename} -> Location: ({center_x}, {center_y})")
                else:
                    print(f"Skipped {filename} (no valid points in cross-section).")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

print(f"Results saved to {output_csv}")

