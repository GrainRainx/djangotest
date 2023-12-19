import hashlib
from django.conf import settings

def md5(data_string):
    # 对加密密码加盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # 正式加密
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
