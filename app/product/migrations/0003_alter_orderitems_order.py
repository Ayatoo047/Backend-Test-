# Generated by Django 4.2.6 on 2024-07-19 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_remove_orderitems_unit_price_order_order_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitems",
            name="order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orderitems",
                to="product.order",
            ),
        ),
    ]
