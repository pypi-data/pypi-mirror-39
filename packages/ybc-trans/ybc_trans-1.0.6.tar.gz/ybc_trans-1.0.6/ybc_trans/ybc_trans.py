import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__TRANSLATE_URL = __PREFIX + ybc_config.uri + '/translate'

__CHINESE = 'zh-CHS'
__ENGLISH = 'EN'


def en2zh(text=''):
    """
    功能：英译中接口

    参数：text: 要翻译的英文

    返回：翻译结果
    """
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")
    if text == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="text'")

    try:
        return translate(text, __ENGLISH, __CHINESE)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_trans')


def zh2en(text=''):
    """
    功能：中译英接口

    参数：text: 要翻译的中文

    返回：翻译结果
    """
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'text'")
    if text == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="text'")

    try:
        return translate(text, __CHINESE, __ENGLISH)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_trans')


def translate(text='', _from='', _to=''):
    """
    功能：翻译接口

    参数:
        text: 要翻译的文本
        _from: 源语言
        _to: 目标语言

    返回：翻译结果
    """
    err_msg = str()
    err_flag = 1
    if not isinstance(text, str):
        err_msg = "'text'"
        err_flag = -1
    if not isinstance(_from, str):
        if err_flag == -1:
            err_msg += "、'_from'"
        else:
            err_flag = -1
            err_msg = "'_from'"
    if not isinstance(_to, str):
        if err_flag == -1:
            err_msg += "、'_to'"
        else:
            err_flag = -1
            err_msg = "'_to'"
    if err_flag == -1:
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=err_msg)

    if text == '':
        err_flag = -1
        err_msg = "'text'"
    if _from == '':
        if err_flag == -1:
            err_msg += "、'_from'"
        else:
            err_flag = -1
            err_msg = "'_from'"
    if _to == '':
        if err_flag == -1:
            err_msg += "、'_to'"
        else:
            err_flag = -1
            err_msg = "'_to'"
    if err_flag == -1:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=err_msg)

    try:
        if text == '':
            return -1

        data = {
            'q': text,
            'from': _from,
            'to': _to
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        url = __TRANSLATE_URL

        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                res = r.json()
                if res['errorCode'] == "0" and res['translation']:
                    return res['translation'][0]
                else:
                    return "翻译结果获取失败"

        raise ConnectionError('获取翻译结果失败', r._content)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_trans')


def main():
    print(zh2en('苹果'))
    print(en2zh('test'))


if __name__ == '__main__':
    main()
