from project import db
import uuid
from project.config import HOST, PORT
from project.api.auth.auth_models import User, UserType
from project.api.utils.util_functions import response_json, internal_server_error
from project.api.utils.constants import JsonConstants, ServerResponse, HTTPStatusCode, FieldInvalidResponse
from project.api.utils.validate_email import regex_email

def validate_data(name, mobile, email, password, user_type):
    response = {
        'success':True,
        'error':''
    }
    if name is None or not name:
        response['success'] = False
        response['error'] = 'Name Required'
    elif not mobile or not isinstance(mobile, int):
        response['success'] = False
        response['error'] = 'Invalid Mobile number'
    elif password is None or not password:
        response['success'] = False
        response['error'] = 'Password Required'
    elif user_type not in ['client', 'operation']:
        response['success'] = False
        response['error'] = "User type must be in ['client', 'operation']"

    if email and not regex_email(email):
        response['success'] = False
        response['error'] = 'Invalid Email ID'
    return response


def register_me(name, mobile, email, password, user_type):
    try:

        sqldata = db.session.query(User).filter(User.email==email).first()
        if sqldata is not None and sqldata.email == email:
            return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"Email Exists!!!"
            })
        
        user_type_data = db.session.query(UserType).filter(UserType.name==user_type).first()

        user =User(
            name=name,
            mobile=mobile,
            email=email,
            password=password,
            verification_slug=uuid.uuid4().hex,
            verified=False if user_type_data.name == "client" else True,
            user_type = user_type_data.id
        )

        user.create()
        return response_json({
            JsonConstants.success : True,
            JsonConstants.msg : f"User Registered!!!, Please click on this link to verify your profile http://{HOST}:{PORT}/api/auth/verify-user/{user.verification_slug}" if user_type == "client" else "User Registered!!!"
        })
    except Exception as e:
        db.session.rollback()
        print(e, flush=True)
        return internal_server_error()
    finally:
        db.session.close()

def verify_user_account(slug):
    try:

        sqldata = db.session.query(User).filter(User.verification_slug==slug).first()
        if sqldata is not None and sqldata.verified == True:
            return response_json({
                JsonConstants.success : False,
                JsonConstants.msg : f"Verification URL not found!!!"
            })

        sqldata.verified = True
        return response_json({
            JsonConstants.success : True,
            JsonConstants.msg : f"User account activated!!!"
        })
    except Exception as e:
        db.session.rollback()
        print(e, flush=True)
        return internal_server_error()
    finally:
        db.session.commit()
        db.session.close()