# @author: xws    time: 2019/8/28 2:04

from rest_framework import serializers
from api import models


class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Role
        fields="__all__"
