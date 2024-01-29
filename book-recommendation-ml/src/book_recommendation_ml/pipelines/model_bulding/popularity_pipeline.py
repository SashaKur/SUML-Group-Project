'''
Code for creating and defining popularity pipeline
'''

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import get_popular_books

def create_popularity_books_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=get_popular_books,
                inputs=["book_ratings", "books"],
                outputs="popular_books",
                name="get_popular_books_node",
            ),
        ]
    )
