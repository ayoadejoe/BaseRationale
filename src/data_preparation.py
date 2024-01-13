import pandas as pd
import statsmodels.api as sm

class DataCleaning:

    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def detect_outliers(self):
        # Calculate the differences in accumulated energy
        self.df['Energy_Diff'] = self.df['Accumulated Energy'].diff()

        # Calculate mean and standard deviation of the differences
        mean_diff = self.df['Energy_Diff'].mean()
        std_diff = self.df['Energy_Diff'].std()

        # Identify spikes that are, for instance, beyond 3 standard deviations from the mean
        outlier_mask = abs(self.df['Energy_Diff']) > mean_diff + 4 * std_diff

        # Print these outliers along with their datetime
        outliers = self.df[outlier_mask]
        if not outliers.empty:
            print("Detected Outliers:")
            print(outliers[['Time', 'Energy_Diff']])
        else:
            print("No significant outliers detected.")

        outliers[['Time', 'Energy_Diff']].to_csv('../data/outliers.csv', index=False)


    def clean_data(self):
        # Detect and replace simple outliers or null values for each column
        for column in self.df.columns:
            if (column != 'Time') and (column != 'DeviceID') and (column != 'Data'):  # Skip the 'Time' column
                mean = self.df[column].mean()
                std = self.df[column].std()

                # Identify outliers using the 2-standard deviation rule
                mask = (self.df[column] < (mean - 2 * std)) | (self.df[column] > (mean + 2 * std))

                # Replace outliers with the column mean
                self.df[column][mask] = mean

        # Current, Voltage, Power calculations
        self.df['Total Current'] = self.df['Current1'] + self.df['Current2'] + self.df['Current3']
        self.df['Total Voltage'] = (self.df['Voltage1'] + self.df['Voltage2'] + self.df['Voltage3']) / 3
        self.df['Total Power'] = self.df['Power1'] + self.df['Power2'] + self.df['Power3']
        self.df['Power Factor'] = (self.df['PowerFactor1'] + self.df['PowerFactor2'] + self.df['PowerFactor3'])/3

        # Energy calculations
        self.df['Accumulated Energy'] = (self.df['Energy1'] - self.df['Energy1'].iloc[0]) + \
                                        (self.df['Energy2'] - self.df['Energy2'].iloc[0]) + \
                                        (self.df['Energy3'] - self.df['Energy3'].iloc[0])
        self.df['Energy1_diff'] = self.df['Energy1'].diff().fillna(self.df['Energy1'].iloc[0])
        self.df['Energy2_diff'] = self.df['Energy2'].diff().fillna(self.df['Energy2'].iloc[0])
        self.df['Energy3_diff'] = self.df['Energy3'].diff().fillna(self.df['Energy3'].iloc[0])

        self.df['Total Energy'] = self.df['Energy1_diff'] + self.df['Energy2_diff'] + self.df['Energy3_diff']

        self.df['Total Energy'].iloc[0] = 0

        initialEnergy = self.df['Energy1'].iloc[0] + self.df['Energy2'].iloc[0] + self.df['Energy3'].iloc[0]
        finalEnergy = self.df['Energy1'].iloc[-1] + self.df['Energy2'].iloc[-1] + self.df['Energy3'].iloc[-1]
        energyConsumed = finalEnergy - initialEnergy
        print("energy consumed:", energyConsumed)

        # Extract relevant columns
        df_cleaned = self.df[
            ['Time', 'Total Current', 'Total Voltage', 'Total Power', 'Power Factor', 'Total Energy', 'Accumulated Energy']]

        return df_cleaned

    def consolidate_to_daily_readings(self, cleandf):

        # first, I convert String 'Time' column to datetime format
        cleandf['Time'] = pd.to_datetime(cleandf['Time'])

        # then set 'Time' column as the index
        cleandf.set_index('Time', inplace=True)

        daily_sum = cleandf[['Total Current', 'Total Power', 'Total Energy', 'Accumulated Energy']].resample('D').sum()

        # Take average for the columns that require average for the day
        daily_avg = cleandf[['Total Voltage', 'Power Factor']].resample('D').mean()

        # Concatenate both dataframes
        daily_data = pd.concat([daily_sum, daily_avg], axis=1)

        # Save to CSV
        daily_data.reset_index(inplace=True)

        return daily_data

    def save_to_csv(self, path):
        self.df.to_csv(path, index=False)
