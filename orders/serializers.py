from rest_framework import serializers, viewsets

from orders.models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["sku", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "marketplace", "purchase_date", "purchase_time", "products"]


#
#
# # ViewSets define the view behavior.
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
