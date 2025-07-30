import pandas as pd
from sklearn.model_selection import train_test_split
from tmp import my_cf_recommendation, get_cd_recommendations_from_titles, recommend_knn_titles

ratings_data = pd.read_csv('dataset/rating.csv')
movies_data = pd.read_csv('dataset/movie.csv')
ratings_df = ratings_data.head(1000000)
movis_df = movies_data

train_data, test_data = train_test_split(ratings_data, test_size=0.2)


def evaluate_cf_precision(user_id, k=10):
    # Filmele pe care utilizatorul le-a evaluat pozitiv în setul de test
    user_test_ratings = test_data[(test_data['userId'] == user_id) & (test_data['rating'] >= 4.0)]
    if user_test_ratings.empty:
        return None  # Nu are ratinguri relevante în test

    # Alege câteva filme pe care le-a evaluat pozitiv în setul de train
    user_train_ratings = train_data[(train_data['userId'] == user_id) & (train_data['rating'] >= 4.0)]
    movie_ids = user_train_ratings['movieId'].tolist()
    titles = movies_data[movies_data['movieId'].isin(movie_ids)]['title'].tolist()

    if not titles:
        return None  # Nu are filme suficiente în train

    # Recomandă pe baza acelor filme
    recommended = my_cf_recommendation(titles, count=k)
    recommended_ids = recommended['movieId'].tolist()

    # Compară cu filmele relevante din test
    relevant_in_test = set(user_test_ratings['movieId'].tolist())
    relevant_recommended = [mid for mid in recommended_ids if mid in relevant_in_test]

    precision = len(relevant_recommended) / k
    return precision


def evaluate_cb_precision(user_id, k=10):
    # Filmele evaluate pozitiv de utilizator în setul de test
    user_test_ratings = test_data[(test_data['userId'] == user_id) & (test_data['rating'] >= 4.0)]
    if user_test_ratings.shape[0] < 2:
        return None  # Nu avem destule date

    # Filmele din train pe care utilizatorul le-a evaluat pozitiv
    user_train_ratings = train_data[(train_data['userId'] == user_id) & (train_data['rating'] >= 4.0)]
    train_movies = user_train_ratings['movieId'].tolist()
    if not train_movies:
        return None

    # Alegem 1-2 titluri ca bază pentru recomandare
    input_movies = movies_data[movies_data['movieId'].isin(train_movies)]['title'].tolist()
    input_titles = input_movies[:min(2, len(input_movies))]

    # Generăm recomandări
    recommendations = get_cd_recommendations_from_titles(input_titles, count=k)
    recommended_titles = recommendations['title'].tolist()

    # Filmele pe care utilizatorul le-a evaluat pozitiv în test
    relevant_titles = movies_data[movies_data['movieId'].isin(user_test_ratings['movieId'])]['title'].tolist()

    # Calculăm precizia
    relevant_recommended = [title for title in recommended_titles if title in relevant_titles]
    precision = len(relevant_recommended) / k
    return precision


def evaluate_knn_precision(user_id, k=10):
    user_test_ratings = test_data[(test_data['userId'] == user_id) & (test_data['rating'] >= 4.0)]
    if user_test_ratings.shape[0] < 2:
        return None  # prea puține date

    user_train_ratings = train_data[(train_data['userId'] == user_id) & (train_data['rating'] >= 4.0)]
    train_movie_ids = user_train_ratings['movieId'].tolist()

    if not train_movie_ids:
        return None

    input_titles = movis_df[movis_df['movieId'].isin(train_movie_ids)]['title'].tolist()[:min(2, len(train_movie_ids))]

    recommended_titles = recommend_knn_titles(input_titles)

    # Filme relevante (vizionate și apreciate de utilizator în test)
    relevant_titles = movis_df[movis_df['movieId'].isin(user_test_ratings['movieId'])]['title'].tolist()

    matched = [title for title in recommended_titles if title in relevant_titles]

    precision = len(matched) / k
    return precision


