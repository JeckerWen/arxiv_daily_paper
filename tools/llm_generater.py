from openai import OpenAI
import os
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


def llm_generater_ds(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = "9.11 and 9.8, which is greater?"
    print(llm_generater_ds(prompt))