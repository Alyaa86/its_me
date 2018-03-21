# Generated by Django 2.0.3 on 2018-03-21 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('its_me', '0008_auto_20180321_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='its_me.Profile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='its_me.Profile'),
        ),
    ]
