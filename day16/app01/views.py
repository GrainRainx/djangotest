from django.core.exceptions import ValidationError
from django.forms import BaseModelForm
from django.shortcuts import render


from app01.utils.form import UserModelForm, PrettyModelNumForm, PrettyEditModelNumForm


# Create your views here.

from app01 import models
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


def user_list(request):
    """用户管理"""
    # 获取用户列表，将用户列表传到前端
    querySet = models.UserInfo.objects.all()
    # for obj in querySet:
    #     print(obj.name, obj.age, obj.create_time.strftime('%Y-%m-%d'), obj.get_gender_display())


        # 如果想知道该员工是哪个部门，又该如何获取
        # print(obj.depart_id)
        # xx = models.Department.objects.filter(id=obj.depart_id).first()
        # print(xx.title)


        # 上述的操作可以实现，但是django已经帮我们封装好了怎么寻找外键，不然我们定义外键的时候有什么用呢
        # obj.depart 获取数据库中存储的id值，由于已经定义了外键
        # 然后根据id值去寻找department表，再返回一个department对象
        # print(obj.depart.title)


    return render(request, 'user_list.html', {'querySet': querySet})



def user_add(request):
    """添加用户"""

    if request.method == 'GET':
        # gender_choices 是一个元组，然后前端可以通过变量gender_choices获取这个元组
        # 同理depart_list 获取了一众部门的对象，然后传到前端去
        contex = {
            'gender_choice': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', contex)

    # 下列的写法有问题，用户提交的数据没有校验
    # 如果出现错误，应该有错误提示
    # 页面的每个字段都需要写一遍
    name = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 获取到数据后就可以添加数据了
    # 难道添加外键要加上_id? 不是很理解django这操作，在数据库中
    # django确实是帮我加了_id, 但是我现在添加到噢·····我好像直到了
    # django的orm组件作为一个翻译官，它只负责翻译一些语言，但是具体添加的数据库字段还需要用户自己指定
    # 在指定完后再翻译，然后添加到数据库中，而在通过django创建数据库外键的时候，创建的是depart_id
    # 所以在指定添加的时候，也应该是depart_id
    models.UserInfo.objects.create(name=name, password=pwd, gender=gender_id,
                                   age=age,depart_id=depart_id,create_time=ctime,account=account)

    return redirect('/user/list/')



from django import forms

from app01.utils.bootstrap import BootStrapModelForm




# class UserModelForm(forms.ModelForm):
#     class Meta:
#         model = models.UserInfo
#         fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']
#         # 修改models的样式
#         # widgets = {
#         #     "name": forms.TextInput(attrs={'class': 'form-control'}),
#         #     "password": forms.TextInput(attrs={'class': 'form-control'}),
#         #     "age": forms.TextInput(attrs={'class': 'form-control'})
#         # }
#
#     # 重新定义init方法
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # 循环找到所有的插件，不用向上面的widget那样一个一个手动添加
#         # 对每个循环的字段加一个样式class
#         for name, filed in self.fields.items():
#
#             # placeholder 是默认显示的内容是什么
#             filed.widget.attrs = {'class': 'form-control', 'placeholder':filed.label}
#


def user_model_form_add(request):
    """基于modelform的用户添加"""
    if request.method == 'GET':
        form = UserModelForm()

        return render(request, 'user_model_form_add.html', {"form":form})

    # post 提交 要对数据进行校验
    # 这个data的作用是什么？
    # 对这个form的使用不是很理解，无论是post传过来的还是在校验出错的时候，
    # 直接返回一个form就能重新将错误信息渲染出来是为什么
    form = UserModelForm(data=request.POST)

    if form.is_valid():
        # print(form.cleaned_data)
        # form知道是哪个表，所以会自动翻译，然后在表上添加数据
        form.save()
        return redirect('/user/list/')
    else:
        # 校验失败，在页面上显示错误信息
        print(form.errors)

    return render(request, 'user_model_form_add.html', {"form":form})


def user_edit(request, nid):
    """编辑用户"""

    # 知道了nid，那么就可以从数据库中获取对象出来
    row_object = models.UserInfo.objects.filter(id=nid).first()
    # 这个instance的使用也不是很理解
    form = UserModelForm(instance=row_object)
    if request.method == 'GET':
        return render(request, 'user_edit.html',{'form':form})

    # 加上instance后就代表不是添加数据，而是更新数据到那一行
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.save()是添加数据的，而不是更新数据的
        # 默认保存用户输入的所有数据，如果想保存不是用户输入的数据
        # 可以form.instance = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form":form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


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


