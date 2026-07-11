"""
Relationship Tests
------------------
Categorical ↔ Categorical

Contains:
1. Chi-Square Test
2. Fisher Exact Test
"""

import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact
from constants import ALPHA


##### Chi-Square Test
def run_chi_square(df, col1, col2):
    """
    Perform Pearson Chi-Square Test of Independence.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    col1 : str
        First categorical variable.

    col2 : str
        Second categorical variable.

    Returns
    -------
    dict
        Test results.
    """

    ##### Create contingency table
    contingency_table = pd.crosstab(
        df[col1],
        df[col2]
    )

    ##### Run Chi-Square Test
    chi2, p, dof, expected = chi2_contingency(
        contingency_table
    )

    p = round(float(p), 4)

    return {

        "test": "Chi-Square",

        "statistic_name": "χ²",

        "statistic": round(float(chi2), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA,

        "dof": int(dof)

    }

##### Fisher Exact Test

def run_fisher(df, col1, col2):
    """
    Perform Fisher Exact Test.

    Used only for 2×2 contingency tables.

    Parameters
    ----------
    df : pandas.DataFrame

    col1 : str

    col2 : str

    Returns
    -------
    dict
        Test results.
    """

    ##### Create contingency table
    contingency_table = pd.crosstab(
        df[col1],
        df[col2]
    )

    ##### Run Fisher Exact Test
    statistic, p = fisher_exact(
        contingency_table
    )

    p = round(float(p), 4)

    return {

        "test": "Fisher Exact Test",

        "statistic_name": "Odds Ratio",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }