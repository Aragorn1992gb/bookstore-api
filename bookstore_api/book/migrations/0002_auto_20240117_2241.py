# Generated by Django 3.2.23 on 2024-01-17 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='editor',
            options={'verbose_name': 'Author', 'verbose_name_plural': 'Authors'},
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('isbn',), name='Book isbn unique constraint'),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('barcode',), name='Book barcode unique constraint'),
        ),
        migrations.AddConstraint(
            model_name='editor',
            constraint=models.UniqueConstraint(fields=('name',), name='Author name unique constraint'),
        ),
    ]
