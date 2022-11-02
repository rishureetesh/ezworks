from crypt import methods
from datetime import datetime, timedelta, timezone
import email
import json
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from project import app, db
from project.api.auth.auth_models import User, UserType
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies
from project.api.utils.req_parser import required_params
from project.api.auth.auth_helper import validate_data, register_me, verify_user_account
from project.api.utils.util_functions import response_json
from project.api.utils.constants import JsonConstants


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
@required_params({"email":str, "password":str})
@cross_origin()
def log_me_in():
    data = request.get_json()
    email = data['email']
    password = data['password']
    response = None
    sqldata = db.session.query(User).filter(User.email==email, User.password == password).first()
    if sqldata is not None and sqldata.email == email:
        user_type = db.session.query(UserType).filter(UserType.id == sqldata.user_type).first()
        additional_claims = {"user_type":user_type.name}
        access_token = create_access_token(identity=sqldata.email, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=sqldata.email, additional_claims=additional_claims)
        response = jsonify(msg="Login Successfull!!!", token=access_token)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    return jsonify(msg="Details not found!!!")


@auth.route("/register", methods=["POST"])
@required_params({'name':str, 'mobile':int, 'email':str, 'password':str, 'user_type':str})
def register_user():
    data = request.get_json()
    name = data.get('name', "")
    mobile = data.get('mobile', "")
    email = data.get('email', "")
    password = data.get('password', "")
    user_type = data.get('user_type',"")

    validate =  validate_data(name, mobile, email, password, user_type)

    if not validate['success']:
        return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"Please input correct data for user registration!!!"
            })
    return register_me(name, mobile, email, password, user_type)

@auth.route("/verify-user/<slug>", methods=["GET"])
def verify_user(slug):

    return verify_user_account(slug)


@auth.route("/logout", methods=["POST"])
@jwt_required()
def log_me_out():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response