import os
import yfinance as yf                                                                                                        # type: ignore

from openai import OpenAI                                                                                                    # type: ignore


def get_data():
    return yf.download("AAPL MSFT", period='1d').to_string()


def prompt_llm(data):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Given today's data, which stock did better? " + data,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


def get_data_prompt_llm():
    print(prompt_llm(get_data()))

if __name__ == "__main__":
    get_data_prompt_llm()
