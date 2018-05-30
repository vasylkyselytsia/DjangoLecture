from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
# print(router.urls)
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/", include(router.urls))
]
