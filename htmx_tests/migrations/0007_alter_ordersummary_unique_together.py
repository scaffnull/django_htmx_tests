# Generated by Django 5.0.6 on 2024-05-30 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('htmx_tests', '0006_location_company_orderer_ordersummary'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ordersummary',
            unique_together={('location', 'order_number')},
        ),
    ]
