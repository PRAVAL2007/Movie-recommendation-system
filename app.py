from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load your model and similarity matrix
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Recommendation logic
def recommend_movie(movie):
    try:
        movie_index = model[model['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = [model.iloc[i[0]].title for i in movies_list]
        return recommended_movies
    except IndexError:
        return "Movie not found in the dataset."

# Route to display the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# POST endpoint for recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    movie = data.get('title')

    recommendations = recommend_movie(movie)
    if isinstance(recommendations, str):
        return jsonify({'error': recommendations}), 404  # Movie not found
    else:
        return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)