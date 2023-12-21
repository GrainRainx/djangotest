"""
URL configuration for day16 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import depart, user, pretty, admin, account, staff

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    # 正则表达式，传参的时候必须将int传送
    path('depart/<int:nid>/edit/', depart.depart_edit),

    path('depart/test/', depart.depart_test),

    # 用户表

    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 手机号靓号管理

    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    # 管理员操作

    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录页面
    path('', account.login),
    path('login/', account.login),
    path('logout/', account.logout),
    path('register/', account.register),

    # 员工登录页面

    path('staff/list/', staff.staff_list),
    path('staff_user/list/', staff.staff_user_list),
    path('staff_depart/list/', staff.staff_depart_list),
    path('staff_pretty/add/', staff.staff_pretty_add),
    path('staff_pretty/<int:nid>/edit/', staff.staff_pretty_edit),
    path('staff_pretty/<int:nid>/delete/', staff.staff_pretty_delete),

]
