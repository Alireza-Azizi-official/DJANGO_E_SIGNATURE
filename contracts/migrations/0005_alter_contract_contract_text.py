# Generated by Django 5.1.4 on 2024-12-18 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_contract_date_field1_contract_date_field2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_text',
            field=models.TextField(),
        ),
    ]