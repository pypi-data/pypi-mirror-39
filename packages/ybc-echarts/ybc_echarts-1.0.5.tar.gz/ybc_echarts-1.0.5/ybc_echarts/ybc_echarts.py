# coding=utf-8
from pyecharts import Geo as GetGeo
from ybc_exception import *
import sys


class Geo(GetGeo):
    def __init__(self, title="", subtitle="", **kwargs):
        error_flag = 1
        error_msg = ""
        if not isinstance(title, str):
            error_flag = -1
            error_msg += "'title'"
        if not isinstance(subtitle, str):
            if error_flag == -1:
                error_msg += "、'subtitle'"
            else:
                error_flag = -1
                error_msg += "'subtitle'"
        if error_flag == -1:
            raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)
        try:
            super().__init__(title, subtitle, **kwargs)
        except Exception as e:
            raise InternalError(e, 'ybc_echarts')

    def add(self, *args, **kwargs):
        try:
            self.__add('',*args, **kwargs)
        except Exception as e:
            raise InternalError(e, 'ybc_echarts')