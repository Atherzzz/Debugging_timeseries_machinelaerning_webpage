from queue import PriorityQueue

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash
import pymysql, os

app = Flask(__name__)

# 数据库配置
HOSTNAME = 'mengzheng.mysql.pythonanywhere-services.com'
PORT = '3306'
DATABASE = 'mengzheng$movic'
USERNAME = 'mengzheng'
PASSWORD = 'zm980131'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD,
                                                                                             HOSTNAME, PORT, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = os.urandom(24)
app.config["FOREIGN_KEY_CHECKS"] = 1
db = SQLAlchemy(app)

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

videoDict = []
# --------------------zero(Test)------------------------#
videoDict.append((0, "0_8_0_OS.mp4"))
videoDict.append((0, "1_0_0_OS.mp4"))
videoDict.append((0, "2_4_0_OS.mp4"))
videoDict.append((0, "3_4_0_OS.mp4"))
videoDict.append((0, "4_8_0_OS.mp4"))
videoDict.append((0, "5_0_0_OS.mp4"))
videoDict.append((0, "6_0_0_OS.mp4"))
videoDict.append((0, "7_0_0_OS.mp4"))
videoDict.append((0, "8_0_0_OS.mp4"))
videoDict.append((0, "9_0_0_OS.mp4"))
# --------------------one(Test)------------------------#
videoDict.append((0, "30_1_1_OS.mp4"))
videoDict.append((0, "31_1_1_OS.mp4"))
videoDict.append((0, "32_1_1_OS.mp4"))
videoDict.append((0, "33_1_1_OS.mp4"))
videoDict.append((0, "34_1_1_OS.mp4"))
videoDict.append((0, "35_1_1_OS.mp4"))
videoDict.append((0, "36_1_1_OS.mp4"))
videoDict.append((0, "37_1_1_OS.mp4"))
videoDict.append((0, "38_1_1_OS.mp4"))
videoDict.append((0, "39_1_1_OS.mp4"))
# --------------------two(Test)------------------------#
videoDict.append((0, "60_9_2_OS.mp4"))
videoDict.append((0, "61_7_2_OS.mp4"))
videoDict.append((0, "62_7_2_OS.mp4"))
videoDict.append((0, "63_9_2_OS.mp4"))
videoDict.append((0, "64_2_2_OS.mp4"))
videoDict.append((0, "65_9_2_OS.mp4"))
videoDict.append((0, "66_4_2_OS.mp4"))
videoDict.append((0, "67_7_2_OS.mp4"))
videoDict.append((0, "68_1_2_OS.mp4"))
videoDict.append((0, "69_2_2_OS.mp4"))
# --------------------three(Test)------------------------#
videoDict.append((0, "90_5_3_OS.mp4"))
videoDict.append((0, "91_3_3_OS.mp4"))
videoDict.append((0, "92_3_3_OS.mp4"))
videoDict.append((0, "93_3_3_OS.mp4"))
videoDict.append((0, "94_3_3_OS.mp4"))
videoDict.append((0, "95_3_3_OS.mp4"))
videoDict.append((0, "96_9_3_OS.mp4"))
videoDict.append((0, "97_3_3_OS.mp4"))
videoDict.append((0, "98_3_3_OS.mp4"))
videoDict.append((0, "99_3_3_OS.mp4"))
# --------------------four(Test)------------------------#
videoDict.append((0, "120_4_4_OS.mp4"))
videoDict.append((0, "121_4_4_OS.mp4"))
videoDict.append((0, "122_4_4_OS.mp4"))
videoDict.append((0, "123_4_4_OS.mp4"))
videoDict.append((0, "124_4_4_OS.mp4"))
videoDict.append((0, "125_4_4_OS.mp4"))
videoDict.append((0, "126_4_4_OS.mp4"))
videoDict.append((0, "127_4_4_OS.mp4"))
videoDict.append((0, "128_4_4_OS.mp4"))
videoDict.append((0, "129_4_4_OS.mp4"))
# --------------------five(Test)------------------------#
videoDict.append((0, "140_5_5_OS.mp4"))
videoDict.append((0, "141_5_5_OS.mp4"))
videoDict.append((0, "142_5_5_OS.mp4"))
videoDict.append((0, "143_5_5_OS.mp4"))
videoDict.append((0, "144_5_5_OS.mp4"))
videoDict.append((0, "145_5_5_OS.mp4"))
videoDict.append((0, "146_5_5_OS.mp4"))
videoDict.append((0, "147_5_5_OS.mp4"))
videoDict.append((0, "148_5_5_OS.mp4"))
videoDict.append((0, "149_5_5_OS.mp4"))
# --------------------six(Test)------------------------#
videoDict.append((0, "160_6_6_OS.mp4"))
videoDict.append((0, "161_6_6_OS.mp4"))
videoDict.append((0, "162_6_6_OS.mp4"))
videoDict.append((0, "163_6_6_OS.mp4"))
videoDict.append((0, "164_6_6_OS.mp4"))
videoDict.append((0, "165_6_6_OS.mp4"))
videoDict.append((0, "166_6_6_OS.mp4"))
videoDict.append((0, "167_6_6_OS.mp4"))
videoDict.append((0, "168_6_6_OS.mp4"))
videoDict.append((0, "169_6_6_OS.mp4"))
# --------------------seven(Test)------------------------#
videoDict.append((0, "182_7_7_OS.mp4"))
videoDict.append((0, "183_7_7_OS.mp4"))
videoDict.append((0, "184_7_7_OS.mp4"))
videoDict.append((0, "186_1_7_OS.mp4"))
videoDict.append((0, "187_7_7_OS.mp4"))
videoDict.append((0, "200_7_7_OS.mp4"))
videoDict.append((0, "201_2_7_OS.mp4"))
videoDict.append((0, "202_9_7_OS.mp4"))
videoDict.append((0, "203_1_7_OS.mp4"))
videoDict.append((0, "204_9_7_OS.mp4"))
# --------------------eight(Test)------------------------#
videoDict.append((0, "210_9_8_OS.mp4"))
videoDict.append((0, "211_7_8_OS.mp4"))
videoDict.append((0, "212_1_8_OS.mp4"))
videoDict.append((0, "214_1_8_OS.mp4"))
videoDict.append((0, "215_1_8_OS.mp4"))
videoDict.append((0, "216_7_8_OS.mp4"))
videoDict.append((0, "217_1_8_OS.mp4"))
videoDict.append((0, "218_1_8_OS.mp4"))
videoDict.append((0, "219_1_8_OS.mp4"))
videoDict.append((0, "220_9_8_OS.mp4"))
# --------------------nine(Test)------------------------#
videoDict.append((0, "240_9_9_OS.mp4"))
videoDict.append((0, "241_9_9_OS.mp4"))
videoDict.append((0, "242_9_9_OS.mp4"))
videoDict.append((0, "243_9_9_OS.mp4"))
videoDict.append((0, "244_9_9_OS.mp4"))
videoDict.append((0, "245_9_9_OS.mp4"))
videoDict.append((0, "246_9_9_OS.mp4"))
videoDict.append((0, "247_9_9_OS.mp4"))
videoDict.append((0, "249_9_9_OS.mp4"))
videoDict.append((0, "250_9_9_OS.mp4"))

# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    userlogs = db.relationship("UserLog", backref="user")  # 会员日志外键关联
    annotated = db.Column(db.String(2000))
    # trained = db.Column(db.Boolean)
    train = db.Column(db.String(200))
    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


class UserLog(db.Model):
    """
    会员登录日志表
    """
    __tablename__ = "userlog"  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间；
    def __repr__(self):
        return "<UserLog %r>" % self.id


class Pic(db.Model):
    __tablename__ = "pic"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    index = db.Column(db.Integer)
    pred = db.Column(db.Integer)
    label = db.Column(db.Integer)
    user_name = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    shouldknow = db.relationship("ShouldKnow", backref="pic")

class ShouldKnow(db.Model):
    __tablename__ = "shouldknow"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pic_id = db.Column(db.Integer, db.ForeignKey('pic.id'))
    pic_annotation = db.Column(db.String(100))


class TestData(db.Model):
    __tablename__ = "testdata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    annotated_time = db.Column(db.Integer)


class TrainData(db.Model):
    __tablename__ = "traindata"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    answer = db.Column(db.String(100))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    for key in trainAns.keys():
        traindata = TrainData(
            name=key,
            answer=trainAns[key]
        )
        db.session.add(traindata)
    db.session.commit()
    while videoDict:
        video = videoDict.pop()
        testdata = TestData(
            name=video[1],
            annotated_time=video[0]
        )
        db.session.add(testdata)
    db.session.commit()