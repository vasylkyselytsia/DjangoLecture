from rest_framework import serializers
from . import models


class CategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        exclude = ()
