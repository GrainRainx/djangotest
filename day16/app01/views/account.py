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

        if not admin_object:
            # 放在password是为了错误信息显示在密码下方
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})

        request.session["info"] = {'id': admin_object.id, 'username': admin_object.username}
        return redirect('/admin/list/')



    return render(request, 'login.html', {"form":form})