import matplotlib
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

url = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"
api_key = "T47FXGoDVqUOnp6q6kERYUBJudjuOIY2ywQdkLy1"

params = {
    "api_key": api_key,
    "frequency": "hourly",
    "data[0]": "value",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000,
    "facets[respondent][]": "ALL",
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

if "response" in data and "data" in data["response"]:
    records = data["response"]["data"]
    df = pd.DataFrame(records)
    print(df.head())
else:
    print("Unexpected data format.")


if "period" in df.columns:
    df["period"] = pd.to_datetime(df["period"])

df['value'] = pd.to_numeric(df['value'], errors='coerce')
df = df.dropna(subset=['value'])
df['value'] = df['value'].astype(int)

# Group data by respondent-name (state)
df_grouped = df.groupby('respondent-name')['value'].mean().reset_index()
print(df['respondent'].unique())  # List unique state or region codes

print(df_grouped)

shapefile_path = "/Users/owencooper/downloads/ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"  # Update this path
us_map = gpd.read_file(shapefile_path)

# Filter for US states only
us_map = us_map[us_map['admin'] == 'United States of America']

# Map state names to respondent-name
state_mapping = {
    # Add mappings if necessary to match respondent-name to state names in the shapefile
    "California": "California",
    # Add other mappings here if needed
}

df_grouped['state_name'] = df_grouped['respondent-name'].map(state_mapping)

# Merge the data with the US map
us_map = us_map.set_index('name').join(df_grouped.set_index('state_name'))

# Plot the heatmap
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
us_map.plot(column='value', ax=ax, legend=True,
            legend_kwds={'label': "Average Value by State",
                         'orientation': "horizontal"})
plt.title("Heatmap of Energy Values by State")

plt.show()
