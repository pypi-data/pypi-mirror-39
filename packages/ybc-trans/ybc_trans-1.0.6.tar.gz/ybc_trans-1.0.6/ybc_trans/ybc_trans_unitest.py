import unittest
from ybc_trans import *
from ybc_exception import *


class MyTestCase(unittest.TestCase):
    def test_zh2en(self):
        self.assertEqual('test', zh2en('测试'))

    def test_en2zh(self):
        self.assertEqual('苹果', en2zh('apple'))

    def test_zh2en_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用zh2en方法时，'text'参数类型错误。$"):
            zh2en(1)

    def test_zh2en_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用zh2en方法时，text'参数不在允许范围内。$"):
            zh2en("")

    def test_en2zh_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用en2zh方法时，'text'参数类型错误。$"):
            en2zh(1)

    def test_en2zh_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用en2zh方法时，text'参数不在允许范围内。$"):
            en2zh("")


if __name__ == '__main__':
    unittest.main()
