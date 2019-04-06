from django.shortcuts import render
from django.db.utils import IntegrityError

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.authtoken.models import Token

from .serializers import *


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    data = request.data

    data['post'] = get_or_none(Post, name=data['post']).pk
    data['science_title'] = get_or_none(ScienceTitle, name=data['science_title']).pk
    try:
        data['science_degree'] = get_or_none(ScienceDegree, name=data['science_degree']).pk
    except (KeyError, AttributeError):
        data['science_degree'] = None

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
