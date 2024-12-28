
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

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
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

# Extract data from JSON
if "response" in data and "data" in data["response"]:
    records = data["response"]["data"]
    df = pd.DataFrame(records)
    print(df.head())  # Display the first few rows
else:
    print("Unexpected data format.")

    # Convert 'period' to datetime if it's a time-related column
if "period" in df.columns:
    df["period"] = pd.to_datetime(df["period"])

# Plot the data
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Drop rows with NaN in the 'value' column if necessary
df = df.dropna(subset=['value'])

# Ensure the values are integers for range()
df['value'] = df['value'].astype(int)

# Plotting
plt.figure(figsize=(10, 6))
sns.lineplot(x="period", y="value", data=df)
plt.title("Value Over Time")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)

# Reduce the number of y-axis ticks
plt.yticks(ticks=range(0, df["value"].max() + 1, 200))  # Adjust step size as needed

plt.show()

