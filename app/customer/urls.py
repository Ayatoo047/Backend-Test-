from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"createuser", views.CustomersView, basename="customer")

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login')
]

urlpatterns += router.urls