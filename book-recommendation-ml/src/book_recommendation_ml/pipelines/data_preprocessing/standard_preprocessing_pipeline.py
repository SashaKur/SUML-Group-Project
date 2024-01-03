"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    merge_datasets,
    drop_rows_with_nulls,
    drop_unnecessary_columns,
    drop_rating_zero_rows,
    drop_year_zero_rows,
    make_isbn_numeric,
)


def create_data_preprocessing_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=merge_datasets,
                inputs=["books", "users", "book_ratings"],
                outputs="merged_data",
                name="merge_datasets_node",
            ),
            node(
                func=drop_unnecessary_columns,
                inputs="merged_data",
                outputs="dropped_unnecessary_columns",
                name="drop_unnecessary_columns_node",
            ),
            node(
                func=drop_rows_with_nulls,
                inputs="dropped_unnecessary_columns",
                outputs="cleaned_data",
                name="clean_datasets_node",
            ),
            node(
                func=drop_year_zero_rows,
                inputs="cleaned_data",
                outputs="data_without_zero_year",
                name="drop_year_zero_rows_node",
            ),
            node(
                func=drop_rating_zero_rows,
                inputs="data_without_zero_year",
                outputs="data_without_zero_rating",
                name="drop_rating_zero_rows_node",
            ),
            node(
                func=make_isbn_numeric,
                inputs="data_without_zero_rating",
                outputs="primary_data",
                name="make_isbn_numeric",
            ),
        ]
    )
