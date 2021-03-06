# Generated by Django 3.2.4 on 2021-06-27 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0002_auto_20210627_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='run_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('none', 'none'), ('ok', 'ok'), ('error', 'error')], default='none', max_length=16),
        ),
    ]
