from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View

from rest_framework.viewsets import ModelViewSet

from DatawizInternsip.permissions import ReadOnlyPermission
from api.serializers import CategoryModelSerializer
from . import models


class IndexView(View):

    def get(self, request):
        context = {"categories": list(models.Category.objects.filter(parent__isnull=False)
                                      .values("id", "name").annotate(product_count=Count("products", distinct=True)))}

        return render(request, "index.html", context=context)


class CategoryViewSet(ModelViewSet):

    queryset = models.Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (ReadOnlyPermission,)
