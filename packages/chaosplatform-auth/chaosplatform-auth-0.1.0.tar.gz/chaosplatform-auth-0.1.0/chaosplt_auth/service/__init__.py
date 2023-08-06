from typing import Any, Dict

import attr

from .account import AccountService

__all__ = ["initialize_services", "shutdown_services", "Services"]


@attr.s
class Services:
    account: AccountService = attr.ib(default=None)


def initialize_services(services: Services, config: Dict[str, Any]):
    """
    Initialize all services that the authentication service needs to work:

    * account service
    """
    if not services.account:
        services.account = AccountService(config)


def shutdown_services(services: Services):
    """
    Clear out the services used by the authentication service.
    """
    pass
