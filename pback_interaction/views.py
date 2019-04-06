from django.shortcuts import render
from django.db.utils import IntegrityError
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.authtoken.models import Token

from pback_auth.models import User
from pback_main.models import Request, RequestType, RequestResultType


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def search(request):
    user = Token.objects.get(key=request.auth).user
    text = request.data['search'].split(' ')

    queryset = set()
    for piece in text:
        for query in User.objects.filter(first_name__icontains=piece):
            queryset.add(query)
        for query in User.objects.filter(last_name__icontains=piece):
            queryset.add(query)
        for query in User.objects.filter(email__icontains=piece):
            queryset.add(query)

    data = {'users': User.objects.all()} if text == '' else {'users': queryset}

    if user in data['users']:
        data['users'].remove(user)

    return Response(user_queryset_to_json(data['users']), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def adopt(request):
    user = Token.objects.get(key=request.auth).user
    adopt = get_or_none(User, email=request.data['email'])

    if not adopt:
        return Response(status=status.HTTP_404_NOT_FOUND)

    old_request = get_or_none(Request, result=None, receiver=adopt, sender=user)

    if old_request:
        return Response(status=status.HTTP_303_SEE_OTHER)

    new_request = Request()
    new_request.sender = user
    new_request.receiver = adopt
    new_request.type = RequestType.objects.get(name='Adopt')
    new_request.save()

    return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def request(request):
    user = Token.objects.get(key=request.auth).user
    requests = Request.objects.all()
    return Response(requests_to_json(requests, user), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def accept(request):
    user = Token.objects.get(key=request.auth).user
    req = get_or_none(Request, id=request.data['id'])
    req.result = get_or_none(RequestResultType, name='True')
    req.answer_date = timezone.now()
    req.save()

    req.sender.adopted_fields = user
    req.sender.save()

    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def decline(request):
    user = Token.objects.get(key=request.auth).user
    req = get_or_none(Request, id=request.data['id'])
    req.result = get_or_none(RequestResultType, name='False')
    req.answer_date = timezone.now()
    req.save()

    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def cancel(request):
    user = Token.objects.get(key=request.auth).user
    req = get_or_none(Request, id=request.data['id'])
    req.delete()

    return Response({}, status=status.HTTP_200_OK)


def user_queryset_to_json(queryset):
    return [{
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'fields': get_adopted_name(user)
    } for user in queryset]


def get_adopted_name(user):
    if user.adopted_fields == user:
        return 'user'
    elif user.adopted_fields is None:
        return 'default'
    else:
        return user.adopted_fields.email


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def requests_to_json(requests, user):
    return [{
        'id': request.id,
        'user': request.receiver.email if request.sender == user else request.sender.email,
        'date': request.create_date.strftime('%d.%m.%Y %H:%M:%S'),
        'status': request.result if request.result is None else to_bool(request.result.name),
        'type': False if request.sender == user else True,
    } for request in requests
      if request.sender == user or request.receiver == user]


def to_bool(string):
    return True if 'True' in string else False
