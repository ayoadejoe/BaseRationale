import os
import pandas as pd
import numpy as np
import statsmodels.api as sm

from api_calls import APICall
from data_preparation import DataCleaning
from statistical_analysis import StatisticalAnalysis

new_data = '../data/EmailSurvey.xlsx'
csv_file_path = '../data/ReClean.xlsx'

# Check if the cleaned data CSV file exists, if not get it from online database
if not os.path.exists(csv_file_path):

    # Attempting to load the file
    try:
        df2 = pd.read_excel(new_data)
        message_2 = "File loaded successfully. No immediate errors detected."
    except Exception as e:
        message_2 = str(e)

        # Clean the fetched data
        cleaner = DataCleaning(new_data)
        #cleaner.save_to_csv(csv_file_path)
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


demographic_columns = pd.read_csv('../data/final_cleaned_temp.csv')

# Counting unique values and identifying empty or incorrect data in each demographic category

# Function to count unique values and identify empty or incorrect data
def analyze_demographic_data(column):
    unique_values = df2[column].nunique()
    empty_or_wrong_data = df2[column].isna().sum() + df2[df2[column].astype(str).str.strip() == ''].shape[0]
    return unique_values, empty_or_wrong_data

# Analyzing each demographic category
demographic_analysis = {col: analyze_demographic_data(col) for col in demographic_columns}
demographic_analysis_result = {
    col: {
        'Unique Values': result[0],
        'Empty or Incorrect Data': result[1]
    } for col, result in demographic_analysis.items()
}

demographic_analysis_result

# Updating the dataset based on the provided instructions

# Updating gender: Replacing empty or unrecognized entries with 'Non-binary'
df2['(4) Please indicate your gender'].fillna('Non-binary', inplace=True)
df2.loc[df2['(4) Please indicate your gender'].astype(str).str.strip() == '', '(4) Please indicate your gender'] = 'Non-binary'

# Updating age group: Replacing empty or unrecognized entries with 'Age-less'
df2['(3) Please indicate your age group'].fillna('Age-less', inplace=True)
df2.loc[df2['(3) Please indicate your age group'].astype(str).str.strip() == '', '(3) Please indicate your age group'] = 'Age-less'

# Counting the updated unique values for each demographic category
updated_demographics = {
    col: df2[col].value_counts() for col in demographic_columns
}

updated_demographics


# Saving the updated DataFrame to a new Excel file
updated_file_path = '../data/Clean_Updated.xlsx'
df2.to_excel(updated_file_path, index=False)

updated_file_path


# Creating separate Excel files for each demographic category


# Reload the dataset
file_path_2 = '../data/Clean.xlsx'
df2 = pd.read_excel(file_path_2)

# Columns for each demographic category
demographic_cols = {
    'College': '(1) Please select your College',
    'Employment': '(2) Please select the category that best represents your employment',
    'Age_Group': '(3) Please indicate your age group',
    'Gender': '(4) Please indicate your gender'
}

# Filtering and saving datasets for each demographic analysis
analysis_file_paths = {}

for demo_name, demo_col in demographic_cols.items():
    # Exclude other demographic columns
    cols_to_exclude = set(demographic_cols.values()) - {demo_col}
    filtered_data = df2.drop(columns=cols_to_exclude)

    # File path for the new Excel file
    file_path = f'../data/Analysis_{demo_name}.xlsx'
    analysis_file_paths[demo_name] = file_path

    # Save the dataset
    filtered_data.to_excel(file_path, index=False)

analysis_file_paths



# Count the frequency of responses in each relevant column
columns_of_interest = [
    '(19) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Innapropriate content]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Agressive tone]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Bullying]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Content you found offensive]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Sent by the sender to avoid face to face contact]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Poorly written]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Hastily composed without due consideration]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [Content that is not relevant to you]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [The same message containing the same content from multiple sources]',
    '(19 answer) Without naming specific individuals, please identify if you have ever received emails from colleagues or managers in your College that you would consider to be: [None of the above]'
]

# Initialize a dictionary to hold frequency counts
frequency_counts = {}

