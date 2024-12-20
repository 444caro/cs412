# Generated by Django 5.1.3 on 2024-12-04 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloomboard', '0006_alter_arrangement_vase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vase',
            name='color',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='vase',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='vase',
            name='size',
            field=models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('none', 'N/A')], max_length=10),
        ),
    ]
