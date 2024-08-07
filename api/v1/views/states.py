#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""view for State objects that handles 
all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid

# route to list all states

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """ list all states"""
    states = storage.all(State)
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)

# route to get state by id

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state():
    """retrieves all state """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

# route to delete a state via id
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state():
    """Deletes a state by id """
    state = storage.get(State, state_id)
    if state:
        storage.delete(State)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

# route to create a state
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ create new state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201
    
# route to update state by id
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state():
    """ update state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
