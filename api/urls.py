from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/", include(router.urls))
]
