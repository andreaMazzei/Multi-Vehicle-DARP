import pandas as pd
import haversine as hs

# service_time = timedelta(minutes=1)
# max_ride_time_client = timedelta(minutes=30)
service_time = 1 # Minutes
max_ride_time_client = 30 # Minutes

def center_of_gravity(filenames):

  # Combine latitude and longitude data from all files
  combined_latitudes = pd.Series([])
  combined_longitudes = pd.Series([])

  for filename in filenames:
      data = pd.read_csv(filename)
      combined_latitudes = pd.concat([combined_latitudes, data['latitude']])
      combined_longitudes = pd.concat([combined_longitudes, data['longitude']])

  # Calculate the center of gravity
  latitude_cg = combined_latitudes.mean()
  longitude_cg = combined_longitudes.mean()

  # Create DataFrame
  ids = ["Source", "Sink"]
  df = pd.DataFrame({'id': ids, 'latitude': latitude_cg, 'longitude': longitude_cg})
  df.to_csv('Dataset/depots.csv', index=False)

  return df

# Read pickup_points and delivery_points csv file
pickup_points_df = pd.read_csv("Dataset/pickup_points.csv")
delivery_points_df = pd.read_csv("Dataset/delivery_points.csv")

# Imposing starting depot position = ending depot position = center of gravity of all points
filenames = ["Dataset/pickup_points.csv", "Dataset/delivery_points.csv"]
depots_df = center_of_gravity(filenames)

# Read vehicles csv file
vehicles_df = pd.read_csv("Dataset/vehicles.csv")

# List of ids of pickup points, delivery points, depots and vehicles
pickup_points = pickup_points_df['id'].tolist()
delivery_points = delivery_points_df['id'].tolist()
depots = depots_df['id'].tolist()
vehicles = vehicles_df['id'].tolist()

# Create a dictionary of demands of points
# Pickup points --> +1, Delivery points --> -1, Depots --> 0
demand = {}
for point in pickup_points:
    demand[point] = 1
for point in delivery_points:
    demand[point] = -1
for point in depots:
    demand[point] = 0

set1 = pickup_points + delivery_points
set1.append(depots[0])
set2 = pickup_points + delivery_points
set2.append(depots[1])
all_points_df = pd.concat([pickup_points_df, delivery_points_df, depots_df])
all_points = all_points_df['id'].tolist()


# Create a dictionary of distances (in Km) between points
distance = {}
for point1 in set1:
    for point2 in set2:
        if point1 != point2:
            pickup_df = all_points_df.loc[all_points_df['id'] == point1, ['latitude', 'longitude']]
            delivery_df = all_points_df.loc[all_points_df['id'] == point2, ['latitude', 'longitude']]

            latitude1 = pickup_df['latitude'].values[0]
            longitude1 = pickup_df['longitude'].values[0]
            latitude2 = delivery_df['latitude'].values[0]
            longitude2 = delivery_df['longitude'].values[0]

            d = hs.haversine((latitude1, longitude1), (latitude2, longitude2))
            distance[point1, point2] = d

# Creating a dictionary of costs of going from pickup point i to delivery point j using vehicle k
# For the moment cost is equal for every
cost = {}
for vehicle in vehicles:
    for (pickup_point, delivery_point), dist in distance.items():
        cost[pickup_point, delivery_point, vehicle] = dist

print("Demands: ",demand)
print("Distances: ", distance)
print("Costs: ", cost)

