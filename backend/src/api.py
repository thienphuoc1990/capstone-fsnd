import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import traceback

from .database.models import setup_db, Actor
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

# ROUTES
def define_routes(app):
    '''
    @DONE implement endpoint
        GET /actors
            it should be a public endpoint
            it should contain only the actor.short() data representation
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''


    @app.route('/actors', methods=['GET'])
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


    @app.route('/actors-detail', methods=['GET'])
    @requires_auth('get:actors-detail')
    def retrieve_actors_detail(payload):
        try:
            actors = Actor.query.order_by(Actor.id).all()

            return jsonify({
                'success': True,
                'actors': [actor.long() for actor in actors],
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
    @requires_auth('post:actors')
    def create_new_row_in_actor(payload):
        try:
            body = request.get_json()

            title = body.get('title', None)
            recipe = body.get('recipe', None)

            if title is None or recipe is None:
                abort(422)

            actor = Actor(
                title=title,
                recipe=json.dumps(recipe)
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
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        try:
            body = request.get_json()

            new_title = body.get('title', None)
            new_recipe = body.get('recipe', None)

            actor = Actor.query.filter_by(id=id).one_or_none()

            if actor is None:
                raise (404)

            if new_title:
                actor.title = new_title
            if new_recipe:
                actor.recipe = json.dumps(new_recipe)

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
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()

            if actor is None:
                abort(404)

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
