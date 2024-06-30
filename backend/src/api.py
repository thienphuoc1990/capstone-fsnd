import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import traceback

from .database.models import setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth

def create_app(db_uri="", test_config=None):
    app = Flask(__name__)
    if db_uri:
        setup_db(app, db_uri)
    else:
        setup_db(app)
    
    configure_cors(app)
    define_routes(app)
    error_handling(app)
    return app


def configure_cors(app):
    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
        
    CORS(app, resources={r"/*": {"origins": "*"}})


    """
    Use the after_request decorator to set Access-Control-Allow
    """
        
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response

# ROUTES
def define_routes(app):
    define_actor_routes(app)
    define_movie_routes(app)

def define_actor_routes(app):
    '''
    @DONE implement endpoint
        GET /actors
            it should be a public endpoint
            it should contain only the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors', methods=['GET'])
    # @requires_auth('get:actors')
    def retrieve_actors():
        try:
            actors = Actor.query.order_by(Actor.id).all()

            return jsonify({
                'success': True,
                'actors': [actor.short() for actor in actors],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        GET /actors-detail
            it should require the 'get:actors-detail' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors/<int:id>', methods=['GET'])
    # @requires_auth('get:actors-detail')
    def retrieve_actors_detail(id):
        try:
            actor = Actor.query.get_or_404(id)

            return jsonify({
                'success': True,
                'actors': actor.long(),
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        POST /actors
            it should create a new row in the actors table
            it should require the 'post:actors' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors', methods=['POST'])
    # @requires_auth('post:actors')
    def create_new_row_in_actor():
        try:
            body = request.get_json()

            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            if new_name is None or new_age is None or new_gender is None:
                abort(422)

            actor = Actor(
                name=new_name,
                age=new_age,
                gender=new_gender
            )

            actor.insert()

            return jsonify({
                'success': True,
                'actors': [actor.long()],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        PATCH /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actors' permission
            it should contain the actor.long() data representation
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:actors')
    def update_actor(id):
        try:
            actor = Actor.query.get_or_404(id)
            body = request.get_json()

            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            if new_name:
                actor.name = new_name
            if new_age:
                actor.age = new_age
            if new_age:
                actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.long()],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:actors')
    def delete_actor(id):
        try:
            actor = Actor.query.get_or_404(id)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


def define_movie_routes(app):
    '''
    @DONE implement endpoint
        GET /movies
            it should be a public endpoint
            it should contain only the movie.short() data representation
        returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movies', methods=['GET'])
    # @requires_auth('get:movies')
    def retrieve_movies():
        try:
            movies = Movie.query.order_by(Movie.id).all()

            return jsonify({
                'success': True,
                'movies': [movie.short() for movie in movies],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        GET /movies-detail
            it should require the 'get:movies-detail' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movies/<int:id>', methods=['GET'])
    # @requires_auth('get:movies-detail')
    def retrieve_movies_detail(id):
        try:
            movie = Movie.query.get_or_404(id)

            return jsonify({
                'success': True,
                'movies': movie.long(),
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        POST /movies
            it should create a new row in the movies table
            it should require the 'post:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movies', methods=['POST'])
    # @requires_auth('post:movies')
    def create_new_row_in_movie():
        try:
            body = request.get_json()

            new_title = body.get('title', None)
            new_release_date = body.get('releaseDate', None)

            if new_title is None or new_release_date is None:
                abort(422)

            movie = Movie(
                title=new_title,
                release_date=new_release_date,
            )

            movie.insert()

            return jsonify({
                'success': True,
                'movies': [movie.long()],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movies/<int:id>', methods=['PATCH'])
    # @requires_auth('patch:movies')
    def update_movie(id):
        try:
            movie = Movie.query.get_or_404(id)
            body = request.get_json()

            new_title = body.get('title', None)
            new_release_date = body.get('releaseDate', None)

            if new_title:
                movie.title = new_title
            if new_release_date:
                movie.release_date = new_release_date

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.long()],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        DELETE /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


    @app.route('/movies/<int:id>', methods=['DELETE'])
    # @requires_auth('delete:movies')
    def delete_movie(id):
        try:
            movie = Movie.query.get_or_404(id)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


# Error Handling
def error_handling(app):
    '''
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    '''
    @DONE implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    '''
    @DONE implement error handler for 404
        error handler should conform to general task above
    '''


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404


    '''
    @DONE implement error handler for AuthError
        error handler should conform to general task above
    '''


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.error['code'],
            'message': error.error['description'],
        }), error.status_code
