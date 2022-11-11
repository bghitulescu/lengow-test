import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("marketplace", models.CharField(max_length=50)),
                (
                    "purchase_date",
                    models.DateField(null=True, verbose_name="date created"),
                ),
                (
                    "purchase_time",
                    models.TimeField(null=True, verbose_name="time created"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sku", models.CharField(max_length=50)),
                ("unit_price", models.FloatField()),
                ("quantity", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="orders.order",
                    ),
                ),
            ],
            options={
                "unique_together": {("sku", "order")},
            },
        ),
    ]
