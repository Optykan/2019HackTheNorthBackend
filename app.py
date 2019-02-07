#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os
import sqlite3
from service.database import initialize_db, User, Skill

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
    User.create(User(name='yes'))
    User.fetch();
    return jsonify({
            "one": 2,
            "two": 3
        })


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
