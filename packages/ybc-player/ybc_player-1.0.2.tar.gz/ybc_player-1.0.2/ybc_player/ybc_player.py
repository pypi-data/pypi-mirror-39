# coding=utf-8
import os
import sys
from ybc_exception import *


def play(filename=''):
    """
    功能：播放filename指定的音频、视频文件。

    参数 filename 是当前目录下期望播放的音频、视频文件的名字，

    返回：无。
    """
    error_msg = "'filename'"
    # 参数类型正确性判断
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)

    # 参数取值正确性判断
    if not filename:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        filepath = os.path.abspath(filename)
        os.system(filepath)
    except Exception as e:
        raise InternalError(e, 'ybc_player')


def main():
    play('test.wav')


if __name__ == '__main__':
    main()
