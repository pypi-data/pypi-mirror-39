import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__TEL_URL = __PREFIX + ybc_config.uri + '/tel'


def detail(tel=''):
    """
    功能：手机号码归属地信息查询

    参数：tel: 手机号码

    返回：手机号码归属地信息
    """
    if not (isinstance(tel, str) or isinstance(tel, int)):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'tel'")
    if isinstance(tel, str) and (tel == '' or not tel.isdigit() or tel.__len__() != 11):
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'tel'")
    if isinstance(tel, int) and tel > 0 and str(tel).__len__() != 11:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'tel'")

    try:
        url = __TEL_URL
        data = {
            'phone': tel
        }

        for i in range(3):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                res = r.json()['result']
                if res:
                    res_info = {
                        'province': res['province'],
                        'city': res['city'],
                        'company': res['company'],
                        'shouji': tel
                    }
                    return res_info
                else:
                    raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'tel'")

        raise ConnectionError('获取翻译结果失败', r._content)
    except (ParameterTypeError, ParameterValueError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_tel')


def main():
    print(detail('18635579617'))
    print(detail(18635579617))


if __name__ == '__main__':
    main()
