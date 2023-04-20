from flask_app import app
from flask_app.models.tree import Tree
from flask_app.models.user import User
from flask_app.controllers import users
from flask import render_template,redirect,session,request

# CREATION OF A TREE
@app.route('/new/tree')
def new_tree():
    if 'user_id' not in session:
        return redirect('/')
    id = { 'id': session['user_id'] }
    user = User.id_in_db(id)
    return render_template('new_tree.html', user=user)

# POST TO CREATE THE TREE
@app.route('/create/tree', methods=['POST'])
def create_tree():
    if 'user_id' not in session:
        return redirect('/')
    if not Tree.vald_tree(request.form):
        return redirect('/new/tree')
    Tree.create_tree(request.form)
    return redirect('/arbortrary')

# EDITING OF TREES
@app.route('/edit/<int:id>')
def edit_tree(id):
    if 'user_id' not in session:
        return redirect('/')
    data = { 'id': id }
    tree = Tree.get_one_tree(data)
    id = { 'id': session['user_id'] }
    user = User.id_in_db(id)
    return render_template('edit.html', tree=tree, user=user)

# UPDATING TREES
@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')
    if not Tree.vald_tree(request.form):
        return redirect('/user/account')
    Tree.update_tree(request.form)
    return redirect('/user/account')

# SHOW TREE BY ITS ID IN THE DB
@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/')
    user_id = {  'id' : session['user_id'] }
    user = User.id_in_db(user_id)
    data = { 'id' : id }
    tree = Tree.get_one_tree(data)
    return render_template('details.html', user=user, tree=tree)

# DELETE A TREE
@app.route('/delete/<int:id>')
def delete(id):
    data = { 'id': id }
    Tree.delete_tree(data)
    return redirect('/user/account')

# :( SO SAD I TRIED BUT COULDNT FIGURE IT OUT
@app.route('/visited/<int:id>')
def visited(id):
    if 'user_id' not in session:
        return redirect('/')
    user_id = {  'id' : session['user_id'] }
    user = User.id_in_db(user_id)
    data = {
        'tree_id': id,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }
    tree = Tree.visited(id)