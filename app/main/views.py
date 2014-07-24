from .. import db
from ..models import User, Address
from flask import render_template
from . import main

@main.route('/test')
def test():
    a = Address()
    return 'ggg'
