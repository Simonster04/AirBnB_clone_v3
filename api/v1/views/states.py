#!/usr/bin/python3
"""Contains amenities module"""
from flask import Flask, Blueprint
from flask import abort, make_response
from flask import jsonify, request
from models import storage, state
from api.v1.views import app_views


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def states():
    """States handles all default RestFul API actions """
    states = []
    my_states = storage.all('State').values()
    for my_state in my_states:
        states.append(my_state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def state_id(state_id):
    """Retrieve an object into a valid JSON"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def state_id_delete(state_id):
    """Deletes a State object"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    my_state.delete()
    storage.save()

    return jsonify({})


@app_views.route('/states/',
                 methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Returns the new State with the status code 201"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_state = state.State(name=request.json.get('name', ""))
    storage.new(my_state)
    my_state.save()
    return make_response(jsonify(my_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Returns the State object with the status code 200"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for req in request.json:
        if req not in ['id', 'created_at', 'updated_at']:
            setattr(my_state, req, request.json[req])
    my_state.save()
    return jsonify(my_state.to_dict())


if __name__ == "__main__":
    pass
