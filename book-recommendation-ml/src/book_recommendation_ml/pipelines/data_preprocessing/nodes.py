"""
This is a boilerplate pipeline 'data_preparation'
generated using Kedro 0.18.14
"""
import sys

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger("nodes logger")
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
logger.addHandler(stdout_handler)


def merge_datasets(
    df_books: pd.DataFrame, df_users: pd.DataFrame, df_ratings: pd.DataFrame
) -> pd.DataFrame:
    return (df_ratings.merge(df_books, on="ISBN")).merge(df_users, on="User-ID")


def drop_rows_with_nulls(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


def drop_year_zero_rows(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(df[df["Year-Of-Publication"] == 0].index, inplace=True)
    return df


def drop_rating_zero_rows(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(df[df["Book-Rating"] == 0].index, inplace=True)
    return df


def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = [
        "Image-URL-S",
        "Image-URL-M",
        "Image-URL-L",
        "Book-Title",
        "Publisher",
    ]
    return df.drop(columns=columns_to_drop)


def make_isbn_numeric(df: pd.DataFrame) -> pd.DataFrame:
    isbn_list = df.ISBN.unique()

    def get_isbn_numeric_id(isbn):
        item_index = np.where(isbn_list == isbn)
        return item_index[0][0]

    df["ISBN"] = df["ISBN"].apply(get_isbn_numeric_id)

    return df
