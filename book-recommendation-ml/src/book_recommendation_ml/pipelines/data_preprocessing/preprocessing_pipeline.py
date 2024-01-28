from kedro.pipeline import Pipeline, node, pipeline

from .nodes import books_cleanup, merge_datasets, add_length_column, add_age_bins, age_column_cleanup, get_rating_stats, year_column_cleanup, select_optimal_books

def create_preprocessing_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=books_cleanup,
                inputs=["books"],
                outputs="books_cleaned",
                name="books_cleanup_node",
            ),
            node(
                func=merge_datasets,
                inputs=["books_cleaned", "book_ratings", "users"],
                outputs="merged_data",
                name="merge_datasets_node",
            ),
            node(
                func=add_length_column,
                inputs=["merged_data"],
                outputs="merged_data_with_length",
                name="add_length_column_node",
            ),
            node(
                func=add_age_bins,
                inputs=["merged_data_with_length"],
                outputs="merged_data_with_age_bins",
                name="add_age_bins_node",
            ),
            node(
                func=age_column_cleanup,
                inputs=["merged_data_with_age_bins"],
                outputs="merged_data_age_clean",
                name="age_column_cleanup_node",
            ),
            node(
                func=get_rating_stats,
                inputs=["merged_data_age_clean"],
                outputs="meged_data_rated",
                name="get_rating_stats_node",
            ),
            node(
                func=year_column_cleanup,
                inputs=["meged_data_rated"],
                outputs="clean_merged_data",
                name="year_column_cleanup_node",
            ),
            node(
                func=select_optimal_books,
                inputs=["clean_merged_data"],
                outputs="primary_data",
                name="select_optimal_books_node",
            ),
        ]
    )