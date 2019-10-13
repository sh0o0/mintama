from rest_framework.exceptions import APIException


class UsernameNoneException(APIException):
    status_code = 400
    default_detail = '不正なURLです。正しいusernameを入力してください。'
    default_code = 'error'