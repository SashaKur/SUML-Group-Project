import streamlit as st
import pandas as pd
import os
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path

def recommend_books(filepath, filepath_ratings, filepath_recom):
    st.title("Users' Book Recommendations")

    df_ratings = pd.read_csv(filepath_ratings, sep=",", encoding="latin1")

    # Check if the user has less than 5 ratings
    user_ratings_count = len(df_ratings[df_ratings["User-ID"] == 0])
    if user_ratings_count < 5:
        st.warning("Not enough ratings for recommendation. Please rate more books for better recommendations.")
    else:
        bootstrap_project(Path(filepath))
        with KedroSession.create() as session:
            session.run(pipeline_name="model_build")
        
        df_recommendations = pd.read_csv(filepath_recom, sep=",")
        st.dataframe(df_recommendations)



def main():
    st.set_page_config(page_title="Get a Recommendation", page_icon="📚")

    script_dir = os.path.dirname(__file__)
    filepath = "..\\..\\book-recommendation-ml\\"
    filepath_ratings = "..\\..\\book-recommendation-ml\\data\\01_raw\\BX-Book-Ratings.csv"
    filepath_recom = "..\\..\\book-recommendation-ml\\data\\07_model_output\\recommended_items.csv"


    abs_path = os.path.join(script_dir, filepath)
    abs_path_ratings = os.path.join(script_dir, filepath_ratings)
    abs_path_recoms = os.path.join(script_dir, filepath_recom)


    print(script_dir)

    recommend_books(abs_path, abs_path_ratings, abs_path_recoms)

if __name__ == "__main__":
    main()
