# -*- coding: utf-8 -*-
from typing import Dict, NoReturn, Union
import uuid
from uuid import UUID

from chaosplt_relational_storage.db import Base
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from sqlalchemy import Boolean, Column, DateTime, String, \
    UniqueConstraint, func
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import UUIDType

__all__ = ["AccessToken", "OAuthToken"]


class AccessToken(Base):  # type: ignore
    __tablename__ = 'access_token'
    __table_args__ = (
        UniqueConstraint(
            'name', 'user_id'
        ),
    )

    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    user_id = Column(UUIDType(binary=False), nullable=False)
    revoked = Column(Boolean(name='revoked'), nullable=False, default=False)
    issued_on = Column(DateTime(), nullable=False, server_default=func.now())
    last_used_on = Column(DateTime(), nullable=True)
    access_token = Column(String(255), index=True, nullable=False)
    refresh_token = Column(String(255), index=True, nullable=False)

    @staticmethod
    def save(name: str, user_id: Union[UUID, str], access_token: str,
             refresh_token: str, session: Session) -> 'AccessToken':
        token = AccessToken(
            name=name,
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token)

        session.add(token)
        return token

    @staticmethod
    def delete(user_id: Union[UUID, str],
               token_id: Union[UUID, str], session: Session) -> NoReturn:
        token = session.query(AccessToken).\
            filter_by(user_id=user_id).\
            filter_by(id=token_id).first()

        if token:
            session.delete(token)

    @staticmethod
    def load_by_user(user_id: Union[UUID, str],
                     session: Session) -> Dict[str, 'AccessToken']:
        return session.query(AccessToken).\
            filter_by(user_id=user_id).all()

    @staticmethod
    def load(user_id: Union[UUID, str], token_id: Union[UUID, str],
             session: Session) -> 'AccessToken':
        return session.query(AccessToken).\
            filter_by(user_id=user_id).\
            filter_by(id=token_id).\
            filter_by(revoked=False).first()


class OAuthToken(Base, OAuthConsumerMixin):
    __tablename__ = 'oauth_token'
    __table_args__ = (
        UniqueConstraint(
            'provider', 'provider_id'
        ),
    )

    provider_id = Column(String(256), unique=True, nullable=False)
    user_id = Column(UUIDType(binary=False), nullable=False)

    @staticmethod
    def load(user_id: Union[UUID, str], oauth_id: Union[UUID, str],
             session: Session) -> 'OAuthToken':
        return session.query(OAuthToken).\
            filter_by(user_id=user_id).\
            filter_by(id=oauth_id).first()

    @staticmethod
    def load_by_user(user_id: Union[UUID, str],
                     session: Session) -> 'OAuthToken':
        return session.query(OAuthToken).filter_by(
            user_id=user_id).first()

    @staticmethod
    def load_by_provider(provider: str, provider_id: str,
                         session: Session) -> 'OAuthToken':
        return session.query(OAuthToken).\
            filter_by(provider=provider).\
            filter_by(provider_id=provider_id).first()

    @staticmethod
    def delete(user_id: Union[UUID, str], oauth_id: Union[UUID, str],
               session: Session) -> NoReturn:
        return session.query(OAuthToken).\
            filter_by(user_id=user_id).\
            filter_by(id=oauth_id).delete()

    @staticmethod
    def delete_by_user(user_id: Union[UUID, str],
                       session: Session) -> NoReturn:
        return session.query(OAuthToken).filter_by(
            user_id=user_id).delete()

    @staticmethod
    def save(user_id: Union[UUID, str], provider: str, provider_id: str,
             token: str, session: Session) -> 'OAuthToken':
        oauth = OAuthToken(
            user_id=user_id,
            token=token,
            provider=provider,
            provider_id=provider_id
        )

        session.add(oauth)
        return oauth

    @staticmethod
    def update_by_user(user_id: Union[UUID, str], token: str,
                       session: Session) -> NoReturn:
        oauth = session.query(OAuthToken).filter_by(
            user_id=user_id).first()
        if oauth:
            oauth.token = token
