from rest_framework.exceptions import APIException


class InvalidQueryStringParameter(APIException):
    status_code = 404
    default_detail = "Invalid query string parameters"
    default_code = "invalid_query_string"


class ModelObjectDoesNotExist(APIException):
    status_code = 404
    default_detail = "Object does not exist"
    default_code = "object_does_not_exist"


class ModelObjectAlreadyExist(APIException):
    status_code = 403
    default_detail = "Object already exist"
    default_code = "object_already_exist"