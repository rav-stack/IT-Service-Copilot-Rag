# app/services/llm_service.py

import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query, context):
    prompt = f"""
You are an enterprise IT support assistant.

Answer ONLY using the provided context.
If the answer is not present, say: "Insufficient data to process an answer".

Also ensure the answer is concise and accurate.
While answering, you MUST cite the exact source file name from the context.
Use this format: [source_file_name]

Do NOT invent or modify source names.
Only use sources explicitly provided in the context.
Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()













# import os
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_answer(query, context):
#     prompt = f"""
#  You are an enterprise support assistant.

#  Answer ONLY from the given context.
#  If the answer is not in the context, say "I don't know".

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     response = client.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )

#     return response.choices[0].message.content.strip()