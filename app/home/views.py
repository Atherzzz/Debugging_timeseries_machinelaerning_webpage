from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm
from app.models import User, db, UserLog, Pic, ShouldKnow, TrainData, TestData
from datetime import datetime
from werkzeug.security import generate_password_hash
from functools import wraps
from queue import PriorityQueue
from random import choice
import heapq


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
    videoName = ""
    userName = session.get("name")
    user = User.query.filter_by(name=userName).first()
    if not user.train:
        annotateList = user.annotated.split(",")
        if len(annotateList) >= 100:
            return render_template("home/complete.html")
        else:
            couldAnnotatedList = TestData.query.filter(TestData.annotated_time < 3).order_by(
                TestData.annotated_time).all()
            for couldAnnotated in couldAnnotatedList:
                if couldAnnotated.name in annotateList:
                    pass
                else:
                    videoName = couldAnnotated.name
                    break
            if videoName:
                videoId = videoName.split('_')[0]
                videoLabel = videoName.split('_')[1]
                trueLabel = videoName.split('_')[2]
                videoAddress = "../../static/video/" + videoId + "_" + videoLabel + "_" + trueLabel + "_OS.mp4"
                originalVideoAddress = "../../static/video/" + videoId + "_" + videoLabel + "_" + trueLabel + ".mp4"
                return render_template("home/annotate.html", videoId=videoId, videoLabel=videoLabel,
                                       videoAddress=videoAddress, originalVideoAddress=originalVideoAddress,
                                       trueLabel=trueLabel)
            else:
                return render_template("home/complete.html")
    else:
        return redirect(url_for('home.user'))


# 用户中心
@home.route("/user")
@user_login_req
def user():
    userName = session.get("name")
    global trainDict
    global trained
    user = User.query.filter_by(name=userName).first()
    if user.train:
        trainList = user.train.split(",")
        videoName = trainList[0]
        trainId = videoName.split('_')[0]
        trainLabel = videoName.split('_')[1]
        tranTrueLabel = videoName.split('_')[2]
        print(videoName)
        trainData = TrainData.query.filter_by(name=videoName).first()
        print()
        if len(trainList) > 1:
            user.train = user.train.replace(videoName + ',', '')
        else:
            user.train = user.train.replace(videoName, '')
        db.session.add(user)
        db.session.commit()
        videoAddress = "../../static/video/" + trainId + "_" + trainLabel + "_" + tranTrueLabel + "_OS.mp4"
        originalVideoAddress = "../../static/video/" + trainId + "_" + trainLabel + "_" + tranTrueLabel + ".mp4"
        return render_template("home/user.html", videoId=trainId, videoLabel=trainLabel,
                               videoAddress=videoAddress, originalVideoAddress=originalVideoAddress,
                               answer=trainData.answer, trueLabel=tranTrueLabel)
    else:
        return redirect(url_for('home.annotate'))


# 用户中心
@home.route("/reannotate")
@user_login_req
def reannotate():
    userName = session.get("name")
    user = User.query.filter_by(name=userName).first()
    user.train = "249_9_9_OS.mp4,210_9_8_OS.mp4,25_8_0_OS.mp4,50_1_1_OS.mp4,75_8_2_OS.mp4,100_3_3_OS.mp4," \
                 "125_4_4_OS.mp4,150_5_5_OS.mp4,175_6_6_OS.mp4,200_7_7_OS.mp4"
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home.annotate'))


@home.route("/train", methods=["GET", "POST"])
@user_login_req
def annotate2():
    return redirect(url_for("home.user"))


# 用户登录
@home.route("/login", methods=["GET", "POST"])
def login():
    global videoDict
    global visited
    global trained
    global trainDict
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if user.check_pwd(data["pwd"]):
                userlog = UserLog(
                    user_id=user.id,
                    ip=request.remote_addr
                )
                db.session.add(userlog)
                db.session.commit()
                session["name"] = user.name
                return redirect(url_for('home.annotate'))
        else:
            return redirect(url_for('home.register'))
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
            addtime=datetime.now(),
            annotated="",
            train="249_9_9_OS.mp4,210_9_8_OS.mp4,25_8_0_OS.mp4,50_1_1_OS.mp4,75_8_2_OS.mp4,100_3_3_OS.mp4,"
                  "125_4_4_OS.mp4,150_5_5_OS.mp4,175_6_6_OS.mp4,200_7_7_OS.mp4"
        )
        db.session.add(user)
        db.session.commit()
        flash("success", "ok")
    return render_template("home/register.html", form=form)


@home.route("/submit", methods=["GET", "POST"])
@user_login_req
def annotate1():
    userName = session.get("name")
    user = User.query.filter_by(name=userName).first()
    input = request.form.get("button")
    print(input)
    inputList = input.split("$")
    if inputList[0]:
        videoName = inputList[1]
        videoList = videoName.split("_")
        pic = Pic(
            name=videoName,
            index=int(videoList[0]),
            pred=int(videoList[1]),
            label=int(videoList[2]),
            user_name=session["name"],
            add_time=datetime.now()
        )
        db.session.add(pic)
        db.session.commit()
        should_know = ShouldKnow(
            pic_id=pic.id,
        )
        should_know.pic_annotation = inputList[0]
        db.session.add(should_know)
        db.session.commit()
        video = TestData.query.filter_by(name=videoName).first()
        video.annotated_time = video.annotated_time + 1
        db.session.add(video)
        db.session.commit()
        annotateList = user.annotated.split(",")
        if annotateList:
            user.annotated = user.annotated + "," + videoName
        else:
            user.annotated = videoName
        db.session.add(user)
        db.session.commit()
    return redirect(url_for("home.annotate"))
