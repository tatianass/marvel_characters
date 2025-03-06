from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_characters


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_characters,
                inputs="character_dataset",
                outputs="preprocess_characters",
                name="preprocess_characters_node",
            )
        ]
    )
