from django.views import View
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http.response import JsonResponse

from fractal_service.helpers.validator import Validator

from .models import Buckets, ToDOs
from .validators import CREATE_TODO, UPDATE_TODO


class Bucket(View):
    def get(self, request, *args, **kwargs):
        try:
            all_buckets = list(Buckets.objects.all().order_by('id').values('id', 'name'))
            return JsonResponse(data=all_buckets, status=200,  safe=False)
        except Exception as e:
            res_msg = {
                'msg': str(e)
            }
            return JsonResponse(data=res_msg, status=500)


class ToDo(View):
    def get(self, request, *args, **kwargs):
        try:
            all_todos = list(ToDOs.objects.select_related('bucket').all().order_by('id').values(
                'id',
                'name',
                'done',
                bucketId=F('bucket__id'),
                bucketName=F('bucket__name'),
            ))
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
                'name':'test todo',
                'done':true,
                'bucketId':1,
                'bucketName':'test bucket',
            }
        '''
        try:
            with transaction.atomic():
                params = request.params
                bucket_id = params.get('bucketId')
                bucket_name = params.get('bucketName')
                if not bucket_id:
                    bucket_obj = Buckets.objects.create(name=params['bucketName'])
                    bucket_id = bucket_obj.id
                    bucket_name = bucket_obj.name

                todo_obj = ToDOs.objects.create(
                    name=params['name'],
                    bucket_id=bucket_id,
                    done=params['done']
                )
                res_dict = {
                    'id': todo_obj.id,
                    'name': todo_obj.name,
                    'done': todo_obj.done,
                    'bucketId': bucket_id,
                    'bucketName': bucket_name,
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

    @Validator(UPDATE_TODO)
    def put(self, request, *args, **kwargs):
        '''
            req_body={
                    "name":"Fix the task",
                    "done":true,
                    "bucketName":"hI"
                }
        '''
        try:
            params = request.params
            id = kwargs.get('id')
            todo_obj = ToDOs.objects.get(id=id)
            todo_obj.name = params['name']
            todo_obj.done = params['done']
            bucket_id = params.get('bucketId')
            bucket_name = params.get('bucketName')
            if not bucket_id:
                bucket_obj = Buckets.objects.create(name=params['bucketName'])
                bucket_id = bucket_obj.id
                bucket_name = bucket_obj.name

            todo_obj.bucket_id = bucket_id
            todo_obj.save()
            res_data = {
                'id': todo_obj.id,
                'name': todo_obj.name,
                'bucketId': bucket_id,
                'bucketName': bucket_name
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
        try:
            id = kwargs.get('id')
            ToDOs.objects.get(id=id).delete()
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
