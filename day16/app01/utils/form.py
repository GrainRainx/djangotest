from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

class PrettyModelNumForm(BootStrapModelForm):
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        # 如果是下面的用法，代表fields全选
        # fileds = "__all__"
        fields = ['mobile', 'price', 'level', 'status']

    # 下面这种方法也能检查输入格式是否是对的
    # clean是django检查的默认前缀
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            # 刚才写成return了，导致直接返回手机号了，应该要抛出错误才行
            raise ValidationError('手机号已存在')

    #     if len(txt_mobile) != 11:
    #         return ValidationError('格式错误')
        return txt_mobile

class PrettyEditModelNumForm(BootStrapModelForm):
    mobile = forms.CharField(
        disabled=False, label='手机号'
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']
    def clean_mobile(self):

        # 拿到当前编辑的那一行手机号的id是多少
        #  通过instance.pk拿到
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')
        return txt_mobile
