import geopandas as gpd
from shapely.geometry import LineString, Polygon

def polyline_to_polygon(polyline: LineString) -> Polygon:
    if not isinstance(polyline, LineString):
        raise ValueError("The provided geometry is not a LineString.")
    
    if not polyline.is_ring:
        coords = list(polyline.coords)
        coords.append(coords[0])
        polygon = Polygon(coords)
    else:
        polygon = Polygon(polyline.coords)
    
    return polygon

def polygon_to_polyline(polygon: Polygon) -> LineString:
    """
    Convert a polygon to a polyline (LineString) by taking its exterior boundary.
    """
    return LineString(polygon.exterior.coords)

def process_plot(file_path: str, expand_distance: float = 0, shrink_distance: float = 0):
    gdf = gpd.read_file(file_path)
    
    # Check the CRS of the file
    print(f"Original CRS: {gdf.crs}")
    
    # Reproject to a suitable CRS (e.g., UTM Zone 55S for Queensland)
    projected_gdf = gdf.to_crs("EPSG:32755")
    print(f"Reprojected CRS: {projected_gdf.crs}")

    polyline = projected_gdf.geometry.iloc[0]
    polygon = polyline_to_polygon(polyline)
    
    expanded_polygon = polygon.buffer(expand_distance) if expand_distance != 0 else None
    shrunk_polygon = polygon.buffer(shrink_distance) if shrink_distance != 0 else None

    # Convert polygons to polylines
    original_polyline = polygon_to_polyline(polygon)
    expanded_polyline = polygon_to_polyline(expanded_polygon) if expanded_polygon else None
    shrunk_polyline = polygon_to_polyline(shrunk_polygon) if shrunk_polygon else None

    # Create GeoDataFrames for output
    original_gdf = gpd.GeoDataFrame(geometry=[polygon], crs=projected_gdf.crs)
    expanded_gdf = gpd.GeoDataFrame(geometry=[expanded_polygon], crs=projected_gdf.crs) if expanded_polygon else None
    shrunk_gdf = gpd.GeoDataFrame(geometry=[shrunk_polygon], crs=projected_gdf.crs) if shrunk_polygon else None

    # Create GeoDataFrames for polylines
    original_line_gdf = gpd.GeoDataFrame(geometry=[original_polyline], crs=projected_gdf.crs)
    expanded_line_gdf = gpd.GeoDataFrame(geometry=[expanded_polyline], crs=projected_gdf.crs) if expanded_polyline else None
    shrunk_line_gdf = gpd.GeoDataFrame(geometry=[shrunk_polyline], crs=projected_gdf.crs) if shrunk_polyline else None

    return {
        "original_polygon": original_gdf,
        "expanded_polygon": expanded_gdf,
        "shrunk_polygon": shrunk_gdf,
        "original_line": original_line_gdf,
        "expanded_line": expanded_line_gdf,
        "shrunk_line": shrunk_line_gdf
    }

def save_to_geojson(geojson_dict: dict, output_dir: str):
    if geojson_dict["original_polygon"] is not None:
        geojson_dict["original_polygon"].to_file(f"{output_dir}/original_plot_polygon.geojson", driver="GeoJSON")
    if geojson_dict["expanded_polygon"] is not None:
        geojson_dict["expanded_polygon"].to_file(f"{output_dir}/expanded_plot_polygon.geojson", driver="GeoJSON")
    if geojson_dict["shrunk_polygon"] is not None:
        geojson_dict["shrunk_polygon"].to_file(f"{output_dir}/shrunk_plot_polygon.geojson", driver="GeoJSON")
    
    if geojson_dict["original_line"] is not None:
        geojson_dict["original_line"].to_file(f"{output_dir}/original_plot_polyline.geojson", driver="GeoJSON")
    if geojson_dict["expanded_line"] is not None:
        geojson_dict["expanded_line"].to_file(f"{output_dir}/expanded_plot_polyline.geojson", driver="GeoJSON")
    if geojson_dict["shrunk_line"] is not None:
        geojson_dict["shrunk_line"].to_file(f"{output_dir}/shrunk_plot_polyline.geojson", driver="GeoJSON")


output_dict = process_plot(
    file_path=r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\russel_river_check.RiSCAN\Exports\Plot_circumference.geojson",
    shrink_distance=-5  # Shrink by 5m
)

output_dir = r"C:\Users\gedsloov\OneDrive - UGent\UGent\PhD\05_Research\01_Australia\02_Data\03_Scanning\RUS01-01_russel_river\russel_river_check.RiSCAN\Exports"
save_to_geojson(output_dict, output_dir)
