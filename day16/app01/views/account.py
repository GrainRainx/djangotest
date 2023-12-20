from django.contrib.auth.forms import UserChangeForm
from django.forms import BaseModelForm
from django.http import HttpResponseRedirect, HttpResponse

from app01.utils.encrypt import md5
from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm



class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={"class":"form-control"}),
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form":form})

    form = LoginForm(data=request.POST)

    if form.is_valid():

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if admin_object is not None:
            request.session["info"] = {'id': admin_object.id, 'username': admin_object.username}
            return redirect('/admin/list/')

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_object = models.UserInfo.objects.filter(name=username,password=password).first()
        if user_object is not None:
            request.session["info"] = {'id': user_object.id, 'username': user_object.name}
            return redirect('/staff/list/')

        # if not admin_object:
        #     # 放在password是为了错误信息显示在密码下方
        form.add_error("password", "用户名或密码错误")
        #     return render(request, 'login.html', {"form": form})

        # request.session["info"] = {'id': admin_object.id, 'username': admin_object.username}
        #
        # return redirect('/admin/list/')
        #
        # user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        #
        # if not user_object:
        #     md5(cleaned_data['password'])
        #     return render(request, 'login.html', {"form": form})
        # return redirect('/admin/list/')

    return render(request, 'login.html', {"form":form})



class UserExModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'age', 'create_time', 'depart', 'gender']
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


def register(request):

    if request.method == 'GET':
        form = UserExModelForm()
        return render(request, 'register.html', {"form":form})

    form = UserExModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/login/')
    else:
        # 校验失败，在页面上显示错误信息
        print(form.errors)

    return render(request, 'register.html', {"form":form})
    # return redirect('/login/')
    # return render(request, 'register.html')



def logout(request):
    """注销"""

    request.session.clear()
    return redirect('/login/')

