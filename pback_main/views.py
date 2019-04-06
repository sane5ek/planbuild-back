from django.shortcuts import render
from django.db.utils import IntegrityError
from django.utils.encoding import smart_str
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.authtoken.models import Token

from .models import *
from pback_auth.models import User

import base64


@api_view(['PUT'])
@permission_classes((AllowAny,))
@parser_classes((MultiPartParser,))
def upload(request):
    user = None

    new_file = UploadFile(file=request.data['file'], owner=user)
    new_file.save()
    new_file.convert_file_to_xlsx()

    return Response({'filename': new_file.file.name}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((AllowAny,))
def subjects(request):
    user = None
    path = request.data['filename']
    if not path:
        return Response(status=status.HTTP_404_NOT_FOUND)
    Subject.objects.set_objects_from_excel(path, user)
    return Response(Subject.objects.get_objects_json(user), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def plan(request):
    email = request.data['email']
    user = get_or_none(User, email=email)
    subjects = request.data['subjects']
    course = request.data['course']
    diploma = request.data['diploma']
    load_path = request.data['filename']
    template_path = 'files/Template.xlsx'

    Field.objects.FillTemplate(subjects, course, diploma, load_path, template_path, user)

    path_to_file = PlanFile.objects.filter(owner=user).last().file.name
    with open(path_to_file, 'rb') as f:
        data = f.read()
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path_to_file)
    response['Filename'] = path_to_file
    response['Access-Control-Expose-Headers'] = 'Filename'
    return response


@api_view(['POST'])
@permission_classes((AllowAny,))
def again(request):
    path_to_file = request.data['filename']
    with open(path_to_file, 'rb') as f:
        data = f.read()
    response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path_to_file)

    return response


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
