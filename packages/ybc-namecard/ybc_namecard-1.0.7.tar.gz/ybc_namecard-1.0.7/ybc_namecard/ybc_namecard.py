import os
import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__NAMECARD_URL = __PREFIX + ybc_config.uri + '/nameCardOcr'

__RETURN_IMAGE = 0


def namecard_info(filename=''):
    """
    功能：名片识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：识别出的名片信息。
    """

    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    try:
        url = __NAMECARD_URL
        filepath = os.path.abspath(filename)
        fo = open(filepath, 'rb')
        files = {
            'file': fo
        }
        data = {
            'returnImage': __RETURN_IMAGE
        }

        for i in range(3):
            r = requests.post(url, files=files, data=data)
            if r.status_code == 200:
                res = r.json()
                # 识别不到名片不会通过该检查
                if 'result_list' in res and res['result_list'][0]['code'] == 0:
                    res_dict = {}
                    for val in res['result_list'][0]['data']:
                        res_dict[val['item']] = val['value']
                    fo.close()
                    return res_dict
                else:
                    fo.close()
                    return '图片中找不到名片哦~'
        fo.close()
        raise ConnectionError('识别身份证图片失败', r._content)

    except (ParameterTypeError, ParameterValueError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_namecard')


def main():
    res = namecard_info('test.jpg')
    print(res)


if __name__ == '__main__':
    main()
