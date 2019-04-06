from .models import *
from pback_main.models import Post, ScienceDegree, ScienceTitle

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            post=validated_data['post'],
            science_degree=validated_data['science_degree'],
            science_title=validated_data['science_title'],
            salary=validated_data['salary']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'post', 'first_name', 'last_name', 'password', 'science_degree', 'science_title', 'salary')
        write_only_fields = ('password',)
