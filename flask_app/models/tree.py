from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models import user
from flask_app import app
from flask import flash

# INITIALIZE CLASS
class Tree:
    DB = 'arbortrary_schema'
    def __init__(self,data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']
        self.visitors = []

    # METHOD TO CREATE A TREE
    @classmethod
    def create_tree(cls,data):
        query = """
        INSERT INTO trees(species,location,reason,date_planted,user_id)
        VALUES(%(species)s,%(location)s,%(reason)s,%(date_planted)s,%(user_id)s)
        """
        return MySQLConnection(cls.DB).query_db(query,data)

    # METHOD TO DELETE A TREE
    @classmethod
    def delete_tree(cls,data):
        query = 'DELETE FROM trees WHERE id = %(id)s'
        return MySQLConnection(cls.DB).query_db(query,data)

    # METHOD TO UPDATE TREE
    @classmethod
    def update_tree(cls,data):
        query = """
        UPDATE trees 
        SET
        species = %(species)s,
        location = %(location)s,
        reason = %(reason)s,
        date_planted = %(date_planted)s,
        updated_at = NOW()
        WHERE trees.id = %(id)s;
        """
        result = MySQLConnection(cls.DB).query_db(query, data)
        if result:
            return result
        else:
            return None

    # METHOD TO GRAB TREE DATA BY USERS ID
    @classmethod
    def get_trees_by_user(cls,data):
        query = """
        SELECT * FROM trees
        JOIN users on trees.user_id = users.id
        WHERE users.id = %(id)s;
        """
        results = MySQLConnection(cls.DB).query_db(query,data)
        all_trees = []
        for row in results:
            posting_user = user.User({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            })
            new_tree = Tree({
                'id': row['id'],
                'species': row['species'],
                'location': row['location'],
                'reason': row['reason'],
                'date_planted': row['date_planted'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'creator': posting_user
            })
            all_trees.append(new_tree)
        return all_trees

    # METHOD TO GET A TREE FROM DB BY ITS ID
    @classmethod
    def get_one_tree(cls,data):
        query = """
        SELECT * FROM trees
        JOIN users on trees.user_id = users.id
        WHERE trees.id = %(id)s;
        """
        result = MySQLConnection(cls.DB).query_db(query,data)
        # print(result)
        for row in result:
            posting_user = user.User({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            })
            new_tree = Tree({
                'id': row['id'],
                'species': row['species'],
                'location': row['location'],
                'reason': row['reason'],
                'date_planted': row['date_planted'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'creator': posting_user
            })
        return new_tree

    # METHOD TO GET ALL TREES IN DB
    @classmethod
    def get_all_trees(cls):
        query = """
        SELECT * FROM trees 
        JOIN users ON trees.user_id = users.id
        ORDER BY trees.date_planted DESC
        """
        results = MySQLConnection(cls.DB).query_db(query)
        print(results)
        all_trees = []
        for row in results:
            posting_user = user.User({
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            })
            new_tree = Tree({
                'id': row['id'],
                'species': row['species'],
                'location': row['location'],
                'reason': row['reason'],
                'date_planted': row['date_planted'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'creator': posting_user
            })
            all_trees.append(new_tree)
        return all_trees

    # VALIDATES THE CREATION OF A TREE
    @staticmethod
    def vald_tree(input):
        is_valid = True
        if not input['species'] or not input['location'] or not input['reason'] or not input['date_planted']:
            flash('All Fields Required')
            is_valid = False
        if len(input['species']) < 5:
            flash('Species Must Be At Least 5 Characters')
            is_valid = False
        if len(input['location']) < 2:
            flash('Location Must Be At Least 2 Characters')
            is_valid = False
        if len(input['reason']) > 50:
            flash('Reason Must Be Below 50 Characters')
            is_valid = False
        return is_valid