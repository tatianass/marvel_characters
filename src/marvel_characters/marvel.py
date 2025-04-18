import json
import time
from hashlib import md5

import requests as rq

test = rq.__version__

MARVEL_API_URL = "https://gateway.marvel.com"


class Marvel:
    def __init__(self):
        self.characters = {}

    def get_characters(self):
        return self.characters

    def request_characters(self, public_key: str, private_key: str, offset: int):
        ts = str(time.time())

        # Hash information
        # See why usedforsecurity is bein used: https://www.codiga.io/blog/python-insecure-hash-functions/
        hash_str = md5(
            f"{ts}{private_key}{public_key}".encode("utf8"), usedforsecurity=False
        ).hexdigest()

        # Set parameters
        params = {
            "apikey": public_key,
            "ts": ts,
            "hash": hash_str,
            "orderBy": "name",
            "offset": offset,
        }
        try:
            # Try to reach out for the information
            r = rq.get(
                "https://gateway.marvel.com:443/v1/public/characters",
                params=params,
                timeout=5,
            )
        except Exception as e:
            return False, e
        else:
            result = r.json()
            if result["code"] != 200:
                raise Exception("Code different than 200", result["code"])

            self.characters = result
            return True, result

    def save_characters_to_json(self, filename: str):
        # Convert into JSON
        # File name is mydata.json
        with open(f"data/01_raw/{filename}", "w") as final:
            json.dump(self.characters, final)
