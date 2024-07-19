# Generated by Django 4.2.6 on 2024-07-19 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitems",
            name="unit_price",
        ),
        migrations.AddField(
            model_name="order",
            name="order_id",
            field=models.CharField(default=2000, max_length=13),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
