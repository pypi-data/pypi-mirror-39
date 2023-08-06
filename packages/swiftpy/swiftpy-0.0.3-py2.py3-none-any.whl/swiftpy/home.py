import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from swiftpy.db import get_db

bp = Blueprint("home", __name__)


@bp.route('/')
def home():
    return 'Hello, World!'
