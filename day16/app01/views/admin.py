from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


def admin_list(request):
    """管理员列表"""
    querySet = models.Admin.objects.all()

    contex = {
        'querySet': querySet
    }
    return render(request, 'admin_list.html', contex)


