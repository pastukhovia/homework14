from flask import Flask, jsonify
from utils import search_title, search_year_range, search_rating, search_genre

app = Flask(__name__)


@app.route('/movie/<title>')
def movie_search(title):
    result = search_title(title)
    return jsonify(result)


@app.route('/movie/<year_from>/to/<year_to>')
def movie_search_year_range(year_from, year_to):
    result = search_year_range(year_from, year_to)
    return jsonify(result)


@app.route('/rating/children')
def search_children_rating():
    # Вместе с G передается случайное слово, потому что по-другому не работает ¯\_(ツ)_/¯.
    # В конце концов, рейтинга фывфыва не существует, и он не повлияет на результаты поиска
    result = search_rating('G', 'фывфыва')
    return jsonify(result)


@app.route('/rating/family')
def search_family_rating():
    result = search_rating('G', 'PG', 'PG-13')
    return jsonify(result)


@app.route('/rating/adult')
def search_adult_rating():
    result = search_rating('R', 'NC-17')
    return jsonify(result)


@app.route('/genre/<genre>')
def search_movie_genre(genre):
    result = search_genre(genre)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
