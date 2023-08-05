import unittest
from ybc_pminfo import *
from ybc_exception import *


class MyTestCase(unittest.TestCase):
    def test_pm25(self):
        self.assertIsNotNone(pm25('北京'))

    def test_pm25_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用pm25方法时，'city'参数类型错误。$"):
            pm25(1)

    def test_pm25_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用pm25方法时，'city'参数不在允许范围内。$"):
            pm25('abc')


if __name__ == '__main__':
    unittest.main()
