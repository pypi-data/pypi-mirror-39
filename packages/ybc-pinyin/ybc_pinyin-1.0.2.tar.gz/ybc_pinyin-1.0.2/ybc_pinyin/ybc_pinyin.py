from pypinyin import pinyin, lazy_pinyin
from ybc_exception import *
import sys


def pin(text):
    """
    功能：获取汉字对应的带注音的拼音。

    参数：一个或多个汉字

    返回：带注音的拼音
    """
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")
    if not text:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")

    try:
        res_list = pinyin(text)
        res = []
        for s in res_list:
            res.append(s[0])
        return '-'.join(res)
    except Exception as e:
        raise InternalError(e, 'ybc_pinyin')


def pin1(text):
    """
    功能：获取汉字对应的不带注音的拼音。

    参数：一个或多个汉字

    返回：不带注音的拼音
    """
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")
    if not text:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")

    try:
        return '-'.join(lazy_pinyin(text))
    except Exception as e:
        raise InternalError(e, 'ybc_pinyin')


def duoyin(text):
    """
    功能：得到多音字。

    参数：一个汉字

    返回：该汉字所有带注音的拼音
    """
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")
    if len(text) != 1:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")

    try:
        res = pinyin(text, heteronym=True)
        res_list = []
        for s in res[0]:
            res_list.append(s)
        return '-'.join(res_list)
    except Exception as e:
        raise InternalError(e, 'ybc_pinyin')


def main():
    print(pin('你好'))
    print(pin1('你好'))
    print(duoyin('车'))


if __name__ == '__main__':
    main()
