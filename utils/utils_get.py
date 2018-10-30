from datetime import datetime

from sqlalchemy import exists,or_,and_,extract

from models import table

def authentication(db,name,password):
    if name and password:
        db =get_teacher(db,name=name,password=password)
        if db:
            return True
        else:
            return False

def get_teacher(db,**kwargs):
    """
    获取老师信息,按照键值对方式查询
    如:name='小明'
    :param db:
    :param kwargs:
    :return:
    """
    teacher = db.query(table.Teachers).filter_by(**kwargs).first()
    # 查询当前老师是否有下属
    if get_islead(db,teacher.teacher_id):
        lead = db.query(table.LeadTheTeacher).filter_by(leadid=teacher.teacher_id).all()
        return True,lead
    else:
        return False ,teacher


def get_islead(db,teacher_id):
    """
    查询当前老师是否有所属成员
    :param db:
    :param teacher_id:
    :return:
    """
    return db.query(exists().where(table.LeadTheTeacher.leadid==teacher_id)).scalar()


def get_student(db,**kwargs):
    """
    按照按照键值对方式查询学员数据
    如:name='小明'
    :param db:
    :param kwargs:
    :return:
    """
    return db.query(table.Student).filter_by(**kwargs)

def get_clss(db,teacher_name):
    """
    查询老师所负责的班级
    :param db:
    :param teacher_name:
    :return:
    """
    teacher = get_teacher(db, name=teacher_name)
    return db.query(table.LeadTheClass).filter_by(teacher_id=teacher.teacher_id).all()

def get_clss_all(db):
    """
    查询当前所有班级
    :param db:
    :return:
    """
    return db.query(table.Class).all()

def get_stu_cls(db,cls_id):
    """
    按照当前班级编号,查询当前班级的所有学员
    :param db:
    :param cls_id:
    :return:
    """
    return db.query(table.Belong).filter_by(class_id=cls_id).all()

def get_attendance(db, cls_id, atten_time=datetime.date(datetime.now())):
    """
    获取当前班级的考勤,并遍历获取的列表,将学员的考勤信息返回
    关于考勤的类型,采用表关系的方式获取
    :param db:
    :param cls_id:
    :param atten_time:
    :return:
    """
    attens = db.query(table.Attendence).filter(
        table.Attendence.stuid == table.Belong.stuid,
        table.Belong.class_id == cls_id,
        extract('year', table.Attendence.atten_time) == atten_time.year,
        extract('month', table.Attendence.atten_time) == atten_time.month,
        extract('day', table.Attendence.atten_time) == atten_time.day,
    ).all()
    atten_dict = dict()
    if attens:
        for atten in attens:
            atten_dict[atten.stuid] = (atten.att_type.name, str(atten.atten_time))
        return atten_dict

def get_homework(db,cls_id):
    """
    获取当前班级的所有已布置的作业
    :param db:
    :param cls_id:
    :return:
    """
    return db.query(table.HomeWork).filter_by(class_id=cls_id).all()

def get_finish_homework(db,workid):
    """
    获取作业完成表中,workid的数据
    :param db:
    :param workid:
    :return:
    """
    return db.query(table.HomeWorkFinish).filter_by(workid=workid).all()

def get_exam_class(db,cls_id):
    """
    获取当前班级所有成员的考试成绩
    :param db:
    :param cls_id:
    :return:
    """

    belong_stu = db.query(table.Belong).filter_by(class_id=cls_id).all()

    exam_dic = {}

    for belong in belong_stu:
        exams = db.query(table.Exam).filter_by(stuid=belong.stuid).all()
        if len(exams)>0:
            exam_dic[belong.stuid] = exams[-1].score,str(exams[-1].time)


    return belong_stu,exam_dic


def get_stu_class_level(db,type,stuid):
    """
    获取当前学员的班级等级,并按照类型返回相关的数据
    :param db:
    :param stuid:
    :return:
    """
    stu = db.query(table.Belong).filter_by(stuid=stuid).first()
    if type=='up':
        res =  db.query(table.Class).filter(table.Class.lever>stu.cls_name.lever).all()
    elif type == 'down':
        res =  db.query(table.Class).filter(table.Class.lever<stu.cls_name.lever).all()
    else:
        res =  db.query(table.Class).filter(table.Class.lever==stu.cls_name.lever).all()
    return stu,res



def get_stu_score_all(db,stuid):
    """
    获取当前学员的所有的分数
    :param db:
    :param stuid:
    :return:
    """
    scores = db.query(table.Exam).filter_by(stuid=stuid).all()
    score_lis = list()
    score_dic = {stuid:stuid}
    for score in scores:
        score_lis.append( {
            "class":score.examcls.class_name,
            "score":score.score,
            "time":str(score.time)
        })
    score_dic[stuid] = score_lis

    return score_dic
