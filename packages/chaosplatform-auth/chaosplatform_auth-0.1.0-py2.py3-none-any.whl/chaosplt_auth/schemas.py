from typing import Any, Dict

from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_load

from .model import AccessToken

__all__ = ["new_token_schema", "token_schema", "ma", "setup_schemas"]

ma = Marshmallow()


def setup_schemas(app: Flask):
    return ma.init_app(app)


class AccessTokenSchema(ma.Schema):
    class Meta:
        ordered = True
    id = fields.UUID(required=False)
    user_id = fields.UUID()
    name = fields.String()
    access_token = fields.String()
    refresh_token = fields.String()
    url = ma.AbsoluteURLFor('token.get', token_id='<id>')
    links = ma.Hyperlinks({
        'self': ma.URLFor('token.get', token_id='<id>'),
    })

    @post_load
    def make_access_token(self, data: Dict[str, Any]):
        return AccessToken(**data)


class NewAccessTokenSchema(ma.Schema):
    name = fields.String(required=True)
    user_id = fields.String(required=True)
    scopes = fields.String(many=True, default=None)


token_schema = AccessTokenSchema()
new_token_schema = NewAccessTokenSchema()
