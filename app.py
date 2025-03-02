from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

users = {}

blog_posts = [
    {
        'id': 1,
        'title': 'AMALYMPICS',
        'content': 'This blog captures some of the best moments from the event, highlighting teamwork, sportsmanship, and unforgettable experiences.',
        'date': datetime(2024, 1, 15),
        'image': 'blog1.png'
    },
    {
        'id': 2,
        'title': 'BEACH',
        'content': 'Nothing compares to the calming waves and breathtaking sunsets by the beach.',
        'date': datetime(2024, 1, 20),
        'image': 'blog2.png'
    },
    {
        'id': 3,
        'title': 'POLYSPORTS',
        'content': 'This blog post highlights the energy and dedication of individuals working on their fitness goals and enjoying the vibrant sports atmosphere.',
        'date': datetime(2024, 1, 25),
        'image': 'blog3.png'
    },
    {
        'id': 4,
        'title': 'ENCHANTED RIVER',
        'content': 'This post captures its natural beauty, the myths surrounding its mysterious waters, and the breathtaking experience of visiting such a magical place.',
        'date': datetime(2024, 1, 30),
        'image': 'blog4.png'
    },
    {
        'id': 5,
        'title': 'RASPBERRY PI',
        'content': 'Exploring the world of Raspberry Pi—this post delves into my latest projects, experiments, and the limitless possibilities of this powerful yet compact device in tech and automation.',
        'date': datetime(2024, 2, 5),
        'image': 'blog5.png'
    }
]

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def landing():
    return redirect(url_for('register'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('error.html', message='Username and password are required')
        
        if username in users:
            return render_template('error.html', message='Username already exists')
        
        users[username] = password
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('error.html', message='Username and password are required')
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        
        return render_template('error.html', message='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/blog')
def blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('blog.html', posts=blog_posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return render_template('error.html', message='Post not found')
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)