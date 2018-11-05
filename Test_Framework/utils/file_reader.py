#!/usr/bin/python3
# -*- coding:utf-8 -*-

import yaml
import os
from xlrd import open_workbook


class YamlReader:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("File not found!")
        self._data = None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, "rb") as f:
                self._data = list(yaml.safe_load_all(f))    # load后是个generator，用list组织成列表
        return self._data


class SheetTypeError(Exception):
    pass


class ExcelReader:
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError("excel not exist!")
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)     #首行为title
                for col in range(1, s.nrows):
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    self._data.append(s.row_values())
        return self._data


if __name__ == '__main__':
    y = 'E:\moving\GIT\Python\Test_Framework\config\config.yml'
    reader = YamlReader(y)
    print(reader.data)

    e = 'E:/moving/GIT/Python/Test_Framework/data/baidu百度.xlsx'
    reader = ExcelReader(e, title_line=True)
    print(reader.data)

