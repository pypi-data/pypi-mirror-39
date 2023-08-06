import unittest
from ybc_player import *


class MyTestCase(unittest.TestCase):
    def test_play(self):
        play('test.wav')

    def test_play_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用play方法时，'filename'参数类型错误。$"):
            play(1)

    def test_play_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用play方法时，'filename'参数不在允许范围内。$"):
            play('')


if __name__ == '__main__':
    unittest.main()