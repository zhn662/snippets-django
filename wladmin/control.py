# -*- coding:utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import User, Role, Permission


def permission_verify():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = DjangoUser.objects.get(id=request.user.id)

            if not user.is_superuser:
                try:
                    user = User.objects.get(user_id=request.user.userid)
                    if not user.role:
                        return HttpResponseRedirect(reverse('nopermission'))
                except:
                    return HttpResponseRedirect(reverse('nopermission'))

                role_permission = Role.objects.get(name=user.role)
                role_permission_list = role_permission.permissions.all()

                matches = []
                for x in role_permission_list:
                    if x.match == 'exact':
                        if request.path == x.url or request.path.rstrip('/') == x.url:
                            matches.append(x.url)
                    else:
                        if request.path.startswith(x.url):
                            matches.append(x.url)

                if len(matches) == 0:
                    return HttpResponseRedirect(reverse('nopermission'))
            else:
                pass

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
