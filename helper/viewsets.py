from django.http import QueryDict


#decorator
def add_user_id_to_request_data(func):
    def wrapper(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
        return func(self, request, *args, **kwargs)
    return wrapper

