from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash
import pymysql, os

app = Flask(__name__)

# 数据库配置
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'movic'
USERNAME = 'root'
PASSWORD = 'zm980131'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD,
                                                                                             HOSTNAME, PORT, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = os.urandom(24)
app.config["FOREIGN_KEY_CHECKS"] = 1
db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    userlogs = db.relationship("UserLog", backref="user")  # 会员日志外键关联

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



if __name__ == '__main__':
    db.drop_all()
    db.create_all()
