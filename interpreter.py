"""
llm_layer.py

This module sends the statistical results to Groq
and returns a natural-language explanation.
"""

from groq import Groq
from config import API_KEY
from prompts import RESULT_INTERPRETATION_PROMPT

####################################################
# Configure Groq

client = Groq(
    api_key=API_KEY
)

####################################################
# Build Prompt

def build_prompt(
    user_question,
    result
):
    """
    Fill the prompt template with the
    statistical result.
    """

    return RESULT_INTERPRETATION_PROMPT.format(

        user_question=user_question,

        test=result["test"],

        reason=result["reason"],

        analysis_type=result["analysis_type"],

        selected_columns=result["selected_columns"],

        variables=result["variables"],

        sample_size=result["sample_size"],

        decision_path=result["decision_path"],

        statistic_name=result["statistic_name"],

        statistic=result["statistic"],

        p_value=result["p_value"],

        alpha=result["alpha"],

        significant=result["significant"]

    )


####################################################
# Explain Result

def explain_result(
    user_question,
    result
):
    """
    Send the statistical result to Groq
    and return the explanation.
    """

    prompt = build_prompt(
        user_question,
        result
    )

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                
                "role": "system",
                "content": "You are an expert statistician and data analyst. Explain statistical test results in simple, educational language."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,
        top_p=0.9

    )

    return response.choices[0].message.content