# Loop through each column and count the frequencies
for column in columns_of_interest:
    frequency_counts[column] = df2[column].fillna('No value').value_counts().to_dict()

frequency_counts


# Calculating the percentage of each response type
total_responses = 1010  # Total number of responses

# Calculate percentages
percentages = {}
for column, counts in {**frequency_counts}.items():
    percentages[column] = {response: (count / total_responses) * 100 for response, count in counts.items()}

percentages


# Column to find
column_to_find = "(22) Have you attended training on the use of email in the past 12 months?"

# Try reading the Excel file and checking for the column
try:
    df_new = pd.read_excel(file_path_2)
    column_exists_new = column_to_find in df_new.columns
except Exception as e:
    column_exists_new = False
    error_message_new = str(e)

column_exists_new if column_exists_new else error_message_new

# Counting the frequency of responses in the specified column, treating empty cells as 'No value'
frequency_column_22 = df_new[column_to_find].fillna('No value').value_counts().to_dict()
frequency_column_22

# Load the Excel file and calculate the percentages
df_new = pd.read_excel(file_path_2)
frequency_column_22 = df_new[column_to_find].fillna('No value').value_counts()
total_responses_22 = frequency_column_22.sum()
percentages_column_22 = (frequency_column_22 / total_responses_22) * 100
percentages_column_22


# Calculating the total number of responders who mentioned at least one issue
# We need to consider if a responder has mentioned any issue across all the identified columns

# Creating a DataFrame with only the identified columns
df_issues = df2[frequency_counts]

# Counting the number of responders who have mentioned at least one issue (excluding 'No value')
total_responders_with_issues = df_issues[df_issues != 'No value'].notna().any(axis=1).sum()
total_responders_with_issues


email_data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
email_data.head()

def parse_average_email_count(email_range):
    """
    Parses the email range string and computes the average.
    Returns 0 for empty or 'no value' entries.
    """
    if pd.isna(email_range) or email_range == 'no value':
        return 0
    try:
        # Split the range and calculate the average
        low, high = map(int, email_range.split('-'))
        return (low + high) / 2
    except ValueError:
        return 0

# Applying the function to the relevant columns
email_data['Average Emails Sent'] = email_data['7 On average how many emails do you send in a day'].apply(parse_average_email_count)
email_data['Average Emails Received'] = email_data['9 On average how many emails do you receive in a day'].apply(parse_average_email_count)

# Calculating the total and average for sent and received emails
total_emails_sent = email_data['Average Emails Sent'].sum()
total_emails_received = email_data['Average Emails Received'].sum()
average_emails_sent = email_data['Average Emails Sent'].mean()
average_emails_received = email_data['Average Emails Received'].mean()

total_emails_sent, total_emails_received, average_emails_sent, average_emails_received


# Re-applying the function to the correct column for emails received
email_data['Average Emails Received'] = email_data['9 On average how many emails do you receive in ...'].apply(parse_average_email_count)

# Recalculating the total and average for sent and received emails
total_emails_sent = email_data['Average Emails Sent'].sum()
total_emails_received = email_data['Average Emails Received'].sum()
average_emails_sent = email_data['Average Emails Sent'].mean()
average_emails_received = email_data['Average Emails Received'].mean()

total_emails_sent, total_emails_received, average_emails_sent, average_emails_received


time_spent_emailing = email_data['11 How much time per day do you spend dealing w...'].unique()
time_spent_emailing

# Re-categorizing the data into the defined time ranges

# Function to categorize time spent on emails
def categorize_time_spent(minutes):
    if minutes <= 30:
        return '0-30 minutes'
    elif minutes <= 60:
        return '31-60 minutes'
    elif minutes <= 120:
        return '61-120 minutes'
    elif minutes <= 180:
        return '121-180 minutes'
    else:
        return 'More than 180 minutes'

# Applying the categorization
email_data['Time Spent Category'] = email_data['11 How much time per day do you spend dealing w...'].apply(categorize_time_spent)

# Counting the number of respondents in each category
time_spent_counts = email_data['Time Spent Category'].value_counts()
time_spent_counts



# Calculating the number of respondents who spend less than 132 minutes on emails
below_average_time = email_data['11 How much time per day do you spend dealing w...'] < 132
count_below_average = below_average_time.sum()

