import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

def load_plot(plot_geojson_path: str) -> gpd.GeoDataFrame:
    """
    Loads a plot from a GeoJSON file.
    Args:
        plot_geojson_path (str): Path to the plot GeoJSON file.
    Returns:
        gpd.GeoDataFrame: The loaded plot as a GeoDataFrame.
    """
    plot_gdf = gpd.read_file(plot_geojson_path)
    return plot_gdf

def load_points_from_csv(csv_path: str, crs: str) -> gpd.GeoDataFrame:
    """
    Loads points from a CSV file and converts them to a GeoDataFrame.
    Args:
        csv_path (str): Path to the CSV file containing the points.
        crs (str): Coordinate Reference System to use for the points (should match the plot).
    Returns:
        gpd.GeoDataFrame: The points as a GeoDataFrame.
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Create Point geometries from the center_x and center_y columns
    geometry = [Point(xy) for xy in zip(df['center_x'], df['center_y'])]
    
    # Create a GeoDataFrame
    points_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    
    return points_gdf

def check_points_within_plot(points_gdf: gpd.GeoDataFrame, plot_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Checks if the points are within the plot and extracts the filenames.
    Args:
        points_gdf (gpd.GeoDataFrame): The points to check.
        plot_gdf (gpd.GeoDataFrame): The plot as a GeoDataFrame.
    Returns:
        pd.DataFrame: A DataFrame containing the filenames of the points within the plot.
    """
    # Assuming the plot is a single polygon or polyline
    plot_polygon = plot_gdf.geometry.iloc[0]
    
    # Check if points are within the plot
    points_within = points_gdf[points_gdf.geometry.within(plot_polygon)]
    
    # Extract filenames of points that are within the plot
    filenames_within = points_within[['filename']]
    
    return filenames_within

def save_filenames_to_csv(filenames_df: pd.DataFrame, output_csv_path: str):
    """
    Saves the extracted filenames to a CSV file.
    Args:
        filenames_df (pd.DataFrame): DataFrame containing filenames.
        output_csv_path (str): Path to save the CSV file.
    """
    filenames_df.to_csv(output_csv_path, index=False)




# Paths to your files
plot_geojson_path = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\russel_river_check.RiSCAN\Exports\shrunk_plot_polygon.geojson"
csv_path = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\tree_locations.csv"
output_csv_path = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\trees_within_plot.csv"

# Load the plot
plot_gdf = load_plot(plot_geojson_path)

# Load the points from CSV (using the CRS of the plot)
points_gdf = load_points_from_csv(csv_path, plot_gdf.crs)

# Check if points are within the plot
filenames_within_df = check_points_within_plot(points_gdf, plot_gdf)

# Save the results to a new CSV file
save_filenames_to_csv(filenames_within_df, output_csv_path)
