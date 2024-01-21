import streamlit as st
import pandas as pd
import os

def recommend_books(filepath):
    st.title("Users' Book Recommendations")

    df = pd.read_csv(filepath, sep=",", encoding="latin1")
    unique_user_ids = df['User-ID'].unique().tolist()
    
    user_id = st.selectbox("Choose a user ID to get recommendations from:", options = unique_user_ids)

    filtered_df = df[df['User-ID'] == user_id]
    filtered_df.drop(["User-ID", "Book-Rating"], axis=1, inplace=True)

    st.write(f"Recommended books on the basis of User-{user_id}")
    st.dataframe(filtered_df, use_container_width=True, hide_index = True)


def main():
    st.set_page_config(page_title="Get a Recommendation", page_icon="📚")

    script_dir = os.path.dirname(__file__)
    filepath = "..\\..\\book-recommendation-ml\\data\\07_model_output\\top_ten_ranked.csv"
    abs_path = os.path.join(script_dir, filepath)

    print(script_dir)

    recommend_books(abs_path)

if __name__ == "__main__":
    main()
