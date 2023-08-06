# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_login import login_required

__all__ = ["view", "github_view"]

view = Blueprint("auth", __name__)
github_view = make_github_blueprint()


@view.route('')
@login_required
def index():
    return "", 200
