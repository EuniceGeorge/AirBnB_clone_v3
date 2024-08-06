#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""initialize blueprint for api"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *

