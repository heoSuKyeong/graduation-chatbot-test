# Generated by Django 5.1.3 on 2024-11-14 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_alter_maincategory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maincategory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterModelTable(
            name='maincategory',
            table='main_categories',
        ),
    ]
