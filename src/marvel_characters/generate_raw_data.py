import logging.config
import os
import time

from dotenv import load_dotenv

from marvel_characters.marvel import Marvel

# Create logging information
logging.basicConfig()

# create logger
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)

# Load env variables

ENV = os.environ.get("ENV", "local")

_ = load_dotenv(f".env.{ENV}")


def main():
    logger.info("Process started.")

    offset = int(os.environ.get("OFFSET"))

    # Loop over different pages
    total = 0
    for i in range(0, offset, 20):
        # Check stop condition
        if i > total:
            break

        marvel = Marvel()
        success_ind, result = marvel.request_characters(
            private_key=os.environ.get("MARVEL_PRIVATE_KEY"),
            public_key=os.environ.get("MARVEL_PUBLIC_KEY"),
            offset=i,
        )

        if success_ind:
            marvel.save_characters_to_json(f"chars_{i}.json")

            if i == 0:
                total = result["data"]["total"]
                logger.info("Total number of Marvel characters is: " + str(total))
            time.sleep(2)
        else:
            raise Exception(result)
    return "Process finished!"


if __name__ == "__main__":
    logger.info(main())
