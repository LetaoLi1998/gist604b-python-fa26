"""
Pandas Basics for GIS Data Analysis - Student Implementation

Complete the four functions in this file.
Use the notebooks to learn and test each function.

📋 FUNCTIONS TO IMPLEMENT IN THIS FILE:
=====================================
✅ Function 1: load_and_explore_gis_data()     → notebooks/01_function_...
✅ Function 2: filter_environmental_data()     → notebooks/02_function_...
✅ Function 3: calculate_station_statistics()  → notebooks/03_function_...
✅ Function 4: join_station_data()             → notebooks/04_function_...
"""

import pandas as pd
from pathlib import Path
import os


# =============================================================================
# FUNCTION 1: LOAD AND EXPLORE GIS DATA
# =============================================================================

def load_and_explore_gis_data(file_path):
    """
    Load a CSV file and display comprehensive information about the dataset.
    
    This function demonstrates the first step in any data analysis project:
    understanding your data through exploration.
    
    Args:
        file_path (str): Path to the CSV file to load
        
    Returns:
        pandas.DataFrame: The loaded dataset, or None if loading failed
    
    Example:
        >>> stations_df = load_and_explore_gis_data('data/weather_stations.csv')
        Loading data from: data/weather_stations.csv
        Dataset shape: (150, 6) - That's 150 rows and 6 columns!
        ...
    """
    
    # TODO: Print a header to show what function is running
    # TODO: Use print("=" * 50) and print("LOADING AND EXPLORING GIS DATA")
    
    # TODO: Print the file path being loaded
    # TODO: Use print(f"Loading data from: {file_path}")
    
    # TODO: Try to load the CSV file using pd.read_csv()
    # TODO: Wrap in try/except to handle missing files gracefully
    # TODO: If file doesn't exist, print error and return None
    
    # TODO: Print the shape of the DataFrame (rows, columns)
    # TODO: Use df.shape to get a tuple like (150, 6)
    # TODO: Print it in a friendly way: "Dataset shape: (150, 6) - That's 150 rows and 6 columns!"
    
    # TODO: Print the column names
    # TODO: Use df.columns to get the list
    # TODO: Print: "Columns: ['station_id', 'name', 'latitude', ...]"
    
    # TODO: Print the first few rows using df.head()
    # TODO: Show this to help understand the data
    
    # TODO: Print basic statistics using df.describe()
    # TODO: This shows min, max, mean for numeric columns
    
    # TODO: Check for missing values using df.isnull().sum()
    # TODO: Print how many missing values in each column
    
    # TODO: Print a completion message
    
    # TODO: Return the loaded DataFrame
    
    print("=" * 50)
    print("LOADING AND EXPLORING GIS DATA")
    print("=" * 50)

    print(f"Loading data from: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nSummary statistics:")
    print(df.describe())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nData exploration complete!")

    return df


# =============================================================================
# FUNCTION 2: FILTER ENVIRONMENTAL DATA
# =============================================================================

