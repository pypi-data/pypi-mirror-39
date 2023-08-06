# -*- coding: utf-8 -*-
from uuid import UUID

from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_login import current_user, login_required
from marshmallow import ValidationError

from chaosplt_auth.schemas import new_token_schema, token_schema

__all__ = ["api"]

api = Blueprint("token", __name__)


@api.route('access', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH'])
@login_required
def validate():
    """
    Endpoint used to validate the credentials from a user. If this function
    is ever called, then it means the credentials are indeed valid otherwise
    an error was triggered before.
    """
    return "", 200


@api.route('', methods=['POST'])
@login_required
def new():
    try:
        payload = new_token_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422

    name = payload["name"]
    user_id = payload["user_id"]

    if str(current_user.id) != user_id:
        return jsonify({
            "message": "Cannot create a token for another user"
        }), 422

    user = request.services.account.registration.get(user_id)
    if not user:
        return jsonify({
            "message": "Unknown user"
        }), 422

    tokens = request.storage.access_token.get_by_user(user_id)
    if name in tokens:
        return jsonify({
            "message": "Name already used for another of your tokens"
        }), 409

    access_token = create_access_token(str(user_id))
    refresh_token = create_refresh_token(str(user_id))
    token = request.storage.access_token.create(
        name, user_id, access_token, refresh_token)
    return token_schema.jsonify(token), 201


@api.route('<uuid:token_id>', methods=['GET'])
@login_required
def get(token_id: UUID):
    token = request.storage.access_token.get(current_user.id, token_id)
    if not token:
        return abort(404)
    return token_schema.jsonify(token)


@api.route('<uuid:token_id>', methods=['DELETE'])
@login_required
def delete(token_id: UUID):
    request.storage.access_token.delete(current_user.id, token_id)
    return "", 204
