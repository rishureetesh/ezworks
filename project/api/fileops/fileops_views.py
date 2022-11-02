from crypt import methods
from datetime import datetime, timedelta, timezone
import email
import json
import os
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
from project.api.utils.util_functions import response_json, allowed_file
from project.api.utils.constants import JsonConstants
from project.api.fileops.fileops_helper import list_file_helper, upload_file_helper, download_file_helper
from werkzeug.utils import secure_filename


file_bp = Blueprint("file_bp", __name__)

@file_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    claims = get_jwt()
    if "user_type" not in claims or claims['user_type'] == "client":
        return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"You don't have permission to access the endpoint!!!, {claims}"
            })
    upload_files = request.files
    if 'file' not in upload_files:
        return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"No files found!!!"
            })
    files = request.files.getlist('file')
    for file in files:
        filename = secure_filename(file.filename)
        mimetype = filename.rsplit('.', 1)[1].lower()
        if not allowed_file(filename):
            return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"{mimetype} file type not allowed!!!"
            })
    return upload_file_helper(claims['sub'], files)
    


@file_bp.route("/download/<file_uuid>", methods=["GET"])
@jwt_required()
def download_file(file_uuid):
    return download_file_helper(file_uuid)


@file_bp.route("/file-list", methods=["GET"])
@jwt_required()
def get_all_files():
    return list_file_helper()