from app import hsexcel
from app import checker
from app import sse
from .checker import ErrorChecker

celery = hsexcel.make_celery()


def get_checker(excel_type):
    return checker.get(excel_type, ErrorChecker)


@celery.task
def check_error(id=None, param=None, error_path=None):
    excel_type = param.get('excel_type')[0]
    Checker = get_checker(excel_type)
    checker = Checker(id, error_path, param)
    task_id = check_error.request.id
    checker.start(sse,task_id)
    return 'success'

def check(id=None, param=None, error_path=None):
    excel_type = param.get('excel_type')[0]
    Checker = get_checker(excel_type)
    checker = Checker(id, error_path, param)
    checker.start()
    return 'success'