from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm
from app.models import User, db, UserLog
from datetime import datetime
from werkzeug.security import generate_password_hash
from functools import wraps
from random import choice

videoDict = {}
videoId = ""
videoLabel = ""


def user_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "name" not in session:
            return redirect(url_for("home.login"))
        return func(*args, **kwargs)

    return decorated_function


@home.route("/index")
def back():
    return redirect(url_for("home.index"))


# 前端首页
@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/annotate", methods=["GET", "POST"])
@user_login_req
def annotate():
    global videoDict
    global videoId
    global videoLabel
    userName = session.get("name")
    videos = videoDict.get(userName)
    if videos:
        video = choice(videos)
        videos.remove(video)
        videoDict[userName] = videos
        videoId = video.split('_')[0]
        videoLabel = video.split('_')[1]
        videoAddress = "http://127.0.0.1:8887/" + videoId + "_" + videoLabel + "_" + "IG.mp4"
        return render_template("home/annotate.html", videoId=videoId, videoLabel=videoLabel, videoAddress=videoAddress)
    else:
        return render_template("home/complete.html")


# 用户中心
@home.route("/user")
@user_login_req
def user():
    return render_template("home/user.html")


# 用户登录
@home.route("/login", methods=["GET", "POST"])
def login():
    global videoDict
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user.check_pwd(data["pwd"]):
            userlog = UserLog(
                user_id=user.id,
                ip=request.remote_addr
            )
            db.session.add(userlog)
            db.session.commit()
            session["name"] = user.name
            videoDict[user.name] = ["100_3_IG.mp4", "200_7_IG.mp4"]
            return redirect(url_for('home.annotate'))
    return render_template("home/login.html", form=form)


# 退出登录
@home.route("/logout", methods=["GET", "POST"])
def logout():
    form = LoginForm()
    if 'name' in session:
        session.clear()
        return render_template("home/logout.html")
    return render_template("home/logout.html")


# 会员注册
@home.route("/register", methods=["GET", "POST"])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            addtime=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")
    return render_template("home/register.html", form=form)


@home.route("/submit", methods=["GET", "POST"])
@user_login_req
def annotate1():
    global videoId
    global videoLabel
    input = request.form.get("button")
    print(videoId + "_" + videoLabel + "_" + "IG.mp4")
    print(input)
    return redirect(url_for("home.annotate"))