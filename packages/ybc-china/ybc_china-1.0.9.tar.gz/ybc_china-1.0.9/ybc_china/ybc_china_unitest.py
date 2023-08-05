import unittest
from ybc_china import *


class MyTestCase(unittest.TestCase):
    def test_chat_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用cities方法时，'proName'参数类型错误。$"):
            cities(1)

    def test_chat_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用cities方法时，'proName'参数不在允许范围内。$"):
            cities('北山')


if __name__ == '__main__':
    unittest.main()