# Calculating the total number of respondents
total_respondents = email_data.shape[0]

# Calculating the percentage
percentage_below_average = (count_below_average / total_respondents) * 100

count_below_average, percentage_below_average


def parse_average_email_count(email_range):
    """
    Parses the email range string and computes the average.
    Returns 0 for empty or 'no value' entries.
    """
    if pd.isna(email_range) or email_range == 'no value':
        return 0
    try:
        # Split the range and calculate the average
        low, high = map(int, email_range.split('-'))
        return (low + high) / 2
    except ValueError:
        return 0

# Applying the function to the relevant columns
email_data['Average Emails Sent'] = email_data['7 On average how many emails do you send in a day'].apply(parse_average_email_count)
email_data['Average Emails Received'] = email_data['9 On average how many emails do you receive in a day'].apply(parse_average_email_count)

# Calculating the total and average for sent and received emails
total_emails_sent = email_data['Average Emails Sent'].sum()
total_emails_received = email_data['Average Emails Received'].sum()
average_emails_sent = email_data['Average Emails Sent'].mean()
average_emails_received = email_data['Average Emails Received'].mean()

total_emails_sent, total_emails_received, average_emails_sent, average_emails_received


# Displaying the column names to identify the correct one
email_data.columns.tolist()

# Re-applying the function to the correct column for emails received
email_data['Average Emails Received'] = email_data['9 On average how many emails do you receive in ...'].apply(parse_average_email_count)

# Recalculating the total and average for sent and received emails
total_emails_sent = email_data['Average Emails Sent'].sum()
total_emails_received = email_data['Average Emails Received'].sum()
average_emails_sent = email_data['Average Emails Sent'].mean()
average_emails_received = email_data['Average Emails Received'].mean()

total_emails_sent, total_emails_received, average_emails_sent, average_emails_received




# Examining the unique values in the specified columns for manageable emails
manageable_sent_emails = email_data['12 In an average work day how many emails do ...'].unique()
manageable_received_emails = email_data['12b In an average day how many emails do y...'].unique()

manageable_sent_emails, manageable_received_emails


# Examining the unique values in the specified columns for manageable emails
manageable_sent_emails = email_data['12 In an average work day how many emails do yo...'].unique()
manageable_received_emails = email_data['12b In an average day how many emails do you be...'].unique()

manageable_sent_emails, manageable_received_emails


# Function to categorize the number of emails
def categorize_email_count(email_count):
    if email_count == 'no value' or pd.isna(email_count):
        return 'No Value'
    elif email_count <= 10:
        return '0-10 emails'
    elif email_count <= 20:
        return '11-20 emails'
    elif email_count <= 50:
        return '21-50 emails'
    elif email_count <= 100:
        return '51-100 emails'
    else:
        return 'More than 100 emails'

# Converting non-numeric values to NaN for proper handling
email_data['12 In an average work day how many emails do yo...'] = pd.to_numeric(email_data['12 In an average work day how many emails do yo...'], errors='coerce')
email_data['12b In an average day how many emails do you be...'] = pd.to_numeric(email_data['12b In an average day how many emails do you be...'], errors='coerce')

# Applying the categorization
email_data['Manageable Emails Sent Category'] = email_data['12 In an average work day how many emails do yo...'].apply(categorize_email_count)
email_data['Manageable Emails Received Category'] = email_data['12b In an average day how many emails do you be...'].apply(categorize_email_count)

# Counting the number of respondents in each category for both sent and received emails
manageable_sent_counts = email_data['Manageable Emails Sent Category'].value_counts()
manageable_received_counts = email_data['Manageable Emails Received Category'].value_counts()

manageable_sent_counts, manageable_received_counts


# Defining midpoints for each category
category_midpoints = {
    '0-10 emails': 5,
    '11-20 emails': 15,
    '21-50 emails': 35,
    '51-100 emails': 75,
    'More than 100 emails': 101
}

# Function to calculate total manageable emails
def calculate_total_manageable_emails(counts):
    total = 0
    for category, count in counts.items():
        if category in category_midpoints:
            total += category_midpoints[category] * count
    return total

