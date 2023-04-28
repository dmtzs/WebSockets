try:
    from app import app
    from http import HTTPStatus
    from flask import Response, make_response, jsonify
except ImportError as eImp:
    print(f"The following import ERROR occurred in {__file__}: {eImp}")

# -----------------------------App errors-----------------------------
@app.errorhandler(HTTPStatus.NOT_FOUND.value)
def access_error_404(error) -> Response:
    resp_json = {
        "code_title": error.name,
        "description": error.description
    }
    return make_response(jsonify(resp_json), error.code)

@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
def access_error_500(error) -> Response:
    resp_json = {
        "code_title": error.name,
        "description": error.description
    }
    return make_response(jsonify(resp_json), error.code)