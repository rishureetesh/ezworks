from project.api.utils.util_functions import allowed_file
from project import db, app
import uuid
import os
from project.config import HOST, PORT, PATH
from project.api.auth.auth_models import User, UserType
from project.api.utils.util_functions import response_json, internal_server_error
from project.api.utils.constants import JsonConstants, ServerResponse, HTTPStatusCode, FieldInvalidResponse
from project.api.utils.validate_email import regex_email
from project.api.fileops.fileops_models import File
from werkzeug.utils import secure_filename
from flask import send_file

def upload_file_helper(user_email, files):
    try:
        for file in files:
            filename = secure_filename(file.filename)
            filenameuuid = uuid.uuid4().hex
            FILE_EXTENSION = filename.rsplit('.', 1)[1].lower()
            UUID_FILENAME = str(filenameuuid) + '.' + FILE_EXTENSION
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], UUID_FILENAME))
            file_data = File(
                name=filename,
                slug_id=uuid.uuid4().hex,
                uploaded_by=user_email,
                file_uuid=UUID_FILENAME
            )
            file_data.create()
        return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"File Uploaded Successfully!!!"
            })
    except Exception as e:
        db.session.rollback()
        print(e, flush=True)
        return internal_server_error()
    finally:
        db.session.commit()
        db.session.close()

def download_file_helper(file_uuid):
    try:
        file = db.session.query(File).filter(File.slug_id==file_uuid).first()
        if not file or file is None:
            return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"File doesn't Exists!!!"
        })
        FILE_PATH = os.path.join(app.config['UPLOAD_FOLDER'], file.file_uuid)
        if os.path.exists(FILE_PATH):
            return send_file(FILE_PATH)
        return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"Oops File not found!!!"
            })
    except Exception as e:
        db.session.rollback()
        print(e, flush=True)
        return internal_server_error()
    finally:
        db.session.commit()
        db.session.close()

def list_file_helper():
    try:
        files = db.session.query(File).all()
        file_data = []
        for file in files:
            file_data.append({
                "id":file.slug_id,
                "filename":file.name,
                "Message": "Pass this id in get URL of Download endpoint."
            })
        return response_json({
                JsonConstants.success : True,
                JsonConstants.msg : file_data
            })
    except Exception as e:
        db.session.rollback()
        print(e, flush=True)
        return internal_server_error()
    finally:
        db.session.close()