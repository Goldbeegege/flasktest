# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/3/9 10:27
# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/3/7 18:23
from hashlib import sha1

from settings import Config



def encrpted_or_decrpted(psd):
    ha = sha1(bytes(Config.SALT,encoding="utf-8"))
    ha.update(bytes(psd,encoding="utf-8"))
    return ha.hexdigest()

