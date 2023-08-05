# -*- coding: utf-8 -*-

'''
custom migration file for database functions
add this file to dependencies list in first migration file (0001_xxxxx)
ex:
    dependencies = [
        ('geodb', 'userfunctions_migration'),
    ]
'''

from __future__ import unicode_literals

from django.db import migrations, models
from pprint import pprint
import django.contrib.gis.db.models.fields
import os

curpath = os.path.dirname(os.path.abspath(__file__))

def getsql_userfunctions_create():
    with open(os.path.join(curpath, 'userfunctions_create.sql'),'r') as f:
        return f.read()

def getsql_userfunctions_drop():
    with open(os.path.join(curpath, 'userfunctions_drop.sql'),'r') as f:
        return f.read()

class Migration(migrations.Migration):

    # def __init__(self, *args, **kwargs):
    #     super(Migration, self).__init__(*args, **kwargs)
    #     curpath = os.path.dirname(os.path.abspath(__file__))
    #     with open(os.path.join(curpath, 'userfunctions.sql'),'r') as f:
    #         self.userfunctions_sql = f.read()
    #         print self.userfunctions_sql

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            getsql_userfunctions_create(),
            reverse_sql=getsql_userfunctions_drop()
        ),
    ]