def evaluate_cb_recall(user_id, k=10):
    test_user = test_data[(test_data['userId'] == user_id) & (test_data['rating'] >= 4.0)]
    train_user = train_data[(train_data['userId'] == user_id) & (train_data['rating'] >= 4.0)]

    if len(test_user) < 2 or len(train_user) < 1:
        return None

    train_titles = movis_df[movis_df['movieId'].isin(train_user['movieId'])]['title'].tolist()[:2]
    recommendations = get_cd_recommendations_from_titles(train_titles, count=k)
    recommended_titles = recommendations['title'].tolist()

    relevant_titles = movis_df[movis_df['movieId'].isin(test_user['movieId'])]['title'].tolist()
    matched = [title for title in recommended_titles if title in relevant_titles]

    recall = len(matched) / len(relevant_titles)
    return recall


def evaluate_cf_recall(user_id, k=10):
    test_user = test_data[(test_data['userId'] == user_id) & (test_data['rating'] >= 4.0)]
    train_user = train_data[(train_data['userId'] == user_id) & (train_data['rating'] >= 4.0)]

    if len(test_user) < 2 or len(train_user) < 1:
        return None

    train_titles = movis_df[movis_df['movieId'].isin(train_user['movieId'])]['title'].tolist()[:2]
    recommendations = my_cf_recommendation(train_titles, count=k)
    recommended_titles = recommendations['title'].tolist()

    relevant_titles = movis_df[movis_df['movieId'].isin(test_user['movieId'])]['title'].tolist()
    matched = [title for title in recommended_titles if title in relevant_titles]

    recall = len(matched) / len(relevant_titles)
    return recall


def evaluate_knn_recall(user_id, k=10):
    test_user = test_data[(test_data['userId'] == user_id) & (test_data['rating'] >= 4.0)]
    train_user = train_data[(train_data['userId'] == user_id) & (train_data['rating'] >= 4.0)]

    if len(test_user) < 2 or len(train_user) < 1:
        return None

    train_titles = movis_df[movis_df['movieId'].isin(train_user['movieId'])]['title'].tolist()[:2]
    recommended_titles = recommend_knn_titles(train_titles)[:k]

    relevant_titles = movis_df[movis_df['movieId'].isin(test_user['movieId'])]['title'].tolist()
    matched = [title for title in recommended_titles if title in relevant_titles]

    recall = len(matched) / len(relevant_titles)
    return recall


if __name__ == '__main__':
    user_ids = test_data['userId'].unique()
    cf_precisions = []
    cb_precisions = []
    knn_precisions = []
    cb_recalls = []
    cf_recalls = []
    knn_recalls = []

    for uid in user_ids[:100]:  # Testează pe 100 de utilizatori
        p_cf = evaluate_cf_precision(uid)
        p_cd = evaluate_cb_precision(uid)
        p_knn = evaluate_knn_precision(uid)
        r_cb = evaluate_cb_recall(uid)
        r_cf = evaluate_cf_recall(uid)
        r_knn = evaluate_knn_recall(uid)

        if p_cf is not None:
            cf_precisions.append(p_cf)
        if p_cd is not None:
            cb_precisions.append(p_cd)
        if p_knn is not None:
            knn_precisions.append(p_knn)
        if r_cb is not None:
            cb_recalls.append(r_cb)
        if r_cf is not None:
            cf_recalls.append(r_cf)
        if r_knn is not None:
            knn_recalls.append(r_knn)

    average_cf_precision = sum(cf_precisions) / len(cf_precisions)
    print(f"Precizia medie (CF): {average_cf_precision:.4f}")

    if cb_precisions:
        avg_cb_precision = sum(cb_precisions) / len(cb_precisions)
        print(f"Precizia medie (Content-Based): {avg_cb_precision:.4f}")
    else:
        print("Niciun utilizator valid pentru testarea Content-Based.")

    if knn_precisions:
        avg_knn_precision = sum(knn_precisions) / len(knn_precisions)
        print(f"Precizia medie pentru recommend_knn_titles: {avg_knn_precision:.4f}")
    else:
        print("Nu am găsit utilizatori valizi pentru test.")

    print(f"Recall@10 mediu CB:  {sum(cb_recalls) / len(cb_recalls):.4f}" if cb_recalls else "Fără date CB")
    print(f"Recall@10 mediu CF:  {sum(cf_recalls) / len(cf_recalls):.4f}" if cf_recalls else "Fără date CF")
    print(f"Recall@10 mediu KNN: {sum(knn_recalls) / len(knn_recalls):.4f}" if knn_recalls else "Fără date KNN")
