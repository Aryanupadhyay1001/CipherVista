import os

from dotenv import load_dotenv
from google import genai

from datetime import datetime

from src.llm.prompts import (
    SYSTEM_PROMPT,
    REPORT_PROMPT
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY1")
)


def generate_response(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                SYSTEM_PROMPT,
                prompt
            ]
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)

        return """
# AI Security Report

Gemini AI is temporarily unavailable (Google server overloaded).

The threat analysis has been completed successfully by the ML engine.

Please retry in a few minutes to generate the complete AI report.
"""


def generate_security_report(
    total,
    benign,
    attacks,
    anomalies,
    risk,
    confidence,
    attack_breakdown,
    dataset,
    classifier,
    anomaly_detector
):

    breakdown = ""

    for attack, count in attack_breakdown.items():
        breakdown += f"- {attack}: {count}\n"

    analysis_date = datetime.now().strftime("%d %B %Y")


    # analysis_date = datetime.now().strftime("%d %B %Y")

    prompt = REPORT_PROMPT.format(
    analysis_date=analysis_date,
    dataset=dataset,
    classifier=classifier,
    anomaly_detector=anomaly_detector,
    total=total,
    benign=benign,
    attacks=attacks,
    anomalies=anomalies,
    risk=risk,
    confidence=confidence,
    attack_breakdown=breakdown
)

    return generate_response(prompt)