# coding: utf-8
from django.utils import six

from rest_framework import serializers
from rest_framework.fields import Field


class ModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs.pop('meta_fields', None)
        kwargs.pop('meta_exclude', None)
        kwargs.pop('meta_preset', None)
        super(ModelSerializer, self).__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        if 'meta_fields' in kwargs:
            fields = kwargs.pop('meta_fields')
            if fields == '__all__':
                fields = []
            return cls.meta_fields(*fields)(*args, **kwargs)
        if 'meta_exclude' in kwargs:
            return cls.meta_exclude(*kwargs.pop('meta_exclude'))(*args, **kwargs)
        if 'meta_preset' in kwargs:
            return cls.meta_preset(kwargs.pop('meta_preset'))(*args, **kwargs)
        return super(ModelSerializer, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def meta_fields(cls, *fields):
        """
        Create new class based on the current with overrode Meta parameters.
        Option `exclude` of base serializer is going to None.

        Example of usage in serializers:
        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User

        class ItemSerializer(serializers.ModelSerializer):
            user = UserSerializer(meta_fields=['id', 'name'])

            class Meta:
                model = Item

        Example of usage in views:
        class UserViewSet(viewsets.ModelViewSet):
            serializer_class = UserSerializer.meta_fields('id', 'name', 'expiration_date')
        """
        if not len(fields):
            fields = '__all__'
        meta = getattr(cls, 'Meta', type(str('Meta'), (object,), {}))
        return type(cls.__name__, (cls, object), {
            six.text_type('Meta'): type(str('Meta'), (meta, object), {
                six.text_type('fields'): fields,
                six.text_type('exclude'): None
            })
        })

    @classmethod
    def meta_exclude(cls, *exclude):
        """
        Create new class based on the current with overrode Meta parameters.
        If base serializer has meta option `fields`, fields will exclude from its.

        Example of usage in serializers:
        class UserSerializer(serializers.ModelSerializer):
            products = ProductsSerializer(many=True)

            class Meta:
                model = User

        class ItemSerializer(serializers.ModelSerializer):
            user = UserSerializer(meta_exclude=['products'])

            class Meta:
                model = Item

        Example of usage in views:
        class UserViewSet(viewsets.ModelViewSet):
            serializer_class = UserSerializer.meta_exclude('products')
        """
        meta = getattr(cls, 'Meta', type(str('Meta'), (object,), {}))
        meta_fields = getattr(meta, 'fields', None)
        exclude_props = []
        if isinstance(meta_fields, list) or isinstance(meta_fields, tuple):
            meta_fields = [field_ for field_ in meta_fields if field_ not in exclude]
            exclude = None
        else:
            meta_fields = None
            exclude_props = [key for key, prop in cls._declared_fields.items() if isinstance(prop, Field)]
            exclude = list(filter(lambda f: f not in exclude_props, exclude))
        cls_dict = {
            'Meta': type(str('Meta'), (meta, object), {
                six.text_type('fields'): meta_fields,
                six.text_type('exclude'): exclude
            })
        }
        cls_dict.update({field: None for field in exclude_props})
        return type(cls.__name__, (cls, object), cls_dict)

    @classmethod
    def meta_preset(cls, name):
        """
        Create new class based on the current with overrode Meta parameters.
        It will check meta option `presets` and try to get it by name.
        Presets - prepared some schemes, which simplify manipulating with meta option.

        Example of usage in serializers:
        class UserSerializer(serializers.ModelSerializer):
            products = ProductsSerializer(many=True)

            class Meta:
                model = User
                presets = {
                    'short': {
                        'fields': ['id', 'name']
                    },
                    'light': {
                        'exclude': ['products']
                    }
                }

        class ItemSerializer(serializers.ModelSerializer):
            user = UserSerializer(meta_preset='short')

            class Meta:
                model = Item

        Example of usage in views:
        class UserViewSet(viewsets.ModelViewSet):
            serializer_class = UserSerializer.meta_preset('light')
        """
        meta = getattr(cls, 'Meta', type(str('Meta'), (), {}))
        presets = getattr(meta, 'presets', {})
        preset = presets.get(name, None)
        assert preset is not None, ('Preset of `%s` with `%s` name doesn\'t exist.' % (cls.__name__, name))
        return type(cls.__name__, (cls,), {
            str('Meta'): type(str('Meta'), (meta, object), preset)
        })
