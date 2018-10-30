import tornado.web
from pycket.session import SessionMixin

from models import table
from utils import utils_set,utils_get


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    """
    全局handler基础
    """
    def prepare(self):
        self.dbsession = table.db.DBSession()

    def current_user(self):
        return self.session.get('teacher', None)

    def on_finish(self):
        self.dbsession.close()

class IndexHandler(BaseHandler):
    """
    网站首页,老师登录
    """
    def get(self, *args, **kwargs):
        if not self.current_user():
            self.render('index.html')
        else:
            self.redirect(r'/login')

    def post(self, *args, **kwargs):
        name = self.get_argument('name', None)
        password = self.get_argument('password', None)
        if utils_get.authentication(self.dbsession, name, password):
            self.session.set('teacher', name)
            self.redirect(r'/login')
        else:
            self.redirect(r'/')

class StuHandler(BaseHandler):
    """
    学员信息管理页面
    可以对学员的休学状态进行操作
    """

    @tornado.web.authenticated
    def get(self, cls_id, *args, **kwargs):
        stus = utils_get.get_stu_cls(self.dbsession, cls_id)
        clss = utils_get.get_clss_all(self.dbsession)
        self.render('student.html', stus=stus, clss=clss,cls_id=cls_id)

    def post(self, *args, **kwargs):
        """
        从浏览器获取数据,来设置学员的是否休学
        :param args:
        :param kwargs:
        :return:
        """
        stuid = self.get_argument('stuid', None)
        rest = self.get_argument('rest', None)
        res =utils_set.set_student_rest(self.dbsession, stuid=stuid, rest=rest)
        self.write(res)

class AttendanceHandler(BaseHandler):
    """
    操作学员考勤
    """

    @tornado.web.authenticated
    def get(self,cls_id, *args, **kwargs):
        stus = utils_get.get_stu_cls(self.dbsession, cls_id)
        attens = utils_get.get_attendance(self.dbsession,cls_id)
        self.render('attendance.html', stus=stus,attens = attens,cls_id=cls_id)

    def post(self, *args, **kwargs):
        stuid = self.get_argument('stuid',None)
        atten_type = self.get_argument('atten_type',None)
        res = utils_set.set_attendance(self.dbsession,stuid=stuid,atten_type=atten_type)
        self.write(res)

class HomeWorkHandler(BaseHandler):
    """
    作业管理页面,仅用于查看作业
    """
    @tornado.web.authenticated
    def get(self,cls_id,*args,**kwargs):
        self.render('homework.html',cls_id=cls_id,homeworks=utils_get.get_homework(self.dbsession,cls_id))

class InspectHandler(BaseHandler):
    """
    作业检查页面
    POST 为老师对当前作业进行评价操作时的数据处理
    """
    @tornado.web.authenticated
    def get(self,workid,*args,**kwargs):
        workfinishs = utils_get.get_finish_homework(self.dbsession,workid=workid)
        self.render('inspect.html',workfinishs=workfinishs)

    def post(self, workid,*args, **kwargs):
        stuid = self.get_argument('stuid',None)
        remark = self.get_argument('remark',None)
        add_remark =  utils_set.set_finish_remark(self.dbsession,workid=workid ,stuid=stuid,remark=remark)
        self.write(add_remark)

class ExamHandler(BaseHandler):
    """
    对学员考试情况进行处理
    """
    @tornado.web.authenticated
    def get(self,cls_id,*args,**kwargs):
        stus,exams = utils_get.get_exam_class(self.dbsession,cls_id)
        self.render('exam.html',cls_id=cls_id,exams=exams,stus=stus)

    def post(self, *args, **kwargs):
        stuid = self.get_argument('stuid',None)
        self.write(utils_get.get_stu_score_all(self.dbsession,stuid))


class LevelHandler(BaseHandler):
    """
    对学员的班级进行调整
    升班(up):返回所有班级等级大于当前班级等级的班级
    降班(down):返回所有班级等于小于当前班级等级的班级
    留级(repeat):返回所有与当前班级等级形同的班级
    """
    @tornado.web.authenticated
    def get(self, type,stuid,*args, **kwargs):
        print(type,stuid)
        stu,res = utils_get.get_stu_class_level(self.dbsession,type,stuid)
        self.render('level.html',stu=stu,res=res)
    def post(self, *args, **kwargs):
        """
        将学员编号为stuid的学员设置为class_id的班级
        :param args:
        :param kwargs:
        :return:
        """
        stuid = self.get_argument('stuid',None)
        class_id = self.get_argument('class_id',None)
        utils_set.set_student_class(self.dbsession,stuid=stuid,class_id=class_id)
        self.write("1")

class AddScoreHandler(BaseHandler):
    """
    添加学员考试成绩
    """
    def post(self,cls_id,stu_id,*args, **kwargs):
        score = self.get_argument('score',None)
        examtime = self.get_argument('datetime',None)
        if score and examtime:
            utils_set.set_class_score(self.dbsession,stu_id,cls_id,score,examtime)
            self.write("True")
        else:
            self.write('Error')

class AddNewStudent(BaseHandler):
    """
    添加新学员
    """
    def post(self, *args, **kwargs):
        stuid = self.get_argument('stuid',None)
        name = self.get_argument('stuname',None)
        tel = self.get_argument('tel',None)
        qq = self.get_argument('qq',None)
        clss = self.get_argument('clss_id',None)
        if stuid and name and tel and qq and clss:
            utils_set.set_new_student(self.dbsession,stuid=stuid,name=name,tel=tel,qq=qq,cls_id=clss)
            self.write("Yes")
        else:
            self.write("Error")

