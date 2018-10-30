from datetime import datetime

from sqlalchemy import exists,or_,and_,extract

from models import table
from utils import utils_get



def set_student_rest(db,rest,stuid):
    """
    设置学员休学状态
    需要传递休学状态及学员编号
    :param db:
    :param rest:
    :param stuid:
    :return:
    """
    student = utils_get.get_student(db=db, stuid=stuid)
    if not bool(int(rest)):
        student.update(
            {table.Student.rest:False,
             table.Student.resttime:None}
        ),
    else:
        student.update(
            {table.Student.rest: True,
             table.Student.resttime: datetime.now()}
        )
    db.commit()
    res = {
        'rest':student.first().rest,
        'resttime':str(student.first().resttime)
    }
    return res

def set_attendance(db,stuid,atten_type):
    """
    设置学员考勤,如果当前学员当日已进行考勤
    将修改学员的考勤类型,并将考勤类型及时间返回
    :param db:
    :param stuid:
    :param atten_type:
    :return:
    """
    atten = db.query(table.Attendence).filter(and_(
        table.Attendence.stuid==stuid,
        extract('year', table.Attendence.atten_time) == datetime.now().year,
        extract('month', table.Attendence.atten_time) == datetime.now().month,
        extract('day', table.Attendence.atten_time) == datetime.now().day,
    ))
    if atten.first():
        atten.update({
            'atten_type':atten_type,
            'atten_time':datetime.now()
        },synchronize_session=False)
        db.commit()
        return {
            'type':atten.first().att_type.name,
            'time':str(atten.first().atten_time)}
    else:
        add_atten = table.Attendence(stuid=stuid,atten_type=atten_type)
        db.add(add_atten)
        db.commit()
        return {
            'type':add_atten.att_type.name,
            'time':str(add_atten.atten_time)
                }

def set_finish_remark(db,stuid,workid,remark):
    """
    老师对学员作业评语后,设置当前做的评语
    :param db:
    :param stuid:
    :param submit:
    :param remark:
    :return:
    """
    sql_db = db.query(table.HomeWorkFinish).filter(and_(
        table.HomeWorkFinish.stuid==stuid,
        table.HomeWorkFinish.workid==workid
    ))
    sql_db.update({
        table.HomeWorkFinish.remark:remark
    })
    db.commit()
    return sql_db.first().remark

def set_student_class(db,stuid,class_id):
    """
    学员升班,降班,留级时用于设置班级
    :param db:
    :param stuid:
    :param class_id:
    :return:
    """
    db.query(table.Belong).filter_by(stuid=stuid).update({
            table.Belong.class_id:class_id
        })
    db.commit()

def set_class_score(db,stuid,cls_id,score,examtime):
    time_format = '%Y-%m-%d %H:%M:%S'
    examtime = datetime.strptime(examtime,time_format)
    new_exam = table.Exam(stuid=stuid,class_id=cls_id,score=score,time=examtime)
    db.add(new_exam)
    db.commit()

def set_new_student(db,stuid,name,tel,qq,cls_id):
    new_stu = table.Student(name=name,stuid=stuid,tel=tel,qq=qq,password='123456')
    new_belong = table.Belong(stuid=stuid,class_id=cls_id)
    db.add(new_stu)
    db.add(new_belong)
    db.commit()