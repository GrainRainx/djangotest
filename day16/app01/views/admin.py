from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


def admin_list(request):
    """管理员列表"""

    info = request.session.get("info")  # 获取session的info字典的用户cookie凭证
    if not info:
        # 如果没有登录，重新登录
        return redirect('/login/')


    querySet = models.Admin.objects.all()

    contex = {
        'querySet': querySet
    }
    return render(request, 'admin_list.html', contex)

from app01.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # print("whereis mde"+md5(pwd))
        return md5(pwd)


    # 在前端增加一个校验格式的函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        return confirm


def admin_add(request):
    """添加管理员"""
    titel = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"form": form, "title": titel})

    form = AdminModelForm(data=request.POST)

    if form.is_valid():
        #  这个是格式正确之后，可以打印出前端发送过来了的数据
        # print(form.cleaned_data)
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form": form, "title": titel})

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]



def admin_edit(request,nid):
    """编辑管理员"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = "编辑管理员"
    # print("nid = " + str(nid))
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form":form, "title": title})


    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form": form,"title": title})

def admin_delete(request,nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # print("whereis mde"+md5(pwd))

        return md5(pwd)
    # 在前端增加一个校验格式的函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        return confirm



def admin_reset(request,nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
    title = "重置密码"
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"form":form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {"form":form, "title":title})
