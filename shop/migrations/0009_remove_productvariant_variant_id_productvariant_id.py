# Generated by Django 5.0.7 on 2024-09-10 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_productvariant_id_productvariant_variant_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='variant_id',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
