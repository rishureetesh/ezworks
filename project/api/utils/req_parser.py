from flask import request, jsonify
from functools import wraps

from project.api.utils.error_fun import wrong_length, wrong_data_type, missing_json_fields, json_required


def required_params(required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _json = request.get_json()
            if _json is None:
                response = json_required()
                return jsonify(response), 400

            missing = [r for r in required.keys()
                       if r not in _json]

            if missing:
                response = missing_json_fields(missing)
                return jsonify(response), 400
            wrong_types = [r for r in required.keys()
                           if not isinstance(_json[r], required[r])]

            if wrong_types:
                response = wrong_data_type(wrong_types)
                return jsonify(response), 400

            length_error = [r for r in required.keys() if isinstance(
                _json[r], str) and not len(_json[r])]

            if length_error:
                response = wrong_length(length_error)
                return jsonify(response), 400

            return fn(*args, **kwargs)

        return wrapper

    return decorator