import json
import os

import pytest
from dotenv import load_dotenv
from kedro.pipeline import Pipeline

from marvel_characters.generate_raw_data import main
from marvel_characters.marvel import Marvel
from marvel_characters.pipelines.data_processing import create_pipeline
from marvel_characters.pipelines.data_processing.nodes import preprocess_characters

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

        with pytest.raises(Exception) as excinfo:
            success_ind, result = marvel.request_characters(
                private_key=os.environ.get("MARVEL_PRIVATE_KEY"),
                public_key=None,
                offset=0,
            )
            assert ~success_ind
            assert type(result) is Exception
            assert result == excinfo

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
