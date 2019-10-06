from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.fields import empty
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject


class IncludeWithExcludeParamsError(APIException):
    status_code = 404
    default_detail = 'includeとexcludeを一緒に指定することはできません。'
    default_code = 'error'


class SkipNoneModelSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields
        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # KEY IS HERE:
            if attribute in [None, '']:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret


class DecideResponseDataModelSerializer(serializers.ModelSerializer):

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        #includeを抽出
        request = self._context.get('request', object)
        query_params = getattr(request, 'query_params', {})
        if query_params:
            self.include_field = self.extract_list_for_query_params(query_params, 'include')
            self.exclude_field = self.extract_list_for_query_params(query_params, 'exclude')
            if len(self.include_field) and len(self.exclude_field):
                raise IncludeWithExcludeParamsError

    def extract_list_for_query_params(self, query_params, key):
        param = query_params.get(key, None)
        if param is None:
            return []
        else:
            return [x.strip() for x in param.split(',')]

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        include_field = getattr(self, 'include_field', None)
        exclude_field = getattr(self, 'exclude_field', None)

        for field in fields:

            if include_field:
                if field.field_name not in include_field:
                    continue

            if exclude_field:
                if field.field_name in exclude_field:
                    continue

            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

