#Cleaning, manipulating, and visulizing data from a csv for the optimization model
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('TkAgg')

df = pd.read_csv('/Users/owencooper/PycharmProjects/EnergyAnalysis/MER_T01_01.csv')

print(df.head())

df.rename(columns={'Description': 'Energy Type'}, inplace=True)
df.rename(columns={'YYYYMM': 'Year/Month'}, inplace=True)

df['Year'] = df['Year/Month'].astype(str).str[:4].astype(int)

plt.figure(figsize=(10,6))
for key, grp in df.groupby('Energy Type'):
    plt.plot(grp.Year, grp.Value, label=key)

plt.title('Fossil Fuels Production Over Time')
plt.xlabel('Year')
plt.ylabel('Value (Quadrillion Btu)')
plt.legend(title='Type')
plt.grid(True)
plt.tight_layout()
plt.show()