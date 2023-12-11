"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import merge_datasets, drop_rows_with_nulls, drop_unnecessary_columns


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=merge_datasets,
            inputs=["books", "users", "book_ratings"],
            outputs="merged_data",
            name="merge_datasets_node"
        ),
        node(
            func=drop_unnecessary_columns,
            inputs="merged_data",
            outputs="dropped_unnecessary_columns",
            name="drop_unnecessary_columns_node"
        ),
        node(
            func=drop_rows_with_nulls,
            inputs="dropped_unnecessary_columns",
            outputs="cleaned_data",
            name="clean_datasets_node"
        ),
    ])
