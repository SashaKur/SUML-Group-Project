from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (
    make_book_rating_dataset,
    drop_unnecessary_columns,
    filter_books_by_ratings,
    get_user_rating,
    filter_users_by_ratings,
    combine,
)


def create_tensor_flow_prep_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=make_book_rating_dataset,
                inputs=["books", "book_ratings"],
                outputs="book_rating_merged",
                name="make_book_rating_dataset",
            ),
            node(
                func=drop_unnecessary_columns,
                inputs="book_rating_merged",
                outputs="book_rating_merged_cleaned",
                name="drop_unnecessary_columns",
            ),
            node(
                func=filter_books_by_ratings,
                inputs="book_rating_merged_cleaned",
                outputs="rating_count",
                name="filter_books_by_ratings",
            ),
            node(
                func=get_user_rating,
                inputs=["rating_count", "book_rating_merged_cleaned"],
                outputs="user_rating",
                name="get_user_rating",
            ),
            node(
                func=filter_users_by_ratings,
                inputs="user_rating",
                outputs="user_count",
                name="filter_users_by_ratings",
            ),
            node(
                func=combine,
                inputs=["user_rating", "user_count"],
                outputs="user_rating_count",
                name="combine_user_rating_and_count",
            ),
        ]
    )
