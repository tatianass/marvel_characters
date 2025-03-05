import os

from dotenv import load_dotenv

ENV = os.environ.get("ENV", "local")

_ = load_dotenv(f".env.{ENV}")


def main():
    return "Hello World!"


if __name__ == "__main__":
    print(main())
