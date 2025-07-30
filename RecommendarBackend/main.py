from flask import Flask, request, jsonify
from flask_cors import CORS
from tmp import get_cd_recommendations_from_titles, my_cf_recommendation, recommend_knn_titles

app = Flask(__name__)

CORS(app)


@app.route('/genres', methods=['POST'])
def recommend_genres():
    data = request.get_json()
    movie_titles = data.get('titles', [])
    print(movie_titles)

    result = get_cd_recommendations_from_titles(movie_titles, count=5)
    recommended_titles = result['title'].tolist()
    return recommended_titles


@app.route('/colab', methods=['POST'])
def recommend_collaborative_filtering():
    data = request.get_json()
    movie_titles = data.get('titles', [])
    print(movie_titles)

    result = my_cf_recommendation(movie_titles, count=5)
    recommended_titles = result['title'].tolist()
    return recommended_titles


@app.route('/knn', methods=['POST'])
def recommend_knn():
    data = request.get_json()
    movie_titles = data.get('titles', [])
    print(movie_titles)

    result = recommend_knn_titles(movie_titles)
    return result


@app.route('/test', methods=['POST'])
def test():
    return jsonify({
        'result': 'hello world'
    })


if __name__ == '__main__':
    app.run()
