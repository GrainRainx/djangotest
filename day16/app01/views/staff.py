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



def staff_pretty_add(request):
    if request.method == "GET":
        form = PrettyModelNumForm()
        return render(request, 'staff_pretty_add.html', {"form":form})

    form = PrettyModelNumForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/staff/list/')

    return render(request, 'staff_pretty_add.html', {"form":form})

def staff_pretty_edit(request,nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelNumForm(instance=row_object)
        return render(request, 'staff_pretty_edit.html', {"form":form})

    form = PrettyEditModelNumForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/staff/list/')

    return render(request, 'staff_pretty_edit.html', {"form":form})


def staff_pretty_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/staff/list/')