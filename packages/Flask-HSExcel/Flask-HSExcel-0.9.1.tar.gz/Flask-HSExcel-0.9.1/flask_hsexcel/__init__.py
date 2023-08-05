import sys, os, logging
from .views import hs_excel
from celery import Celery
from .checker import ErrorChecker
from .utils import excel_no_to_db, excel_date_to_db

logger = logging.getLogger(__name__)


class HsExcel(object):

    def __init__(self, app=None, checker=None, celery=None):
        if app is not None:
            self.app = app
            self.checker = checker
            self.celery = celery
            # self.db = db
            self.init_app(app, checker, celery)
        else:
            self.app = None
            # self.db = None

    def init_app(self, app, checker, celery=None,sse=None):
        self.app = app
        self.checker = checker
        self.celery = celery
        excel_path = self.app.config.get('EXCEL_PATH')
        # 判断是否传入　excelpath
        if not excel_path:
            logger.error("EXCEL_PATH没有配置")
            sys.exit(0)
        # 判断checker是否正确
        if not isinstance(self.checker, dict):
            logger.error('checker不是一个dict')
            sys.exit(0)
        if isinstance(self.checker, dict):
            for value in self.checker.values():
                if not isinstance(value, type):
                    logger.error('checker配置错误')
                    sys.exit(0)
                if not issubclass(value, ErrorChecker):
                    logger.error('checker配置不正确')
                    sys.exit(0)
        if not sse:
            logger.error("没有注册see")
            sys.exit(0)
        # 注册路由
        self.app.register_blueprint(hs_excel, url_prefix='/hs_excel')
        # 注册see
        self.app.register_blueprint(sse, url_prefix='/stream')
    def make_celery(self):
        if self.celery:
            return self.celery
        celery = Celery(self.app.import_name, broker=self.app.config['CELERY_BROKER_URL'])
        celery.conf.update(self.app.config)
        return celery

    def print_test(self):

        # print('hhhh')
        return '这是插件里面的内容'


__all__ = [HsExcel, excel_date_to_db, excel_no_to_db]
