import jwt

from flask import request
from flask_restx import abort

from constants import JWT_SECRET, JWT_ALGORITHM


def auth_required(func):
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer')[-1]
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            print('JWT Decode Error', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer')[-1]
        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            role = user.get('role')

            if role != 'admin':
                abort(401)

        except Exception as e:
            print('JWT Decode Error', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
