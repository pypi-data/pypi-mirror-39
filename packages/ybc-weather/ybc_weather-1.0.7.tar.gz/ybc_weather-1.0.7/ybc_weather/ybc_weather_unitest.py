import unittest
from ybc_weather import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test1 = today('北京')
        test2 = today('北京')
        self.assertEqual(test1, test2)

    def test_todayy_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用today方法时，'cityname'参数类型错误。$"):
            today(1)

    def test_today_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用today方法时，'cityname'参数不在允许范围内。$"):
            today('')

    def test_week_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用week方法时，'cityname'参数类型错误。$"):
            week(1)

    def test_week_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用week方法时，'cityname'参数不在允许范围内。$"):
            week('')


if __name__ == '__main__':
    unittest.main()