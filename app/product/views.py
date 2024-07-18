from rest_framework.views import APIView
from app.modules.utils import incoming_request_checks
from product.models import Product
from product.serializers import ProductSerializerOut
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.modules.exceptions import raise_serializer_error_msg
from app.modules.utils import api_response, get_incoming_request_checks, incoming_request_checks
from app.modules.permissions import IsAgentAdmin, IsAdmin
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializerIn, ProductSerializerOut
from .models import Order, OrderItems, Product, Color 
from django.shortcuts import get_object_or_404

# Create your views here.

class ProductAPIView(APIView):
    # permission_classes = [IsAuthenticated & (IsAdmin | IsAgentAdmin)]
    serializer_class = ProductSerializerOut

    def get_queryset(self):
        return Product.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return super().get_permissions()

    def update(self, request, pk, partial=None, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializerIn(instance, data=data, partial=True)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        link = serializer.save()
        return Response(
            api_response(
                message="Product updated successfully", status=True, data=link
            )
        )

    def get(self, request, pk=None, format=None):
        if pk:
            instance = get_object_or_404(Product, pk=pk)
            serializer = self.serializer_class(instance)
            return Response(
                api_response(
                    message="Product retrieved successfully",
                    status=True,
                    data=serializer.data,
                )
            )
        else:
            category = request.query_params.get('category', None)
            if category:
                if category == 'popular':
                    queryset = self.get_queryset().order_by('-number_sold')
                elif category == 'lowest':
                    queryset = self.get_queryset().order_by('amount')
                elif category == 'highest':
                    queryset = self.get_queryset().order_by('-amount')
                else:
                    queryset = self.get_queryset().filter(category__title=category)
            else:
                queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            message = "Products retrieved successfully" if len(serializer.data) > 0 else "No product available"
            return Response(
                api_response(
                    message=message,
                    status=True,
                    data=serializer.data,
                )
            )

    def post(self, request, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ProductSerializerIn(data=data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        data = serializer.save()
        return Response(
            api_response(
                message="Product created successfully", status=True, data=data
            )
        )

    def put(self, request, pk, format=None):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializerIn(instance, data=data, partial=True)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        link = serializer.save()
        return Response(
            api_response(
                message="Product updated successfully", status=True, data=link
            )
        )

    def patch(self, request, pk, format=None):
        self.update()
    
    def delete(self, request, pk, format=None):
        instance = get_object_or_404(Product, pk=pk)
        instance.delete()
        return Response(
            api_response(message="Product deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT,
        )

