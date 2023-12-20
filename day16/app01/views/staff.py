from app01.utils.encrypt import md5
from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm



def staff_list(request):

    querySet = models.PrettyNum.objects.all().order_by('-level')
    return render(request, 'staff_list.html', {'querySet': querySet})

def staff_user_list(request):
    querySet = models.UserInfo.objects.all()
    return render(request, 'staff_user_list.html', {'querySet': querySet})

def staff_depart_list(request):
    querySet = models.Department.objects.all()
    return render(request, 'staff_depart_list.html', {'querySet': querySet})
