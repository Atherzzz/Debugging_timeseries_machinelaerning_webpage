from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm
from app.models import User, db, UserLog, Pic, ShouldKnow
from datetime import datetime
from werkzeug.security import generate_password_hash
from functools import wraps
from queue import PriorityQueue
from random import choice
import heapq

videoDict = PriorityQueue()
# videoDict = [(0, "0_8_0_OS.mp4"), (0, "1_0_0_OS.mp4"), (0, "2_4_0_OS.mp4"), (0, "3_4_0_OS.mp4"), (0, "4_8_0_OS.mp4"),
#              (0, "5_0_0_OS.mp4"), (0, "6_0_0_OS.mp4"), (0, "7_0_0_OS.mp4"), (0, "8_0_0_OS.mp4"), (0, "9_0_0_OS.mp4")]
trainDict = {}
trained = {"a": True, "1": True, "2": True}
videoId = ""
videoLabel = ""
trueLabel = ""
visited = {}
# --------------------zero(Test)------------------------#
videoDict.put((0, "0_8_0_OS.mp4"))
videoDict.put((0, "1_0_0_OS.mp4"))
videoDict.put((0, "2_4_0_OS.mp4"))
videoDict.put((0, "3_4_0_OS.mp4"))
videoDict.put((0, "4_8_0_OS.mp4"))
videoDict.put((0, "5_0_0_OS.mp4"))
videoDict.put((0, "6_0_0_OS.mp4"))
videoDict.put((0, "7_0_0_OS.mp4"))
videoDict.put((0, "8_0_0_OS.mp4"))
videoDict.put((0, "9_0_0_OS.mp4"))
# --------------------one(Test)------------------------#
videoDict.put((0, "30_1_1_OS.mp4"))
videoDict.put((0, "31_1_1_OS.mp4"))
videoDict.put((0, "32_1_1_OS.mp4"))
videoDict.put((0, "33_1_1_OS.mp4"))
videoDict.put((0, "34_1_1_OS.mp4"))
videoDict.put((0, "35_1_1_OS.mp4"))
videoDict.put((0, "36_1_1_OS.mp4"))
videoDict.put((0, "37_1_1_OS.mp4"))
videoDict.put((0, "38_1_1_OS.mp4"))
videoDict.put((0, "39_1_1_OS.mp4"))
# --------------------two(Test)------------------------#
videoDict.put((0, "60_9_2_OS.mp4"))
videoDict.put((0, "61_7_2_OS.mp4"))
videoDict.put((0, "62_7_2_OS.mp4"))
videoDict.put((0, "63_9_2_OS.mp4"))
videoDict.put((0, "64_2_2_OS.mp4"))
videoDict.put((0, "65_9_2_OS.mp4"))
videoDict.put((0, "66_4_2_OS.mp4"))
videoDict.put((0, "67_7_2_OS.mp4"))
videoDict.put((0, "68_1_2_OS.mp4"))
videoDict.put((0, "69_2_2_OS.mp4"))
# --------------------three(Test)------------------------#
videoDict.put((0, "90_5_3_OS.mp4"))
videoDict.put((0, "91_3_3_OS.mp4"))
videoDict.put((0, "92_3_3_OS.mp4"))
videoDict.put((0, "93_3_3_OS.mp4"))
videoDict.put((0, "94_3_3_OS.mp4"))
videoDict.put((0, "95_3_3_OS.mp4"))
videoDict.put((0, "96_9_3_OS.mp4"))
videoDict.put((0, "97_3_3_OS.mp4"))
videoDict.put((0, "98_3_3_OS.mp4"))
videoDict.put((0, "99_3_3_OS.mp4"))
# --------------------four(Test)------------------------#
videoDict.put((0, "120_4_4_OS.mp4"))
videoDict.put((0, "121_4_4_OS.mp4"))
videoDict.put((0, "122_4_4_OS.mp4"))
videoDict.put((0, "123_4_4_OS.mp4"))
videoDict.put((0, "124_4_4_OS.mp4"))
videoDict.put((0, "125_4_4_OS.mp4"))
videoDict.put((0, "126_4_4_OS.mp4"))
videoDict.put((0, "127_4_4_OS.mp4"))
videoDict.put((0, "128_4_4_OS.mp4"))
videoDict.put((0, "129_4_4_OS.mp4"))
# --------------------five(Test)------------------------#
videoDict.put((0, "140_5_5_OS.mp4"))
videoDict.put((0, "141_5_5_OS.mp4"))
videoDict.put((0, "142_5_5_OS.mp4"))
videoDict.put((0, "143_5_5_OS.mp4"))
videoDict.put((0, "144_5_5_OS.mp4"))
videoDict.put((0, "145_5_5_OS.mp4"))
videoDict.put((0, "146_5_5_OS.mp4"))
videoDict.put((0, "147_5_5_OS.mp4"))
videoDict.put((0, "148_5_5_OS.mp4"))
videoDict.put((0, "149_5_5_OS.mp4"))
# --------------------six(Test)------------------------#
videoDict.put((0, "160_6_6_OS.mp4"))
videoDict.put((0, "161_6_6_OS.mp4"))
videoDict.put((0, "162_6_6_OS.mp4"))
videoDict.put((0, "163_6_6_OS.mp4"))
videoDict.put((0, "164_6_6_OS.mp4"))
videoDict.put((0, "165_6_6_OS.mp4"))
videoDict.put((0, "166_6_6_OS.mp4"))
videoDict.put((0, "167_6_6_OS.mp4"))
videoDict.put((0, "168_6_6_OS.mp4"))
videoDict.put((0, "169_6_6_OS.mp4"))
# --------------------seven(Test)------------------------#
videoDict.put((0, "182_7_7_OS.mp4"))
videoDict.put((0, "183_7_7_OS.mp4"))
videoDict.put((0, "184_7_7_OS.mp4"))
videoDict.put((0, "186_1_7_OS.mp4"))
videoDict.put((0, "187_7_7_OS.mp4"))
videoDict.put((0, "200_7_7_OS.mp4"))
videoDict.put((0, "201_2_7_OS.mp4"))
videoDict.put((0, "202_9_7_OS.mp4"))
videoDict.put((0, "203_1_7_OS.mp4"))
videoDict.put((0, "204_9_7_OS.mp4"))
# --------------------eight(Test)------------------------#
videoDict.put((0, "210_9_8_OS.mp4"))
videoDict.put((0, "211_7_8_OS.mp4"))
videoDict.put((0, "212_1_8_OS.mp4"))
videoDict.put((0, "214_1_8_OS.mp4"))
videoDict.put((0, "215_1_8_OS.mp4"))
videoDict.put((0, "216_7_8_OS.mp4"))
videoDict.put((0, "217_1_8_OS.mp4"))
videoDict.put((0, "218_1_8_OS.mp4"))
videoDict.put((0, "219_1_8_OS.mp4"))
videoDict.put((0, "220_9_8_OS.mp4"))
# --------------------nine(Test)------------------------#
videoDict.put((0, "240_9_9_OS.mp4"))
videoDict.put((0, "241_9_9_OS.mp4"))
videoDict.put((0, "242_9_9_OS.mp4"))
videoDict.put((0, "243_9_9_OS.mp4"))
videoDict.put((0, "244_9_9_OS.mp4"))
videoDict.put((0, "245_9_9_OS.mp4"))
videoDict.put((0, "246_9_9_OS.mp4"))
videoDict.put((0, "247_9_9_OS.mp4"))
videoDict.put((0, "249_9_9_OS.mp4"))
videoDict.put((0, "250_9_9_OS.mp4"))
trainAns = {"25_8_0_OS.mp4": "9,6 6,3 3,2 2,1 1,4 4,7 7,8 8,9",
            "50_1_1_OS.mp4": "2,5 5,8",
            "75_8_2_OS.mp4": "2,3 3,6 6,8 8,9 7,8 8,7",
            "100_3_3_OS.mp4": "2,3 3,6 6,5 5,6 6,9 9,8 8,7",
            "125_4_4_OS.mp4": "2,4 4,5 5,6 6,5 5,2 2,5 5,8",
            "150_5_5_OS.mp4": "2,5 5,4 4,5 5,6 6,9 9,8 8,7 7,8 8,5 5,2 2,3",
            "175_6_6_OS.mp4": "3,5 5,4 4,7 7,8 8,9 9,5 5,8",
            "200_7_7_OS.mp4": "1,2 2,3 3,6 6,9",
            "210_9_8_OS.mp4": "5,6 6,3 3,2 2,1 1,4 4,5 5,9 9,8 8,7 7,5",
            "249_9_9_OS.mp4": "3,2 2,5 5,6 6,3 3,6 6,9 9,8"
            }


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
    global trueLabel
    global visited
    store = []
    userName = session.get("name")
    if trained.get(userName):
        if len(visited.get(userName)) >= videoDict.qsize():
            return render_template("home/complete.html")
        else:
            video = videoDict.get()
            while video[1] in visited.get(userName):
                store.append(video)
                video = videoDict.get()
            while store:
                videoDict.put(store.pop())
            videoId = video[1].split('_')[0]
            videoLabel = video[1].split('_')[1]
            trueLabel = video[1].split('_')[2]
            videoAddress = "../../static/video/" + videoId + "_" + videoLabel + "_" + trueLabel + "_OS.mp4"
            originalVideoAddress = "../../static/video/" + videoId + "_" + videoLabel + "_" + trueLabel + ".mp4"
            if video[0] >= 2:
                return render_template("home/annotate.html", videoId=videoId, videoLabel=videoLabel,
                                       videoAddress=videoAddress, originalVideoAddress=originalVideoAddress,
                                       trueLabel=trueLabel)
            else:
                videoDict.put((video[0] + 1, video[1]))
                tempSet = visited.get(userName)
                tempSet.add(video[1])
                visited[userName] = tempSet
                return render_template("home/annotate.html", videoId=videoId, videoLabel=videoLabel,
                                       videoAddress=videoAddress, originalVideoAddress=originalVideoAddress,
                                       trueLabel=trueLabel)
    else:
        return redirect(url_for('home.user'))


