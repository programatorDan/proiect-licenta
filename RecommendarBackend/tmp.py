import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from keras.models import load_model
import numpy as np

ratings_data = pd.read_csv('dataset/rating.csv')
movies_data = pd.read_csv('dataset/movie.csv')
movie_ratings_data = pd.merge(ratings_data, movies_data, on='movieId')

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_data['genres'])
cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
title_to_index = pd.Series(movies_data.index, index=movies_data['title']).drop_duplicates()


def get_cd_recommendations_from_titles(titles, count=10):
    copy_factor = count / len(titles)
    rest = count % len(titles)
    input_indices = []
    for title in titles:
        if title in title_to_index:
            input_indices.append(title_to_index[title])
        else:
            print(f'[WARN] Movie title not found in dataset: {title}')
    if not input_indices:
        return []
    sim_scores = []
    for idx in input_indices:
        scores = list(enumerate(cosine_sim_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        if rest > 0:
            rest = rest - 1
            sim_scores.extend(scores[:int(copy_factor+1)])
        else:
            sim_scores.extend(scores[:int(copy_factor)])
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    seen_indices = set(input_indices)
    recommended = []
    for idx, score in sim_scores:
        if idx not in seen_indices:
            recommended.append(idx)
            seen_indices.add(idx)
        if len(recommended) >= count:
            break

    return movies_data.iloc[recommended][['title', 'genres']].reset_index(drop=True)


def my_cf_recommendation(titles, count=10):
    target_movies = movies_data[movies_data['title'].isin(titles)]
    merged = ratings_data.merge(target_movies, on='movieId')
    high_ratings = merged[merged['rating'] >= 4.0]
    user_movie_counts = high_ratings.groupby('userId')['title'].nunique()
    qualified_users = user_movie_counts[user_movie_counts == len(titles)].index.tolist()
    filtered_ratings = ratings_data[ratings_data['userId'].isin(qualified_users)]
    filtered_ratings = filtered_ratings[~filtered_ratings['movieId'].isin(target_movies['movieId'])]
    high_rated_movies = filtered_ratings[filtered_ratings['rating'] >= 4.0]
    recommended = high_rated_movies.groupby('movieId').size().reset_index(name='count')
    recommended = recommended.sort_values(by='count', ascending=False)
    recommendations = recommended.merge(movies_data, on='movieId')

    return recommendations.head(count)


ratings_df = ratings_data.head(1000000)
movis_df = movies_data

num_users = ratings_df['userId'].nunique()
num_movies = ratings_df['movieId'].nunique()
movie_ids = ratings_df['movieId'].unique()

# model = load_model('./models/model100k.h5')
model = load_model('./models/largeModel.h5')


def recommend_for_input_movies(input_movie_ids, top_n=5):
    fake_user_id = 0
    candidate_movie_ids = [m for m in movie_ids if m not in input_movie_ids]

    predictions = model.predict([np.full(len(candidate_movie_ids), fake_user_id), np.array(candidate_movie_ids)],
                                verbose=0)
    top_indices = predictions.flatten().argsort()[::-1][:top_n]
    recommended_movie_ids = [candidate_movie_ids[i] for i in top_indices]

    return recommended_movie_ids


def titles_to_ids(titles):
    ids = movis_df[movis_df['title'].isin(titles)]['movieId'].tolist()
    return ids


def ids_tot_titles(ids):
    titles = movis_df[movis_df['movieId'].isin(ids)]['title'].tolist()
    return titles


def recommend_knn_titles(titles):
    titles_ids = titles_to_ids(titles)
    titles_ids = recommend_for_input_movies(titles_ids)
    recommendations = ids_tot_titles(titles_ids)

    return recommendations


if __name__ == '__main__':
    input_titles = ['Timeline (2003)', 'Toy Story (1995)', 'Insidious (2010)']
    res1 = get_cd_recommendations_from_titles(input_titles)
    print(res1)
    res2 = my_cf_recommendation(input_titles)
    print(res2[['title', 'count']])

    input_movies = ['GoldenEye (1995)', 'To Die For (1995)', 'Black Sheep (1996)']
    converted_ids = titles_to_ids(input_movies)
    recommended_ids = recommend_for_input_movies(converted_ids)
    print("Ids:", recommended_ids)
    recommendations_test = ids_tot_titles(recommended_ids)
    print("Filme recomandate:", recommendations_test)
    input_movies = ["Jurassic Park (1993)", "Star Wars: Episode I - The Phantom Menace (1999)", "Captain America: The First Avenger (2011)", "Divergent (2014)", "Maze Runner, The (2014)", "Insidious (2010)", "Babadook, The (2014)", "Interstellar (2014)", "Life Is Beautiful (La Vita è bella) (1997)"]
    converted_ids = titles_to_ids(input_movies)
    recommended_ids = recommend_for_input_movies(converted_ids)
    print("Ids:", recommended_ids)

    input_movies = ["Godfather: Part II, The (1974)",
    "...And Justice for All (1979)",
    "Lilies of the Field (1963)",
    "Before Sunset (2004)",
    "3-Iron (Bin-jip) (2004)"]
    converted_ids = titles_to_ids(input_movies)
    recommended_ids = recommend_for_input_movies(converted_ids)
    print("Ids:", recommended_ids)

    input_movies = ["Boys of St. Vincent, The (1992)",
    "To Be or Not to Be (1942)",
    "Man Who Would Be King, The (1975)",
    "After Life (Wandafuru raifu) (1998)",
    "Auntie Mame (1958)"]
    converted_ids = titles_to_ids(input_movies)
    recommended_ids = recommend_for_input_movies(converted_ids)
    print("Ids:", recommended_ids)
