import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import traceback

from .database.models import setup_db, Drink
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
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''


    @app.route('/drinks', methods=['GET'])
    def retrieve_drinks():
        try:
            drinks = Drink.query.order_by(Drink.id).all()

            return jsonify({
                'success': True,
                'drinks': [drink.short() for drink in drinks],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''


    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')
    def retrieve_drinks_detail(payload):
        try:
            drinks = Drink.query.order_by(Drink.id).all()

            return jsonify({
                'success': True,
                'drinks': [drink.long() for drink in drinks],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''


    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_new_row_in_drink(payload):
        try:
            body = request.get_json()

            title = body.get('title', None)
            recipe = body.get('recipe', None)

            if title is None or recipe is None:
                abort(422)

            drink = Drink(
                title=title,
                recipe=json.dumps(recipe)
            )

            drink.insert()

            return jsonify({
                'success': True,
                'drinks': [drink.long()],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''


    @app.route('/drinks/<int:id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(payload, id):
        try:
            body = request.get_json()

            new_title = body.get('title', None)
            new_recipe = body.get('recipe', None)

            drink = Drink.query.filter_by(id=id).one_or_none()

            if drink is None:
                raise (404)

            if new_title:
                drink.title = new_title
            if new_recipe:
                drink.recipe = json.dumps(new_recipe)

            drink.update()

            return jsonify({
                'success': True,
                'drinks': [drink.long()],
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            abort(422)


    '''
    @DONE implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


    @app.route('/drinks/<int:id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(payload, id):
        try:
            drink = Drink.query.filter(Drink.id == id).one_or_none()

            if drink is None:
                abort(404)

            drink.delete()

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