# Calculate total manageable emails for sending and receiving
total_manageable_sent = calculate_total_manageable_emails(manageable_sent_counts)
total_manageable_received = calculate_total_manageable_emails(manageable_received_counts)

# Community averages
community_average_sent = 17.4
community_average_received = 23.6

# Internet general averages
internet_average_sent = 40
internet_average_received = 121

# Comparison percentages
comparison_sent_community = (total_manageable_sent / community_average_sent) * 100
comparison_received_community = (total_manageable_received / community_average_received) * 100

comparison_sent_internet = (total_manageable_sent / internet_average_sent) * 100
comparison_received_internet = (total_manageable_received / internet_average_received) * 100

total_manageable_sent, total_manageable_received, \
comparison_sent_community, comparison_received_community, \
comparison_sent_internet, comparison_received_internet

# Calculating the total number of respondents
total_respondents = email_data.shape[0]


# Handling 'no value' and NaN by treating them as 0
email_data['12 In an average work day how many emails do yo...'] = email_data['12 In an average work day how many emails do yo...'].fillna(0)
email_data['12b In an average day how many emails do you be...'] = email_data['12b In an average day how many emails do you be...'].fillna(0)

# Calculating the direct sum of manageable emails to send and receive
direct_total_manageable_sent = email_data['12 In an average work day how many emails do yo...'].sum()
direct_total_manageable_received = email_data['12b In an average day how many emails do you be...'].sum()

# Comparison percentages with community and internet averages
direct_comparison_sent_community = (direct_total_manageable_sent / community_average_sent) * 100
direct_comparison_received_community = (direct_total_manageable_received / community_average_received) * 100

direct_comparison_sent_internet = (direct_total_manageable_sent / internet_average_sent) * 100
direct_comparison_received_internet = (direct_total_manageable_received / internet_average_received) * 100

direct_total_manageable_sent, direct_total_manageable_received, \
direct_comparison_sent_community, direct_comparison_received_community, \
direct_comparison_sent_internet, direct_comparison_received_internet


# Recalculating the mean (average) number of manageable emails sent and received per respondent
mean_manageable_sent = direct_total_manageable_sent / total_respondents
mean_manageable_received = direct_total_manageable_received / total_respondents

# Comparison percentages with community and internet averages
mean_comparison_sent_community = (mean_manageable_sent / community_average_sent) * 100
mean_comparison_received_community = (mean_manageable_received / community_average_received) * 100

mean_comparison_sent_internet = (mean_manageable_sent / internet_average_sent) * 100
mean_comparison_received_internet = (mean_manageable_received / internet_average_received) * 100

mean_manageable_sent, mean_manageable_received, \
mean_comparison_sent_community, mean_comparison_received_community, \
mean_comparison_sent_internet, mean_comparison_received_internet



# Recalculating the total counts of 'Yes', 'No', and 'No Value' for the column "17 Do you waste any time using email"
waste_time_email_counts = email_data['17 Do you waste any time using email'].value_counts(dropna=False)
waste_time_email_counts['No Value'] = waste_time_email_counts.pop(np.nan)  # Rename NaN to 'No Value'

# Calculating percentages
waste_time_email_percentages = (waste_time_email_counts / total_respondents) * 100

waste_time_email_counts, waste_time_email_percentages

# Recalculating the total counts of 'Yes', 'No', and 'No Value' for the column "17 Do you waste any time using email"
waste_time_email_counts = email_data['17 Do you waste any time using email'].value_counts(dropna=False)
waste_time_email_counts['No Value'] = waste_time_email_counts.get(np.nan, 0)  # Handle NaN values

# Removing the NaN key if it exists
waste_time_email_counts = waste_time_email_counts.drop(np.nan, errors='ignore')

# Calculating percentages
waste_time_email_percentages = (waste_time_email_counts / total_respondents) * 100

waste_time_email_counts, waste_time_email_percentages


# Counting the frequency of each unique response in "19a Please provide an example of how time is wasted..."
time_wasted_examples_counts = email_data['19a Please provide an example of how time is wa...'].value_counts()

time_wasted_examples_counts

