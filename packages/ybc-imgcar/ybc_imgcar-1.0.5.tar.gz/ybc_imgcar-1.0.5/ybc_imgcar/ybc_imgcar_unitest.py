import unittest
from ybc_imgcar import *


class MyTestCase(unittest.TestCase):
    def test_car_recognition(self):
        self.assertEqual('阿斯顿马丁DBS', car_recognition('test.jpg'))

    def test_car_recogniton_erro(self):
        self.assertEqual('非车类', car_recognition('cup.jpg'))

    def test_car_recognition_typeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用car_recognition方法时，'filename'参数类型错误。$"):
            car_recognition(123)

    def test_car_recognition_valueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用car_recognition方法时，'filename'参数不在允许范围内。$"):
            car_recognition('')


if __name__ == '__main__':
    unittest.main()
