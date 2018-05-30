from rest_framework import serializers
from . import models


class CategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        exclude = ()


class BrandModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand
        exclude = ()


class ProductModelSerializer(serializers.ModelSerializer):

    prices = serializers.SerializerMethodField()

    @classmethod
    def get_prices(cls, obj):
        return list(obj.prices.all().values("currency__name", "currency__code", "original", "discount"))

    class Meta:
        model = models.Product
        exclude = ()


class FilterProductSerializer(serializers.Serializer):
    brands = serializers.ListField(default=[], allow_empty=True, allow_null=True, child=serializers.IntegerField())
    categories  = serializers.ListField(default=[], allow_empty=True, allow_null=True, child=serializers.IntegerField())

    def validate(self, attrs):
        attrs = super(FilterProductSerializer, self).validate(attrs)
        attrs["filters"] = {}
        if attrs.get("brands"):
            attrs["filters"].update({"brand__in": models.Brand.objects.filter(id__in=attrs["brands"])})
        if attrs.get("categories"):
            attrs["filters"].update({"category__in": models.Brand.objects.filter(id__in=attrs["categories"])})
        attrs.pop("categories", None)
        attrs.pop("brands", None)
        return attrs


class OrderModelSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    @classmethod
    def get_items(cls, obj):
        return list(obj.orderitem_set.all().values("product_id", "price", "qty", "total_price"))

    class Meta:
        model = models.Order
        exclude = ()


class OrderItemModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        exclude = ()
