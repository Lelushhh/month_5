from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'Not found'}, status=404)

        return Response(ProductSerializer(product).data)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'Not found'}, status=404)

        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({'error': 'Not found'}, status=404)

        product.delete()
        return Response(status=204)
