# Generated by Django 5.0.7 on 2024-11-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp1', '0002_dsamasterdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dsamasterdata',
            name='MasterDataImage',
            field=models.FileField(upload_to='DSA/MasterData/'),
        ),
    ]
