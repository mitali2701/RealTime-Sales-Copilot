import ollama

MODEL = "llama3"

def llama(system_prompt, user_prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response["message"]["content"].strip()
