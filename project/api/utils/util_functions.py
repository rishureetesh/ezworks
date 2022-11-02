import datetime
import json
from random import randint

import pytz

from project.api.utils.constants import JsonConstants, ServerResponse, HTTPStatusCode
from project.api.utils.dbOperations import alchemy_encoder
TZ = 330


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def bad_request_error():
    error = {JsonConstants.msg: ServerResponse.badRequest,
             JsonConstants.status: HTTPStatusCode.BadRequest,  JsonConstants.success: False}
    return json.dumps(error, default=alchemy_encoder), HTTPStatusCode.BadRequest, {JsonConstants.contentType: JsonConstants.applicationJson}


def missing_params_error():
    error = {JsonConstants.msg: ServerResponse.missingParams,
             JsonConstants.status: 400, JsonConstants.success: False}
    return json.dumps(error, default=alchemy_encoder), 400, {JsonConstants.contentType: JsonConstants.applicationJson}


def internal_server_error():
    error = {JsonConstants.msg: ServerResponse.serverError,JsonConstants.success: False}
    return json.dumps(error, default=alchemy_encoder), 502, {JsonConstants.contentType: JsonConstants.applicationJson}

def internal_server_error_msg():
    error = {JsonConstants.msg: ServerResponse.serverError,JsonConstants.success: False}
    return error

def get_data_inconsistency_error(error_msg):
    if error_msg == None:
        error = {JsonConstants.msg: "An unexpected error occurred. This could be because of temporary DB connectivity issues or data inconsistencies in the database ", JsonConstants.status: 500,  JsonConstants.success: False}
    else:
        error = {JsonConstants.msg: error_msg, JsonConstants.status: 500,  JsonConstants.success: False}
    return json.dumps(error, default=alchemy_encoder), 500, {JsonConstants.contentType: JsonConstants.applicationJson}

def data_not_found_error(error_msg):
    error = {JsonConstants.msg: error_msg, JsonConstants.status: 422,  JsonConstants.success: False}
    return json.dumps(error, default=alchemy_encoder), 422, {JsonConstants.contentType: JsonConstants.applicationJson}

def valid_number(phone_number):
    if len(phone_number) != 10:
        return False

    for i in range(len(phone_number)):
        if i == 0 and phone_number[0] == '0':
            return False

    if phone_number.isalnum():
        return True
        
    return False

def connection_db_error():
    error = {JsonConstants.msg: ServerResponse.connnectionDbError,
             JsonConstants.success: False}
    return json.dumps(error, default=alchemy_encoder), 500, {JsonConstants.contentType: JsonConstants.applicationJson}


def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True


def response_json(data):
    return json.dumps(data, default=alchemy_encoder), 200, {JsonConstants.contentType: JsonConstants.applicationJson}


def get_current_date():
    current_date = datetime.datetime.now(pytz.timezone(TZ))
    year = str(current_date.year)
    month = "0" + str(current_date.month) if len(str(current_date.month)
                                                 ) < 2 else str(current_date.month)
    day = "0" + str(current_date.day) if len(str(current_date.day)
                                             ) < 2 else str(current_date.day)
    return '"' + year + "-" + month + "-" + day + " 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-" + day + " 23:59:59" + '"'


def get_current_week():
    current_date = datetime.datetime.now(pytz.timezone(TZ))
    year = str(current_date.year)
    month = "0" + str(current_date.month) if len(str(current_date.month)
                                                 ) < 2 else str(current_date.month)
    day = current_date.day
    if day <= 7:
        return '"' + year + "-" + month + "-01 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-07 23:59:59" + '"'
    elif day > 7 and day <= 14:
        return '"' + year + "-" + month + "-08 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-14 23:59:59" + '"'
    elif day > 14 and day <= 21:
        return '"' + year + "-" + month + "-15 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-21 23:59:59" + '"'
    elif day > 21 and day <= 31:
        return '"' + year + "-" + month + "-22 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-31 23:59:59" + '"'


def get_week_range(slot):
    current_date = datetime.datetime.now(pytz.timezone(TZ))
    year = str(current_date.year)
    month = "0" + str(current_date.month) if len(str(current_date.month)
                                                 ) < 2 else str(current_date.month)
    if slot == 1:
        return '"' + year + "-" + month + "-01 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-07 23:59:59" + '"'
    elif slot == 2:
        return '"' + year + "-" + month + "-08 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-14 23:59:59" + '"'
    elif slot == 3:
        return '"' + year + "-" + month + "-15 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-21 23:59:59" + '"'
    elif slot == 4:
        return '"' + year + "-" + month + "-22 00:00:00" + '"' + " and " + '"' + year + "-" + month + "-31 23:59:59" + '"'

def get_age(dob):
    try:
        born = datetime.datetime.strptime(dob, '%m/%d/%Y')
        today = datetime.date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        if age < 18 and age > 99:
            return False
        return True
    except Exception as e:
        return False

def response_with_status(data, status):
    return json.dumps(data, default=alchemy_encoder), status, {JsonConstants.contentType: JsonConstants.applicationJson}


def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['pptx', 'docx', 'xlsx', 'pdf']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS