# Generated by Django 3.2.18 on 2023-06-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erttiwtBack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilpictures',
            name='profilPicture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]