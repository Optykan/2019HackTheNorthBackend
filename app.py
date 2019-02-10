#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, abort
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os
import sqlite3
from service.database import initialize_db, delete_db, User, Skill
from sqlalchemy.exc import StatementError
from scripts.db_utils import load_database

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
# @app.teardown_request
# def shutdown_session(exception=None):
#     #db_session.remove()

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    User.fetch();
    return jsonify({
            "one": 2,
            "two": 3
        })

@app.route('/users/<int:user_id>', methods=['GET', 'PUT'])
def users_by_id(user_id):
    user, session = User.get(user_id)
    if user is None:
        return abort(404)
    if request.method == 'PUT':
        user.merge(request.get_json())
        try:
            session.commit()
        except StatementError as e:
            # statements are good unless the data doesn't conform
            return abort(400)
        except:
            return abort(500)

    return jsonify(user.toJson())

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def handle_users():
    if request.method == 'POST':
        load_database()
        return jsonify({
            "message": "Created successfully"
        }), 201
    elif request.method == 'GET':
        User.fetch()
        return ('', 204)
    else:
        delete_db()
        return ('', 204)

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "message": "not found",
        "status": 404
        }), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        "message": "Bad request",
        "status": 400
        }), 400

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    initialize_db()
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
