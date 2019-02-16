# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, abort
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os
import sqlite3
from models import initialize_db, delete_db, User, Skill
from sqlalchemy.exc import StatementError
from scripts.db_utils import load_database
from models import Junction
from service.stats import average_skill_rating, users_with_skill, filter_stats

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')


# Automatically tear down SQLAlchemy.
# @app.teardown_request
# def shutdown_session(exception=None):
#     #db_session.remove()

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def home():
    User.fetch()
    return jsonify({
        "one": 2,
        "two": 3
    })


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def users_by_id(user_id):
    user, session = User.get_by_id(user_id)
    if user is None:
        return abort(404)
    if request.method == 'PUT':
        try:
            user.update_user(request.get_json(), session)
            user.validate()
            session.commit()
        except TypeError:
            # .validate() throws a TypeError if it fails
            return abort(400)
        except StatementError as e:
            # statements are good unless the data doesn't conform
            # this will be thrown if validation fails for whatever reason
            return abort(400)
        except Exception as e:
            print(e)
            return abort(500)
    if request.method == 'DELETE':
        session.delete(user)
        session.commit()

    return jsonify(user.to_json())


@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        load_database()
        return jsonify({
            "message": "Created successfully"
        }), 201
    elif request.method == 'GET':
        return jsonify(User.retrieve_all())
    else:
        delete_db()
        return ('', 204)


@app.route('/skills')
def retrieve_skills():
    junctions = list(map(lambda junction: junction.represent_as_skill(), Junction.retrieve_all()))
    
    try:
        min_rating = float(request.args.get('min_rating') or 0)
        max_rating = float(request.args.get('max_rating') or 10)
        min_frequency = float(request.args.get('min_frequency') or 0)
        max_frequency = float(request.args.get('max_frequency') or -1)
    except ValueError:
        abort(400)

    skills = Skill.retrieve_all()
    stats = []
    for skill in skills:
        stats.append({
            "average": average_skill_rating(skill['id']),
            "count": users_with_skill(skill['id']),
            "name": skill['name'],
            "id": skill['id']
        })

    print(stats)

    return jsonify(
        list(filter(lambda stat: filter_stats(stat, min_rating, max_rating, min_frequency, max_frequency), stats)))


@app.route('/skills/<int:skill_id>')
def skill_stats(skill_id):
    return jsonify({
        "average": average_skill_rating(skill_id),
        "count": users_with_skill(skill_id)
    })


# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "message": "internal server error",
        "status": 500
    }), 500


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


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    delete_db()
    initialize_db()
    load_database()
    app.run()