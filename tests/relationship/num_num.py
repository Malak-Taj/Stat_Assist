"""
Relationship Tests
------------------
Numerical ↔ Numerical

Contains:
1. Pearson Correlation
2. Spearman Correlation
"""

from scipy.stats import pearsonr, spearmanr
from constants import ALPHA


############################################################
# Pearson Correlation
############################################################

def run_pearson(df, col1, col2):
    """
    Perform Pearson Correlation.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    col1 : str
        First numerical variable.

    col2 : str
        Second numerical variable.

    Returns
    -------
    dict
        Test results.
    """

    # Calculate Pearson correlation
    statistic, p = pearsonr(
        df[col1],
        df[col2]
    )

    p = round(float(p), 4)

    return {

        "test": "Pearson Correlation",

        "statistic_name": "r",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# Spearman Correlation
############################################################

def run_spearman(df, col1, col2):
    """
    Perform Spearman Rank Correlation.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    col1 : str
        First numerical variable.

    col2 : str
        Second numerical variable.

    Returns
    -------
    dict
        Test results.
    """

    # Calculate Spearman correlation
    statistic, p = spearmanr(
        df[col1],
        df[col2]
    )

    p = round(float(p), 4)

    return {

        "test": "Spearman Correlation",

        "statistic_name": "ρ",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }