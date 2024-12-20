# Generated by Django 5.1.3 on 2024-12-04 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloomboard', '0004_arrangement_post_arrangement_flowerusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrangement',
            name='type',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='vase',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bloomboard.vase'),
        ),
    ]
