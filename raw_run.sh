#!/usr/bin/env sh
if find data/01_raw/*.json | read; then
  echo "Skipping raw data retrieval, since data/01_raw is not empty."
else
  echo "Retrieving raw data..."
   python3 -m marvel_characters.generate_raw_data
   echo "Unifying json files into characters.json..."
   jq -s '.' data/01_raw/chars_*.json > data/01_raw/characters.json
   echo "Raw process finished!"
fi
