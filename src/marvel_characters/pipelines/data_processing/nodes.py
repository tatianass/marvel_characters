from datetime import date

import polars as pl
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Character(BaseModel):
    # Ignore other fields
    model_config = ConfigDict(extra="ignore")

    id: int = Field(gt=0, frozen=True)
    name: str = Field(max_length=50, frozen=True)
    description: str = Field(max_length=500, frozen=True)
    modified: date = Field(frozen=True)
    resource_uri: str = Field(alias="resourceURI", frozen=True)
    total_comics_in_num: int = Field(frozen=True)
    total_series_in_num: int = Field(frozen=True)
    total_stories_in_num: int = Field(frozen=True)
    total_events_in_num: int = Field(frozen=True)

    @field_validator("modified")
    @classmethod
    def check_valid_age(cls, modified: date) -> date:
        today = date.today()

        if modified > today:
            raise ValueError("Date must not be from the future.")

        return modified


def preprocess_characters(characters: dict) -> pl.DataFrame:
    """Preprocesses the data for characters.

    Args:
        characters: Raw data.
    Returns:
        Preprocessed data from json to parquet and add variables for counts.
    """

    # Iterate over multiple json results
    chars_list = []
    for result in characters:
        data = result["data"]["results"]
        # Iterate over multiple characters
        for char in data:
            # Get additional information
            char["total_comics_in_num"] = char["comics"]["available"]
            char["total_series_in_num"] = char["series"]["available"]
            char["total_stories_in_num"] = char["stories"]["available"]
            char["total_events_in_num"] = char["events"]["available"]
            char["modified"] = char["modified"][:10]
            char_obj = Character(**char)
            chars_list.append(char_obj)

    # Transform to Polars
    pre_characters = pl.DataFrame([vars(c) for c in chars_list])
    return pre_characters