def filter_environmental_data(df, min_temp=15, max_temp=30, quality="good"):
    """
    Filter environmental data based on temperature range and data quality.
    
    This function demonstrates how to apply multiple filtering conditions
    to clean and prepare environmental data for analysis.
    
    Args:
        df (pandas.DataFrame): Environmental data with temperature and quality columns
        min_temp (float): Minimum acceptable temperature in Celsius (default: 15)
        max_temp (float): Maximum acceptable temperature in Celsius (default: 30)
        quality (str): Required data quality level (default: "good")
        
    Returns:
        pandas.DataFrame: Filtered data meeting all specified conditions
    
    Example:
        >>> filtered_df = filter_environmental_data(readings_df, min_temp=20, max_temp=30, quality='good')
        Original data: 1000 rows
        After filtering: 247 rows (24.7% of data retained)
        Filters applied:
          - Temperature: 20.0°C to 30.0°C
          - Data quality: good
    """
    
    # TODO: Print a header
    # TODO: Use print("=" * 50) and print("FILTERING ENVIRONMENTAL DATA")
    
    # TODO: Print the original DataFrame shape
    # TODO: Use len(df) to get the number of rows
    
    # TODO: Filter by temperature range using boolean indexing
    # TODO: Create a mask: (df['temperature_c'] >= min_temp) & (df['temperature_c'] <= max_temp)
    # TODO: Apply the mask: filtered_df = df[mask]
    
    # TODO: Filter by data quality
    # TODO: Add another condition: filtered_df = filtered_df[filtered_df['data_quality'] == quality]
    
    # TODO: Calculate and print filtering statistics
    # TODO: - How many rows remain after filtering
    # TODO: - What percentage of data was retained
    # TODO: - Show the filter criteria used
    
    # TODO: Return the filtered DataFrame
    
    print("=" * 50)
    print("FILTERING ENVIRONMENTAL DATA")
    print("=" * 50)

    if df is None or df.empty:
        print("ERROR: Empty or None DataFrame provided")
        return pd.DataFrame()

    required_columns = ['temperature_c', 'data_quality']
    for col in required_columns:
        if col not in df.columns:
            print(f"ERROR: Missing required column: {col}")
            return pd.DataFrame()

    original_count = len(df)

    mask = (
        (df['temperature_c'] >= min_temp) &
        (df['temperature_c'] <= max_temp)
    )

    filtered_df = df[mask]
    filtered_df = filtered_df[
        filtered_df['data_quality'] == quality
    ].copy()

    filtered_count = len(filtered_df)
    removed_count = original_count - filtered_count
    retained_percent = (filtered_count / original_count) * 100

    print(f"Original rows: {original_count}")
    print(f"Filtered rows: {filtered_count}")
    print(f"Removed rows: {removed_count}")
    print(f"Retained: {retained_percent:.1f}%")
    print(f"Temperature range: {min_temp} to {max_temp} °C")
    print(f"Data quality: {quality}")
    print("Filtering complete!")

    return filtered_df


# =============================================================================
# FUNCTION 3: CALCULATE STATION STATISTICS
# =============================================================================

def calculate_station_statistics(df):
    """
    Calculate station statistics
    
    This function groups temperature readings by weather station and calculates
    summary statistics (average temperature, number of readings, etc.) for each
    station.
    
    Args:
        df (pandas.DataFrame): Environmental readings data with 'station_id', 'temperature_c' and 'humidity_percent' columns
    
    Returns:
        pandas.DataFrame: Statistics for each station with columns:
            - station_id: The weather station identifier
            - avg_temperature: Average temperature for this station
            - avg_humidity: Average humidity for this station
            - reading_count: Number of readings from this station
    
    Example:
        >>> stats_df = calculate_station_statistics(readings_df)
        Calculating statistics for 5 unique stations...
        Statistics calculated:
          - Total readings analyzed: 1000
          - Stations with data: 5
          - Average readings per station: 200.0
    """
    
    # TODO: Print a header
    # TODO: Use print("=" * 50) and print("CALCULATING STATION STATISTICS")
    
    # TODO: Count unique stations
    # TODO: Use df['station_id'].nunique()
    
    # TODO: Group by station_id
    # TODO: Use df.groupby('station_id')
    
    # TODO: Calculate statistics for each group
    # TODO: - Count of readings: use .size() or .count()
    # TODO: - Average temperature: use .mean()
    # TODO: Create a new DataFrame with these statistics
    
    # TODO: Reset the index to make station_id a regular column
    # TODO: Use .reset_index()
  
    
    # TODO: Rename columns to be clear
    # TODO: Use .rename(columns={'temperature_c': 'avg_temperature', ...})
    
    # TODO: Print summary statistics
    # TODO: - Total readings analyzed
    # TODO: - Number of stations
    # TODO: - Average readings per station
    
    # TODO: Return the statistics DataFrame
    

    print("=" * 50)
    print("CALCULATING STATION STATISTICS")
    print("=" * 50)

    if df is None or df.empty:
        print("ERROR: DataFrame is empty or None")
        return pd.DataFrame()

    required_columns = ['station_id', 'temperature_c', 'humidity_percent']
    for col in required_columns:
        if col not in df.columns:
            print(f"ERROR: Missing required column: {col}")
            return pd.DataFrame()

    station_count = df['station_id'].nunique()
    print(f"Calculating statistics for {station_count} unique stations...")

    stats_df = df.groupby('station_id').agg(
        avg_temperature=('temperature_c', 'mean'),
        avg_humidity=('humidity_percent', 'mean'),
        reading_count=('temperature_c', 'size')
    ).reset_index()
    stats_df['avg_temperature'] = stats_df['avg_temperature'].round(1)
    stats_df['avg_humidity'] = stats_df['avg_humidity'].round(1)

    print("\nStatistics calculated:")
    print(f"Total readings analyzed: {len(df)}")
    print(f"Stations with data: {station_count}")
    print(f"Average readings per station: {len(df) / station_count:.1f}")

    return stats_df



