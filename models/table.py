from datetime import datetime

from sqlalchemy import  Column,Integer,String,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import relationship

from models import db

class Class(db.Base):
    """
    班级表
    可反查学员表,与分数表和班主任表
    包含字段:
    班级编号、班级名称、班级等级
    """
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(String(255),unique=True)
    class_name = Column(String(50),nullable=False)
    lever = Column(Integer,default=1)

class Teachers(db.Base):
    """
    老师档案表
    可反查班级
    含有字段
    老师编号、老师姓名、登录密码、电话、QQ、入职时间、是否离职、离职时间
    """
    __tablename__ = 'teachers'
    id = Column(Integer,primary_key=True,autoincrement=True)
    teacher_id = Column(String(255),unique=True)
    name = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)
    tel = Column(String(15),nullable=False)
    qq = Column(String(11),nullable=False)
    hiredate = Column(DateTime,default=datetime.now())
    resigned = Column(Boolean,default=False)
    leavedate = Column(DateTime)

    tl = relationship('TeacherLever',backref='tl')
    ltc = relationship('LeadTheClass',backref='ltc')

class LeadTheClass(db.Base):
    """
    老师负责的班级
    含有字段
    老师编号,班级编号
    """
    __tablename__ = 'leadtheclass'
    id = Column(Integer,primary_key=True,autoincrement=True)
    teacher_id = Column(String(255),ForeignKey('teachers.teacher_id'))
    class_id = Column(String(255),ForeignKey('class.class_id'))

    cls_name = relationship('Class',backref='cls',uselist=False)

class TeacherLever(db.Base):
    """
    老师职位表
    level 1 普通老师
    level 2 高级老师
    level 3 班主任
    level 4 教导主任
    level 5 校长
    默认注册为普通老师
    包含字段
    """
    __tablename__ = 'teacherlevel'
    id = Column(Integer,primary_key=True,autoincrement=True)
    teacher_id = Column(String(255),ForeignKey("teachers.teacher_id"))
    level = Column(Integer,default=1)

class Student(db.Base):
    """
    学员档案表
    包含字段
    学员编号、学员姓名、登录密码、电话、QQ、入学时间、是否休学、休学时间
    """
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True,autoincrement=True)
    stuid = Column(String(255),unique=True)
    name = Column(String(20),nullable=False)
    password = Column(String(255),nullable=False)
    tel = Column(String(15),nullable=False)
    qq = Column(String(11),nullable=False)
    enrollment = Column(DateTime,default=datetime.now())
    rest = Column(Boolean,default=False)
    resttime = Column(DateTime)

class Belong(db.Base):
    """
    学员所属班级表
    包含字段
    班级编号,学员编号
    """
    __tablename__ = 'belong'
    id = Column(Integer,primary_key=True,autoincrement=True)
    class_id = Column(String(255),ForeignKey("class.class_id"))
    stuid = Column(String(255), ForeignKey('students.stuid'))

    stu = relationship('Student',backref='stu')
    cls_name = relationship('Class',backref='cls_name')

class Exam(db.Base):
    """
    学员考试情况表
    包含字段
    学员编号,学员班级,考试时间,得分
    """
    __tablename__ = 'exam'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stuid = Column(String(255), ForeignKey('students.stuid'))
    class_id = Column(String(255), ForeignKey('class.class_id'))
    time = Column(DateTime, default=datetime.now())
    score = Column(Integer, nullable=False)

    # stuname = relationship('Student',backref='stuname')
    examcls = relationship('Class',backref='examcls')

class Attendence(db.Base):
    """
    学员考勤表
    包含字段
    学员编号,考勤类型,考勤时间
    """
    __tablename__ = 'attendance'
    id = Column(Integer,primary_key=True,autoincrement=True)
    stuid = Column(String(255),ForeignKey('students.stuid'))
    atten_type = Column(Integer,ForeignKey('attendencetype.id'))
    content = Column(String(255))
    atten_time  = Column(DateTime,default=datetime.now())

    att_type = relationship('AttendenceType',backref='att_type')

class AttendenceType(db.Base):
    """
    用于存放各种类型的学员考勤状况
    默认
    atten_type 1 正常
    atten_type 2 请假
    atten_type 3 旷课
    包含字段
    考勤类型,考勤名称
    """
    __tablename__ = "attendencetype"
    id = Column(Integer,primary_key=True,autoincrement=True)
    atten_type = Column(Integer,nullable=False)
    name = Column(String(255),nullable=False)

class HomeWork(db.Base):
    """
    作业表
    包含字段
    作业的编号,作业的标题,作业的内容,所属班级
    """
    __tablename__ = 'homework'
    id = Column(Integer,primary_key=True,autoincrement=True)
    workid = Column(String(255),unique=True)
    titile = Column(String(255),nullable=False)
    content = Column(String(1024),nullable=False)
    class_id = Column(String(255),ForeignKey("class.class_id"))

    cls_home = relationship('Class',backref='cls_home')
    fin_num = relationship('HomeWorkFinish',backref='fin_num')

class HomeWorkFinish(db.Base):
    """
    作业完成情况表
    包含字段pycharm2018 同步代码
    学员编号,作业的编号,提交的内容,提交时间
    """
    __tablename__ = 'homeworkfinish'
    id = Column(Integer,primary_key=True,autoincrement=True)
    stuid = Column(String(255),ForeignKey('students.stuid'))
    workid = Column(String(255),ForeignKey('homework.workid'))
    content = Column(String(1024),nullable=False)
    submit  = Column(DateTime,default=datetime.now())
    remark = Column(String(1024))  # 添加老师评语

    finish_stu = relationship('Student',backref='finish_stu')

class LeadTheTeacher(db.Base):
    """
    老师领导表,比如版主任下级的老师
    """
    __tablename__ = 'leadtheteacher'
    id = Column(Integer,primary_key=True,autoincrement=True)
    leadid = Column(String(255),ForeignKey('teachers.teacher_id'))
    teacherid = Column(String(255),ForeignKey('leadtheclass.teacher_id'))

    ltt_cls = relationship("LeadTheClass",backref="ltt_cls",uselist=False)