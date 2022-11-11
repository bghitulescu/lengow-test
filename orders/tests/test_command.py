from datetime import date, time
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from orders.management.commands.import_orders import Command
from orders.models import Order, Product


class MockResponse:
    def __init__(self):
        self.status_code = 200
        self.content = """<?xml version="1.0" encoding="ISO-8859-1"?>
<root>
    <orders>
        <order>
            <marketplace><![CDATA[amazon]]></marketplace>
            <order_id><![CDATA[111-2222222-3333333]]></order_id>
            <order_purchase_date><![CDATA[2014-10-21]]></order_purchase_date>
            <order_purchase_heure><![CDATA[14:59:51]]></order_purchase_heure>
            <cart>
                <products>
                    <product>
                        <sku><![CDATA[11_12]]></sku>
                        <quantity><![CDATA[1]]></quantity>
                        <price_unit><![CDATA[29.0]]></price_unit>
                    </product>
                </products>
                <products>
                    <product>
                        <sku><![CDATA[13_14]]></sku>
                        <quantity><![CDATA[2]]></quantity>
                        <price_unit><![CDATA[21.1]]></price_unit>
                    </product>
                </products>
            </cart>
        </order>
    </orders>
</root>
        """


class ImportOrdersTest(TestCase):
    @patch("requests.get", return_value=MockResponse())
    def test_xml_parser(self, _):
        result = Command()._read_xml()

        expected_result = [
            {
                "order_id": "111-2222222-3333333",
                "marketplace": "amazon",
                "order_purchase_date": "2014-10-21",
                "order_purchase_heure": "14:59:51",
                "cart": [
                    {
                        "sku": "11_12",
                        "price_unit": "29.0",
                        "quantity": "1",
                    },
                    {
                        "sku": "13_14",
                        "price_unit": "21.1",
                        "quantity": "2",
                    },
                ],
            }
        ]

        self.assertEqual(result, expected_result)

    @patch("requests.get", return_value=MockResponse())
    def test_order_and_products_are_saved_in_the_database(self, _):
        call_command("import_orders", [])

        orders = Order.objects.all()
        products = Product.objects.all()
        self.assertEquals(len(orders), 1)
        self.assertEquals(len(products), 2)

        self.assertEquals(orders[0].id, "111-2222222-3333333")
        self.assertEquals(orders[0].marketplace, "amazon")
        self.assertEquals(orders[0].purchase_date, date(2014, 10, 21))
        self.assertEquals(orders[0].purchase_time, time(14, 59, 51))

        self.assertEquals(products[0].sku, "11_12")
        self.assertEquals(products[0].unit_price, 29)
        self.assertEquals(products[0].quantity, 1)

        self.assertEquals(products[1].sku, "13_14")
        self.assertEquals(products[1].unit_price, 21.1)
        self.assertEquals(products[1].quantity, 2)

    @patch("requests.get", return_value=MockResponse())
    def test_command_is_idempotent(self, _):
        for _ in range(0, 3):
            call_command("import_orders", [])

        orders = Order.objects.all()
        products = Product.objects.all()
        self.assertEquals(len(orders), 1)
        self.assertEquals(len(products), 2)

        self.assertEquals(orders[0].id, "111-2222222-3333333")
        self.assertEquals(products[0].sku, "11_12")
        self.assertEquals(products[1].sku, "13_14")
