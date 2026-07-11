"""
Comparison Tests
----------------
Independent Samples

Contains:
1. Independent T-Test
2. Welch T-Test
3. One-Way ANOVA
4. Welch ANOVA
5. Mann-Whitney U Test
6. Kruskal-Wallis Test
"""

from scipy.stats import (
    ttest_ind,
    f_oneway,
    mannwhitneyu,
    kruskal
)

import pingouin as pg

from constants import ALPHA


############################################################
# Independent T-Test
############################################################

def run_t_test(df, cat_col, num_col):
    """
    Perform Independent Samples T-Test.
    """

    groups = df[cat_col].unique()

    group1 = df[
        df[cat_col] == groups[0]
    ][num_col]

    group2 = df[
        df[cat_col] == groups[1]
    ][num_col]

    statistic, p = ttest_ind(
        group1,
        group2,
        equal_var=True
    )

    p = round(float(p), 4)

    return {

        "test": "Independent T-Test",

        "statistic_name": "t",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# Welch T-Test
############################################################

def run_welch_t_test(df, cat_col, num_col):
    """
    Perform Welch's T-Test.
    """

    groups = df[cat_col].unique()

    group1 = df[
        df[cat_col] == groups[0]
    ][num_col].dropna()

    group2 = df[
        df[cat_col] == groups[1]
    ][num_col].dropna()

    statistic, p = ttest_ind(
        group1,
        group2,
        equal_var=False
    )

    p = round(float(p), 4)

    return {

        "test": "Welch T-Test",

        "statistic_name": "t",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# One-Way ANOVA
############################################################

def run_anova(df, cat_col, num_col):
    """
    Perform One-Way ANOVA.
    """

    groups = [

        group[num_col].values

        for _, group in df.groupby(cat_col)

    ]

    statistic, p = f_oneway(*groups)

    p = round(float(p), 4)

    return {

        "test": "One-Way ANOVA",

        "statistic_name": "F",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# Welch ANOVA
############################################################

def run_welch_anova(df, cat_col, num_col):
    """
    Perform Welch ANOVA.
    """

    result = pg.welch_anova(

        data=df,

        dv=num_col,

        between=cat_col

    )

    p = round(float(result["p-unc"][0]), 4)

    return {

        "test": "Welch ANOVA",

        "statistic_name": "F",

        "statistic": round(float(result["F"][0]), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA,

        "df1": round(float(result["ddof1"][0]), 2),

        "df2": round(float(result["ddof2"][0]), 2)

    }


############################################################
# Mann-Whitney U Test
############################################################

def run_mann_whitney(df, cat_col, num_col):
    """
    Perform Mann-Whitney U Test.
    """

    groups = df[cat_col].unique()

    group1 = df[
        df[cat_col] == groups[0]
    ][num_col]

    group2 = df[
        df[cat_col] == groups[1]
    ][num_col]

    statistic, p = mannwhitneyu(
        group1,
        group2
    )

    p = round(float(p), 4)

    return {

        "test": "Mann-Whitney U",

        "statistic_name": "U",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }


############################################################
# Kruskal-Wallis Test
############################################################

def run_kruskal(df, cat_col, num_col):
    """
    Perform Kruskal-Wallis Test.
    """

    groups = [

        group[num_col].values

        for _, group in df.groupby(cat_col)

    ]

    statistic, p = kruskal(*groups)

    p = round(float(p), 4)

    return {

        "test": "Kruskal-Wallis",

        "statistic_name": "H",

        "statistic": round(float(statistic), 4),

        "p_value": p,

        "alpha": ALPHA,

        "significant": p < ALPHA

    }