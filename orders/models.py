from django.db import models


class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    marketplace = models.CharField(max_length=50)
    purchase_date = models.DateField("date created", null=True)
    purchase_time = models.TimeField("time created", null=True)


class Product(models.Model):
    sku = models.CharField(max_length=50)
    unit_price = models.FloatField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")

    class Meta:
        unique_together = [["sku", "order"]]
