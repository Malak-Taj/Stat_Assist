import streamlit as st
import pandas as pd

from preprocessing.cleaning import clean_data
from preprocessing.metadata import extract_metadata
from test_selector import choose_and_run_test
from interpreter import explain_result


##################################################
# Title

st.title("StatAssist")

##################################################
# Upload Dataset

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv" , "xlsx"]
)

if uploaded_file is not None:

    ##################################################
    # Read Dataset

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset")

    st.dataframe(df.head())

    ##################################################
    # Clean Data

    df = clean_data(df)

    ##################################################
    # Extract Metadata

    metadata = extract_metadata(df)

    ##################################################
    # User Question

    user_question = st.text_input(
        "What would you like to know?"
    )

    ##################################################
    # Select Columns

    selected_columns = st.multiselect(
        "Select Two Variables",
        options = df.columns,
        max_selections = 2
    )

    ##################################################
    # Run

    if st.button("Analyze"):

        result = choose_and_run_test(

            df,

            selected_columns,

            metadata

        )

        ##################################################

        if "error" in result:

            st.error(result["error"])

        else:

            st.subheader("Statistical Result")

            st.json(result)

            ##################################################

            explanation = explain_result(

                user_question,

                result

            )

            st.subheader("AI Explanation")

            st.write(explanation)