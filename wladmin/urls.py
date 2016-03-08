from django.conf.urls import patterns, url
from . import views, views_patterns, views_payments, views_users, views_manages, views_sales, views_designers

urlpatterns = patterns('',
    url(r'^$', views.default, name='default'),
    url(r'^nopermission/$', views.nopermission, name='nopermission'),

    url(r'^control/user/$', views.control_userlist),
    url(r'^control/user/(?P<action>(add)|(edit)|(delete))/$', views.control_userlist),
    url(r'^control/role/$', views.control_rolelist),
    url(r'^control/role/(?P<action>(add)|(edit)|(delete))/$', views.control_rolelist),
    url(r'^control/permission/$', views.control_permissionlist),
    url(r'^control/permission/(?P<action>(add)|(edit)|(delete))/$', views.control_permissionlist),

)