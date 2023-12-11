"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""
import sys

import pandas as pd
import logging

logger = logging.getLogger("nodes logger")
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
logger.addHandler(stdout_handler)


def merge_datasets(df_books: pd.DataFrame, df_users: pd.DataFrame, df_ratings: pd.DataFrame) -> pd.DataFrame:
    return (df_ratings.merge(df_books, on='ISBN')).merge(df_users, on="User-ID")


def drop_rows_with_nulls(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = ["Image-URL-S", "Image-URL-M", "Image-URL-L"]
    return df.drop(columns=columns_to_drop)


