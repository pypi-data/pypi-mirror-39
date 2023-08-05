import unittest
from ybc_tel import *
from ybc_exception import *


class MyTestCase(unittest.TestCase):
    def test_detail_str(self):
        self.assertEqual({'province': '山西', 'city': '太原', 'company': '联通', 'shouji': '18635579617'}, detail('18635579617'))

    def test_detail_int(self):
        self.assertEqual({'province': '山西', 'city': '太原', 'company': '联通', 'shouji': 18635579617}, detail(18635579617))

    def test_detail_exType(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用detail方法时，'tel'参数类型错误。$"):
            detail([])

    def test_detail_exValue(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用detail方法时，'tel'参数不在允许范围内。$"):
            detail('123456789797946')


if __name__ == '__main__':
    unittest.main()
