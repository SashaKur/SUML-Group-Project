import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

# --- Nodes for collaborative filtering model ---

def select_eager_users(df_ratings: pd.DataFrame, df_books: pd.DataFrame) -> pd.DataFrame:
        #Selecting users who have given more than 200 ratings
        #Merging Books and Ratings dataframes
        ratings_with_name = df_ratings.merge(df_books,on='ISBN')
        x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 4
        reliable_users = x[x].index

        filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(reliable_users)]

        #Selecting top 50 books with highest number of rating 
        y = filtered_rating.groupby('Book-Title').count()['Book-Rating']>=50
        famous_books = y[y].index

        final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

        #Applying Pivot table on final_ratings dataframe
        pt = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
        pt.fillna(0,inplace=True)

        return pt


def singular_val_decompose(users_items_pivot_matrix : pd.DataFrame) -> pd.DataFrame:
        
        # The number of factors to factor the user-item matrix.
        NUMBER_OF_FACTORS_MF = 15

        pt_sparse = csr_matrix(users_items_pivot_matrix.fillna(0))

        #Performs matrix factorization of the original user item matrix
        U, sigma, Vt = svds(pt_sparse, k = NUMBER_OF_FACTORS_MF)

        sigma = np.diag(sigma) 
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) 

        #Converting the reconstructed matrix back to a Pandas dataframe
        cf_preds_df = pd.DataFrame(all_user_predicted_ratings, columns = users_items_pivot_matrix.columns)
        
        return cf_preds_df


def recommend_items(cf_predictions_df: pd.DataFrame, user_id, topn=10, items_to_ignore=[]) -> pd.DataFrame:
        # Get and sort the user's predictions
        sorted_user_predictions = cf_predictions_df[user_id].sort_values(ascending=False).reset_index().rename(columns={user_id: 'recStrength'})

        # Recommend the highest predicted rating content that the user hasn't seen yet.
        recommendations_df = sorted_user_predictions[~sorted_user_predictions['Book-Title'].isin(items_to_ignore)].sort_values('recStrength', ascending = False).head(topn)

        return recommendations_df

# --------------------------------------------------

# --- Node for popularity based recommendations ---

def get_popular_books(df_ratings: pd.DataFrame, df_books: pd.DataFrame) -> pd.DataFrame:
        # Merging Books and Ratings dataframes
        ratings_with_name = df_ratings.merge(df_books, on='ISBN')

        # Counting the number of ratings for each book
        num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()

        num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

        # Calculating the average rating for each book
        avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
        avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)

        # Merging num_rating and avg_rating dataframes on the 'Book-Title' column
        popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')

        # Sorting books that have received more than 250 ratings and highest average ratings
        popular_df = popular_df[popular_df['num_ratings'] >= 250].sort_values('avg_rating', ascending=False)

        # Merging with the 'df_books' DataFrame on 'Book-Title'
        popular_df = popular_df.merge(df_books, on='Book-Title')

        return popular_df

# --------------------------------------------------
    