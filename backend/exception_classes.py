from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class InvalidQueryStringParameter(APIException):
    status_code = 400
    default_detail = "Invalid query string parameters"
    default_code = "invalid_query_string"


class ModelObjectDoesNotExist(APIException):
    status_code = 404
    default_detail = "Object does not exist"
    default_code = "object_does_not_exist"


class ModelObjectAlreadyExist(APIException):
    status_code = 409
    default_detail = "Object already exist"
    default_code = "object_already_exist"