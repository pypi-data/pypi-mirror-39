from typing import Dict, NoReturn, Union
from uuid import UUID

from chaosplt_auth.model import AccessToken, OAuthToken
from chaosplt_relational_storage import RelationalStorage
from chaosplt_relational_storage.db import orm_session

from .interface import BaseAccessTokenService, BaseOAuthTokenService
from .model import AccessToken as AccessTokenModel, \
    OAuthToken as OAuthTokenModel


class AccessTokenService(BaseAccessTokenService):
    def __init__(self, driver: RelationalStorage):
        self.driver = driver

    def get(self, user_id: Union[UUID, str],
            token_id: Union[UUID, str]) -> AccessToken:
        with orm_session() as session:
            token = AccessTokenModel.load(user_id, token_id, session=session)
            if not token:
                return

            return AccessToken(
                name=token.name,
                id=token.id,
                user_id=token.user_id,
                access_token=token.access_token,
                refresh_token=token.refresh_token
            )

    def create(self, name: str, user_id: str, access_token: str,
               refresh_token: str) -> AccessToken:
        with orm_session() as session:
            token = AccessTokenModel.save(
                name, user_id, access_token, refresh_token, session=session)
            session.flush()

            return AccessToken(
                name=name,
                id=token.id,
                user_id=user_id,
                access_token=access_token,
                refresh_token=refresh_token
            )

    def get_by_user(self, user_id: Union[UUID, str]) -> Dict[str, AccessToken]:
        with orm_session() as session:
            result = {}
            tokens = AccessTokenModel.load_by_user(user_id, session=session)
            if tokens:
                for token in tokens:
                    result[token.name] = AccessToken(
                        name=token.name,
                        id=token.id,
                        user_id=token.user_id,
                        access_token=token.access_token,
                        refresh_token=token.refresh_token
                    )
            return result

    def delete(self, user_id: Union[UUID, str], token_id: Union[UUID, str]):
        with orm_session() as session:
            AccessTokenModel.delete(user_id, token_id, session=session)


class OAuthTokenService(BaseOAuthTokenService):
    def __init__(self, driver: RelationalStorage):
        self.driver = driver

    def get(self, user_id: Union[UUID, str],
            oauth_id: Union[UUID, str]) -> OAuthToken:
        with orm_session() as session:
            oauth = OAuthTokenModel.load(user_id, oauth_id, session=session)

            if oauth:
                return OAuthToken(
                    id=oauth.id,
                    user_id=oauth.user_id,
                    provider=oauth.provider,
                    provider_id=oauth.provider_id,
                    token=oauth.token
                )

    def get_by_provider(self, provider: str, provider_id: str) -> OAuthToken:
        with orm_session() as session:
            oauth = OAuthTokenModel.load_by_provider(
                provider, provider_id, session=session)

            if oauth:
                return OAuthToken(
                    id=oauth.id,
                    user_id=oauth.user_id,
                    provider=oauth.provider,
                    provider_id=oauth.provider_id,
                    token=oauth.token
                )

    def get_by_user(self, user_id: Union[UUID, str]) -> OAuthToken:
        with orm_session() as session:
            oauth = OAuthTokenModel.load_by_user(user_id, session=session)

            if oauth:
                return OAuthToken(
                    id=oauth.id,
                    user_id=oauth.user_id,
                    provider=oauth.provider,
                    provider_id=oauth.provider_id,
                    token=oauth.token
                )

    def create(self, user_id: Union[UUID, str], provider: str,
               provider_id: str, token: str) -> OAuthToken:
        with orm_session() as session:
            oauth = OAuthTokenModel.save(
                user_id, provider, provider_id, token, session=session)
            session.flush()

            return OAuthToken(
                id=oauth.id,
                user_id=oauth.user_id,
                provider=oauth.provider,
                provider_id=oauth.provider_id,
                token=oauth.token
            )

    def delete(self, user_id: Union[UUID, str],
               oauth_id: Union[UUID, str]) -> NoReturn:
        with orm_session() as session:
            OAuthTokenModel.delete(user_id, oauth_id, session=session)

    def delete_by_user(self, user_id: Union[UUID, str]) -> NoReturn:
        with orm_session() as session:
            OAuthTokenModel.delete_by_user(user_id, session=session)

    def set_for_user(self, user_id: Union[UUID, str], token: str) -> NoReturn:
        with orm_session() as session:
            OAuthTokenModel.update_by_user(user_id, token, session=session)
