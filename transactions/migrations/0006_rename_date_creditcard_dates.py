# Generated by Django 4.2.4 on 2023-10-12 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_creditcard_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditcard',
            old_name='date',
            new_name='dates',
        ),
    ]
