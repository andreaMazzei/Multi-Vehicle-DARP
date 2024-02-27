import plotly.express as px
import pandas as pd

# Load datasets
pickup_points = pd.read_csv("../Dataset/pickup_points.csv")
delivery_points = pd.read_csv("../Dataset/delivery_points.csv")

# Create a scattermapbox plot with pickup points
fig = px.scatter_mapbox(pickup_points, lat="latitude", lon="longitude", zoom=10,
                        color_discrete_sequence=['blue'], hover_data=['id'])

# Add delivery points to the same map
fig.add_trace(
    px.scatter_mapbox(delivery_points, lat="latitude", lon="longitude",
                      color_discrete_sequence=['red'], hover_data=['id']).data[0]
)

# Customize with Plotly options (optional)
fig.update_layout(mapbox_style="open-street-map")

# Display the map
fig.show()
