"""
GeoPandas Spatial Operations - Student Implementation

Complete the seven functions in this file.
Use the notebooks to learn and test each function.

📋 FUNCTIONS TO IMPLEMENT IN THIS FILE:
=====================================
✅ Function 1: load_spatial_data()        → notebooks/geopandas/01_function_...
✅ Function 2: explore_properties()       → notebooks/geopandas/02_function_...
✅ Function 3: transform_crs()            → notebooks/geopandas/03_function_...
✅ Function 4: geometry_operations()      → notebooks/geopandas/04_function_...
✅ Function 5: spatial_relationships()    → notebooks/geopandas/05_function_...
✅ Function 6: spatial_joins()            → notebooks/geopandas/06_function_...
✅ Function 7: overlay_and_visualize()    → notebooks/geopandas/07_function_...
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from typing import Dict, List, Tuple, Union, Optional, Any
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# Function 1: Load Spatial Data

def load_spatial_data(file_path: Union[str, Path], **kwargs) -> gpd.GeoDataFrame:
    """
    Load spatial data from various vector file formats.
    
    Supports GeoJSON, Shapefile, GeoPackage, and other formats readable by GeoPandas.
    Professional implementation with comprehensive error handling.
    
    Args:
        file_path: Path to the spatial data file
        **kwargs: Additional arguments to pass to gpd.read_file()
        
    Returns:
        GeoDataFrame containing the loaded spatial data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is invalid or cannot be read
        
    Example:
        >>> gdf = load_spatial_data('data/cities.geojson')
        >>> print(f"Loaded {len(gdf)} features")
    """
    
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        gdf = gpd.read_file(file_path, **kwargs)
    except Exception as e:
        raise ValueError(f"Cannot read spatial data: {e}")

    if gdf.empty:
        raise ValueError("Spatial data is empty")

    return gdf



# Function 2: Explore Properties

def explore_properties(gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
    """
    Analyze and extract key spatial properties from a GeoDataFrame.
    
    Provides comprehensive exploration of:
    - Coordinate Reference System (CRS)
    - Spatial bounds (extent)
    - Geometry types present
    - Feature count and basic statistics
    
    Args:
        gdf: Input GeoDataFrame to explore
        
    Returns:
        Dictionary containing spatial properties:
        - 'crs': CRS object or None
        - 'bounds': [minx, miny, maxx, maxy] or empty list
        - 'geometry_types': List of unique geometry types
        - 'feature_count': Number of features
        - 'columns': List of attribute column names
        
    Example:
        >>> props = explore_properties(gdf)
        >>> print(f"CRS: {props['crs']}")
        >>> print(f"Bounds: {props['bounds']}")
        >>> print(f"Geometry types: {props['geometry_types']}")
    """
   
    if gdf is None or gdf.empty:
        return {
            'crs': None,
            'bounds': gdf.total_bounds.tolist(),
            'geometry_types': [],
            'feature_count': 0,
            'columns': []
        }

    return {
        'crs': gdf.crs,
        'bounds': gdf.total_bounds.tolist(),
        'geometry_types': gdf.geometry.geom_type.unique().tolist(),
        'feature_count': len(gdf),
        'columns': gdf.columns.tolist()
    }



# Function 3: Transform CRS

def transform_crs(
    gdf: gpd.GeoDataFrame, 
    target_crs: Union[str, int]
) -> gpd.GeoDataFrame:
    """
    Transform GeoDataFrame to a different coordinate reference system.
    
    Handles CRS transformation with proper validation and error handling.
    Essential for ensuring spatial data alignment and accurate measurements.
    
    Args:
        gdf: Input GeoDataFrame
        target_crs: Target CRS (e.g., 'EPSG:4326', 'EPSG:3857', or EPSG code as int)
        
    Returns:
        New GeoDataFrame in the target CRS
        
    Raises:
        ValueError: If GeoDataFrame has no CRS or target CRS is invalid
        
    Example:
        >>> # Transform to Web Mercator (EPSG:3857)
        >>> gdf_mercator = transform_crs(gdf, 'EPSG:3857')
        >>> print(f"New CRS: {gdf_mercator.crs}")
    """
    
    if gdf.crs is None:
        raise ValueError("Input GeoDataFrame has no CRS defined")

    try:
        result = gdf.to_crs(target_crs)
    except Exception as e:
        raise ValueError(f"Invalid target CRS: {e}")

    return result


# Function 4: Geometry Operations

def geometry_operations(
    gdf: gpd.GeoDataFrame,
    operation: str = 'buffer',
    **kwargs
) -> Dict[str, Any]:
    """
    Perform fundamental geometry operations on spatial data.
    
    Supports multiple geometric operations:
    - 'buffer': Create buffers around geometries
    - 'centroid': Calculate geometric centers
    - 'area': Calculate polygon areas
    - 'length': Calculate line lengths
    - 'simplify': Generalize geometries
    
    Args:
        gdf: Input GeoDataFrame
        operation: Operation to perform ('buffer', 'centroid', 'area', 'length', 'simplify')
        **kwargs: Operation-specific parameters:
            - buffer: distance (float, required)
            - simplify: tolerance (float, required)
            
    Returns:
        Dictionary containing:
        - 'result': GeoDataFrame with operation results
        - 'statistics': Dictionary of computed statistics
        - 'operation': Name of operation performed
        
    Raises:
        ValueError: If operation is invalid or parameters are missing
        
    Example:
        >>> # Create 1000m buffer
        >>> result = geometry_operations(gdf, 'buffer', distance=1000)
        >>> buffered_gdf = result['result']
        
        >>> # Calculate centroids
        >>> result = geometry_operations(gdf, 'centroid')
        >>> centroids = result['result']
    """
   
    valid_operations = ['buffer', 'centroid', 'area', 'length', 'simplify']

    if operation not in valid_operations:
        raise ValueError(f"Invalid operation: {operation}")

    result_gdf = gdf.copy()
    statistics = {}

    if operation == 'buffer':
        if 'distance' not in kwargs:
            raise ValueError("Buffer requires distance")
        result_gdf['geometry'] = gdf.geometry.buffer(kwargs['distance'])
        statistics['total_area'] = result_gdf.geometry.area.sum()

    elif operation == 'centroid':
        result_gdf['geometry'] = gdf.geometry.centroid

    elif operation == 'area':
        result_gdf['area'] = gdf.geometry.area
        statistics['total_area'] = result_gdf['area'].sum()
        statistics['mean_area'] = result_gdf['area'].mean()

    elif operation == 'length':
        result_gdf['length'] = gdf.geometry.length
        statistics['total_length'] = result_gdf['length'].sum()
        statistics['mean_length'] = result_gdf['length'].mean()

    elif operation == 'simplify':
        if 'tolerance' not in kwargs:
            raise ValueError("Simplify requires tolerance")
        result_gdf['geometry'] = gdf.geometry.simplify(kwargs['tolerance'])

    return {
        'result': result_gdf,
        'statistics': statistics,
        'operation': operation
    }



# Function 5: Spatial Relationships

def spatial_relationships(
    gdf1: gpd.GeoDataFrame,
    gdf2: gpd.GeoDataFrame,
    relationship: str = 'intersects'
) -> Dict[str, Any]:
    """
    Test spatial relationships between two GeoDataFrames.
    
    Supports spatial predicates:
    - 'intersects': Geometries that intersect
    - 'contains': Geometries from gdf1 that contain gdf2
    - 'within': Geometries from gdf1 within gdf2
    - 'distance': Calculate distances between geometries
    - 'nearest': Find nearest features
    
    Args:
        gdf1: First GeoDataFrame
        gdf2: Second GeoDataFrame
        relationship: Type of spatial relationship to test
        
    Returns:
        Dictionary containing:
        - 'relationship': Type of relationship tested
        - 'results': Boolean series or distance measurements
        - 'count': Number of features meeting criteria
        - 'indices': Indices of matching features
        
    Raises:
        ValueError: If inputs are invalid or CRS don't match
        
    Example:
        >>> # Find cities that intersect countries
        >>> result = spatial_relationships(cities, countries, 'intersects')
        >>> print(f"{result['count']} cities intersect countries")
        
        >>> # Calculate distances
        >>> result = spatial_relationships(points, lines, 'distance')
        >>> distances = result['results']
    """
   
    valid_relationships = [
        'intersects', 'contains', 'within', 'distance', 'nearest'
    ]

    if relationship not in valid_relationships:
        raise ValueError(f"Invalid relationship: {relationship}")

    if gdf1.crs != gdf2.crs:
        raise ValueError("CRS mismatch between GeoDataFrames")

    if gdf1.empty or gdf2.empty:
        return {
            'relationship': relationship,
            'results': [],
            'count': 0,
            'indices': []
        }

    if relationship in ['intersects', 'contains', 'within']:
        results = gdf1.geometry.apply(
            lambda geom: getattr(geom, relationship)(gdf2.union_all())
        )

    elif relationship == 'distance':
        results = gdf1.geometry.apply(
            lambda geom: gdf2.distance(geom).min()
        )

    elif relationship == 'nearest':
        results = gdf1.geometry.apply(
            lambda geom: gdf2.distance(geom).idxmin()
        )

    if relationship in ['intersects', 'contains', 'within']:
        indices = results[results].index.tolist()
    else:
        indices = results.index.tolist()

    return {
        'relationship': relationship,
        'results': results,
        'count': len(indices),
        'indices': indices
    }


# Function 6: Spatial Joins

def spatial_joins(
    left_gdf: gpd.GeoDataFrame,
    right_gdf: gpd.GeoDataFrame,
    how: str = 'inner',
    predicate: str = 'intersects'
) -> gpd.GeoDataFrame:
    """
    Join two GeoDataFrames based on spatial relationships.
    
    Combines attribute data from two spatial datasets based on their
    spatial relationship (e.g., points within polygons, lines intersecting areas).
    
    Args:
        left_gdf: Left GeoDataFrame (preserved geometries)
        right_gdf: Right GeoDataFrame (attributes joined)
        how: Type of join ('inner', 'left', 'right')
        predicate: Spatial predicate ('intersects', 'contains', 'within')
        
    Returns:
        Joined GeoDataFrame with combined attributes
        
    Raises:
        ValueError: If inputs are invalid or CRS incompatible
        
    Example:
        >>> # Join cities with their countries
        >>> result = spatial_joins(cities, countries, how='left', predicate='within')
        >>> print(f"Joined {len(result)} features")
    """
    
    # Validate input types
    if not isinstance(left_gdf, gpd.GeoDataFrame):
        raise ValueError("left_gdf must be a GeoDataFrame")

    if not isinstance(right_gdf, gpd.GeoDataFrame):
        raise ValueError("right_gdf must be a GeoDataFrame")

    # Validate join type and spatial predicate
    if how not in ['inner', 'left', 'right']:
        raise ValueError(f"Invalid join type: {how}")

    if predicate not in ['intersects', 'contains', 'within']:
        raise ValueError(f"Invalid spatial predicate: {predicate}")

    # Check coordinate reference systems
    if left_gdf.crs is None or right_gdf.crs is None:
        raise ValueError("Both GeoDataFrames must have a CRS")

    
    # Check CRS compatibility
    if left_gdf.crs != right_gdf.crs:
        raise ValueError("CRS mismatch between GeoDataFrames")


    # Perform spatial join
    result = gpd.sjoin(
        left_gdf,
        right_gdf,
        how=how,
        predicate=predicate
    )

    # Check for empty inner join
    if how == 'inner' and result.empty:
        raise ValueError("Spatial join returned no matching features")

    return result


# Function 7: Overlay and Visualize

def overlay_and_visualize(
    gdf1: gpd.GeoDataFrame,
    gdf2: Optional[gpd.GeoDataFrame] = None,
    overlay_how: str = 'intersection',
    save_path: Optional[Union[str, Path]] = None
) -> Dict[str, Any]:
    """
    Perform overlay operations and create visualizations.
    
    Combines two spatial datasets using geometric overlay operations
    and generates both static and interactive visualizations.
    
    Overlay operations:
    - 'intersection': Areas where both datasets overlap
    - 'union': Combined areas from both datasets
    - 'difference': Areas in gdf1 not in gdf2
    - 'symmetric_difference': Areas in either but not both
    
    Args:
        gdf1: First GeoDataFrame
        gdf2: Second GeoDataFrame (optional for visualization only)
        overlay_how: Type of overlay operation
        save_path: Optional path to save the visualization
        
    Returns:
        Dictionary containing:
        - 'overlay_result': GeoDataFrame with overlay results (if gdf2 provided)
        - 'figure': Matplotlib figure object
        - 'statistics': Dictionary of geometry counts and areas
        
    Raises:
        ValueError: If inputs are invalid or overlay operation fails
        
    Example:
        >>> # Find intersection of two polygon layers
        >>> result = overlay_and_visualize(parks, flood_zones, 'intersection')
        >>> overlay_gdf = result['overlay_result']
        >>> print(f"Intersection area: {overlay_gdf.geometry.area.sum()}")
        
        >>> # Just visualize a single layer
        >>> result = overlay_and_visualize(cities, save_path='cities_map.png')
        >>> plt.show()
    """
   
    import matplotlib.pyplot as plt

    # Validate inputs
    if not isinstance(gdf1, gpd.GeoDataFrame):
        raise ValueError("gdf1 must be a GeoDataFrame")

    if gdf2 is not None and not isinstance(gdf2, gpd.GeoDataFrame):
        raise ValueError("gdf2 must be a GeoDataFrame")

    valid_operations = [
        'intersection', 'union',
        'difference', 'symmetric_difference'
    ]

    if overlay_how not in valid_operations:
        raise ValueError(f"Invalid overlay operation: {overlay_how}")

    # Perform overlay if second dataset is provided
    overlay_result = None

    if gdf2 is not None:
        if gdf1.crs != gdf2.crs:
            raise ValueError("CRS mismatch between GeoDataFrames")

        overlay_result = gpd.overlay(
            gdf1,
            gdf2,
            how=overlay_how
        )

    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 8))

    if not gdf1.empty:
        gdf1.plot(ax=ax, color='lightblue', edgecolor='black',
                  alpha=0.5)

    if gdf2 is not None and not gdf2.empty:
        gdf2.plot(ax=ax, color='lightgreen', edgecolor='black',
                  alpha=0.5)

    if overlay_result is not None and not overlay_result.empty:
        overlay_result.plot(
            ax=ax, color='red', edgecolor='black', alpha=0.7
        )

    ax.set_title(f"Spatial Overlay: {overlay_how}")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    # Calculate statistics
    statistics = {
        'gdf1_count': len(gdf1),
        'gdf2_count': len(gdf2) if gdf2 is not None else 0,
        'overlay_count': (
            len(overlay_result)
            if overlay_result is not None else 0
        ),
        'gdf1_area': float(gdf1.geometry.area.sum()),
        'overlay_area': (
            float(overlay_result.geometry.area.sum())
            if overlay_result is not None else 0.0
        )
    }

    # Save visualization if requested
    if save_path is not None:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

   
    result = {
        'figure': fig,
        'statistics': statistics
    }

    if gdf2 is not None:
        result['overlay_result'] = overlay_result

    return result




# Helper Functions (provided for you)

def _validate_crs_compatibility(
    gdf1: gpd.GeoDataFrame, 
    gdf2: gpd.GeoDataFrame
) -> Tuple[bool, str]:
    """
    Check if two GeoDataFrames have compatible CRS.
    
    Returns:
        Tuple of (compatible: bool, message: str)
    """
    if gdf1.crs is None:
        return False, "First GeoDataFrame has no CRS defined"
    if gdf2.crs is None:
        return False, "Second GeoDataFrame has no CRS defined"
    if gdf1.crs != gdf2.crs:
        return False, f"CRS mismatch: {gdf1.crs} vs {gdf2.crs}"
    return True, "CRS compatible"


def _get_appropriate_utm_crs(gdf: gpd.GeoDataFrame) -> str:
    """
    Determine appropriate UTM CRS based on dataset centroid.
    
    Returns:
        EPSG code string for appropriate UTM zone
    """
    try:
        # Get centroid of all geometries
        centroid = gdf.geometry.centroid.unary_union.centroid
        lon, lat = centroid.x, centroid.y
        
        # Calculate UTM zone
        utm_zone = int((lon + 180) // 6) + 1
        
        # Northern or Southern hemisphere
        if lat >= 0:
            epsg_code = 32600 + utm_zone  # UTM North
        else:
            epsg_code = 32700 + utm_zone  # UTM South
            
        return f'EPSG:{epsg_code}'
    except Exception:
        return 'EPSG:3857'  # Web Mercator as fallback


def _calculate_geometry_statistics(gdf: gpd.GeoDataFrame) -> Dict[str, Any]:
    """
    Calculate comprehensive geometry statistics.
    
    Returns:
        Dictionary of statistics including counts, areas, lengths
    """
    stats = {
        'feature_count': len(gdf),
        'geometry_types': gdf.geometry.geom_type.value_counts().to_dict()
    }
    
    # Calculate areas for polygons
    if any(gdf.geometry.geom_type.isin(['Polygon', 'MultiPolygon'])):
        stats['total_area'] = gdf.geometry.area.sum()
        stats['mean_area'] = gdf.geometry.area.mean()
    
    # Calculate lengths for lines
    if any(gdf.geometry.geom_type.isin(['LineString', 'MultiLineString'])):
        stats['total_length'] = gdf.geometry.length.sum()
        stats['mean_length'] = gdf.geometry.length.mean()
    
    return stats
