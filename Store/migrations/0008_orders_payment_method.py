# Generated by Django 5.0.1 on 2024-01-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_remove_orders_products_info_orders_products_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payment_method',
            field=models.CharField(default='cod', max_length=200),
        ),
    ]
