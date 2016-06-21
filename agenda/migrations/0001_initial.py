# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-21 15:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayStamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Stamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('path', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='daystamp',
            name='stamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.Stamp'),
        ),
        migrations.AlterUniqueTogether(
            name='daystamp',
            unique_together=set([('date', 'stamp')]),
        ),
    ]
