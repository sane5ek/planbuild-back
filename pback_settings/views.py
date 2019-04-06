from django.shortcuts import render
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.authtoken.models import Token

from pback_main.models import *
from pback_auth.models import User

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit(request):
    data = request.data
    user = Token.objects.get(key=request.auth).user

    data['post'] = get_or_none(Post, name=data['post'])
    data['science_title'] = get_or_none(ScienceTitle, name=data['title'])
    try:
        data['science_degree'] = get_or_none(ScienceDegree, name=data['degree'])
    except KeyError:
        data['science_degree'] = None

    user.post = data['post']
    user.science_degree = data['science_degree']
    user.science_title = data['science_title']
    user.salary = data['salary']
    user.last_name = data['last_name']
    user.first_name = data['first_name']
    user.save()

    return Response(_build_dict_from_model(user), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def email(request):
    data = request.data
    user = Token.objects.get(key=request.auth).user
    user.email = data['email']

    try:
        user.save()
    except IntegrityError:
        return Response({}, status=status.HTTP_409_CONFLICT)

    return Response(_build_dict_from_model(user), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def password(request):
    user = Token.objects.get(key=request.auth).user
    old_password = request.data['old']
    new_password = request.data['new']

    check = check_password(old_password, user.password)
    if check:
        user.set_password(new_password)
    else:
        return Response(status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
    user.save()
    return Response(_build_dict_from_model(user), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def info(request):
    response = {
        'posts': [obj.name for obj in Post.objects.all()],
        'degrees': [obj.name for obj in ScienceDegree.objects.all()],
        'titles': [obj.name for obj in ScienceTitle.objects.all()]
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user(request):
    user = Token.objects.get(key=request.auth).user

    return Response(_build_dict_from_model(user), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def fields(request):
    user = Token.objects.get(key=request.auth).user
    fields = Field.objects.filter(owner=user.adopted_fields)

    data = fields_to_json(fields)

    if user.adopted_fields is None:
        owner = 'default'
    elif user.adopted_fields == user:
        owner = 'user'
    else:
        owner = user.adopted_fields.email

    return Response(data, status=status.HTTP_200_OK, headers={
        'owner': owner,
        'Access-Control-Expose-Headers': 'owner'
    })


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def default(request):
    user = Token.objects.get(key=request.auth).user
    Field.objects.filter(owner=user).delete()
    for us in User.objects.filter(adopted_fields=user):
        us.adopted_fields = None
        us.save()

    fields = Field.objects.filter(owner=None)
    response = fields_to_json(fields)

    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def owner(request):
    user = Token.objects.get(key=request.auth).user
    owner = request.data['owner']

    if owner == 'default':
        user.adopted_fields = None
    elif owner == 'user':
        user.adopted_fields = user
    else:
        adopt_user = get_or_none(User, email=owner)
        if adopt_user:
            user.adopted_fields = adopt_user
    user.save()
    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def save(request):
    user = Token.objects.get(key=request.auth).user
    fields = request.data['fields']
    types = Load.objects.all()

    Field.objects.filter(owner=user).delete()

    newFields = [Field(
            column_in_load=field['loadColumn'],
            column_in_plan=field['planColumn'],
            name_in_load=field['loadName'],
            name_in_plan=field['planName'],
            load_type=field['studyType'],
            type_of_load=get_type_of_load(types, field['courseType']),
            owner=user
        ) for field in fields]

    Field.objects.bulk_create(newFields)

    return Response({}, status=status.HTTP_200_OK)


def get_type_of_load(types, name):
    for lType in types:
        if lType.name == name:
            return lType


def _build_dict_from_model(user):
    degree = user.science_degree.name if user.science_degree else ''
    return {
        'email': user.email,
        'post': user.post.name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'degree': degree,
        'title': user.science_title.name,
        'salary': user.salary
    }


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def fields_to_json(fields):
    return [{
                'planName': field.name_in_plan,
                'loadName': field.name_in_load,
                'planColumn': field.column_in_plan,
                'loadColumn': field.column_in_load,
                'studyType': field.load_type,
                'courseType': field.type_of_load.name
            } for field in fields]
