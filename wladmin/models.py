# -*- coding:utf-8 -*-

import datetime
from django.db import models
from walan.models import Users


class Permission(models.Model):
    name = models.CharField(max_length=50)
    match = models.CharField(max_length=50)
    url = models.CharField(max_length=250)
    add_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.url)


class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, null=True, blank=True, through='RolePermission')
    add_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role)
    permission = models.ForeignKey(Permission)
    add_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return '%s(%s)' % (self.role.name, self.permission.name)


class User(models.Model):
    user = models.ForeignKey(Users, unique=True, related_name='wladmin_user')
    role = models.ForeignKey(Role, blank=True, null=True)
    add_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return '%s#%s' % (self.user_id, self.user.realname)
