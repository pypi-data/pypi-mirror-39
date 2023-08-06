# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict, NoReturn, Union
from uuid import UUID

from flask import Blueprint
from flask_caching import Cache
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend import BaseBackend
from flask_login import login_user

from chaosplt_auth.model import OAuthToken, User
from chaosplt_auth.storage import AuthStorage

__all__ = ["setup_oauth_provider"]

logger = logging.getLogger("chaoshub")


class OAuthBackend(BaseBackend):
    def __init__(self, services, storage: AuthStorage, cache: Cache):
        self.services = services
        self.storage = storage
        self.cache = cache

    def make_cache_key(self, blueprint: Blueprint,
                       user_id: Union[UUID, str]) -> str:
        return "oauth_token|{name}|{user_id}".format(
            name=blueprint.name, user_id=user_id,
        )

    def get_oauth_token(self, user_id: Union[UUID, str]) -> OAuthToken:
        return self.storage.oauth_token.get_by_user(user_id)

    def get_oauth_token_by_provider(self, provider: str,
                                    provider_id: str) -> OAuthToken:
        return self.storage.oauth_token.get_by_provider(
            provider, provider_id)

    def delete_oauth_token(self, user_id: Union[UUID, str]) -> NoReturn:
        self.storage.oauth_token.delete_by_user(user_id)

    def set_oauth_token(self, user_id: Union[UUID, str],
                        token: str) -> OAuthToken:
        return self.storage.oauth_token.set_for_user(user_id, token)

    def create_oauth_token(self, user_id: Union[UUID, str], provider: str,
                           provider_id: str,
                           token: Dict[str, Any]) -> OAuthToken:
        return self.storage.oauth_token.create(
            user_id, provider, provider_id, token)

    def get_account(self, user_id: Union[UUID, str]) -> User:
        return self.services.account.registration.get(str(user_id))

    def create_account(self, username: str, name: str, email: str) -> User:
        return self.services.account.registration.create(
            username, name, email)

    def get(self, blueprint: Blueprint, user_id: Union[UUID, str]) -> str:
        cache_key = self.make_cache_key(
            blueprint=blueprint, user_id=user_id)
        token = self.cache.get(cache_key)
        if token:
            return token

        token = self.get_oauth_token(user_id)
        if token:
            value = token.token
            self.cache.set(cache_key, value)
            return value

    def set(self, blueprint: Blueprint, token: str,
            user_id: str) -> NoReturn:
        cache_key = self.make_cache_key(
            blueprint=blueprint, user_id=user_id)
        self.cache.delete(cache_key)
        self.delete_oauth_token(user_id)
        self.set_oauth_token(user_id, token)
        self.cache.set(cache_key, token)

    def delete(self, blueprint: Blueprint, user_id: str) -> NoReturn:
        cache_key = self.make_cache_key(
            blueprint=blueprint, user_id=user_id)
        self.cache.delete(cache_key)
        self.delete_oauth_token(user_id)


def setup_oauth_provider(blueprint: Blueprint, services, storage: AuthStorage,
                         cache: Cache):
    blueprint.backend = OAuthBackend(
        services=services, storage=storage, cache=cache)

    @oauth_authorized.connect_via(blueprint)
    def github_logged_in(blueprint: Blueprint, token: str):
        if not token:
            logger.error("Missing token")
            return False

        resp = blueprint.session.get("/user")
        if not resp.ok:
            logger.error("Failed to fetch GitHub OAuth response")
            return False

        github_info = resp.json()
        provider = blueprint.name
        provider_id = str(github_info["id"])
        username = github_info["login"]
        name = github_info["name"]
        email = github_info.get("email")

        oauth = blueprint.backend.get_oauth_token_by_provider(
            blueprint.name, provider_id)

        user = None
        user_id = None
        if oauth:
            user = blueprint.backend.get_account(oauth.user_id)
            user_id = oauth.user_id
        else:
            logger.info("Creating user's account")
            user = blueprint.backend.create_account(username, name, email)
            user_id = user.id
            logger.info("Account created {}".format(user_id))

        if not oauth:
            oauth = blueprint.backend.create_oauth_token(
                user_id, provider, provider_id, token)
            logger.info("Created OAuth token {}".format(oauth.id))

        login_user(user, remember=True)

        return False

    @oauth_error.connect_via(blueprint)
    def github_error(blueprint: Blueprint, error, error_description=None,
                     error_uri=None):
        msg = (
            "OAuth error from {name}! "
            "error={error} description={description} uri={uri}"
        ).format(
            name=blueprint.name,
            error=error,
            description=error_description,
            uri=error_uri,
        )
        print(msg)
