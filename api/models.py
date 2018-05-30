from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва бренду", unique=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.PROTECT, verbose_name="Батьківська категорія",
                               null=True, default=None, related_name="children_set")
    name = models.CharField(max_length=150, verbose_name="Назва категорії", unique=True)

    def children(self):
        return self.children_set.all()

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва товару", unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категорія", related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="brands")

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    original = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "api_product_price"
        unique_together = (("product", "currency"),)


class Order(models.Model):
    total_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    products_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "api_order_item"
        unique_together = (("order", "product"),)
