import streamlit as st
import pandas as pd
import os

# Function to browse books
def browse_books(filepath):
    st.title("Book Search")

    columns_to_drop = [
        "Image-URL-S",
        "Image-URL-M",
        "Image-URL-L"
    ]

    df = pd.read_csv(filepath, sep=";", encoding="latin1")
    df.drop(columns_to_drop, axis=1, inplace=True)
    df = df.dropna()
    
    # Create form elements
    title = st.text_input("Enter Title:")
    author = st.text_input("Enter Author:")
    publisher = st.text_input("Enter Publisher")

    print(f"Title Filter: {title}")
    print(f"Author Filter: {author}")
    print(f"Publisher Filter: {publisher}")

    filter_books(df, title, author, publisher)

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
    filepath = "..\\..\\book-recommendation-ml\\data\\01_raw\\BX_Books.csv"
    abs_path = os.path.join(script_dir, filepath)

    print(script_dir)

    browse_books(abs_path)

if __name__ == "__main__":
    main()