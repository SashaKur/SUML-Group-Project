import sys

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger("nodes logger")
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.addFilter(lambda rec: rec.levelno <= logging.INFO)
logger.addHandler(stdout_handler)


# -------- Helper functions ----------
def change_title(str1,str2):
    #changing the title of books
    str1 = str1 +" "+'by' +" "+str2
    return str1

# a function to extract the country names
def get_country(x):
    return x.split(',')[-1]

# ------------------------------------


def books_cleanup(df_books: pd.DataFrame) -> pd.DataFrame:

    df_books['Book-Author'].fillna('Unknown',inplace=True)
    df_books['new_title'] = df_books.apply(lambda x : change_title(x['Book-Title'],x['Book-Author']),axis = 1)

    df_books = df_books.drop_duplicates(subset='new_title',keep='first')

    return df_books

def merge_datasets(df_books: pd.DataFrame, df_ratings: pd.DataFrame, df_users: pd.DataFrame) -> pd.DataFrame:
   
    #merging all the three dataset
    df_merged = df_ratings.merge(df_books,how='inner',on='ISBN')
    df_merged = df_merged.merge(df_users,how='inner',on='User-ID')

    return df_merged

def add_length_column(df_merged: pd.DataFrame) -> pd.DataFrame:

    #adding a new column that measures the length of the title
    df_merged['Title-Length'] = df_merged['Book-Title'].apply(len)
    df_merged['Year-Of-Publication'] = pd.to_numeric(df_merged['Year-Of-Publication'], errors='coerce').fillna(2099, downcast = 'infer')


    # extracting countries from location column
    df_merged['Location'] = df_merged['Location'].apply(get_country)

    return df_merged


def add_age_bins(df_merged: pd.DataFrame) -> pd.DataFrame:

    # Create age groups using age column
    bins = [-1,12,20,50,100]
    labels = ['Kid','Teenager','Adult','Old']
    df_merged['age_bins'] = pd.cut(x=df_merged['Age'], bins=bins,labels=labels)

    # Number of outliers
    outliers = sum(df_merged['Age']>90)
    print(outliers)

    # Handling outliers by randomly replacing age >90 by values between 90 and 100
    age2 = df_merged['Age'].copy()
    random_age2 = np.random.randint(90,100,outliers)
    age2[df_merged['Age']>90]=random_age2
    df_merged['Age'] = age2

    return df_merged

def age_column_cleanup(df_merged: pd.DataFrame) -> pd.DataFrame:

    # Null values in age column
    nulls = sum(df_merged['Age'].isnull())

    # Replacing null values
    median = df_merged['Age'].median()
    std = df_merged['Age'].std()
    random_age = np.random.randint(median - std, median + std, size = nulls)
    age = df_merged['Age'].copy()
    age[pd.isnull(age)] = random_age
    df_merged['Age'] = age
    df_merged['Age'] = df_merged['Age'].astype(int)

    return df_merged

def get_rating_stats(df_merged: pd.DataFrame) -> pd.DataFrame:

    # Calculating the rating count and mean rating given to each book by the user.
    rating_count = df_merged.groupby('Book-Title')['Book-Rating'].count().to_frame()
    rating_mean = df_merged.groupby('Book-Title')['Book-Rating'].mean().to_frame()

    # Renaming the column names before merging them with the final dataset.
    rating_count.rename(columns={'Book-Rating':'Rating-Count'}, inplace=True)
    rating_mean.rename(columns={'Book-Rating':'Rating-Mean'}, inplace=True)

    df_merged = pd.merge(df_merged, rating_count, on='Book-Title', how='inner')
    df_merged = pd.merge(df_merged, rating_mean, on='Book-Title', how='inner')

    # rounding off the rating mean feature to 2 decimal points
    df_merged['Rating-Mean'] = df_merged['Rating-Mean'].round(2)

    df_merged.drop(columns=['Image-URL-M','Image-URL-S','Image-URL-L'],inplace=True)

    return df_merged

def year_column_cleanup(df_merged: pd.DataFrame) -> pd.DataFrame:

    # Casting Year-Of-Publication to numeric datatype and removing all String Noice Values using coerce functionality.
    df_merged['Year-Of-Publication'] = pd.to_numeric(df_merged['Year-Of-Publication'], 'coerce')

    # Removing all the integer Noice Values from the Dataset since the dataset used contains only books released before 2007.
    df_merged = df_merged[(df_merged['Year-Of-Publication']<=2006)]

    return df_merged

def select_optimal_books(df_merged: pd.DataFrame) -> pd.DataFrame:

    # counting the ratings per ISBN
    books_reduce=df_merged.groupby(['ISBN'])['Book-Rating'].count().reset_index().sort_values('Book-Rating',ascending=False)
    
    #Considering all the counts greater than 10
    reduced_books=books_reduce[books_reduce['Book-Rating']>10]['ISBN']

    #merging it with the original dataset
    df_merged=df_merged.merge(reduced_books,how='inner',left_on='ISBN',right_on='ISBN')

    return df_merged
