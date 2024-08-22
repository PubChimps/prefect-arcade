import os
import yfinance as yf

from openai import OpenAI


def get_data():
    return yf.download("AAPL MSFT", period='1d').to_string()

def prompt_llm():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Given today's data, which stock did better? " + get_data(),
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    print(prompt_llm())