# 用户中心
@home.route("/user")
@user_login_req
def user():
    userName = session.get("name")
    global trainDict
    global trained
    if trainDict[userName]:
        videoName = trainDict[userName].pop()
        trainId = videoName.split('_')[0]
        trainLabel = videoName.split('_')[1]
        tranTrueLabel = videoName.split('_')[2]
        videoAddress = "../../static/video/" + trainId + "_" + trainLabel + "_" + tranTrueLabel + "_OS.mp4"
        originalVideoAddress = "../../static/video/" + trainId + "_" + trainLabel + "_" + tranTrueLabel + ".mp4"
        return render_template("home/user.html", videoId=trainId, videoLabel=trainLabel,
                               videoAddress=videoAddress, originalVideoAddress=originalVideoAddress,
                               answer=trainAns[videoName], trueLabel=tranTrueLabel)
    else:
        trained[userName] = True
        trainDict[userName] = ["249_9_9_OS.mp4", "210_9_8_OS.mp4", "25_8_0_OS.mp4", "50_1_1_OS.mp4", "75_8_2_OS.mp4",
                               "100_3_3_OS.mp4",
                               "125_4_4_OS.mp4", "150_5_5_OS.mp4", "175_6_6_OS.mp4", "200_7_7_OS.mp4",
                               ]
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
                if user.name not in visited.keys():
                    trained[user.name] = False
                    visited[user.name] = set()
                    trainDict[user.name] = ["249_9_9_OS.mp4", "210_9_8_OS.mp4", "25_8_0_OS.mp4", "50_1_1_OS.mp4",
                                            "75_8_2_OS.mp4", "100_3_3_OS.mp4",
                                            "125_4_4_OS.mp4", "150_5_5_OS.mp4", "175_6_6_OS.mp4", "200_7_7_OS.mp4"
                                            ]
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
    if input:
        pic = Pic(
            name=videoId + "_" + videoLabel + "_" + trueLabel + "_" + "IG.mp4",
            index=int(videoId),
            pred=int(videoLabel),
            label=int(videoLabel),
            user_name=session["name"],
            add_time=datetime.now()
        )
        db.session.add(pic)
        db.session.commit()
        should_know = ShouldKnow(
            pic_id=pic.id,
        )
        should_know.pic_annotation = input
        db.session.add(should_know)
        db.session.commit()
    return redirect(url_for("home.annotate"))
