import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES


#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
#


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    if drinks:
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        })

    # aborts if no drinks could be found in the database
    else:
        abort(404)

#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure


@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail():
    drinks = Drink.query.all()

    if drinks:
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        })

    # aborts if no drinks could be found in the database
    else:
        abort(404)

#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drink():  # may be errors when getting recipe values since it is unclear if recipe is passed as a string or list
    body = request.get_json()
    drink = Drink(
        title=body.get("title", None),
        recipe=json.dumps(body.get("recipe", None))
    )

    # commits new drink to the database, aborts if drink could not be added
    try:
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(422)

#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drinks(drink_id):  # DONE, check for correctness
    drink = Drink.query.get(drink_id)

    # aborts if drink with drink_id could not be found
    if not drink:
        abort(404)

    # updates data for a particular drink, values for title and drink remain the same if body.get returns no value for title or recipe
    body = request.get_json()
    drink.title = body.get("title", drink.title)
    drink.recipe = json.dumps(body.get("recipe", drink.recipe))

    # commits changes to database, throws error if there was an issue updating the drink
    try:
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(422)

#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(drink_id):
    drink = Drink.query.get(drink_id)

    # aborts if drink with drink_id could not be found
    if not drink:
        abort(404)

    # deletes drink from database, throws error if there was an issue removing the drink
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except Exception as e:
        print(e)
        abort(422)

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error,
    }), error.status_code
