# Generated by Django 5.1.4 on 2024-12-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exames', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaoexame',
            name='senha',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
