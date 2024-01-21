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
        "Book-Author",
        "Publisher",
        "Year-Of-Publication",
    ]
    df.drop(columns_to_drop, axis=1, inplace=True)
    return df


def make_isbn_numeric(df: pd.DataFrame) -> pd.DataFrame:
    isbn_list = df.ISBN.unique()

    def get_isbn_numeric_id(isbn):
        item_index = np.where(isbn_list == isbn)
        return item_index[0][0]

    df["ISBN"] = df["ISBN"].apply(get_isbn_numeric_id)

    return df


def make_book_rating_dataset(
    df_books: pd.DataFrame, df_ratings: pd.DataFrame
) -> pd.DataFrame:
    return pd.merge(df_ratings, df_books, on="ISBN")


def filter_books_by_ratings(
    df_book_rating: pd.DataFrame, threshold: int = 25
) -> pd.DataFrame:
    rating_count = (
        df_book_rating.groupby(by=["Book-Title"])["Book-Rating"]
        .count()
        .reset_index()
        .rename(columns={"Book-Rating": "RatingCount_book"})[
            ["Book-Title", "RatingCount_book"]
        ]
    )

    rating_count = rating_count.query("RatingCount_book >= @threshold")

    return rating_count


def get_user_rating(rating_count: pd.DataFrame, book_rating: pd.DataFrame):
    return pd.merge(
        rating_count,
        book_rating,
        left_on="Book-Title",
        right_on="Book-Title",
        how="left",
    )


def filter_users_by_ratings(
    df_user_rating: pd.DataFrame, threshold: int = 20
) -> pd.DataFrame:
    user_count = (
        df_user_rating.groupby(by=["User-ID"])["Book-Rating"]
        .count()
        .reset_index()
        .rename(columns={"Book-Rating": "RatingCount_user"})[
            ["User-ID", "RatingCount_user"]
        ]
    )

    user_count = user_count.query("RatingCount_user >= @threshold")

    return user_count


def combine(user_rating: pd.DataFrame, user_count: pd.DataFrame):
    return user_rating.merge(
        user_count, left_on="User-ID", right_on="User-ID", how="inner"
    )
