from typing import Any, Dict

from chaosplt_grpc import remote_channel
from chaosplt_grpc.registration.client import create_registration, \
    get_by_id

from ..model import User

__all__ = ["AccountService"]


class AccountService:
    def __init__(self, config: Dict[str, Any]):
        self.account_addr = config["grpc"]["account"]["addr"]
        self.user = UserService(self.account_addr)
        self.registration = RegistrationService(self.account_addr)

    def release(self):
        pass


class UserService:
    def __init__(self, addr: str):
        self.addr = addr


class RegistrationService:
    def __init__(self, addr: str):
        # gRPC address of the remote service
        self.addr = addr

    def create(self, username: str, name: str, email: str) -> User:
        """
        Register a new user.
        """
        with remote_channel(self.addr) as channel:
            registration = create_registration(channel, username, name, email)
            return User(
                registration.id, registration.username, registration.name,
                registration.email, is_active=registration.is_active,
                is_authenticated=registration.is_authenticated,
                is_anonymous=registration.is_anonymous)

    def get(self, registration_id: str) -> User:
        """
        Retrieve an user by its registration identifier.
        """
        with remote_channel(self.addr) as channel:
            registration = get_by_id(channel, registration_id)
            return User(
                registration.id, registration.username, registration.name,
                registration.email, is_active=registration.is_active,
                is_authenticated=registration.is_authenticated,
                is_anonymous=registration.is_anonymous)
