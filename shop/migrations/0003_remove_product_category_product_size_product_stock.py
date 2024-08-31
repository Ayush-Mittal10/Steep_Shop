# Generated by Django 5.0.7 on 2024-07-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('small', '250 g'), ('medium', '500 g'), ('large', '1 Kg')], default='500 g', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
    ]