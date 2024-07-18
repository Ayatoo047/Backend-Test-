from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.ProductAPIView.as_view(), name="create_product"),
    path("products/<int:pk>/", views.ProductAPIView.as_view(), name="product_detail"),
]

# urlpatterns += router.urls
