from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    normalise_rating,
    create_user_book_matrix,
    train_tf_model,
)


def create_model_training_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=normalise_rating,
                inputs="user_rating_count",
                outputs="user_rating_count_normalised",
                name="normalise_rating",
            ),
            node(
                func=create_user_book_matrix,
                inputs="user_rating_count_normalised",
                outputs=["users_list", "books_list", "user_book_matrix"],
                name="create_user_book_matrix",
            ),
            node(
                func=train_tf_model,
                inputs=[
                    "users_list",
                    "books_list",
                    "user_book_matrix",
                    "user_rating_count_normalised",
                ],
                outputs="top_ten_ranked",
                name="train_tf_model",
            ),
        ]
    )
