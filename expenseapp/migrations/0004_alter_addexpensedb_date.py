# Generated by Django 4.1.7 on 2023-10-23 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenseapp', '0003_alter_addexpensedb_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpensedb',
            name='Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]