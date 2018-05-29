from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва бренду", unique=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.PROTECT, verbose_name="Батьківська категорія",
                               null=True, default=None)
    name = models.CharField(max_length=150, verbose_name="Назва категорії", unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва товару", unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категорія")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    photo = models.ImageField(upload_to="products/", null=True, blank=True)
    reviews = models.IntegerField(default=0, verbose_name="Кількість переглядів")
    sale = models.BooleanField(default=False)
    detail = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        unique_together = (("name", "category"),)


class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    class Meta:
        unique_together = (("name", "code"),)


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    original = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "api_product_price"
        unique_together = (("product", "currency"),)
