from datetime import datetime
from decimal import Decimal
from functools import wraps

from django.utils.decorators import available_attrs
from django.http.response import JsonResponse

from fractal_service.exceptions import InvalidRequest


class Validator():
    def __init__(self, param_types=[]):
        self.param_types = param_types

    def validate_datetime(self, key, date_str, *args):
        date_fmt = '%Y-%m-%d'
        date_str = date_str.split('T')[0] if 'T' in date_str else date_str
        try:
            datetime.strptime(date_str, date_fmt)
        except Exception:
            raise InvalidRequest(
                '{} should be of date type and format should be YY-mm-dd'.format(key))

    def validate_enum(self, key, value, enum_list):
        if value not in enum_list:
            raise InvalidRequest('{} is having invalid value'.format(key))

    def validate_Decimal(self, key, value, *args):
        try:
            Decimal(value)
        except Exception as e:
            raise InvalidRequest(
                '{} should be of decimal type'.format(key))

    def validate_params_type(self, key, key_type, value, enum_list, blank):
        if blank:
            return
        try:
            attr = getattr(self, 'validate_{}'.format(key_type.__name__))
            attr(key, value, enum_list)
        except AttributeError as e:
            if type(value) != key_type:
                raise InvalidRequest('{} should be of {} type'.format(
                    key, key_type.__name__
                ))

    @staticmethod
    def is_allow_blank(request_dict, blank):
        allow_blank = False
        try:
            allow_blank = blank[0]
            try:
                dependent_field = blank[1]
                dependent_field_value = request_dict[dependent_field]
                if dependent_field_value:
                    allow_blank = True
                else:
                    allow_blank = False
                return allow_blank
            except IndexError:
                return allow_blank

        except IndexError:
            return allow_blank

    def is_valid(self, request_dict, required_params_with_type):
        '''
            required_params_with_type shape should be list of dicts
            [{'field_name':'sample',
                'type': int,
                'required': True,
                'choices':('me','abhi'),
                If you are expecting a field that can be empty only if dependent field has value, then pass dependent field_name in 2nd index of touple
                'blank': (True, 'if_any_dipendent_field_name')
            }]
        '''
        for params in required_params_with_type:
            key = params['field_name']
            key_type = params['type']
            enum_list = params.get('choices', ())
            blank = params.get('blank', ())

            if key in request_dict.keys():
                value = request_dict[key]
                allow_blank = self.is_allow_blank(request_dict, blank)
                if not value and value != 0 and not allow_blank:
                    raise InvalidRequest('{} can\'t be empty or None'.format(key))
                self.validate_params_type(key, key_type, value, enum_list, blank)
            else:
                required = params.get('required', True)
                if required:
                    raise InvalidRequest('{} is missing in request body'.format(
                        key
                    ))
            return True

    def __call__(self, func, *args, **kwargs):
        @wraps(func, assigned=available_attrs(func))
        def inner(*args, **kwargs):
            try:
                request = args[1]
                self.is_valid(request.params, self.param_types)
                return func(*args, **kwargs)
            except InvalidRequest as e:
                return JsonResponse(data={
                    'msg': str(e)
                },
                    status=422
                )
            except Exception as e:
                return JsonResponse(data={
                    'msg': str(e)
                },
                    status=500
                )
        return inner
