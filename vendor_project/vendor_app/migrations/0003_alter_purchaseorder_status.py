# Generated by Django 5.0.4 on 2024-05-05 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0002_remove_purchaseorder_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], max_length=50),
        ),
    ]
