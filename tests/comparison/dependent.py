"""
Comparison Tests
----------------
Dependent (Paired) Samples

Contains:
1. Paired T-Test
2. Wilcoxon Signed-Rank Test
3. Repeated Measures ANOVA
4. Friedman Test
"""

from scipy.stats import (
    ttest_rel,
    wilcoxon,
    friedmanchisquare
)

from statsmodels.stats.anova import AnovaRM

from constants import ALPHA


############################################################
# Paired T-Test
############################################################

def run_paired_t_test(df, col1, col2):
    """
    Perform Paired Samples T-Test.

    Parameters
    ----------
    df : pandas.DataFrame

    col1 : str
        First measurement.

    col2 : str
        Second measurement.

    Returns
    -------
    dict
        Test results.
    """

    # Remove missing values
    paired_data = df[[col1, col2]].dropna()

    group1 = paired_data[col1]
    group2 = paired_data[col2]

    statistic, p = ttest_rel(
        group1,
        group2
    )

    p = round(float(p), 4)

    return {

        "test": "Paired T-Test",

        "statistic_name": "t",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# Wilcoxon Signed-Rank Test
############################################################

def run_wilcoxon(df, col1, col2):
    """
    Perform Wilcoxon Signed-Rank Test.

    Parameters
    ----------
    df : pandas.DataFrame

    col1 : str
        First measurement.

    col2 : str
        Second measurement.

    Returns
    -------
    dict
        Test results.
    """

    # Remove missing values
    paired_data = df[[col1, col2]].dropna()

    group1 = paired_data[col1]
    group2 = paired_data[col2]

    statistic, p = wilcoxon(
        group1,
        group2
    )

    p = round(float(p), 4)

    return {

        "test": "Wilcoxon Signed-Rank Test",

        "statistic_name": "W",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# Repeated Measures ANOVA
############################################################

def run_repeated_measures_anova(
    df,
    subject_col,
    within_col,
    value_col
):
    """
    Perform Repeated Measures ANOVA.

    Parameters
    ----------
    df : pandas.DataFrame

    subject_col : str
        Subject ID column.

    within_col : str
        Within-subject factor.

    value_col : str
        Numerical measurement.

    Returns
    -------
    dict
        Test results.
    """

    result = AnovaRM(

        data=df,

        depvar=value_col,

        subject=subject_col,

        within=[within_col]

    ).fit()

    table = result.anova_table

    p = round(float(table["Pr > F"][0]), 4)

    return {

        "test": "Repeated Measures ANOVA",

        "statistic_name": "F",

        "statistic": round(float(table["F Value"][0]), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA,

        "df1": round(float(table["Num DF"][0]), 2),

        "df2": round(float(table["Den DF"][0]), 2)

    }


############################################################
# Friedman Test
############################################################

def run_friedman(df, columns):
    """
    Perform Friedman Test.

    Parameters
    ----------
    df : pandas.DataFrame

    columns : list
        List of repeated measurement columns.

    Returns
    -------
    dict
        Test results.
    """

    clean_data = df[columns].dropna()

    groups = [

        clean_data[col]

        for col in columns

    ]

    statistic, p = friedmanchisquare(*groups)

    p = round(float(p), 4)

    return {

        "test": "Friedman Test",

        "statistic_name": "χ²",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }