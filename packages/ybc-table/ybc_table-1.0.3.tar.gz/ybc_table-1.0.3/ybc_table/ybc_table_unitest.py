import unittest
from ybc_table import *
from ybc_exception import *


class MyTestCase(unittest.TestCase):
    def test_table(self):
        s = '+---+---+---+\n| 1 | 2 | 3 |\n+---+---+---+\n| 4 | 5 | 6 |\n+---+---+---+'
        l = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(s, table(l))

    def test_table_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用table方法时，'table_type'参数不在允许范围内。$"):
            table([], '')

    def test_table_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用table方法时，'data'、'table_type'参数类型错误。$"):
            table('', 1)


if __name__ == '__main__':
    unittest.main()
