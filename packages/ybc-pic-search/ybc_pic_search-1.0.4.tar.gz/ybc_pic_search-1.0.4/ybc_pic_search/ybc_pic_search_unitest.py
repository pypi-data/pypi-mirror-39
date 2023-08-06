import unittest
from .ybc_pic_search import *


class MyTestCase(unittest.TestCase):
    def test_pic_search(self):
        self.assertEqual(0, pic_search('彭于晏'))

    def test_pic_search_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用pic_search方法时，'keyword'、'total'参数类型错误。$"):
            pic_search(123, '')

    def test_pic_search_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用pic_search方法时，'keyword'、'total'参数不在允许范围内。$"):
            pic_search('', 50)


if __name__ == '__main__':
    unittest.main()
