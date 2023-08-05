import unittest
from ybc_namecard import *


class MyTestCase(unittest.TestCase):
    def test_namecard_info(self):
        res = {'姓名': '何山', '职位': '研发总监', '地址': '0北京市朝阳区望京利星行中心A座F区6层', '邮箱': 'heshan@fenbi.com', '手机': '18635579617'}
        self.assertEqual(res, namecard_info('test.jpg'))

    def test_namecard_info_error(self):
        self.assertEqual('图片中找不到名片哦~', namecard_info('cup.jpg'))

    def test_namecard_info_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用namecard_info方法时，'filename'参数类型错误。$"):
            namecard_info(123)

    def test_namecard_info_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用namecard_info方法时，'filename'参数不在允许范围内。$"):
            namecard_info('')


if __name__ == '__main__':
    unittest.main()
