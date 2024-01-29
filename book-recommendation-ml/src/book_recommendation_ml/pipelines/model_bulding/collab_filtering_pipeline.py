'''
Code for creating and defining collab filtering pipeline
'''

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import select_eager_users, singular_val_decompose, recommend_items

def create_model_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=select_eager_users,
                inputs=["book_ratings", "books"],
                outputs="pivot_matrix",
                name="select_eager_users_node",
            ),
            node(
                func=singular_val_decompose,
                inputs=["pivot_matrix"],
                outputs="cf_preds_df",
                name="singular_val_decompose_node",
            ),
            node(
                func=recommend_items,
                inputs=["pivot_matrix", "params:user_id", "params:top_n"],
                outputs="recommended_items",
                name="recommend_items_node",
            ),
        ]
    )
