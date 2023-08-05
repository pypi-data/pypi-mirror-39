import requests
import ybc_config
from ybc_exception import *
import sys

__PREFIX = ybc_config.config['prefix']
__IDIOM_URL = __PREFIX + ybc_config.uri + '/bot'


def chat(text=''):
    error_msg = "'text'"
    if not isinstance(text, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    if text == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg=error_msg)
    try:
        data = {
            'text': text
        }
        url = __IDIOM_URL
        for i in range(3):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                res = r.json()
                if res['results'] and res['results'][0]['values']:
                    res = res['results'][0]['values']['text']
                    return res

        raise ConnectionError('获取机器人对话失败', r._content)

    except Exception as e:
        raise InternalError(e, 'ybc_bot')


def main():
    print(chat('你好呀,你叫什么名字'))


if __name__ == '__main__':
    main()
