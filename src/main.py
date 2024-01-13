import os
import pandas as pd
import statsmodels.api as sm

from scipy import stats
from api_calls import APICall
from data_preparation import DataCleaning
from statistical_analysis import StatisticalAnalysis

csv_file_path = '../data/temp_december.csv'

# Check if the cleaned data CSV file exists, if not get it from online database
if not os.path.exists(csv_file_path):
    # If not, fetch data from the API
    print('calling online')
    api = APICall('https://www.eucalyptus.iq-joy.com/joseph1/powerdata_api_data.php')
    data = api.fetch_data('2023-12-01 00:00:00', '2023-12-31 23:59:59')

    # Clean the fetched data
    cleaner = DataCleaning(data)
    cleaner.save_to_csv(csv_file_path)
    df_cleaned = cleaner.clean_data()
    cleaner.detect_outliers()

    print(df_cleaned.head(10))
    df_cleaned.to_csv('../data/cleaned_temp.csv', index=False)

    #
else:
    # load it
    data = pd.read_csv(csv_file_path)
    # Clean the fetched data again in case of adjustments
    cleaner = DataCleaning(data)
    df_cleaned = cleaner.clean_data()
    cleaner.detect_outliers()
    df_cleaned.to_csv('../data/cleaned_temp.csv', index=False)
    print(df_cleaned.head(10))

# Energy consumption readings for August to November
data = {
    "Commercial Power Energy Consumed": [10838, 11738, 11622, 10697],
    "SPAD Energy Consumed": [11022.3, 11622.77, 12017.52, 10763.4]
}

# Create a DataFrame
df2 = pd.DataFrame(data)

# Perform a paired t-test
t_stat, p_value = stats.ttest_rel(df2['Commercial Power Energy Consumed'], df2['SPAD Energy Consumed'])

print("T-statistic:", t_stat)
print("P-value:", p_value)

cleandf = pd.read_csv('../data/final_cleaned_temp.csv')

X = cleandf[['Total Power', 'Total Voltage', 'Total Current', 'Power Factor']]  # Independent variables
X = sm.add_constant(X)
y = cleandf['Accumulated Energy']  # Dependent variable

model = sm.OLS(y, X).fit()  # Fit the regression model
print(model.summary())

# prepare the daily readings
cleaner = DataCleaning(cleandf)
daily_data = cleaner.consolidate_to_daily_readings(cleandf)
print(daily_data.head(10))
daily_data.to_csv('../data/daily_log.csv', index=False)

# Proceed with statistical analysis
stats = StatisticalAnalysis(df_cleaned)
# stats.plot_grid_consumption_rate(df_cleaned)  # assuming you've added this method in your StatisticalAnalysis class
# stats.plot_grid_consumption_rate(df_cleaned)
# stats.plot_acummulated_consumption_rate(df_cleaned)
# stats.plot_consumption(df_cleaned)
