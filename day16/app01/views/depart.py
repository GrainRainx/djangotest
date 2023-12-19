from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm

def depart_list(request):

    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


from  django.shortcuts import redirect

def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')

    # title 是否会为空
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.create(title=title)

    return redirect('/depart/list/')


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()

    return redirect('/depart/list/')


def depart_edit(request, nid):
    """修改部门"""
    if request.method == 'GET':
        # 根据nid去获取对象
        row_object = models.Department.objects.filter(id=nid).first()
        print(row_object.id, row_object.title)
        return render(request, "depart_edit.html", {'row_object': row_object})

    # 从网页获取数据回后台
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')



def depart_test(request):
    return render(request, 'temp_test.html')
