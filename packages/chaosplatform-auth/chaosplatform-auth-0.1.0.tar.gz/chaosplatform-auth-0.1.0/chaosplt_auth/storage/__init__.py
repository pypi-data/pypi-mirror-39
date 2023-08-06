from typing import Any, Dict, NoReturn

from chaosplt_relational_storage import initialize_storage as init_storage, \
    configure_storage, release_storage
import pkg_resources

from .concrete import AccessTokenService, OAuthTokenService
from .interface import BaseAuthStorage

__all__ = ["initialize_storage", "shutdown_storage", "AuthStorage"]


class AuthStorage(BaseAuthStorage):
    def __init__(self, config: Dict[str, Any]):
        self.driver = init_storage(config)
        configure_storage(self.driver)

        access_token = AccessTokenService(self.driver)
        oauth_token = OAuthTokenService(self.driver)
        BaseAuthStorage.__init__(self, access_token, oauth_token)

    def release(self) -> NoReturn:
        """
        Release the storage resources.
        """
        release_storage(self.driver)


def initialize_storage(config: Dict[str, Any]) -> BaseAuthStorage:
    """
    Initialize the underlying authentication storage.

    If an installed package exposes the `chaosplatform.storage` class
    entrypoint for the `"auth"` group, it will be loaded. Otherwise, it'll be
    the default `AuthStorage` from this module.
    """
    for plugin in pkg_resources.iter_entry_points('chaosplatform.storage'):
        if plugin.name == "auth":
            service_class = plugin.load()
            return service_class(config)

    return AuthStorage(config)


def shutdown_storage(storage: BaseAuthStorage) -> NoReturn:
    """
    Release the storage resources by calling its `release` method.
    """
    storage.release()
