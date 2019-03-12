# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/3/8 22:25

# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/3/7 16:22

from flask import Blueprint,render_template, request,session,redirect,url_for
from ..utils import sha
from ..utils.sql_helper import helper

account = Blueprint("account",__name__)

@account.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")

    sql = "SELECT id, username FROM user_info WHERE username=%s and password=%s"
    params = (username,sha.encrpted_or_decrpted(password))
    data = helper.fetchone()
    if data:
        session["userinfo"] = data
        return redirect("/index")
    return "用户名或密码错误"

@account.route("/logout")
def logout():
    try:
        del session["userinfo"]
        return redirect("/login")
    except Exception as e:
        return "请先登录"



