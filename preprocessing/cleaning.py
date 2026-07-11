import pandas as pd

def clean_data(df,
               column_threshold=0.5,
               row_threshold=0.5):
    """
    Clean the dataset by:

    1. Removing columns with many missing values.
    2. Removing rows with many missing values.
    3. Imputing remaining missing values.
    4. Removing duplicate rows.
    5. Resetting the index.
    6. Converting binary and categorical variables to category dtype.

    Parameters
    ----------
    df : pandas.DataFrame

    column_threshold : float

    row_threshold : float

    Returns
    -------
    pandas.DataFrame
        Cleaned dataset.
    """

    # Create a copy
    df_cleaned = df.copy()

    ## Remove columns with > 50% missing values
    col_missing = df_cleaned.isna().mean()

    cols_to_drop = col_missing [ col_missing > column_threshold ].index

    df_cleaned = df_cleaned.drop (columns = cols_to_drop)

    # Remove rows with > 50% missing values
    row_missing = df_cleaned.isna().mean(axis=1)

    rows_to_drop = row_missing > row_threshold

    df_cleaned = df_cleaned.loc [~rows_to_drop]

    # Impute remaining missing values
    for col in df_cleaned.columns:

        if df_cleaned[col].isna ().sum () == 0:
            continue

        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
            median = df_cleaned[col].median()
            df_cleaned [col] = df_cleaned [col].fillna (median)

        else:
            mode = df_cleaned [col].mode()[0]
            df_cleaned [col] = df_cleaned [col].fillna(mode)

    # Remove duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()

    # Reset index
    df_cleaned = df_cleaned.reset_index(drop=True)

    # Handle binary and ordinal variables
    for col in df_cleaned.columns:

        unique_values = df_cleaned[col].nunique()

        if unique_values < 6:
            df_cleaned[col] = df_cleaned[col].astype("category")
        else:
            continue

    return df_cleaned