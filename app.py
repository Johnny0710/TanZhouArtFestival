import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define,options


from handlers import main,auth

define('port',default=9999, help='Default Run Port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',main.IndexHandler),
            (r'/login',auth.LoginHandler),
            (r'/cls/(?P<cls_id>[\d\D]+)',main.StuHandler),
            (r'/stu',main.StuHandler),
            (r'/loginout',auth.LoginOutHandler),
            (r'/attendance/(?P<cls_id>[\d\D]+)',main.AttendanceHandler),
            (r'/homework/(?P<cls_id>[\d\D]+)',main.HomeWorkHandler),
            (r'/inspect/(?P<workid>[\d\D]+)',main.InspectHandler),
            (r'/exam/(?P<cls_id>[\d\D]+)',main.ExamHandler),
            (r'/level/(?P<type>[\d\D]+)/(?P<stuid>[\d\D]+)',main.LevelHandler),
            (r'/addscore/(?P<cls_id>[\d\D]+)/(?P<stu_id>[\d\D]+)',main.AddScoreHandler),
            (r'/addstu',main.AddNewStudent),

        ]
        setting = dict(
            template_path = 'templates',
            static_path = 'statics',
            debug = True,
            cookie_secret = 'dhjakhdjklsahdjklashdkjlasd',
            login_url = '/',
            pycket = {
                'engine':'redis',
                'storage':{
                    'host': 'localhost',
                    'port': '6379',
                    'db_sessions': 5,
                    'db_notifications': 11,
                    'max_connections': 2 ** 31,
                },
                'cookie':{
                    'expires_days': 30
                }
            }
        )
        super().__init__(handlers,**setting)

application = Application()

if __name__ == '__main__':
    options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()