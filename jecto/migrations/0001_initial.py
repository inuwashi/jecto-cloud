# Generated by Django 2.0.7 on 2018-07-23 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Injection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Injection Date')),
            ],
        ),
        migrations.CreateModel(
            name='InjectionSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Zone name. E.g. Left Thigh.', max_length=32)),
                ('pos_x', models.SmallIntegerField(help_text='Display X Position on the Vitruvian Man Image.')),
                ('pos_y', models.SmallIntegerField(help_text='Display Y Position on the Vitruvian Man Image.')),
            ],
        ),
        migrations.AddField(
            model_name='injection',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jecto.InjectionSite'),
        ),
        migrations.AddField(
            model_name='injection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
