from kedro.pipeline import Pipeline, node, pipeline

from .intermediate import preprocess_characters
from .reporting import reporting


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_characters,
                inputs="character_dataset",
                outputs="preprocess_characters",
                name="preprocess_characters_node",
            ),
            node(
                func=reporting,
                inputs="preprocess_characters",
                outputs="reporting",
                name="reporting_node",
            ),
        ]
    )
