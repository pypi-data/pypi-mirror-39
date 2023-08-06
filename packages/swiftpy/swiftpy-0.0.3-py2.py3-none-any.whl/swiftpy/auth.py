import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from swiftpy.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
