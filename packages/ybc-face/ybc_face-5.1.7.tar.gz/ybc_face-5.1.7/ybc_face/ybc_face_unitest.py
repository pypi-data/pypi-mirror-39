import unittest
from ybc_face import *


class MyTestCase(unittest.TestCase):
    def test_gender(self):
        self.assertEqual('男', gender('test.jpg'))

    def test_glass(self):
        self.assertEqual(False, glass('test.jpg'))

    def test_info(self):
        self.assertIsNotNone(info('test.jpg'))

    def test_info_all(self):
        self.assertIsNotNone(info_all('three.jpg'))

    def test_ps(self):
        self.assertIsNotNone(ps('test.jpg'))

    def test_mofa(self):
        self.assertIsNotNone(mofa('test.jpg'))

    def test_gender_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用gender方法时，'filename'参数类型错误。$"):
            gender(123)

    def test_glass_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用glass方法时，'filename'参数类型错误。$"):
            glass(123)

    def test_info_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用info方法时，'filename'参数类型错误。$"):
            info(123)

    def test_info_all_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用info_all方法时，'filename'参数类型错误。$"):
            info_all(123)

    def test_ps_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用ps方法时，'filename'参数类型错误。$"):
            ps(123)

    def test_mofa_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用mofa方法时，'filename'参数类型错误。$"):
            mofa(123)

    def test_gender_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用gender方法时，'filename'参数不在允许范围内。$"):
            gender('')

    def test_glass_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用glass方法时，'filename'参数不在允许范围内。$"):
            glass('')

    def test_info_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用info方法时，'filename'参数不在允许范围内。$"):
            info('')

    def test_info_all_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用info_all方法时，'filename'参数不在允许范围内。$"):
            info_all('')

    def test_ps_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用ps方法时，'filename'参数不在允许范围内。$"):
            ps('')

    def test_mofa_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用mofa方法时，'filename'参数不在允许范围内。$"):
            mofa('')

    def test_info_error(self):
        self.assertEqual('图片中找不到人哦~', info('cup.jpg'))

    def test_info_png(self):
        self.assertEqual('图片中找不到人哦~', info('rgba.png'))

    def test_ps_error(self):
        self.assertEqual('图片中找不到人哦~', ps('cup.jpg'))

    def test_mofa_error(self):
        self.assertEqual('图片中找不到人哦~', mofa('cup.jpg'))


if __name__ == '__main__':
    unittest.main()
