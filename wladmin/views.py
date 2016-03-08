# -*- coding:utf-8 -*-

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template.context import RequestContext
from .models import User, Role, Permission, RolePermission
from walan.models import Users
from wladmin.control import permission_verify


@login_required
def default(request):
    return render(request, 'wladmin/base/dashboard.html', locals())


@login_required
def nopermission(request):
    return render(request, 'wladmin/base/nopermission.html', locals())


@login_required
@permission_verify()
def control(request):
    return HttpResponseRedirect(reverse('control_userlist'))


@login_required
@permission_verify()
def control_userlist(request, action=None):
    curuser = None
    id = request.POST.get('id', '')
    userid = request.POST.get('userid', '')
    roleid = request.POST.get('roleid', '')

    if userid:
        userid = int(userid)
        if action == 'add':
            if Users.objects.filter(id=userid).exists():
                if not User.objects.filter(user_id=userid).exists():
                    user = User()
                    user.user_id = userid
                    if roleid:
                        user.role_id = int(roleid)
                    user.save()
        if action == 'edit':
            user = User.objects.get(user_id=userid)
            user.role_id = None if not roleid else int(roleid)
            user.save(update_fields=['role_id'])

    if id:
        id = int(id)
        curuser = User.objects.get(id=id)
        if action == 'delete':
            curuser.delete()
            curuser = None

    dsusers = User.objects.all().order_by('role_id')
    dsroles = Role.objects.all().order_by('id')

    return render_to_response('wladmin/control/userlist.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_verify()
def control_rolelist(request, action=None):
    currole, currolepermissions = None, None
    id = request.POST.get('id', '')
    name = request.POST.get('name', '')
    permissions = request.POST.getlist('permissions', '')
    permissions = [int(x) for x in permissions if x]
    permissions.sort()

    if name and action == 'add':
        if not Role.objects.filter(name=name).exists():
            role = Role()
            role.name = name
            role.save()

            qslist = []
            for item in permissions:
                qslist.append(RolePermission(role_id=role.id, permission_id=item))
            if qslist:
                RolePermission.objects.bulk_create(qslist)

    if id and action:
        id = int(id)
        currole = Role.objects.get(id=id)
        if action == 'edit':
            currolepermissions = currole.permissions.values_list('id')
            currolepermissions = [x[0] for x in currolepermissions]

            if name or permissions:
                if name and not Role.objects.filter(name=name).exists():
                    currole.name = name
                    currole.save(update_fields=['name'])

                if permissions:
                    RolePermission.objects.filter(role_id=id, permission_id__in=currolepermissions).delete()
                    qslist = []
                    for item in permissions:
                        qslist.append(RolePermission(role_id=id, permission_id=item))
                    if qslist:
                        RolePermission.objects.bulk_create(qslist)

                currole = None
                currolepermissions = None

        elif action == 'delete':
            users = User.objects.filter(role_id=id)
            if users:
                for item in users:
                    item.role_id = None
                    item.save(update_fields=['role_id'])

            currole.delete()
            currole = None

    dsroles = Role.objects.all().order_by('id')
    dspermissions = Permission.objects.all().order_by('url')

    return render_to_response('wladmin/control/rolelist.html', locals(), context_instance=RequestContext(request))


@login_required
@permission_verify()
def control_permissionlist(request, action=None):
    curpermission = None
    id = request.POST.get('id', '')
    name = request.POST.get('name', '')
    match = request.POST.get('match', '')
    url = request.POST.get('url', '')
    if url:
        if url.find('http://') != -1:
            index = url.find('/', 7)
            url = url[index:]
        if url.find('/') != 0:
            url = '/' + url

    if name and url and action == 'add':
        if not Permission.objects.filter(url=url).exists():
            permission = Permission()
            permission.name = name
            permission.match = match
            permission.url = url
            permission.save()

    if id and action:
        id = int(id)
        curpermission = Permission.objects.get(id=id)
        if action == 'edit':
            if name and url and not Permission.objects.filter(url=url).exclude(id=id).exists():
                curpermission.name = name
                curpermission.match = match
                curpermission.url = url
                curpermission.save(update_fields=['name', 'match', 'url'])
                curpermission = None
        elif action == 'delete':
            curpermission.delete()
            curpermission = None

    dspermissions = Permission.objects.all().order_by('url')

    return render_to_response('wladmin/control/permissionlist.html', locals(), context_instance=RequestContext(request))
