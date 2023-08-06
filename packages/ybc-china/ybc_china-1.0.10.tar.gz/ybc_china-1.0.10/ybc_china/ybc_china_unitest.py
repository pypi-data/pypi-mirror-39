import unittest
from ybc_china import *


class MyTestCase(unittest.TestCase):
    def test_all_cities(self):
        self.assertIsNotNone(all_cities())

    def test_provinces(self):
        self.assertIsNotNone(provinces())

    def test_cities(self):
        self.assertEqual(cities('湖南'), ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西土家族苗族自治州'])

    def test_chat_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用cities方法时，'proName'参数类型错误。$"):
            cities(1)

    def test_chat_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用cities方法时，'proName'参数不在允许范围内。$"):
            cities('北山')


if __name__ == '__main__':
    unittest.main()
