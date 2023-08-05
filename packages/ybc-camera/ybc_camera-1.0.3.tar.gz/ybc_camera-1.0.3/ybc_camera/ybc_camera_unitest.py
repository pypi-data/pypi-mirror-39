import unittest
from ybc_camera import *


class MyTestCase(unittest.TestCase):
    def test_camera(self):
        self.assertIsNotNone(camera("1.jpg"))

    def test_camera_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用camera方法时，'filename'参数类型错误。$"):
            camera(1)

    def test_camera_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用camera方法时，'filename'参数不在允许范围内。$"):
            camera('')


if __name__ == '__main__':
    unittest.main()
