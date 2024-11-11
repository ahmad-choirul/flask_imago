from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'kunci'  # Diperlukan untuk session

@app.route('/')
def index():
    buah = ["apel", "jeruk", "mangga", "pisang", "durian"]
    listdic = [
        {"id": 1, "name": "alice", "category": "A", "sub_category": "X"},
        {"id": 2, "name": "Bob", "category": "B", "sub_category": "Y"},
        {"id": 3, "name": "Charlie", "category": "A", "sub_category": "Z"},
        {"id": 4, "name": "David", "category": "B", "sub_category": "X"}]

    categories = {}
    # Menggunakan listdic untuk mengelompokkan data
    for item in listdic:
        category = item["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append({"id": item["id"], "name": item["name"]})
    
    return render_template('index.html', dic=categories)

@app.route('/parsing', methods=['POST'])
def parsing():
    # Mendapatkan data dari POST request
    data = request.get_json()
    
    if not data:
        return {"error": "No data provided"}, 400
    
    # Mengelompokkan data berdasarkan kategori 
    categories = {}
    for item in data:  # Menggunakan data dari request
        category = item["category"]
        sub_category = item["sub_category"]
        if category not in categories:
            categories[category] = {}
        if sub_category not in categories[category]:
            categories[category][sub_category] = []
        categories[category][sub_category].append(item)
        
    return render_template('index.html', dic=categories)

@app.route('/about/')
def about():
    return '<h1> about us </h1>'

@app.route('/contact/')
def contact():
    return '<h1> contact us </h1>'

@app.route('/profile/')
def profile():
    return '<h1> profile </h1>'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # contoh password manual 
        if username == "admin" and password == "admin123":
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error="Username atau password salah")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

app.run(debug=True)