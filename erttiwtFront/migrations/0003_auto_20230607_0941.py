# Generated by Django 2.2.28 on 2023-06-07 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erttiwtFront', '0002_auto_20230607_0800'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='messages',
            name='idConversation',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
      
        
    ]
