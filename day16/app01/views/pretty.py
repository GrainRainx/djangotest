from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


# Create your views here.


def pretty_list(request):
    """靓号列表"""

    # 相当于select * from 表 by order desc;
    querySet = models.PrettyNum.objects.all().order_by('-level')

    return render(request, 'pretty_list.html', {'querySet':querySet})


from django import forms



from django.core.validators import RegexValidator



# class PrettyModelNumForm(forms.ModelForm):
#     mobile = forms.CharField(
#         label='手机号',
#         validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
#     )
#
#     class Meta:
#         model = models.PrettyNum
#         # 如果是下面的用法，代表fields全选
#         # fileds = "__all__"
#         fields = ['mobile', 'price', 'level', 'status']
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # 循环找到所有的插件，不用向上面的widget那样一个一个手动添加
#         # 对每个循环的字段加一个样式class
#         for name, filed in self.fields.items():
#             # placeholder 是默认显示的内容是什么
#             filed.widget.attrs = {'class': 'form-control', 'placeholder':filed.label}
#
#
#     # 下面这种方法也能检查输入格式是否是对的
#     # clean是django检查的默认前缀
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data['mobile']
#         exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
#         if exists:
#             # 刚才写成return了，导致直接返回手机号了，应该要抛出错误才行
#             raise ValidationError('手机号已存在')
#
#     #     if len(txt_mobile) != 11:
#     #         return ValidationError('格式错误')
#         return txt_mobile

def pretty_add(request):
    """靓号增加"""
    if request.method == "GET":
        form = PrettyModelNumForm()
        return render(request, 'pretty_add.html', {"form":form})

    form = PrettyModelNumForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_add.html', {"form":form})



# class PrettyEditModelNumForm(forms.ModelForm):
#     mobile = forms.CharField(
#         disabled=False, label='手机号'
#     )
#
#     class Meta:
#         model = models.PrettyNum
#         fields = ['mobile', 'price', 'level', 'status']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for name, filed in self.fields.items():
#             filed.widget.attrs = {'class': 'form-control', 'placeholder': filed.label}
#     # 对于编辑的手机号，应该排除自己外的手机号不能重复
#
#     def clean_mobile(self):
#
#         # 拿到当前编辑的那一行手机号的id是多少
#         #  通过instance.pk拿到
#         txt_mobile = self.cleaned_data['mobile']
#         exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
#         if exists:
#             raise ValidationError('手机号已经存在')
#         return txt_mobile


def pretty_edit(request,nid):
    """靓号编辑"""

    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelNumForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form":form})

    form = PrettyEditModelNumForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {"form":form})


def pretty_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
