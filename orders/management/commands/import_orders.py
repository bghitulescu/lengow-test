import xml.etree.ElementTree as ET

import requests
from django.core.management.base import BaseCommand, CommandError

from orders.models import Order, Product


class Command(BaseCommand):
    help = "Imports orders from URL"

    def _read_xml(self):
        response = requests.get("http://test.lengow.io/orders-test.xml")
        xml_tree = ET.fromstring(response.content)

        orders = []
        for child in xml_tree.find("orders"):
            orders.append(
                {
                    "order_id": child.find("order_id").text,
                    "marketplace": child.find("marketplace").text,
                    "order_purchase_date": child.find("order_purchase_date").text,
                    "order_purchase_heure": child.find("order_purchase_heure").text,
                    "cart": [],
                }
            )
            for product in child.iter("product"):
                orders[-1]["cart"].append(
                    {
                        "sku": product.find("sku").text,
                        "price_unit": product.find("price_unit").text,
                        "quantity": product.find("quantity").text,
                    }
                )

        return orders

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        orders = self._read_xml()
        for order_xml in orders:
            try:
                order = Order.objects.get(pk=order_xml["order_id"])
                Product.objects.filter(order=order).delete()
            except Order.DoesNotExist:
                order = Order()

            order.id = order_xml["order_id"]
            order.marketplace = order_xml["marketplace"]
            order.purchase_date = order_xml["order_purchase_date"]
            order.purchase_time = order_xml["order_purchase_heure"]
            order.save()

            for product_xml in order_xml["cart"]:
                product = Product(
                    sku=product_xml["sku"],
                    unit_price=product_xml["price_unit"],
                    quantity=product_xml["quantity"],
                    order=order,
                )
                product.save()

        self.stdout.write(self.style.SUCCESS("Orders imported"))
