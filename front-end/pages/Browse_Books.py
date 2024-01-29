'''
Browse books tab used for browsing and filtering books
'''

import os

import streamlit as st
import pandas as pd

# Function to browse books
def browse_books(filepath_books, filepath_ratings):
    st.title("Book Search")

    user_id = 40943

    columns_to_drop = [
        "Image-URL-S",
        "Image-URL-M",
        "Image-URL-L"
    ]

    df_ratings = pd.read_csv(filepath_ratings, sep=";", encoding="latin1")
    df_books = pd.read_csv(filepath_books, sep=";", encoding="latin1")
    df_books.drop(columns_to_drop, axis=1, inplace=True)
    df_books = df_books.dropna()
    
    # Create form elements
    title = st.text_input("Enter Title:")
    author = st.text_input("Enter Author:")
    publisher = st.text_input("Enter Publisher")

    filter_books(df_books, title, author, publisher)

    st.sidebar.title("Rate Books")

    # Select a book from the sidebar

    isbn = st.sidebar.text_input('Enter ISBN number:')

    # Slider for rating
    rating = st.sidebar.slider("Rate the book (0-10):", 0, 10, 5)

    # Save the user's rating in a separate dataframe or file
    if st.sidebar.button("Submit"):
        user_rating_entry = pd.DataFrame({"User-ID": [user_id],
                                           "ISBN": [isbn], "Book-Rating": [rating]})
        df_ratings = df_ratings[(df_ratings["User-ID"] != user_id) | (df_ratings["ISBN"] != isbn)]
        df_ratings = pd.concat([df_ratings, user_rating_entry], ignore_index=True)

        df_ratings.to_csv(filepath_ratings, index=False, sep=";")

        st.sidebar.success("Rating submitted successfully!")

def filter_books(df, title, author, publisher):
    st.subheader("Filtered Books:")

    filtered_df = df[
        (df["Book-Title"].str.contains(title, case=False)) &
        (df["Book-Author"].str.contains(author, case=False)) &
        (df["Publisher"].str.contains(publisher, case=False))
    ]

    st.dataframe(filtered_df)


def main():
    st.set_page_config(page_title="Book Browser", page_icon="📚")

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join("..","..","book-recommendation-ml", "data", "01_raw")
    filepath_books = os.path.join(filepath, "BX_Books.csv")
    filepath_ratings = os.path.join(filepath, "BX-Book-Ratings.csv")
    abs_path_books = os.path.join(script_dir, filepath_books)
    abs_path_ratings = os.path.join(script_dir, filepath_ratings)

    browse_books(abs_path_books, abs_path_ratings)

if __name__ == "__main__":
    main()
