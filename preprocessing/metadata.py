import pandas as pd

from .check_normality import check_normality

def extract_metadata(df):
    """
    Extract metadata for every column in the dataset.

    Metadata includes:
    - Data type
    - Variable type
    - Number of unique values
    - Sample size
    - Normality (numerical variables only)

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    dict
        Metadata for all variables.
    """

    # Run normality test once
    normality_results = check_normality(df)

    # Store metadata
    metadata = {}

    # Loop through columns
    for col in df.columns:

        dtype = str(df[col].dtype)

        n_unique = int(df[col].nunique())

        sample_size = int(df[col].count())

        metadata[col] = {

            "dtype": dtype,

            "n_unique": n_unique,

            "sample_size": sample_size

        }

        ####################################################
        # Object / Category
        ####################################################

        if dtype in ["object", "category"]:

            if n_unique == 2:

                metadata[col]["variable_type"] = "binary"

            else:

                metadata[col]["variable_type"] = "categorical"

        ####################################################
        # Numerical
        ####################################################

        elif pd.api.types.is_numeric_dtype(df[col]):

            if n_unique == 2:

                metadata[col]["variable_type"] = "binary"

            else:

                metadata[col]["variable_type"] = "numerical"

                metadata[col]["normal"] = normality_results.get(col)

    return metadata