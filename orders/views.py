from django.http import JsonResponse
from rest_framework import status

from orders.models import Order
from orders.serializers import OrderSerializer


def list_orders(request):
    serializer = OrderSerializer(Order.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


def order_details(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(instance=order)
    return JsonResponse(serializer.data, safe=False)
