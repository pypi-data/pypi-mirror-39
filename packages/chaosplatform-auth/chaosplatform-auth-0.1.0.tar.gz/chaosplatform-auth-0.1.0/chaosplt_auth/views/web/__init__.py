# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
import os
from typing import Any, Dict

from flask import Blueprint, Flask, request, after_this_request, Response
from flask_caching import Cache

from chaosplt_auth.auth import setup_login
from chaosplt_auth.service import Services
from chaosplt_auth.storage import AuthStorage

from .backend import setup_oauth_provider
from .oauth2 import view as oauth2_view, github_view

__all__ = ["create_app", "cleanup_app", "serve_app"]


def create_app(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = True if os.getenv('CHAOSHUB_DEBUG') else False

    logger = logging.getLogger('flask.app')
    logger.propagate = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.secret_key = app.config["SECRET_KEY"]

    app.config["GRPC_LISTEN_ADDR"] = os.getenv("GRPC_LISTEN_ADDR")

    app.config["CACHE_TYPE"] = os.getenv("CACHE_TYPE", "simple")
    if app.config["CACHE_TYPE"] == "redis":
        app.config["CACHE_REDIS_HOST"] = os.getenv("CACHE_REDIS_HOST")
        app.config["CACHE_REDIS_PORT"] = os.getenv("CACHE_REDIS_PORT", 6379)

    # OAUTH2
    app.config["GITHUB_OAUTH_CLIENT_ID"] = os.getenv("AUTH_GITHUB_CLIENT_ID")
    app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.getenv(
        "AUTH_GITHUB_CLIENT_SECRET")

    setup_login(app, from_session=True)

    return app


def cleanup_app(app: Flask):
    pass


def serve_app(app: Flask, cache: Cache, services: Services,
              storage: AuthStorage, config: Dict[str, Any],
              mount_point: str = '/oauth2', log_handler: StreamHandler = None):
    register_views(app, cache, services, storage)


###############################################################################
# Internals
###############################################################################
def register_views(app: Flask, cache: Cache, services, storage: AuthStorage):
    patch_request(oauth2_view, services, storage)
    patch_request(github_view, services, storage)

    app.register_blueprint(github_view, url_prefix="/auth/oauth2/via")
    app.register_blueprint(oauth2_view, url_prefix="/auth/oauth2")

    setup_oauth_provider(github_view, services, storage, cache)


def patch_request(bp: Blueprint, services, storage: AuthStorage):
    @bp.before_request
    def prepare_request():
        request.services = services
        request.storage = storage

        @after_this_request
        def clean_request(response: Response):
            request.services = None
            request.storage = None
            return response
