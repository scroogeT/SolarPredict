import pandas as pd

# Load all datasets
df = pd.read_csv('Type1 Data.xlsx_flattened.csv')
df2 = pd.read_csv('Type2 Data.xlsx_flattened.csv')
df4 = pd.read_csv('Type 4 Data.xlsx_flattened.csv')

# Combine All flattened datasets into one Dataframe
df = df.append(df2).append(df4)

# Delete any rows with missing values
df = df.dropna()

df.to_csv('flattened_data.csv', index=False)

print(df.shape)
print(df.head())

dropIndexes = []

# 1. Remove Night-time readings
for index, row in df.iterrows():
    if row['SolIrr'] < 2 or row['Pdc'] < 1:
        # Mark index to be dropped
        dropIndexes.append(index)

# Delete Night-time data or with zero DC-Voltages
df = df.drop(dropIndexes)

print(df.count())

# Save dataframe ready to be fed into Machine Learning model
df.to_csv('daytime_readings.csv', index=False)
