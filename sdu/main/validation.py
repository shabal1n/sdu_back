from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import DataError
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


from rest_framework.utils.representation import smart_repr


def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
class APIException200(exceptions.APIException):
    status_code = 200

def qs_exists(queryset):
    try:
        return queryset.exists()
    except (TypeError, ValueError, DataError):
        return False


def qs_filter(queryset, **kwargs):
    try:
        return queryset.filter(**kwargs)
    except (TypeError, ValueError, DataError):
        return queryset.none()
    
class UniqueValidator:
    message = _('This field must be unique.')
    requires_context = True

    def __init__(self, queryset, message=None, lookup='exact'):
        self.queryset = queryset
        self.message = message or self.message
        self.lookup = lookup

    def filter_queryset(self, value, queryset, field_name):
        filter_kwargs = {'%s__%s' % (field_name, self.lookup): value}
        return qs_filter(queryset, **filter_kwargs)

    def exclude_current_instance(self, queryset, instance):
        if instance is not None:
            return queryset.exclude(pk=instance.pk)
        return queryset

    def __call__(self, value, serializer_field):
        field_name = serializer_field.source_attrs[-1]
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if qs_exists(queryset):
            raise APIException200(detail={"status": "error", "error": {field_name: self.message}})

    def __repr__(self):
        return '<%s(queryset=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.queryset)
        )