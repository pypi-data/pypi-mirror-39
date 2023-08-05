import re, os, time, random, xlrd, xlutils.copy, openpyxl, shutil, logging
from .utils import is_int
from datetime import datetime

logger = logging.getLogger()


class ErrorChecker(object):
    config = [
    ]
    no_repeat = []

    def __init__(self, id, error_path, param):
        from .models import get_session, ExcelModel
        db_session = get_session()
        self.db_session = db_session
        excel = db_session.query(ExcelModel).filter(ExcelModel.excel_id == id).first()
        self.excel = excel
        self.error_path = error_path
        self.param = param

    @staticmethod
    def key_handle(key):
        return re.sub(r'\s', '_', key).lower()

    def check(self, row_dict, index):
        configs = self.config
        error_list = []
        for config in configs:
            method = config[1]
            error = self.__getattribute__(method)(name=config[0], error_str=config[2],
                                                  row_dict=row_dict, index=index)
            if error:
                if isinstance(error, list):
                    error_list.extend(error)
                else:
                    error_list.append(error)
        return error_list

    def check_date(self, name, error_str, row_dict, index):
        key = self.key_handle(name)
        _date = row_dict.get(key)
        # print(_date)
        if isinstance(_date, str):
            try:
                a = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')
                return None
            except Exception as e:
                return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)
        elif isinstance(_date, float) and len(str(_date)) == 7:
            return None
        elif isinstance(_date, datetime):
            return None
        else:
            return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)

    def check_datetime(self, name, error_str, row_dict, index):
        key = self.key_handle(name)
        _datetime = row_dict.get(key)
        if isinstance(_datetime, str):
            try:
                datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S')
                return None
            except:
                return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)
        elif isinstance(_datetime, float) and len(str(_datetime)) == 17:
            return None
        elif isinstance(_datetime, datetime):
            return None
        else:
            return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)

    def check_float(self, name, error_str, row_dict, index):
        key = self.key_handle(name)
        _float = row_dict.get(key)
        if isinstance(_float, float):
            return None
        else:
            return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)

    def float2decimal(self, name, error_str, row_dict, index):
        key = self.key_handle(name)
        _float = row_dict.get(key)
        if isinstance(_float, (float, int)):
            row_dict[key] = round(float(_float), 4)
            return None
        else:
            return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)

    def check_str(self, name, error_str, row_dict, index):
        key = self.key_handle(name)
        _str = row_dict.get(key)
        if isinstance(_str, str):
            if _str.strip():
                return None
            else:
                return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)
        elif _str is None:
            return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)
        else:
            return None

    def check_int(self, name, error_str, row_dict, index):
        key = self.key_handle(name)
        num = row_dict.get(key)
        if is_int(num):
            return None
        return '第{index}行{name}{error_str}'.format(index=index, name=name, error_str=error_str)

    def as_json(self, sse, task_id):
        """考虑xls和xlsx的不同"""
        path = self.excel.path
        # print(path)
        no_repeat_keys = self.no_repeat_list()
        flag_dict = dict()
        if path.split('.')[2] == 'xls':
            excel_open = xlrd.open_workbook(path)
            table = excel_open.sheet_by_index(0)
            rows = table.nrows
            old_excel_title = table.row_values(1)
            excel_title = []
            for title in old_excel_title:
                real_title = self.key_handle(title)
                excel_title.append(real_title)
            json_list = []
            for i in range(2, rows):
                row_dict = dict(zip(excel_title, table.row_values(i)))
                row_dict['error'] = self.check(row_dict, i + 1)
                row_dict['is_use'] = '0'
                row_dict['row'] = i + 1
                for key_list in no_repeat_keys:
                    flag = ''
                    for key in key_list:
                        flag = flag + str(row_dict.get(key))
                    if (flag not in flag_dict) and (not flag == ''):
                        flag_dict[flag] = row_dict
                    else:
                        # flag_dict[flag]['error'].append("第{a}行与第{b}行数据重复".format(a=flag_dict[flag]['row'], b=i + 1))
                        row_dict['error'].append("第{b}行与第{a}行数据重复".format(a=flag_dict[flag]['row'], b=i + 1))
                json_list.append(row_dict)
                sse.publish(data={"data":
                                      {"now": i, "total": rows,"excel_name":self.excel.name},
                                  "type": {"name": "excel",
                                           "step": "as_json",
                                           "id": self.excel.excel_id,
                                           "status": "pending",
                                           "type":self.excel.excel_type
                                           }},
                            type=self.excel.excel_type,
                            id=task_id)

        else:
            excel_open = openpyxl.load_workbook(path)
            sheets = excel_open.sheetnames
            sheet0 = sheets[0]
            table = excel_open[sheet0]
            rows = table.rows
            # print(next(rows))
            old_excel_title = [col.value for col in list(rows)[1]]
            excel_title = []
            for title in old_excel_title:
                real_title = self.key_handle(title)
                excel_title.append(real_title)
            json_list = []
            i = 0
            rows = table.rows
            for row in rows:
                i = i + 1
                if i <= 2:
                    continue
                row_value = [col.value for col in row]
                row_dict = dict(zip(excel_title, row_value))  # []
                row_dict['error'] = self.check(row_dict, i)
                row_dict['is_use'] = '0'
                row_dict['row'] = i + 1
                for key_list in no_repeat_keys:
                    flag = ''
                    for key in key_list:
                        flag = flag + str(row_dict.get(key))
                    if (flag not in flag_dict) and (not flag == ''):
                        flag_dict[flag] = row_dict
                    else:
                        # flag_dict[flag]['error'].append("第{a}行与第{b}行数据重复".format(a=flag_dict[flag]['row'], b=i + 1))
                        row_dict['error'].append("第{b}行与第{a}行数据重复".format(a=flag_dict[flag]['row'], b=i + 1))
                json_list.append(row_dict)
                sse.publish(data={"data":
                                      {"now": i, "total": rows,"excel_name":self.excel.name},
                                  "type": {"name": "excel",
                                           "step": "as_json",
                                           "id": self.excel.excel_id,
                                           "status": "pending",
                                           "type": self.excel.excel_type
                                           }},
                            type=self.excel.excel_type,
                            id=task_id)
        # json_str = json.dumps(json_list, default=json_serial, ensure_ascii=False)
        self.excel.content = json_list
        self.excel.status = 1
        self.db_session.flush()

    def add_error(self, sse, task_id):
        path = self.excel.path
        time_str = str(time.time())
        random_str = str(random.randint(1, 10000))
        if path.split('.')[2] == 'xls':
            file_save_name = time_str + random_str + '.xls'
            real_path = os.path.join(self.error_path, file_save_name)
            shutil.copyfile(path, real_path)
            rb = xlrd.open_workbook(real_path, formatting_info=True)
            wb = xlutils.copy.copy(rb)
            sheet = rb.sheet_by_index(0)
            cols = sheet.ncols
            write_sheet = wb.get_sheet(0)
            write_sheet.write(0, cols, 'ERROR')
            contents = self.excel.content
            rows = len(contents)
            for i, content in enumerate(contents):
                write_sheet.write(i + 2, cols, str(content.get('error'))[1:-1])
                sse.publish(data={"data":
                                      {"now": i, "total":rows ,"excel_name":self.excel.name},
                                  "type": {"name": "excel",
                                           "step": "add_error",
                                           "id": self.excel.excel_id,
                                           "status": "pending",
                                           "type": self.excel.excel_type

                                           }},
                            type=self.excel.excel_type,
                            id=task_id)
        else:
            file_save_name = time_str + random_str + '.xlsx'
            real_path = os.path.join(self.error_path, file_save_name)
            shutil.copyfile(path, real_path)
            wb = openpyxl.load_workbook(real_path)
            sheets = wb.sheetnames
            sheet0 = sheets[0]
            table = wb[sheet0]
            cols = len(list(table.columns))
            table.cell(row=1, column=cols + 1).value = 'Error'
            contents = self.excel.content
            rows = len(contents)
            for i, content in enumerate(contents):
                table.cell(row=i + 3, column=cols + 1).value = str(content.get('error'))[1:-1]
                sse.publish(data={"data":
                                      {"now": i, "total":rows ,"excel_name":self.excel.name},
                                  "type": {"name": "excel",
                                           "step": "add_error",
                                           "id": self.excel.excel_id,
                                           "status": "pending",
                                           "type": self.excel.excel_type

                                           }},
                            type=self.excel.excel_type,
                            id=task_id)
        wb.save(real_path)
        self.excel.error_path = real_path
        self.excel.status = 2
        self.db_session.flush()

    # 要校验行数据之间的唯一性

    def no_repeat_list(self):
        res = []
        for i in self.no_repeat:
            _list = []
            for key in i:
                key = self.key_handle(key)
                _list.append(key)
            res.append(_list)
        return res

    def start(self, sse=None, task_id=None):
        try:
            self.as_json(sse, task_id)
            sse.publish(data={"data":
                                  {"now": 100, "total": 100, "excel_name": self.excel.name},
                              "type": {"name": "excel",
                                       "step": "as_json",
                                       "id": self.excel.excel_id,
                                       "status": "success",
                                       "type": self.excel.excel_type
                                       }},
                        type=self.excel.excel_type,
                        id=task_id)

            self.add_error(sse, task_id)
            sse.publish(data={"data":
                                  {"now": 100, "total": 100, "excel_name": self.excel.name},
                              "type": {"name": "excel",
                                       "step": "add_error",
                                       "id": self.excel.excel_id,
                                       "status": "success",
                                       "type": self.excel.excel_type
                                       }},
                        type=self.excel.excel_type,
                        id=task_id)
        except Exception as e:
            logger.error(str(e))
            sse.publish(data={"data":
                                  {"now": 0, "total": 0, "excel_name": self.excel.name},
                              "type": {"name": "excel",
                                       "step": "failure",
                                       "id": self.excel.excel_id,
                                       "status": "failure",
                                       "type": self.excel.excel_type
                                       }},
                        type=self.excel.excel_type,
                        id=task_id)
            self.excel.status = 3
            self.db_session.flush()
