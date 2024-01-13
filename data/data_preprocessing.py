import pandas as pd


def load_data(file_path):
    """
    Load the data from a CSV file into a Pandas DataFrame.
    """
    df = pd.read_csv(file_path)
    return df


def handle_missing_values(df):
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column].fillna(df[column].mean(), inplace=True)
        else:
            df[column].fillna(df[column].mode()[0], inplace=True)  # Replace with mode for non-numeric columns
    return df



def convert_data_types(df):
    """
    Convert data types if necessary.
    This is a placeholder; add specific conversions based on your data.
    """
    # Example: Convert a column to float
    # df['some_column'] = df['some_column'].astype(float)
    return df


if __name__ == "__main__":
    # Define the path to the data file
    file_path = '../August/raw_data2.csv'

    # Load the data into a DataFrame
    df = load_data(file_path)

    # Handle missing values
    df = handle_missing_values(df)
    print(df.head())
    # Convert data types
    df = convert_data_types(df)

    # Save the cleaned DataFrame back to CSV (Optional)
    df.to_csv('../data/cleaned_data.csv', index=False)
