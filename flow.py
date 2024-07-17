


def say_hello(name: str):
    print(f"Hello, {name}!")


def hello_prefect(names: list[str]=["Prefect", "Arcade"]):
    for name in names:
        say_hello(name)

if __name__ == "__main__":
    hello_prefect()
