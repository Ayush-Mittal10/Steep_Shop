# Generated by Django 5.0.7 on 2024-09-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='id',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='variant_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
