from flask import Flask, request, jsonify, render_template
import os
import ast
import json
import numpy as np
import pandas as pd
from .text_pipeline import text_pipeline

# app home directory path
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# path from APP_ROOT to the FullMatrix.csv
FM_PATH = os.path.join(APP_ROOT, 'FullMatrix.csv')
# path from APP_ROOT to the Top1000.csv
T1000PATH = os.path.join(APP_ROOT, 'Top1000.csv')


def filter(nlp):
    name_list = []
    genre_list = []
    person_list = []
    for name, cat in nlp:
        if cat == "MOVIE":
            name_list.append(name)
        elif cat == "PERSON":
            person_list.append(str(name))
        elif cat == "GENRE":
            genre_list.append(name)

    indices = np.array([[name == movie_name_orig for movie_name_orig in movies_df["title"]] for name in name_list])
    indices = np.sum(indices, axis=0).astype(bool) if len(indices) > 0 else [False for i in range(len(movies_df))]
    name_titles = movies_df[indices]
    name_titles = list(name_titles["title"]) if len(name_titles.keys()) > 0 else []

    indices = [[genre in movie_genres for movie_genres in movies_df["genre"]] for genre in genre_list]
    indices = np.sum(indices, axis=0).astype(bool) if len(indices) > 0 else [False for i in range(len(movies_df))]
    genre_titles = movies_df[indices]
    genre_titles = list(genre_titles["title"]) if len(genre_titles.keys()) > 0 else []

    person_titles = np.concatenate([
        np.array([[person in film_actors for film_actors in movies_df["actors"]] for person in person_list]),
        np.array([[person in film_dirs for film_dirs in movies_df["directors"]] for person in person_list])])
    person_titles = np.sum(person_titles, axis=0).astype(bool)
    person_titles = list(movies_df["title"][person_titles]) if person_titles.shape else []

    return name_titles, genre_titles, person_titles


