import controlflow as cf
import yfinance as yf

def get_data():
    return yf.download("AAPL MSFT", period='1d').to_string()


def prompt_llm():
    task = cf.Task("Given today's data, which stock did better? " + get_data())
    task.run()

if __name__ == "__main__":
    prompt_llm()
