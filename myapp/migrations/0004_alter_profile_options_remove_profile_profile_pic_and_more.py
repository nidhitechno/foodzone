# Generated by Django 5.1.7 on 2025-04-01 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_category_team_dish'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Profile Table'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profile',
            name='contact_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(blank=True, max_length=100)),
                ('payer_id', models.CharField(blank=True, max_length=100)),
                ('ordered_on', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.profile')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.dish')),
            ],
            options={
                'verbose_name_plural': 'Order Table',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='Profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='Profile/%y/%m%/%d'),
        ),
    ]
