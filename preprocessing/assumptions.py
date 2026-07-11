import pandas as pd

from scipy.stats import chi2_contingency
from scipy.stats import levene


def check_expected_counts(df, col1, col2):
    """
    Check the expected frequencies for a contingency table.

    Parameters
    ----------
    df : pandas.DataFrame

    col1 : str

    col2 : str

    Returns
    -------
    dict

        all_expected_ge_5 : bool
            True if every expected frequency is at least 5.

        is_2x2 : bool
            True if the contingency table is 2×2.
    """

    ####################################################
    # Create contingency table

    contingency_table = pd.crosstab(
        df[col1],
        df[col2]
    )

    ####################################################
    # Calculate expected frequencies

    _, _, _, expected = chi2_contingency(
        contingency_table
    )

    ####################################################
    # Return results

    return {

        "all_expected_ge_5": bool(
            (expected >= 5).all()
        ),

        "is_2x2": contingency_table.shape == (2, 2)

    }


############################################################
# Homogeneity of Variance
############################################################

def check_homogeneity(df, cat_col, num_col):
    """
    Check homogeneity of variances using Levene's Test.

    Parameters
    ----------
    df : pandas.DataFrame

    cat_col : str
        Grouping variable.

    num_col : str
        Numerical variable.

    Returns
    -------
    dict
    """

    ####################################################
    # Split observations into groups

    groups = [

        group[num_col].dropna()

        for _, group

        in df.groupby(cat_col)

    ]

    ####################################################
    # Perform Levene's Test

    statistic, p = levene(*groups)

    ####################################################
    # Return results

    return {

        "test": "Levene Test",

        "statistic": round(
            float(statistic),
            3
        ),

        "p_value": round(
            float(p),
            3
        ),

        "equal_variance": bool(
            p > 0.05
        )

    }