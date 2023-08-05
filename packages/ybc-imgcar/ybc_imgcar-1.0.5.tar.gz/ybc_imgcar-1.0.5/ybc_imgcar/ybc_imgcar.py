import os
import requests
import ybc_config
import sys
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__CAR_URL = __PREFIX + ybc_config.uri + '/carRecognition'


__TOP_NUM = 3


def car_recognition(filename='', topNum=__TOP_NUM):
    """
    功能：识别一个车辆图片的车型。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：识别出的车型信息。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(topNum, int):
        if error_flag == -1:
            error_msg += "、'topNum'"
        else:
            error_flag = -1
            error_msg += "'topNum'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if topNum < 1 or topNum > 10:
        if error_flag == -1:
            error_msg += "、'topNum'"
        else:
            error_flag = -1
            error_msg += "'topNum'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        url = __CAR_URL
        filepath = os.path.abspath(filename)
        fo = open(filepath, 'rb')
        files = {
            'file': fo
        }
        data = {
            'topNum': topNum
        }

        for i in range(3):
            r = requests.post(url, files=files, data=data)
            if r.status_code == 200:
                res = r.json()
                # 识别不到车辆时也有该字段返回，返回结果为 "非车类"
                if res['result']:
                    fo.close()
                    return res['result'][0]['name']
        fo.close()
        raise ConnectionError('识别车辆图片失败', r._content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_imgcar')


def main():
    print(car_recognition('test.jpg'))


if __name__ == '__main__':
    main()
