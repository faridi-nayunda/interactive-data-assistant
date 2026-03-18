import os
import json
from groq import Groq

# Lazy-load Groq client
_client = None
def get_groq_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables")
        _client = Groq(api_key=api_key)
    return _client

def generate_summary(question: str, results: list) -> str:
    if not results:
        return "No data found for this query."

    # Limit rows to avoid token explosion
    limited_results = results[:20]

    # Convert to compact JSON string
    results_json = json.dumps(limited_results, default=str)

    prompt = f"""
You are a factual data summarizer.

You are ONLY allowed to use the provided query results.
You MUST NOT invent numbers, percentages, trends, or business assumptions.

========================
USER QUESTION
========================
{question}

========================
QUERY RESULTS (first 20 rows)
========================
{results_json}

========================
STRICT RULES
========================

1. Only describe what is explicitly visible in the data.
2. Do NOT calculate totals unless visible.
3. Do NOT assume trends.
4. Do NOT mention row counts unless you explicitly count them.
5. Do NOT speculate.
6. If data is limited, say so.
7. Maximum 120 words.

Return a concise factual summary only.
"""

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    summary = response.choices[0].message.content.strip()

    # Remove markdown/code blocks if present
    if summary.startswith("```"):
        summary = "\n".join(summary.split("\n")[1:-1])

    return summary