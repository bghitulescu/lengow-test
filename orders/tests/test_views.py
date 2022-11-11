from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from orders.models import Order, Product


class ListOrdersViewTests(TestCase):
    def test_when_no_orders(self):
        response = self.client.get(reverse("list_orders"))
        self.assertJSONEqual(response.content, [])

    def test_response_structure(self):
        dt = datetime.strptime("2022-02-18 07:35:00", "%Y-%m-%d %H:%M:%S")

        order = Order.objects.create(
            id="123-123",
            marketplace="amazon",
            purchase_date=dt.date(),
            purchase_time=dt.time(),
        )
        Order.objects.create(
            id="123-321",
            marketplace="cdiscount",
        )

        Product.objects.create(sku="sku-123", unit_price=12.2, quantity=2, order=order)
        Product.objects.create(sku="sku-321", unit_price=32, quantity=1, order=order)

        response = self.client.get(reverse("list_orders"))
        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": "123-123",
                    "marketplace": "amazon",
                    "purchase_date": "2022-02-18",
                    "purchase_time": "07:35:00",
                    "products": [
                        {
                            "sku": "sku-123",
                            "unit_price": 12.2,
                            "quantity": 2,
                        },
                        {
                            "sku": "sku-321",
                            "unit_price": 32,
                            "quantity": 1,
                        },
                    ],
                },
                {
                    "id": "123-321",
                    "marketplace": "cdiscount",
                    "purchase_date": None,
                    "purchase_time": None,
                    "products": [],
                },
            ],
        )


class OrderDetailsViewTests(TestCase):
    def test_when_order_is_missing(self):
        response = self.client.get(reverse("order_details", kwargs={"order_id": 1}))
        self.assertJSONEqual(response.content, {})

    def test_order_details_structure(self):
        order = Order.objects.create(id="123-123", marketplace="amazon")
        Product.objects.create(sku="sku-123", unit_price=13.2, quantity=6, order=order)

        response = self.client.get(
            reverse("order_details", kwargs={"order_id": "123-123"})
        )
        self.assertJSONEqual(
            response.content,
            {
                "id": "123-123",
                "marketplace": "amazon",
                "purchase_date": None,
                "purchase_time": None,
                "products": [
                    {
                        "sku": "sku-123",
                        "unit_price": 13.2,
                        "quantity": 6,
                    },
                ],
            },
        )
