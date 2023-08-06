from datetime import timedelta
from typing import Any, Dict, NoReturn, Union
from uuid import UUID

from flask.json import JSONEncoder
from flask_jwt_extended import JWTManager
from flask_jwt_extended.tokens import encode_refresh_token, encode_access_token

from chaosplt_grpc.auth.message import AccessToken
from chaosplt_grpc.auth.server import AuthService as GRPCAuthService

from .storage import AuthStorage

__all__ = ["AuthRPC"]


class NoAppJWTManager(JWTManager):
    def __init__(self, config: Dict[str, Any]):
        JWTManager.__init__(self, app=None)
        self.config = config
        self._encode_key_callback = self.encode_key_callback

    def encode_key_callback(self, identity: Union[UUID, str]):
        return self.config["secret_key"]

    def _user_identity_callback(self, identity: Union[UUID, str]):
        return identity

    def _create_refresh_token(self, identity: Union[UUID, str]):
        expires_delta = timedelta(
            seconds=int(self.config["refresh_token_expires"]))

        if self.config["user_claims_in_refresh_token"]:
            user_claims = self._user_claims_callback(identity)
        else:
            user_claims = None

        refresh_token = encode_refresh_token(
            identity=self._user_identity_callback(identity),
            secret=self._encode_key_callback(identity),
            algorithm=self.config["algorithm"],
            expires_delta=expires_delta,
            user_claims=user_claims,
            csrf=False,
            identity_claim_key=self.config["identity_claim_key"],
            user_claims_key=self.config["user_claims_key"],
            json_encoder=JSONEncoder
        )
        return refresh_token

    def _create_access_token(self, identity: Union[UUID, str]):
        expires_delta = timedelta(
            seconds=int(self.config["access_token_expires"]))

        access_token = encode_access_token(
            identity=self._user_identity_callback(identity),
            secret=self._encode_key_callback(identity),
            algorithm=self.config["algorithm"],
            expires_delta=expires_delta,
            fresh=False,
            user_claims=self._user_claims_callback(identity),
            csrf=False,
            identity_claim_key=self.config["identity_claim_key"],
            user_claims_key=self.config["user_claims_key"],
            json_encoder=JSONEncoder
        )
        return access_token


class AuthRPC(GRPCAuthService):
    def __init__(self, storage: AuthStorage, config: Dict[str, Any]):
        GRPCAuthService.__init__(self)
        self.storage = storage
        self.jwt = NoAppJWTManager(config.get("jwt"))

    def create_access_token(self, user_id: str, name: str) -> AccessToken:
        access_token = self.jwt._create_access_token(str(user_id))
        refresh_token = self.jwt._create_refresh_token(str(user_id))

        token = self.storage.access_token.create(
             name, user_id, access_token, refresh_token)
        return AccessToken(
            id=str(token.id),
            user_id=str(token.user_id),
            name=token.name,
            access_token=token.access_token,
            refresh_token=token.refresh_token
        )

    def delete_access_token(self, user_id: str, token_id: str) -> NoReturn:
        self.storage.access_token.delete(user_id, token_id)
