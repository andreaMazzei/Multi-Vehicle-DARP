import random
import pandas as pd
import instance_data as data

num_points, min_longitude, max_longitude, min_latitude, max_latitude = data.num_points, data.min_longitude, data.max_longitude, data.min_latitude, data.max_latitude
def generate_pickup_points(num_points, min_lat, max_lat, min_long, max_long):

    # Generate random coordinates
    latitudes = [random.uniform(min_lat, max_lat) for _ in range(num_points)]
    longitudes = [random.uniform(min_long, max_long) for _ in range(num_points)]

    # Assign IDs
    ids = list(range(1, num_points + 1))

    # Create DataFrame
    df = pd.DataFrame({'id': ids, 'latitude': latitudes, 'longitude': longitudes})
    df.to_csv('pickup_points.csv', index=False)
    return df

def generate_delivery_points(num_points, min_lat, max_lat, min_long, max_long):

    # Generate random coordinates
    latitudes = [random.uniform(min_lat, max_lat) for _ in range(num_points)]
    longitudes = [random.uniform(min_long, max_long) for _ in range(num_points)]

    # Assign IDs
    ids = list(range(num_points + 1, 2*num_points + 1))

    # Create DataFrame
    df = pd.DataFrame({'id': ids, 'latitude': latitudes, 'longitude': longitudes})
    df.to_csv('delivery_points.csv', index=False)
    return df

generate_pickup_points(num_points, min_latitude, max_latitude, min_longitude, max_longitude)
generate_delivery_points(num_points, min_latitude, max_latitude, min_longitude, max_longitude)
