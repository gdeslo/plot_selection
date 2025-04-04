# Plot Selection Scripts 🌳

This repository contains a set of scripts designed to help you work with segmented trees within a plot area. The scripts allow you to **select areas of interest**, **extract coordinates**, and **filter files based on boundaries**.  

---

## Scripts Overview 📂  

### 1. `polyline.py`  
This script processes a **plot boundary polyline** to create polygon representations of the plot area, with options to **expand or shrink** the plot area using buffers.  

#### Features  
- Converts a `LineString` polyline to a `Polygon`.  
- Expands or shrinks the polygon area by a specified buffer distance.  
- Converts polygons back to polylines for visualization.  
- Reprojects data to a specified CRS (EPSG:32755 - UTM Zone 55S, suitable for Queensland).  
- Outputs results as GeoJSON files.  

#### Inputs  
- A GeoJSON file containing the polyline representing the plot boundary.  
- `expand_distance` (float): Positive value to expand the plot area.  
- `shrink_distance` (float): Negative value to shrink the plot area.  

#### Outputs  
GeoJSON files saved to the specified output directory:  
- `original_plot_polygon.geojson`  
- `expanded_plot_polygon.geojson` (if expansion is applied)  
- `shrunk_plot_polygon.geojson` (if shrinking is applied)  
- `original_plot_polyline.geojson`  
- `expanded_plot_polyline.geojson`  
- `shrunk_plot_polyline.geojson`  

#### Example Usage  
```python
output_dict = process_plot(
    file_path=r"C:\path\to\your\Plot_circumference.geojson",
    shrink_distance=-5  # Shrink by 5m
)

output_dir = r"C:\path\to\output\directory"
save_to_geojson(output_dict, output_dir)
```

---

### 2. `coordinate_extraction.py`  
This script extracts the **coordinates of tree stems** from `.las` files and saves them into a CSV file. It calculates the centroid of a defined cross-section of each tree.

#### Features  
- Processes `.las` files in a specified folder.  
- Filters points based on a cross-section height range (`0.5m` above the minimum Z value).  
- Calculates the centroid (`center_x`, `center_y`) of points within the cross-section.  
- Saves results to a CSV file.  

#### Inputs  
- A folder containing `.las` files of segmented trees.  
- Cross-section height: **0.5m above the minimum Z value**.  

#### Outputs  
- A CSV file named `tree_locations.csv` with the following columns:  
  - `filename`: The name of the `.las` file processed.  
  - `center_x`: X-coordinate of the tree center.  
  - `center_y`: Y-coordinate of the tree center.  

#### Example Usage  
```python
folder_path = r"C:\path\to\your\extracted_trees_folder"
output_csv = r"C:\path\to\output\directory\tree_locations.csv"
```

#### CSV Output Format  
| filename         | center_x   | center_y   |
|------------------|------------|------------|
| tree_01_fixed.las| 654321.123  | 1234567.456 |
| tree_02_fixed.las| 654328.321  | 1234573.789 |
| ...              | ...         | ...         |

---

### 3. `select_in_boundaries.py`  
This script checks which trees (based on their center coordinates) **fall within a specified plot boundary** and saves the valid filenames to a CSV file.  

#### Features  
- Loads a **polygon plot boundary** from a GeoJSON file.  
- Loads **tree center points** from a CSV file generated by `coordinate_extraction.py`.  
- Checks if points fall **within the plot boundary**.  
- Saves filenames of valid points to a new CSV file.  

#### Inputs  
1. **Plot boundary**: A GeoJSON file containing a polygon or polyline plot boundary (e.g., `shrunk_plot_polygon.geojson`).  
2. **Tree center points**: A CSV file containing filenames and their respective `center_x` and `center_y` coordinates (e.g., `tree_locations.csv`).  
3. **CRS**: The CRS of the plot boundary (should match the CRS of the input points).  

#### Outputs  
- A CSV file named `trees_within_plot.csv` containing:  
  - `filename`: The filenames of the trees within the plot boundary.  

#### Example Usage  
```python
plot_geojson_path = r"C:\path\to\your\shrunk_plot_polygon.geojson"
csv_path = r"C:\path\to\your\tree_locations.csv"
output_csv_path = r"C:\path\to\output\directory\trees_within_plot.csv"
```

The output CSV will have a simple structure:  
| filename         |
|------------------|
| tree_01_fixed.las|
| tree_02_fixed.las|
| ...              |

---

### 4. `file_copy_new_folder.py`  
This script copies the tree files listed in a CSV file to a new folder. It is used after filtering trees that fall within a specified plot boundary.  

#### Features  
- Reads a CSV file containing the filenames of trees within the plot.  
- Copies each file from the **source folder** to the **destination folder**.  
- Creates the destination folder if it does not already exist.  
- Maintains file metadata during the copy process.  
- Logs which files were successfully copied or not found.  

#### Inputs  
1. **CSV file**: A CSV file containing a column named `filename` (e.g., `trees_within_plot.csv`).  
2. **Source folder**: The folder where the original tree files are located.  
3. **Destination folder**: The folder where the selected files will be copied.  

#### Outputs  
- Files copied to the specified destination folder.  

#### Example Usage  
```python
csv_path = r"C:\path\to\trees_within_plot.csv"
source_folder = r"C:\path\to\extracted_trees_folder"
destination_folder = r"C:\path\to\new_trees_folder"
```

#### Log Output  
```
Copied: tree_01_fixed.las  
Copied: tree_02_fixed.las  
File not found: tree_03_fixed.las  
```

---

## Usage ⚙️  
1. **Modify paths and parameters** within each script to suit your project.  
2. **Run scripts in order**:  
   - `polyline.py` → `coordinate_extraction.py` → `select_in_boundaries.py` → `file_copy_new_folder.py`  
3. **Check your output directories** to verify results.  

---

## Requirements 📋  
- This script was made and tested with Python 3.11
- Required libraries:  
  - `geopandas`  
  - `shapely`  
  - `laspy`  
  - `numpy`  
  - `pandas`  

---

## For questions, mail to geike.desloover@ugent.be

---
