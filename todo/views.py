from django.views import View
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http.response import JsonResponse

from fractal_service.helpers.validator import Validator

from .models import ToDOs, Buckets
from .validators import CREATE_TODO


class ToDo(View):
    def get(self, request, *args, **kwargs):
        try:
            all_todos = list(ToDOs.objects.all().values('id', 'name', 'bucket__id', 'bucket__name'))
            return JsonResponse(data=all_todos, status=200,  safe=False)
        except Exception as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=500)

    @Validator(CREATE_TODO)
    def post(self, request, *args, **kwargs):
        '''
            req_body={
                'bucket__id':1,
                'bucket__name':'test bucket',
                'name':'test todo'
            }
        '''
        try:
            with transaction.atomic():
                params = request.params
                bucket_id = params.get('bucket__id')
                bucket_name = params.get('bucket__name')
                if not bucket_id:
                    bucket_obj = Buckets.objects.create(name=params['bucket__name'])
                    bucket_id = bucket_obj.id
                    bucket_name = bucket_obj.name

                todo_obj = ToDOs.objects.create(name=params['name'], bucket_id=bucket_id)
                res_dict = {
                    'bucket__id': bucket_id,
                    'bucket__name': bucket_name,
                    'id': todo_obj.id,
                    'name': todo_obj.name
                }
                return JsonResponse(data=res_dict, status=200)
        except ValidationError as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=422)
        except Exception as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=500)

    def put(self, request, *args, **kwargs):
        '''
            req_body={
                'id':1,
                'name':'test todo'
            }
        '''
        try:
            params = request.params
            todo_obj = ToDOs.objects.get(id=params['id'])
            todo_obj.name = params['name']
            bucket_id = params.get('bucket__id')
            bucket_name = params.get('bucket__name')
            if not bucket_id:
                bucket_obj = Buckets.objects.create(name=params['bucket__name'])
                bucket_id = bucket_obj.id
                bucket_name = bucket_obj.name

            todo_obj.bucket_id = bucket_id
            todo_obj.save()
            res_data = {
                'id': todo_obj.id,
                'name': todo_obj.name,
                'bucket__id': bucket_id,
                'bucket__name': bucket_name
            }
            return JsonResponse(data=res_data, status=200)
        except ObjectDoesNotExist as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=404)
        except ValidationError as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=422)
        except Exception as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=500)

    def delete(self, request, *args, **kwargs):
        '''
            req_body={
                'id':1,
            }
        '''
        try:
            params = request.params
            ToDOs.objects.get(id=params['id']).delete()
            res_msg = {
                'msg': 'Todo deleted succesfully.'
            }
            return JsonResponse(data=res_msg, status=200)
        except ObjectDoesNotExist as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=404)
        except ValidationError as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=422)
        except Exception as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=500)
