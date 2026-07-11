import pandas as pd
from scipy.stats import zscore
from scipy.stats import kstest

def check_normality(df):
    """
    Check the normality of all numerical columns using
    the Kolmogorov-Smirnov test.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
        Dictionary containing the normality result
        for each numerical column.
    """

    # Store results
    normality = {}

    # Loop through all columns
    for col in df.columns:

        # Skip non-numerical columns
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue

        # Remove missing values
        data = df[col].dropna()

        # Skip constant columns
        if data.nunique() <= 1:

            normality[col] = False
            continue

        try:

            # Standardize data
            data_std = zscore(data)

            # Perform K-S test
            statistic, p = kstest(
                data_std,
                "norm"
            )

            # Save result
            normality[col] = p > 0.05

        except Exception:

            # If the test fails for any reason
            normality[col] = False

    return normality