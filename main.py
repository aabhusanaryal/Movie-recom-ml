import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# define a function that creates similarity matrix
# if it doesn't exist
def create_sim():
    data = pd.read_csv('data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data,sim


# defining a function that recommends 10 most similar movies
def rcmd(m):
    m = m.lower()
    # check if data and sim are already assigned
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    # check if the movie is in our database or not
    if m not in data['movie_title'].unique():
        return('This movie is not in our database.\nPlease check if you spelled it correct.')
    else:
        # getting the index of the movie in the dataframe
        i = data.loc[data['movie_title']==m].index[0]

        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

        # taking top 1- movie scores
        # not taking the first index since it is the same movie
        lst = lst[1:11]

        # making an empty list that will containg all 10 movie recommendations
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    return send_from_directory('static/frontend', 'index.html')

@app.route("/recommend/<movie>")
def recommend(movie):
    r = rcmd(movie)
    movie = movie.upper()
    success = True
    # If the movie is not found
    if type(r)==type('string'):
        success = False
    return jsonify({'success': success, 'data': r})

@app.route("/recommend/")
def recom():
    return jsonify({'data': 'Please use the format /recommend/movie-name'})



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
