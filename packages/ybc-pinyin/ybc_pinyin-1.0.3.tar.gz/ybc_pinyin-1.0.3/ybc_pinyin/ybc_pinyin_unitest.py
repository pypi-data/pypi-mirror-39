import unittest
from ybc_pinyin import *


class MyTestCase(unittest.TestCase):
    def test_pin(self):
        self.assertEqual('nǐ-hǎo', pin('你好'))

    def test_pin1(self):
        self.assertEqual('ni-hao', pin1('你好'))

    def test_pin(self):
        self.assertEqual('chē-jū', duoyin('车'))

    # 带注音的拼音
    def test_pin_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用pin方法时，'text'参数类型错误。$"):
            pin(1)

    def test_pin_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用pin方法时，'text'参数不在允许范围内。$"):
            pin('')

    # 不带注音的拼音
    def test_pin1_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用pin1方法时，'text'参数类型错误。$"):
            pin1(1)

    def test_pin1_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用pin1方法时，'text'参数不在允许范围内。$"):
            pin1('')

    # 该汉字所有带注音的拼音
    def test_duoyin_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用duoyin方法时，'text'参数类型错误。$"):
            duoyin(1)

    def test_duoyin_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用duoyin方法时，'text'参数不在允许范围内。$"):
            duoyin('你好')


if __name__ == '__main__':
    unittest.main()
