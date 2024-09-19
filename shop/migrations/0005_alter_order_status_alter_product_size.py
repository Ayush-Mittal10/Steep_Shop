# Generated by Django 5.0.7 on 2024-09-01 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_order_items_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('O', 'Ordered'), ('f', 'Failed')], default='ordered', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('small', '250 g'), ('medium', '500 g'), ('large', '1 Kg')], default='medium', max_length=50),
        ),
    ]