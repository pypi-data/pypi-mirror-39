from abc import ABC, abstractmethod
from typing import Dict, NoReturn, Union
from uuid import UUID

import attr

from chaosplt_auth.model import AccessToken, OAuthToken

__all__ = ["BaseAuthStorage", "BaseAccessTokenService",
           "BaseOAuthTokenService"]


class BaseAccessTokenService(ABC):
    @abstractmethod
    def get(self, user_id: Union[UUID, str],
            token_id: Union[UUID, str]) -> AccessToken:
        """
        Fetch a token for the given user
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_user(self, user_id: Union[UUID, str]) -> Dict[str, AccessToken]:
        """
        Fetch all tokens for the given user.

        The returned dictionary uses the tokens' name as keys.
        """
        raise NotImplementedError()

    @abstractmethod
    def create(self, name: str, user_id: Union[UUID, str]) -> AccessToken:
        """
        Create a new token with the given name for the user
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, user_id: Union[UUID, str],
               token_id: Union[UUID, str]) -> NoReturn:
        """
        Delete a token from the given user
        """
        raise NotImplementedError()


class BaseOAuthTokenService(ABC):
    @abstractmethod
    def get(self, oauth_id: Union[UUID, str]) -> OAuthToken:
        """
        Fetch a token for the given user
        """
        return self.load(oauth_id)

    @abstractmethod
    def create(self, user_id: str, provider: str, provider_id: str,
               token: str) -> OAuthToken:
        """
        Create a new token
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, oauth_id: str) -> NoReturn:
        """
        Delete the given token
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_by_user(self, user_id: Union[UUID, str]) -> NoReturn:
        """
        Delete the OAuth token of the given user.
        """
        raise NotImplementedError()

    @abstractmethod
    def set_for_user(self, user_id: Union[UUID, str], token: str) -> NoReturn:
        """
        Set the OAuth token of the given user.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_user(self, user_id: Union[UUID, str]) -> OAuthToken:
        """
        Get the OAuth token of the given user.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_provider(self, provider: str, provider_id: str) -> OAuthToken:
        """
        Get the OAuth token for the given provider/provider-id pair which
        should be uniq.
        """
        raise NotImplementedError()


@attr.s
class BaseAuthStorage:
    access_token: BaseAccessTokenService = attr.ib()
    oauth_token: BaseOAuthTokenService = attr.ib()

    def release(self) -> NoReturn:
        raise NotImplementedError()
