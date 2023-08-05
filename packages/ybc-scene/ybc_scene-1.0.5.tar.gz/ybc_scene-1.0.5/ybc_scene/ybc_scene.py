import requests
import os
import math
import sys
import ybc_config
from ybc_exception import *

__PREFIX = ybc_config.config['prefix']
__SCENE_URL = __PREFIX + ybc_config.uri + '/sceneRecognition'
__OBJECT_URL = __PREFIX + ybc_config.uri + '/objectRecognition'


def scene_recog(filename=''):
    """
    功能：场景识别。

    参数：filename: 待识别图片文件。

    返回：识别结果及置信度字典组成的列表。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")
    if filename == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")

    try:
        url = __SCENE_URL
        return _imageRecognition(filename, url)
    except (ParameterTypeError, ParameterValueError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_scene')


def object_recog(filename=''):
    """
    功能：物体识别

    参数：filename: 待识别图片文件

    返回：识别结果及置信度字典组成的列表
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")
    if filename == '':
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")

    try:
        url = __OBJECT_URL
        return _imageRecognition(filename, url)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_scene')


def _imageRecognition(filename='', url=''):
    if not filename:
        raise ParameterValueError(function_name=sys._getframe().f_code.co_name, error_msg="'filename'")

    filepath = os.path.abspath(filename)
    files = dict()
    with open(filepath, 'rb') as f:
        files['file'] = f.read()

    for i in range(3):
        r = requests.post(url, files=files)
        if r.status_code == 200:
            res = r.json()
            if res['errno'] == 0 and res['tags']:
                res_list = []
                sum = 0
                for val in res['tags']:
                    res_list.append({'label_id': val['value'],
                                     'label_confd': val['confidence']})
                    sum += val['confidence']
                for val in res_list:
                    val['label_confd'] = str(math.floor(val['label_confd']/sum * 100)) + '%'

                return res_list
            else:
                return "图片中未识别到场景或物体"

    raise ConnectionError('识别物体或场景信息失败', r._content)


def main():
    res = object_recog('test.jpg')
    print(res)
    res = scene_recog('test.jpg')
    print(res)


if __name__ == '__main__':
    main()
