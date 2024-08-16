"""helps with flash errors"""
from functools import wraps
from flask import redirect, session, flash

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Error: please log in first.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
