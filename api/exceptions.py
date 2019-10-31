from rest_framework.exceptions import APIException


class UsernameNoneException(APIException):
    status_code = 400
    default_detail = '不正なURLです。正しいusernameを入力してください。'
    default_code = 'error'


class IncludeWithExcludeParamsError(APIException):
    status_code = 404
    default_detail = 'includeとexcludeを一緒に指定することはできません。'
    default_code = 'error'

