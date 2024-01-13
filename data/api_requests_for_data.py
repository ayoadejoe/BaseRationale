import requests
import json
import pandas as pd

# API endpoint URL where the database is located
url = 'https://www.eucalyptus.iq-joy.com/joseph1/powerdata_api_data.php'

# I make requests via POST; selecting a range of values using the timestamps
payload = {
    'startTimestamp': '2023-08-01 00:00:00',  # time to start picking values
    'endTimestamp': '2023-08-31 23:59:59'  # time to end
}

response = requests.post(url, data=payload)
data = response.json()  # we acquire the data from the database

# then we load data into panda for cleaning
df = pd.DataFrame(data)

# we start cleaning
# first we sum up all the current flow, voltage and power consumed in the grid
df['Total Current'] = df['Current1'] + df['Current2'] + df['Current3']
df['Total Voltage'] = (df['Voltage1'] + df['Voltage2'] + df['Voltage3']) / 3
df['Total Power'] = df['Power1'] + df['Power2'] + df['Power3']


initialEnergy = df['Energy1'].iloc[0] + df['Energy2'].iloc[0] + df['Energy3'].iloc[0]
finalEnergy = df['Energy1'].iloc[-1] + df['Energy2'].iloc[-1] + df['Energy3'].iloc[-1]
energyConsumed = finalEnergy - initialEnergy
print("energy consumed: " + str(energyConsumed))


# next, we work on the energy
df['Energy1_diff'] = df['Energy1'].diff().fillna(df['Energy1'].iloc[0])
df['Energy2_diff'] = df['Energy2'].diff().fillna(df['Energy2'].iloc[0])
df['Energy3_diff'] = df['Energy3'].diff().fillna(df['Energy3'].iloc[0])
# then sum it up
df['Total Energy'] = df['Energy1_diff'] + df['Energy2_diff'] + df['Energy3_diff']

# finally the cleaned data
df['Total Energy'].iloc[0] = 0  # first row should be zero
df_cleaned = df[['Time', 'Total Current', 'Total Voltage', 'Total Power', 'Total Energy']]

# Print the first 10 rows
for row in df_cleaned[:10]:
    print(row)

# save in a csv file (optional)
df_cleaned.to_csv('../data/temp.csv', index=False)

