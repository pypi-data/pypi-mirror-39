import terminaltables as tt
import sys
from ybc_exception import *


def table(data, table_type='ascii'):
    """
    功能：返回 Ascii Table 字符格式的表格

    参数：
        data: 要转换的数据（二维列表）
        table_type: 可以指定的转换类型 ['ascii', 'single', 'double', 'github']

    返回: 表格形式的字符串
    """
    err_msg = str()
    err_flag = 1
    if not isinstance(data, list):
        err_flag = -1
        err_msg = "'data'"
    if not isinstance(table_type, str):
        if err_flag == -1:
            err_msg += "、'table_type'"
        else:
            err_flag = -1
            err_msg = "'table_type'"
    if err_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=err_msg)

    type_list = ['ascii', 'single', 'double', 'github']
    if table_type not in type_list:
        err_msg = "'table_type'"
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=err_msg)

    try:
        if table_type == 'ascii':
            t = tt.AsciiTable(data)
        elif table_type == 'single':
            t = tt.SingleTable(data)
        elif table_type == 'double':
            t = tt.DoubleTable(data)
        elif table_type == 'github':
            t = tt.GithubFlavoredMarkdownTable(data)

        return t.table
    except Exception as e:
        raise InternalError(e, 'ybc_table')


def main():
    data = [[1, 2, 3], [4, 5, 6]]
    print(table(data, 'ascii'))
    print(table(data, 'single'))
    print(table(data, 'double'))
    print(table(data, 'github'))


if __name__ == '__main__':
    main()
