import sqlite3


def open_connection(func):
    '''
    Декоратор для подключения в БД
    '''

    def inner(*args, **kwargs):
        with sqlite3.connect('./netflix.db') as connect:
            cur = connect.cursor()
            returned_value = func(cur, *args, **kwargs)
            return returned_value

    return inner


@open_connection
def search_title(cur, title):
    '''
    :param cur: - курсор БД
    :param title: - название фильма
    :return: - словарь с информацией о найденном фильме
    '''

    query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title = '{title}' 
            AND type = 'Movie'
            ORDER BY release_year DESC
            LIMIT 1
            """

    cur.execute(query)
    exec_query = cur.fetchall()
    result = []
    if exec_query:
        result.append({'title': exec_query[0][0],
                       'country': exec_query[0][1],
                       'release_year': exec_query[0][2],
                       'listed_in': exec_query[0][3],
                       'description': exec_query[0][4], })

    return result


@open_connection
def search_year_range(cur, year_from, year_to):
    '''
    :param cur: - курсор БД
    :param year_from: - год для поиска "от"
    :param year_to: - год для поиска "до"
    :return: - список с информацией о найденных фильмах
    '''

    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {year_from} AND {year_to}
            ORDER BY release_year DESC
            LIMIT 100
            """

    cur.execute(query)
    exec_query = cur.fetchall()

    result = []
    for entity in exec_query:
        result.append({'title': entity[0],
                       'release_year': entity[1], })

    return result


@open_connection
def search_rating(cur, *rating):
    '''
    :param cur: - курсор БД
    :param rating: - кортеж из рейтингов
    :return: - список с информацией о найденных фильмах
    '''

    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN {rating}
            ORDER BY title DESC
            """

    cur.execute(query)
    exec_query = cur.fetchall()

    result = []
    for entity in exec_query:
        result.append({'title': entity[0],
                       'rating': entity[1],
                       'description': entity[2]})

    return result


@open_connection
def search_genre(cur, genre):
    '''
    :param cur: - курсор БД
    :param genre: - жанр для поиска
    :return: - список с информацией о найденных фильмах
    '''

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
            """

    cur.execute(query)
    exec_query = cur.fetchall()

    result = []
    for entity in exec_query:
        result.append({'title': entity[0],
                       'description': entity[1], })

    return result


@open_connection
def search_matching_actors(cur, actor1, actor2):
    '''
    :param cur: курсор БД
    :param actor1: имя первого актера для поиска
    :param actor2: имя второго актера для поиска
    :return: список актеров, которые снимались с двумя актерами из поиска более 2 раз
    '''

    query = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
            ORDER BY "cast" DESC
            """

    cur.execute(query)
    exec_query = cur.fetchall()

    list_of_actors = []
    # собирает все списки актеров в один
    for item in exec_query:
        list_of_actors = list_of_actors + item[0].split(', ')

    # создает словарь всех актеров и количества их нахождения в общем списке
    dict_of_actors = {i: list_of_actors.count(i) for i in list_of_actors}
    # создает новый список, где нет тех, кто встречался в предыдущем словаре меньше 2 раз
    resulting_list = [k for k, v in dict_of_actors.items() if v >= 2 and k != actor1 and k != actor2]

    return resulting_list


@open_connection
def search_movie_by_type_year_genre(cur, movie_type, year, genre):
    '''
    :param cur: курсов БД
    :param movie_type: тип записи в БД (фильм, сериал)
    :param year: год выпуска
    :param genre: жанр
    :return: список найденных фильмов
    '''

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE type = '{movie_type}'
            AND release_year = {year}
            AND listed_in LIKE '%{genre}%'
            ORDER BY title DESC
            """

    cur.execute(query)
    exec_query = cur.fetchall()

    result = []
    for entity in exec_query:
        result.append({'title': entity[0],
                       'description': entity[1], })

    return result

# print(search_matching_actors('Jack Black', 'Dustin Hoffman'))
# print(search_movie_by_type_year_genre('TV Show', 2019, 'Drama'))
