# Generated by Django 3.0.4 on 2020-04-28 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_orderadd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderadd',
            name='apartment_address',
        ),
        migrations.RemoveField(
            model_name='orderadd',
            name='country',
        ),
        migrations.RemoveField(
            model_name='orderadd',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='orderadd',
            name='zip',
        ),
        migrations.AddField(
            model_name='orderadd',
            name='address',
            field=models.CharField(default='', max_length=111),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='city',
            field=models.CharField(default='', max_length=111),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='email',
            field=models.CharField(default='', max_length=111),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='name',
            field=models.CharField(default='', max_length=90),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='phone',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='state',
            field=models.CharField(default='', max_length=111),
        ),
        migrations.AddField(
            model_name='orderadd',
            name='zip_code',
            field=models.CharField(default='', max_length=111),
        ),
    ]
