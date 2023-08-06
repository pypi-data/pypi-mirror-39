import unittest
from ybc_idiom import *


class MyTestCase(unittest.TestCase):
    def test_search(self):
        self.assertIsNotNone(search('一'))

    def test_meaning(self):
        self.assertIsNotNone(meaning('为所欲为'))

    def test_search_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用search方法时，'keyword'参数类型错误。$"):
            search(123)

    def test_meaning_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用meaning方法时，'keyword'参数类型错误。$"):
            meaning(123)

    def test_search_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用search方法时，'keyword'参数不在允许范围内。$"):
            search('')

    def test_meaning_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用meaning方法时，'keyword'参数不在允许范围内。$"):
            meaning('')

    def test_meaning_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用meaning方法时，'keyword'参数不在允许范围内。$"):
            meaning('dsafsda')


if __name__ == '__main__':
    unittest.main()
