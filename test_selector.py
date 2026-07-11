"""
test_selector.py
----------------

Selects the appropriate statistical test based on:

1. Variable types
2. Number of groups
3. Normality
4. Homogeneity of variances

Returns both the statistical result and
additional metadata for the LLM layer.
"""

from preprocessing.assumptions import (
    check_expected_counts,
    check_homogeneity
)

from tests.relationship.cat_cat import (
    run_chi_square,
    run_fisher
)

from tests.relationship.num_num import (
    run_pearson,
    run_spearman
)

from tests.comparison.independent import (
    run_t_test,
    run_welch_t_test,
    run_mann_whitney,
    run_anova,
    run_welch_anova,
    run_kruskal
)


def choose_and_run_test(
    df,
    selected_columns,
    metadata
):
    """
    Automatically select and execute
    the appropriate statistical test.

    Parameters
    ----------
    df : pandas.DataFrame

    selected_columns : list
        Two selected columns.

    metadata : dict
        Output of extract_metadata().

    Returns
    -------
    dict
        Statistical result and information
        required by the LLM.
    """

    ####################################################
    # Validate Input

    if len(selected_columns) != 2:

        return {

            "error": "Please select exactly two columns."

        }

    ####################################################
    # Selected Columns

    col1, col2 = selected_columns

    ####################################################
    # Variable Types

    type1 = metadata[col1]["variable_type"]
    type2 = metadata[col2]["variable_type"]

    categorical_types = ("binary", "categorical")

    ####################################################
    # Information for the LLM

    result = {}

    decision_path = []

    ####################################################
    # CASE 1
    # Categorical ↔ Categorical

    if (

        type1 in categorical_types

        and

        type2 in categorical_types

    ):

        decision_path.append(
            "Detected two categorical variables."
        )

        expected = check_expected_counts(
            df,
            col1,
            col2
        )

        if expected["all_expected_ge_5"]:

            result = run_chi_square(
                df,
                col1,
                col2
            )

            decision_path.append(
                "All expected frequencies ≥ 5."
            )

            reason = (
                "Chi-Square assumptions were satisfied."
            )

        else:

            if expected["is_2x2"]:

                result = run_fisher(
                    df,
                    col1,
                    col2
                )

                decision_path.append(
                    "2×2 contingency table."
                )

                decision_path.append(
                    "Expected frequencies < 5."
                )

                reason = (
                    "Small expected frequencies in a 2×2 table."
                )

            else:

                result = run_chi_square(
                    df,
                    col1,
                    col2
                )

                decision_path.append(
                    "Table larger than 2×2."
                )

                reason = (
                    "Chi-Square remains appropriate."
                )

        result["analysis_type"] = "relationship"

    ####################################################
    # CASE 2
    # Numerical ↔ Numerical

    elif (

        type1 == "numerical"

        and

        type2 == "numerical"

    ):

        decision_path.append(
            "Detected two numerical variables."
        )

        normal1 = metadata[col1]["normal"]
        normal2 = metadata[col2]["normal"]

        if normal1 and normal2:

            result = run_pearson(
                df,
                col1,
                col2
            )

            decision_path.append(
                "Both variables are normally distributed."
            )

            reason = (
                "Pearson correlation assumptions satisfied."
            )

        else:

            result = run_spearman(
                df,
                col1,
                col2
            )

            decision_path.append(
                "At least one variable is not normally distributed."
            )

            reason = (
                "Spearman correlation selected."
            )

        result["analysis_type"] = "relationship"

    ####################################################
    # CASE 3
    # Categorical ↔ Numerical

    elif (

        (type1 in categorical_types and type2 == "numerical")

        or

        (type2 in categorical_types and type1 == "numerical")

    ):

        decision_path.append(
            "Detected one categorical and one numerical variable."
        )

        ################################################
        # Identify Variables

        if type1 in categorical_types:

            cat_col = col1
            num_col = col2

        else:

            cat_col = col2
            num_col = col1

        ################################################
        # Number of Groups

        n_groups = metadata[cat_col]["n_unique"]

        ################################################
        # Normality

        normal = metadata[num_col]["normal"]

        ################################################
        # Two Groups

        if n_groups == 2:

            decision_path.append(
                "Detected two groups."
            )

            if normal:

                decision_path.append(
                    "Normality assumption satisfied."
                )

                homogeneity = check_homogeneity(
                    df,
                    cat_col,
                    num_col
                )

                if homogeneity["equal_variance"]:

                    result = run_t_test(
                        df,
                        cat_col,
                        num_col
                    )

                    decision_path.append(
                        "Equal variances satisfied."
                    )

                    reason = (
                        "Independent T-Test assumptions satisfied."
                    )

                else:

                    result = run_welch_t_test(
                        df,
                        cat_col,
                        num_col
                    )

                    decision_path.append(
                        "Unequal variances detected."
                    )

                    reason = (
                        "Welch T-Test selected."
                    )

                result["assumptions"] = homogeneity

            else:

                result = run_mann_whitney(
                    df,
                    cat_col,
                    num_col
                )

                decision_path.append(
                    "Normality assumption failed."
                )

                reason = (
                    "Mann-Whitney U selected."
                )

        ################################################
        # More Than Two Groups

        else:

            decision_path.append(
                "Detected more than two groups."
            )

            if normal:

                decision_path.append(
                    "Normality assumption satisfied."
                )

                homogeneity = check_homogeneity(
                    df,
                    cat_col,
                    num_col
                )

                if homogeneity["equal_variance"]:

                    result = run_anova(
                        df,
                        cat_col,
                        num_col
                    )

                    decision_path.append(
                        "Equal variances satisfied."
                    )

                    reason = (
                        "One-Way ANOVA selected."
                    )

                else:

                    result = run_welch_anova(
                        df,
                        cat_col,
                        num_col
                    )

                    decision_path.append(
                        "Unequal variances detected."
                    )

                    reason = (
                        "Welch ANOVA selected."
                    )

                result["assumptions"] = homogeneity

            else:

                result = run_kruskal(
                    df,
                    cat_col,
                    num_col
                )

                decision_path.append(
                    "Normality assumption failed."
                )

                reason = (
                    "Kruskal-Wallis selected."
                )

        result["analysis_type"] = "comparison"

        result["group_column"] = cat_col
        result["numeric_column"] = num_col

    ####################################################
    # Unsupported Combination

    else:

        return {

            "error": "Unsupported variable combination."

        }

    ####################################################
    # Add Information for LLM

    result["reason"] = reason

    result["decision_path"] = decision_path

    result["sample_size"] = len(df)

    result["variables"] = {

        col1: metadata[col1],

        col2: metadata[col2]

    }

    result["selected_columns"] = selected_columns

    return result