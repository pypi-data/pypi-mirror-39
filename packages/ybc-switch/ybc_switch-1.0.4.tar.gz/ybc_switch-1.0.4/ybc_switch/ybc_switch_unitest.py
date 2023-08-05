import unittest
from ybc_switch import *


class MyTestCase(unittest.TestCase):
    def test_analysis(self):
        self.assertEqual('天气', analysis('1.mp3'))
        self.assertEqual('天气', analysis('tmp.wav'))

    def test_analysis_error(self):
        with self.assertRaises(InternalError):
            analysis('cup.jpg')

    def test_analysis_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用analysis方法时，'filename'参数类型错误。$"):
            analysis(123)

    def test_analysis_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用analysis方法时，'filename'参数不在允许范围内。$"):
            analysis('')


if __name__ == '__main__':
    unittest.main()
