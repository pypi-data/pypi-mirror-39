# -*- coding: utf-8 -*-
import glob
import logging
import logging.handlers
import os
from typing import Any, Dict

import cherrypy
from dotenv import load_dotenv

__all__ = ["load_settings"]
logger = logging.getLogger("chaosplatform")


def load_settings(env_path: str = None) -> Dict[str, Any]:
    """
    Load settings from the environment:

    * if `env_path` is not set, read configuration from environment variables
    * if `env_path` is a file, read it
    * if `env_path` is a directory, load, all its `*.env` files
    """
    if env_path:
        if os.path.isdir(env_path):
            pattern = os.path.join(env_path, '**', '.env')
            for env_file in glob.iglob(pattern, recursive=True):
                logger.info("Loading: {}".format(env_file))
                load_dotenv(dotenv_path=env_file)
        else:
            logger.info("Loading: {}".format(env_path))
            load_dotenv(dotenv_path=env_path)

    debug = True if os.getenv('CHAOSPLATFORM_DEBUG') else False
    cherrypy.config.update({
        'server.socket_host': os.getenv('SERVER_LISTEN_ADDR'),
        'server.socket_port': int(os.getenv('SERVER_LISTEN_PORT', 8080)),
        'engine.autoreload.on': False,
        'log.screen': False,
        'log.access_file': '',
        'log.error_file': '',
        'environment': '' if debug else 'production',
        'tools.proxy.on': True,
        'tools.proxy.base': os.getenv('HTTP_PROXY_BASE')
    })
    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

    config = {
        'GRPC_LISTEN_ADDR': os.getenv("GRPC_LISTEN_ADDR"),
        'db': {
            'uri': os.getenv("DATABASE_URI"),
            'debug': debug,
        },
        'debug': debug,
        'grpc': {
            'account': {
                'addr': os.getenv('ACCOUNT_SERVICE_GRPC_ADDR')
            }
        },
        'jwt': {
            'secret_key': os.getenv("JWT_SECRET_KEY"),
            'public_key': os.getenv("JWT_PUBLIC_KEY"),
            'algorithm': os.getenv("JWT_ALGORITHM", "HS256"),
            'identity_claim_key': os.getenv("JWT_IDENTITY_CLAIM", "identity"),
            'user_claims_key': os.getenv("JWT_USER_CLAIMS", "user_claims"),
            'access_token_expires': os.getenv("JWT_ACCESS_TOKEN_EXPIRES"),
            'refresh_token_expires': os.getenv(
                "JWT_REFRESH_TOKEN_EXPIRES", 30*24*60*60),
            'user_claims_in_refresh_token': os.getenv(
                "JWT_CLAIMS_IN_REFRESH_TOKEN")
        }
    }

    return config
