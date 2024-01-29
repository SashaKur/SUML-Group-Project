'''
Recommend books page used for recommendations based on 
popularity and colaborative filtering approaches
'''

import os
from pathlib import Path

import streamlit as st
import pandas as pd
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

def recommend_books(filepath, filepath_ratings, filepath_recom, filepath_popular):
    st.title("Users' Book Recommendations")

    df_ratings = pd.read_csv(filepath_ratings, sep=";", encoding="latin1")

    # Check if the user has less than 5 ratings
    user_ratings_count = len(df_ratings[df_ratings["User-ID"] == 40943])

    if st.sidebar.button("Get popular books"):
        bootstrap_project(Path(filepath))
        with KedroSession.create(conf_source="conf") as session:
            session.run(pipeline_name="popular_books")

        df_recommendations = pd.read_csv(filepath_popular, sep=",")
        st.dataframe(df_recommendations[["Book-Title", "avg_rating"]],
                      hide_index=True, use_container_width=True)

    if st.sidebar.button("Get recommendations"):
        if user_ratings_count < 5:
            st.warning("Not enough ratings for recommendation. Please rate more books for better recommendations.")
        else:
            bootstrap_project(Path(filepath))
            with KedroSession.create(conf_source="conf") as session:
                session.run(pipeline_name="model_build")

            df_recommendations = pd.read_csv(filepath_recom,
                                              sep=",")
            st.dataframe(df_recommendations["Book-Title"],
                             hide_index=True, use_container_width=True)

def main():
    st.set_page_config(page_title="Get a Recommendation", page_icon="📚")

    script_dir = os.path.dirname(__file__)

    filepath = os.path.join("..","..","book-recommendation-ml")
    filepath_recom = os.path.join(filepath, "data", "07_model_output", "recommended_items.csv")
    filepath_popular = os.path.join(filepath, "data", "07_model_output", "popular_books.csv")
    filepath_ratings = os.path.join(filepath, "data", "01_raw", "BX-Book-Ratings.csv")


    abs_path = os.path.abspath(os.path.join(script_dir, filepath))
    abs_path_ratings = os.path.join(script_dir, filepath_ratings)
    abs_path_recoms = os.path.join(script_dir, filepath_recom)
    abs_path_popular = os.path.join(script_dir, filepath_popular)


    print(script_dir)

    recommend_books(abs_path, abs_path_ratings, abs_path_recoms, abs_path_popular)

if __name__ == "__main__":
    main()
