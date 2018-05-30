from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from DatawizInternsip.permissions import ReadOnlyPermission
from . import serializers
from . import models


class IndexView(View):

    def get(self, request):
        context = {"categories": list(models.Category.objects.filter(parent__isnull=False)
                                      .values("id", "name").annotate(product_count=Count("products", distinct=True)))}

        return render(request, "index.html", context=context)


class CategoryViewSet(ModelViewSet):

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryModelSerializer
    permission_classes = (ReadOnlyPermission,)

    @action(methods=["GET"], detail=False, url_path="tree")
    def category_tree(self, request):
        categories = models.Category.objects.filter(parent__isnull=True)
        result = []
        for category in categories:
            result.append({"name": category.name, "id": category.id,
                           "children": list(category.children().values("id", "name"))})
        return Response(result)


class BrandViewSet(ModelViewSet):

    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandModelSerializer
    permission_classes = (ReadOnlyPermission,)


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer

    @action(methods=["POST"], detail=False, url_path="filter")
    def products_filter(self, request):
        validator = serializers.FilterProductSerializer(data=request.data)
        validator.is_valid(raise_exception=True)

        queryset = self.get_queryset().filter(**validator.validated_data["filters"])
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderModelSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.closed:
            raise ValidationError("Order Closed Now!")
        return super(OrderViewSet, self).update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if self.get_queryset().filter(closed=True).exists():
            raise ValidationError("You have unClosed Order!")
        return super(OrderViewSet, self).create(request, *args, **kwargs)

    def order_update(self, order):
        order.total_price = order


    @action(methods=["POST"], detail=True, url_path="add_product")
    def add_product(self, request, *args, **kwargs):
        order = self.get_object()
        if order.closed:
            raise ValidationError("Order Closed Now!")
        params = request.data
        params.update({"order": order.id})
        item_validator = serializers.OrderItemModelSerializer(data=params)
        item_validator.is_valid(raise_exception=True)
        if order.orderitem_set.filter(product=item_validator.validated_data["product"]).exists():
            raise ValidationError("Order has item for given Product. Use `update_product` method")
        item_validator.save()
        return Response({"success": True})

    @action(methods=["POST"], detail=True, url_path="update_product")
    def update_product(self, request, *args, **kwargs):
        order = self.get_object()
        if order.closed:
            raise ValidationError("Order Closed Now!")
        params = request.data
        params.update({"order_id": order.id})
        params.update({"product_id": params.pop("product", None)})

        if not order.orderitem_set.filter(product_id=params.get("product_id")).exists():
            raise ValidationError("Order has no item for given Product. Use `add_product` method")

        item = order.orderitem_set.get(product_id=params.get("product_id"))
        for k, v in params.items():
            setattr(item, k, v)
        try:
            item.save()
        except Exception as e:
            raise ValidationError("Invalid params given: [%s]." % e)
        return Response({"success": True})

    @action(methods=["POST"], detail=True, url_path="delete_product")
    def delete_product(self, request, *args, **kwargs):
        order = self.get_object()
        if order.closed:
            raise ValidationError("Order Closed Now!")

        product_id = request.data.get("product")
        order.orderitem_set.filter(product_id=product_id).delete()
        return Response({"success": True})
