import tornado.web

from .main import BaseHandler
from utils import utils_get


class LoginHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        islead,cls = utils_get.get_teacher(self.dbsession, name=self.current_user())
        self.render('login.html', islead=islead,clss=cls)

class LoginOutHandler(BaseHandler):
    """
    退出登录页面
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.session.delete('teacher')
        self.redirect(r'/')