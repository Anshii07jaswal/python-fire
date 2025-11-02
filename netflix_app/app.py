"""
Netflix-like Web Application
A Flask-based streaming platform UI inspired by Netflix
"""

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'netflix-clone-secret-key-2025'

# Load movie data
def load_movies():
    """Load movie data from JSON file"""
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'movies.json')
    with open(data_path, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    """Home page with featured content"""
    return render_template('index.html')

@app.route('/browse')
def browse():
    """Browse all content"""
    return render_template('browse.html')

@app.route('/api/movies')
def get_movies():
    """API endpoint to get all movies"""
    movies = load_movies()
    return jsonify(movies)

@app.route('/api/movies/category/<category>')
def get_movies_by_category(category):
    """API endpoint to get movies by category"""
    movies = load_movies()
    filtered = [m for m in movies['movies'] if category.lower() in [c.lower() for c in m.get('categories', [])]]
    return jsonify({'movies': filtered})

@app.route('/api/search')
def search():
    """API endpoint for search"""
    query = request.args.get('q', '').lower()
    movies = load_movies()
    
    if not query:
        return jsonify({'movies': []})
    
    results = [
        m for m in movies['movies'] 
        if query in m['title'].lower() or query in m['description'].lower()
    ]
    
    return jsonify({'movies': results})

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
