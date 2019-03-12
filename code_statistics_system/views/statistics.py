# -*-coding:utf-8-*-
# @Author: JinFeng 
# @Date: 2019-03-11 11:16:06 
from flask import Blueprint,redirect,session,render_template,request
import os
import uuid
import shutil
import datetime
from ..utils.sql_helper import helper

ind = Blueprint("ind",__name__)

@ind.before_request
def get_session():
    if session.get("userinfo"):
        return None
    return redirect("/login")


def index():
    user_id = session["userinfo"].get("id")
    sql = "SELECT line,date FROM code WHERE user_id=%s ORDER BY id DESC"
    params = (user_id,)
    code_list = helper.fetchmany(sql,params,3)
    return render_template("index.html",code_list=code_list)

ind.add_url_rule("/index",None,index)

@ind.route("/user_list")
def user_list():
    sql = "SELECT username,id FROM user_info"
    params = []
    users = helper.fetchall(sql,params)
    return render_template("user_list.html",users=users)

@ind.route("/home/<int:nid>")
def home(nid):
    sql = "SELECT line,date FROM code WHERE user_id=%s ORDER BY id DESC"
    params = (nid,)
    codes = helper.fetchall(sql,params)
    return render_template("home.html",codes=codes)

@ind.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")

    file_obj = request.files.get("code")
    file_name = file_obj.filename
    if not file_name.endswith(".zip"):
        return "请上传zip格式的压缩文件"

    target_path = os.path.join("file",str(uuid.uuid4()))
    shutil._unpack_zipfile(file_obj.stream,target_path)

    try:    
        total_num = 0
        for base_dir,floder_list,file_list in os.walk(target_path):        
            for filename in file_list:
                if not filename.endswith(".py"):
                    continue
                full_path = os.path.join(base_dir,filename)
                each_num = 0
                with open(full_path,"rb") as f:
                    for line in f:
                        line = line.strip()
                        if not line or not line.startswith(b"#"):
                            each_num += 1
                        continue
                total_num += each_num
    except Exception as e:
        return e

    date = datetime.date.today()
    sql = "SELECT id FROM code WHERE date=%s and user_id=%s"
    params = (date, session["userinfo"]["id"])
    if helper.fetchone(sql,params):
        return "you have uploaded already today"

    insert_sql = "INSERT INTO code(line,date,user_id) VALUES (%s,%s,%s)"
    insert_params = (total_num,date,session["userinfo"]["id"])
    helper.insert(insert_sql,insert_params)
    return "upload successfully"