def get_recs(lines, nlp=True, num_recs=10, verbose=False):
    lines = json.loads(lines)
    user_movies = pd.DataFrame(lines).T
    sim_mat = pd.read_csv(FM_PATH).set_index("title")
    if nlp:
        review_sentiment = user_movies["Review"].apply(pipe.gauge_sentiment)  # -> 1 for positive, 0 for negative
        positive_feats = user_movies["Review"][review_sentiment].apply(pipe.extract_features)  # Only use positive
        nlp_feats = []
        for feats_list in positive_feats:
            nlp_feats.extend(feats_list)
        if verbose:
            print("Extracted:", nlp_feats)
        name_titles, genre_titles, people_titles = filter(nlp_feats)

    # Get the names of the highly rated movies
    movie_names = user_movies[user_movies["Rating"].astype(float) >= 8]["Title"]
    movie_names = [movie for movie in movie_names if movie in sim_mat.index]

    # Get the names of the low-rated movies
    exclude = user_movies[user_movies["Rating"].astype(float) <= 4]["Title"]
    exclude = [movie for movie in exclude if movie in sim_mat.index]
    if nlp:
        negative_feats = user_movies["Review"][np.logical_not(review_sentiment)].apply(pipe.extract_features)
        nlp_feats = []
        for feats_list in negative_feats:
            nlp_feats.extend(feats_list)
        if verbose:
            print("Excluding:", nlp_feats)
        exclude.extend(filter(nlp_feats)[0])

    exclude.extend(film for film in sim_mat.index[np.argsort(sim_mat[exclude].values, axis=0).T[:, -2:].flatten()] if
                   film not in movie_names)
    if verbose:
        print("Dropping:", ", ".join(exclude), end="\n\n")
    sim_mat = sim_mat.drop(columns=exclude).T.drop(columns=exclude)
    rec_movies = []

    # Filter out movies we can't recommend, add one random movie from the remaining ones if possible
    def add_rand(movie_list, num=2, prefix=""):
        movie_list = np.unique(movie_list)
        for i in range(num):
            movie_list = [movie for movie in movie_list if movie not in movie_names + rec_movies + exclude]
            if verbose:
                print(prefix + "Movies are: {}".format(", ".join(movie_list)))
            if movie_list:
                rec_movies.append(movie_list[np.random.randint(len(movie_list))])
                if verbose:
                    print("--> chose", rec_movies[-1])
        if verbose:
            print("\n")

    ####################################################################################################################
    # NLP recommendations as are possible
    ####################################################################################################################
    if nlp:
        # Filter down to preferred genres if applicable, and select one of the top two most similar to each movie
        if genre_titles:
            genre_titles = np.unique([g for g in genre_titles + movie_names if g not in exclude])
            genre_mat = sim_mat[genre_titles].T[genre_titles]
            indices = np.argsort(genre_mat[movie_names].values, axis=0)[-2:].T
            poss_movies = [film_name for i, s in enumerate(indices) for film_name in
                           genre_mat[movie_names[i]].iloc[s].index]
            poss_movies = [movie for movie in poss_movies if movie not in movie_names + rec_movies]
            add_rand(poss_movies, num=1 if len(genre_titles) <= 4 else 2, prefix="Genre ")

        # If user mentions movie in positive review, add film to list
        if name_titles:
            name_titles = [n for n in name_titles if n not in movie_names + exclude]
            name_mat = sim_mat[name_titles]
            indices = np.argsort(name_mat[name_titles].values, axis=0).T[:, -4:]
            poss_movies = [film_name for i, s in enumerate(indices) for film_name in name_mat[name_titles[i]].index[s]]
            poss_movies = [movie for movie in poss_movies if movie not in movie_names + rec_movies]
            add_rand(poss_movies, num=1 if len(name_titles) <= 10 else 2, prefix="Name ")

        if people_titles:
            people_titles = [p for p in people_titles if p not in movie_names + exclude]
            people_mat = sim_mat[people_titles]
            indices = np.argsort(people_mat[people_titles].values, axis=0)[-1]
            poss_movies = [people_mat[people_titles[i]].index[s] for i, s in enumerate(indices)]
            poss_movies.extend(people_titles * 2)  # People often like seeing familiar actors/directors in recommendations
            poss_movies = [movie for movie in poss_movies if movie not in movie_names + rec_movies]
            add_rand(poss_movies, num=1 if len(people_titles) <= 2 else 2, prefix="People ")

    ####################################################################################################################
    # Fill remaining slots with recommendations via the graph
    ####################################################################################################################

    num_tog = (num_recs - len(rec_movies)) // 2
    num_sep = num_recs - len(rec_movies) - num_tog

    # Take most similar to all inputs by mean (random from top 5)
    indices = np.argsort(np.mean(sim_mat[movie_names].values, axis=1))[-5:]
    add_rand(sim_mat.index[indices], num=num_tog, prefix="Aggregated Similarity ")

    # Take random movie in five most similar to each one they like
    add_rand([film_name for i in sim_mat[movie_names].T.values for film_name in sim_mat.index[np.argsort(i)[-5:]]],
             num=num_sep, prefix="Individual Similarity ")

    # Randomize order
    np.random.shuffle(rec_movies)
    return rec_movies

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def classify_reviews():
    reviews = request.json['reviews']
    recs = get_recs(json.dumps(reviews))
    # print(recs)
    return jsonify(recs)

@app.route('/')
def home():
    return render_template("content.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)



# Clean data
movies_df = pd.read_csv(T1000PATH)
movies_df.drop(columns=["Unnamed: 0", "votes", "metascore", "year", "certificate", "rating", "simple_desc", "time"], inplace=True)
movies_df["title"] = [i.split("\n")[1] for i in movies_df["title"]]
movies_df["genre"] = movies_df["genre"].str.split(", ")
movies_df["directors"] = movies_df["directors"].astype(str)
movies_df["actors"] = [", ".join(a) for a in movies_df["actors"].apply(ast.literal_eval)]
movies_df.drop_duplicates(subset=["title"], inplace=True)
movies_df.index = [i for i in range(len(movies_df))]

pipe = text_pipeline()

# import time
# start_time = time.time()
# print(get_recs(lines))
# print("Time for 1 was", time.time() - start_time)
# start_time = time.time()
# print(get_recs(lines, num_recs=10, nlp=False))
# print("Time for 2 was", time.time()-start_time)
