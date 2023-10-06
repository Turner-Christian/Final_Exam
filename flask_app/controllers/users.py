from flask_app import app
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask_app.controllers import trees
from flask import flash,render_template,redirect,session,request
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register_page')
def register_page():
    if 'user_id' in session:
        return redirect('/arbortrary')
    return render_template('index.html')

# INDEX -->register<--
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/arbortrary')
    return render_template('landing.html')

# --> login page <--
@app.route('/login_page')
def login_page():
    if 'user_id' in session:
        return redirect('/arbortrary')
    return (render_template('login.html'))

# MAIN DASHBOARD 
@app.route('/arbortrary')
def arbortrary():
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id' : session['user_id'] }
    user = User.id_in_db(data)
    trees = Tree.get_all_trees()
    return render_template('arbortrary.html', user=user, trees=trees)


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# REGISTER USER
@app.route('/register', methods=['POST'])
def register():
    email = { 'email' : request.form['email'] }
    if not User.vald_user_reg(request.form):
        return redirect('/register_page')
    if request.form['password'] != request.form['confirm_password']:
        flash('Passwords do not match', 'register')
        return redirect('/register_page')
    if User.if_user_in_db(email) == True:
        flash('Email is already registered', 'register')
        return redirect('/register_page')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    return redirect('/arbortrary')

# LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():
    if not User.vald_user_login(request.form):
        return redirect('/login_page')
    email = { 'email' : request.form['email'] }
    user_in_db = User.user_in_db(email)
    print('user:', user_in_db)
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/login_page')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/login_page')
    session['user_id'] = user_in_db.id
    print(bcrypt.check_password_hash(user_in_db.password, request.form['password']))
    return redirect('/arbortrary')

# GOES TO USERS PROFILE
@app.route('/user/account')
def user_account():
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id' : session['user_id'] }
    user = User.id_in_db(data)
    trees = Tree.get_trees_by_user(data)
    return render_template('my_trees.html', user=user, trees=trees)