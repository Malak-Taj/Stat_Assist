# StatAssist

StatAssist is a Streamlit-based statistical analysis app that helps users explore datasets, choose appropriate statistical tests, and receive beginner-friendly explanations of the results.

It is designed for quick exploratory analysis and supports common relationships and group-comparison questions with an automatic rule-based test selection workflow.

## Features

- Upload CSV or XLSX files
- Automatically clean and inspect uploaded data
- Detect variable types and basic metadata
- Select an appropriate statistical test based on the data structure
- Support for common analyses such as:
  - Chi-square / Fisher's exact test
  - Pearson / Spearman correlation
  - T-test / Welch T-test
  - ANOVA / Welch ANOVA
  - Mann-Whitney U test
  - Kruskal-Wallis test
- Generate plain-language explanations of statistical results with Gemini

## Project Structure

- app.py — Streamlit web app interface
- test_selector.py — Rule-based statistical test selection
- preprocessing/ — Data cleaning and metadata extraction
- tests/ — Statistical test implementations
- interpreter.py — Gemini-based explanation layer

## Requirements

- Python 3.9+
- streamlit
- pandas
- google-genai

## Installation

Install the required dependencies:

```bash
pip install streamlit pandas google-genai
```

## Configuration

The app uses a Gemini API key for result explanations. Update the API key in the configuration file before running the app.

## Run the App

From the project directory, run:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## How to Use

1. Launch the app.
2. Upload a dataset in CSV or XLSX format.
3. Enter a question about the analysis you want to perform.
4. Select two variables from the dataset.
5. Click Analyze.

The app will show:
- the selected statistical test
- the result summary
- a simple explanation of the outcome in plain language

## Notes

- The app is intended for educational and exploratory analysis.
- Make sure your dataset contains the relevant columns for the analysis you want to run.
- Results should be interpreted carefully and validated against the context of your study.
