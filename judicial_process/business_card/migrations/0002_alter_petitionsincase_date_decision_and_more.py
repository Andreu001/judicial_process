# Generated by Django 4.2.6 on 2023-10-24 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_card', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petitionsincase',
            name='date_decision',
            field=models.DateField(null=True, verbose_name='Дата решения по ходатайству'),
        ),
        migrations.AlterField(
            model_name='petitionsincase',
            name='decision_rendered',
            field=models.CharField(max_length=150, null=True, verbose_name='наименование вынесенного решения'),
        ),
        migrations.AlterField(
            model_name='petitionsincase',
            name='notation',
            field=models.TextField(max_length=300, null=True, verbose_name='примечания'),
        ),
    ]
