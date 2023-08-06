import unittest
from ybc_poetry import *


class MyTestCase(unittest.TestCase):
    def test_shici(self):
        content = '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不尽，轻舟已过万重山。'
        self.assertEqual(content, shici('早发白帝城', '李白'))

    def test_shici_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用shici方法时，'title'、'author'参数类型错误。$"):
            shici(1, 3)

    def test_shici_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用shici方法时，'title'、'author'参数不在允许范围内。$"):
            shici('', '')


if __name__ == '__main__':
    unittest.main()
