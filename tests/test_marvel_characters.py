import json
import os

import pandas as pd
import pytest
from bokeh.models.layouts import Column
from dotenv import load_dotenv
from kedro.pipeline import Pipeline

from marvel_characters.generate_raw_data import main
from marvel_characters.marvel import Marvel
from marvel_characters.pipelines.data_processing import create_pipeline
from marvel_characters.pipelines.data_processing.intermediate import (
    preprocess_characters,
)
from marvel_characters.pipelines.data_processing.reporting import reporting_bokeh

ENV = os.environ.get("ENV", "local")

_ = load_dotenv(f".env.{ENV}")


class TestMarvelCharacters:
    def test_main(self):
        result = main()
        assert result == "Process finished!"

    def test_marvel(self):
        marvel = Marvel()
        success_ind, result = marvel.request_characters(
            private_key=os.environ.get("MARVEL_PRIVATE_KEY"),
            public_key=os.environ.get("MARVEL_PUBLIC_KEY"),
            offset=0,
        )

        # Check results
        assert success_ind
        assert result["code"] == 200

        assert len(marvel.get_characters()) == 7

        with pytest.raises(Exception) as exc_info:
            success_ind, result = marvel.request_characters(
                private_key=os.environ.get("MARVEL_PRIVATE_KEY"),
                public_key="",
                offset=0,
            )
            assert ~success_ind
            assert type(result) is Exception
            assert result == exc_info

    def test_pipeline_create_pipeline(self):
        pipeline = create_pipeline()

        assert type(pipeline) is Pipeline

    def test_nodes_preprocess_characters(self):
        # Set dummy
        dummy_data = json.loads("""[{"data": {"results": [{
                    "id": 1,
                    "name": "Spider Man",
                    "modified": "2013-10-17T00:00:00.000Z",
                    "resourceURI": "https://",
                    "comics": {"available": 10},
                    "series": {"available": 10},
                    "stories": {"available": 10},
                    "events": {"available": 10}
                },{
            "id": 1,
            "name": "Iron Man",
            "modified": "2013-10-17T00:00:00.000Z",
            "resourceURI": "https://",
            "comics": {"available": 10},
            "series": {"available": 10},
            "stories": {"available": 10},
            "events": {"available": 10}
        },{
            "id": 1,
            "name": "Black Widow",
            "modified": "2013-10-17T00:00:00.000Z",
            "resourceURI": "https://",
            "comics": {"available": 10},
            "series": {"available": 10},
            "stories": {"available": 10},
            "events": {"available": 10}
        }]}}]""")
        results_df = preprocess_characters(dummy_data)

        assert len(results_df) == 3

    def test_nodes_reporting(self):
        dummy_data = pd.DataFrame(
            {
                "id": [1011334],
                "name": ["3-D Man"],
                "modified": ["2014-04-29T00:00:00.000Z"],
                "resource_uri": [
                    "http://gateway.marvel.com/v1/public/characters/1011334"
                ],
                "total_comics_in_num": [12],
                "total_series_in_num": [3],
                "total_stories_in_num": [21],
                "total_events_in_num": [1],
            }
        )

        results = reporting_bokeh(dummy_data)

        assert type(results) is Column
