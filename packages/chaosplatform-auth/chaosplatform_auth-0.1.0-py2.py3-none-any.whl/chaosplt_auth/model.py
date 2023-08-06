from uuid import UUID

import attr

__all__ = ["AccessToken", "OAuthToken", "User"]


@attr.s
class AccessToken:
    name: str = attr.ib()
    id: UUID = attr.ib()
    user_id: UUID = attr.ib()
    access_token: str = attr.ib()
    refresh_token: str = attr.ib()


@attr.s
class OAuthToken:
    id: UUID = attr.ib()
    user_id: UUID = attr.ib()
    provider: str = attr.ib()
    provider_id = attr.ib()
    token = attr.ib()


@attr.s
class User:
    id: UUID = attr.ib()
    username: str = attr.ib()
    name: str = attr.ib()
    email: str = attr.ib()
    is_authenticated: bool = attr.ib(default=False)
    is_active: bool = attr.ib(default=False)
    is_anonymous: bool = attr.ib(default=True)

    def get_id(self) -> UUID:
        return self.id
