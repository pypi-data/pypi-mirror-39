# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forcastedvalue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datadate', models.DateTimeField()),
                ('forecasttype', models.CharField(max_length=50)),
                ('riskstate', models.IntegerField()),
                ('basin', models.ForeignKey(related_name='basins', to='geodb.AfgShedaLvl4')),
            ],
            options={
                'db_table': 'forcastedvalue',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='forecastedLastUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datadate', models.DateTimeField()),
                ('forecasttype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'forecastedlastupdate',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='afgavsa',
            name='basinmember',
        ),
        migrations.DeleteModel(
            name='AfgEqHzda',
        ),
        migrations.DeleteModel(
            name='AfgEqtUnkPplEqHzd',
        ),
        migrations.DeleteModel(
            name='AfgIncidentOasis',
        ),
        migrations.DeleteModel(
            name='AfgIncidentOasisTemp',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmChelsaBioclim',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmWorldclimBioclim2050Rpc26',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmWorldclimBioclim2050Rpc45',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmWorldclimBioclim2050Rpc85',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmWorldclimBioclim2070Rpc26',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmWorldclimBioclim2070Rpc45',
        ),
        migrations.DeleteModel(
            name='AfgMettClim1KmWorldclimBioclim2070Rpc85',
        ),
        migrations.DeleteModel(
            name='AfgMettClimperc1KmChelsaPrec',
        ),
        migrations.DeleteModel(
            name='AfgMettClimtemp1KmChelsaTempavg',
        ),
        migrations.DeleteModel(
            name='AfgMettClimtemp1KmChelsaTempmax',
        ),
        migrations.DeleteModel(
            name='AfgMettClimtemp1KmChelsaTempmin',
        ),
        migrations.DeleteModel(
            name='AfgSnowaAverageExtent',
        ),
        migrations.DeleteModel(
            name='earthquake_events',
        ),
        migrations.DeleteModel(
            name='earthquake_shakemap',
        ),
        migrations.DeleteModel(
            name='HistoryDrought',
        ),
        migrations.DeleteModel(
            name='RefSecurity',
        ),
        migrations.DeleteModel(
            name='villagesummaryEQ',
        ),
        migrations.DeleteModel(
            name='AfgAvsa',
        ),
    ]
