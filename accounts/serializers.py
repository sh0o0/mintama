from collections import OrderedDict

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from django_filters import rest_framework as filter

from .models import User, Category, Portfolio, Reference
from .constant import RESIDENCE_CHOICIES, CRACK_LEVEL_CHOICIES, GENDER_CHOICIES


class UserSerializer(serializers.ModelSerializer):
    clear_icon = serializers.SerializerMethodField()
    introduction = serializers.CharField(allow_blank=True, allow_null=True, trim_whitespace=True)
    icon = serializers.ImageField(max_length=None, allow_empty_file=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'gender',
            'residence',
            'learning_started_date',
            'crack_level',
            'icon',
            'introduction',
            'clear_icon',
        ]

    def get_clear_icon(self, instance):
        initial_data = getattr(self, 'initial_data', None)
        if initial_data is None: return None

        if initial_data['clear_icon'] == 'true':
            ret = True
        else:
            ret = False

        return ret

    def update(self, instance, validated_data):
        ret = super().update(instance, validated_data)
        is_clear_icon = self.get_clear_icon(instance)
        if is_clear_icon:
            instance.icon.delete(save=True)
        return ret

    def create(self, validated_data):
        return super().create(validated_data)

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

    #validate_<field_name>でvalidate_dataをいじれる
    def validate_icon(self, value):
        return value

    #overrideでフィールドを追加できる。
    def to_internal_value(self, data):
        return super().to_internal_value(data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = [
            'user',
            'title',
            'evaluation',
            'content',
            'link',
        ]


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = [
            'user',
            'title',
            'content',
            'link',
        ]