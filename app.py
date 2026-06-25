from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# =======================================================
# 1. DIABETES PREDICTION CONFIGURATION
# =======================================================
try:
    diabetes_model = pickle.load(open('model.pkl', 'rb'))
except Exception as e:
    print("Diabetes model loading error:", e)

@app.route('/diabetes')
def diabetes_home():
    return render_template('diabetes_predict.html')

@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    if request.method == 'POST':
        try:
            # Fetching features by their exact HTML input name attribute
            input_features = [
                float(request.form['pregnancies']),
                float(request.form['glucose']),
                float(request.form['blood_pressure']),
                float(request.form['skin_thickness']),
                float(request.form['insulin']),
                float(request.form['bmi']),
                float(request.form['dpf']),
                float(request.form['age'])
            ]
            
            # Direct prediction using the 8 features array
            prediction = diabetes_model.predict([input_features])
            
            if prediction == 1:
                res_val = "Diabetes Positive"
            else:
                res_val = "Diabetes Negative"
                
            return render_template('diabetes_predict.html', prediction_text=f'Result: {res_val}')
        except Exception as e:
            return render_template('diabetes_predict.html', prediction_text=f'Error: {str(e)}')

# =======================================================
# 2. MOVIE RECOMMENDATION CONFIGURATION
# =======================================================
try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    print("Movie model loading error:", e)

@app.route('/')
@app.route('/movie')
def movie_home():
    return render_template('index.html', movie_list=movies['title'].values)

@app.route('/recommend_movie', methods=['POST'])
def recommend_movie():
    selected_movie = request.form.get('movie_name')
    if not selected_movie:
        return render_template('index.html', movie_list=movies['title'].values)
        
    try:
        movie_index = movies[movies['title'] == selected_movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
            
        return render_template('index.html', 
                               movie_list=movies['title'].values, 
                               recommendations=recommended_movies, 
                               selected_movie=selected_movie)
    except Exception as e:
        return render_template('index.html', movie_list=movies['title'].values, error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