# =============================================================================
# FUNCTION 4: JOIN STATION DATA
# =============================================================================

def join_station_data(stations_df, readings_df):
    """
    Join sensor readings with station metadata
    
    This function joins station information (name, location) with temperature readings.
    You'll add station details (like station name and coordinates) to each temperature reading.
    
    Args:
        stations_df (pandas.DataFrame): Station information with 'station_id', 'station_name', 
                                       'latitude', 'longitude', etc.
        readings_df (pandas.DataFrame): Temperature readings with 'station_id', 'date', 
                                       'temperature_c', etc.
    
    Returns:
        pandas.DataFrame: Combined dataset with readings AND station information
    
    Example:
        >>> joined_df = join_station_data(stations_df, readings_df)
        Joining station information with readings...
        Stations table: 5 stations
        Readings table: 1000 readings
        Joined table: 1000 rows with station details added!
    """
    
    # TODO: Print a header
    # TODO: Use print("=" * 50) and print("JOINING STATION DATA")
    
    # TODO: Print the shapes of both input DataFrames
    # TODO: Show how many stations and how many readings
    
    # TODO: Join the DataFrames using pd.merge()
    # TODO: Use the 'station_id' column as the key
    # TODO: Use how='left' to keep all readings even if station info is missing
    
    # TODO: Print the shape of the joined DataFrame
    # TODO: Verify all readings are still present
    
    # TODO: Print the new columns that were added
    # TODO: Show which columns came from the stations table
    
    # TODO: Return the joined DataFrame
    
    print("=" * 50)
    print("JOINING STATION DATA")
    print("=" * 50)

    if stations_df is None or stations_df.empty:
        print("ERROR: Stations DataFrame is empty or None")
        return pd.DataFrame()

    if readings_df is None or readings_df.empty:
        print("ERROR: Readings DataFrame is empty or None")
        return pd.DataFrame()

    if 'station_id' not in stations_df.columns:
        print("ERROR: 'station_id' column missing from stations data")
        return pd.DataFrame()

    if 'station_id' not in readings_df.columns:
        print("ERROR: 'station_id' column missing from readings data")
        return pd.DataFrame()

    print(f"Stations table: {len(stations_df)} stations")
    print(f"Readings table: {len(readings_df)} readings")

    joined_df = pd.merge(
        readings_df,
        stations_df,
        on='station_id',
        how='left'
    )

    print(f"Joined table: {len(joined_df)} rows")
    print(f"All readings preserved: {len(joined_df) == len(readings_df)}")

    new_columns = [col for col in joined_df.columns if col not in readings_df.columns]
    print(f"New columns added: {new_columns}")

    return joined_df


# =============================================================================
# HELPER FUNCTIONS (You don't need to modify these - they're provided!)
# =============================================================================

def _check_required_columns(df, required_columns, data_name="DataFrame"):
    """
    Helper function to check if required columns exist in a DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame to check
        required_columns (list): List of required column names
        data_name (str): Name to use in error messages
    
    Returns:
        tuple: (bool, list) - (all_present, missing_columns)
    """
    if df is None or df.empty:
        return False, required_columns
    
    missing = [col for col in required_columns if col not in df.columns]
    return len(missing) == 0, missing


def _format_number(value, decimals=1):
    """
    Helper function to format numbers for display.
    
    Args:
        value: Number to format
        decimals (int): Number of decimal places
    
    Returns:
        str: Formatted number
    """
    try:
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)
