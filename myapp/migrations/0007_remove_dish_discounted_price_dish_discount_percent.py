# Generated by Django 5.1.7 on 2025-04-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_order_payer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='discounted_price',
        ),
        migrations.AddField(
            model_name='dish',
            name='discount_percent',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
