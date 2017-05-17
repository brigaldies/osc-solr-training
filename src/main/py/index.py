import json

import pysolr


def read_movies(filename):
    print('Reading movies from {0}'.format(filename))
    f = open(filename)
    print(filename + ' opened.')
    if f:
        movies = json.loads(f.read())
        # print(type(movies))
        print('{0} movies loaded.'.format(len(movies)))

        # Display the first movie's title
        keys = movies.keys()
        # print(type(keys))
        print(movies[list(keys)[0]]['title'])
        return movies
    else:
        print("Can't read {0}".format(filename))


def index_movies(solr, movies):
    print("Constructing documents...")
    documents = []
    for key, movie in movies.items():
        genres = []
        for genre in movie["genres"]:
            genres.append(genre["name"])
        casts = []
        for cast in movie["cast"]:
            casts.append(cast["name"])
        doc = {
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie["overview"],
            "genres": genres,
            "cast_name": casts
        }
        documents.append(doc)

    print("Adding documents to Solr...")
    resp = solr.add(documents, commit=True)
    print(resp)
    return resp


def connect(url):
    print('Connecting to Solr at {0}...'.format(url))
    solr = pysolr.Solr(url, timeout=10)
    print('Connected!')
    print(solr)
    return solr


def search(solr, search_string):
    print('Searching {0}...'.format(search_string))
    results = solr.search(search_string)
    print("{0} result(s).".format(len(results)))


def main():
    # Read movies from the Json file
    movies = read_movies("tmdb.json")
    solr = connect('http://localhost:8983/solr/movies/')
    index_movies(solr, movies)
    # search(solr, 'blade runner')


if __name__ == "__main__":
    main()
