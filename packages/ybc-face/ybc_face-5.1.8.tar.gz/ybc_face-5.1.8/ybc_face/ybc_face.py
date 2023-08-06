import base64
import os
import tempfile
import requests
import time
from PIL import Image
import ybc_config
from ybc_exception import *
import sys

__BASIC_URL = ybc_config.config['prefix'] + ybc_config.uri
__FACE_URL = __BASIC_URL + '/faceDetect'
__MERGE_URL = __BASIC_URL + "/faceMerge/base64"

__MODE = 1


def _resize_img(file_path, temp_file=None):
    """
    对图片进行缩放, 如果是临时图片文件, 则必须传文件对象,
    因为在 windows 系统下 NamedTemporaryFile 不能二次打开, 但是可以直接读写

    :param file_path: 原文件路径
    :param temp_file: 临时文件对象
    :return:
        如果传入临时文件对象, 返回临时文件路径, 否则返回原文件路径
    """
    try:
        im = Image.open(file_path)
        src_w = im.size[0]
        src_h = im.size[1]
        dst_w = 500
        dst_h = (src_h / src_w) * 500
        dst_size = dst_w, dst_h

        im.thumbnail(dst_size)
        if temp_file:
            im.save(temp_file)
            temp_file.seek(0)
            return temp_file.name
        else:
            im.save(file_path)
            return file_path
    except Exception as e:
        raise InternalError(e, 'ybc_face')


def _get_info(filename='', mode=__MODE):
    """
    功能: 对图片进行人脸检测

    :param filename: 图片名
    :param mode: 检测模式: 0 - 所有人脸; 1 - 最大人脸
    :return:
        成功: 返回包含人脸信息的字典
        失败: -1
    """
    try:
        url = __FACE_URL
        file_path = os.path.abspath(filename)
        # 为了检测 file_path 参数是否合法，不合法抛出异常
        f = open(file_path)
        f.close()
        basename, suffix = os.path.splitext(filename)
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        _resize_img(file_path, temp_file)

        data = {
            'mode': mode
        }
        files = {
            'file': temp_file
        }

        for i in range(3):
            r = requests.post(url, data=data, files=files)

            if r.status_code == 200:
                res = r.json()
                # 识别到人脸时才有该字段
                if res['code'] == 0 and res['data']:
                    if mode == 1:
                        res = res['data']['face'][0]
                        res_dict = {
                            'age': res['age'],
                            'gender': res['gender'],
                            'beauty': res['beauty'],
                            'glass': res['glass']
                        }
                        temp_file.close()
                        return res_dict
                    else:
                        return res['data']['face']
                # 识别不到人脸时返回 -1 作为其调用函数的判断依据
                else:
                    return -1
        temp_file.close()
        raise ConnectionError("获取人脸信息失败", r.content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face')


def gender1(filename=''):
    """
    功能：识别人脸图片的性别信息。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的性别信息[0(女性)~100(男性)]。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['gender']


def gender(filename=''):
    """
    功能：识别人脸图片的性别。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的性别。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return '男' if res['gender'] > 90 else '女'


def age(filename=''):
    """
    功能：识别人脸图片的年龄信息。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的年龄信息[0~100]。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['age']


def glass1(filename=''):
    """
    功能：识别人脸图片的是否戴眼镜。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的是否戴眼镜 [true,false]。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return bool(res['glass'])


def glass(filename=''):
    """
    功能：识别人脸图片的是否戴眼镜。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的是否戴眼镜。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['glass']


def beauty(filename=''):
    """
    功能：识别人脸图片的魅力值。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的魅力值 [0~100]。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['beauty']


def info(filename=''):
    """
    功能：识别图片中一张人脸信息。

    参数 filename 是待识别的人脸图片，

    返回：识别出的人脸信息。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename, 1)
    if res == -1:
        return '图片中找不到人哦~'

    _gender = '男性' if res['gender'] >= 50 else '女性'
    _glass = '戴' if res['glass'] else '不戴'
    res_str = '{gender}，{age}岁左右，{glass}眼镜，颜值打分：{beauty}分'.format(
        gender=_gender, age=res['age'], glass=_glass, beauty=res['beauty'])

    return res_str


def info_all(filename=''):
    """
    功能：识别图片中所有人脸信息。

    参数 filename 是待识别的图片，

    返回：识别出的所有人脸信息。
    """
    if not isinstance(filename, str):
        raise ParameterTypeError(sys._getframe().f_code.co_name, "'filename'")
    if not filename:
        raise ParameterValueError(sys._getframe().f_code.co_name, "'filename'")

    res = _get_info(filename, 0)
    if res == -1:
        return '图片中找不到人哦~'

    res_str = '图片中总共发现{face_len}张人脸：'.format(face_len=len(res)) + os.linesep
    i = 1
    for val in res:
        _gender = '男性' if val['gender'] >= 50 else '女性'
        _glass = '戴' if val['glass'] else '不戴'
        res_str += '第{i}个人脸信息：{gender}，{age}岁左右，{glass}眼镜，颜值打分：{beauty}分'.format(
            i=i, gender=_gender, age=val['age'], glass=_glass, beauty=val['beauty'])
        res_str += os.linesep
        i += 1
    return res_str


def ps(filename='', decoration=21):
    """
    功能：人脸变妆。

    参数 filename 是待变妆的图片，

    可选参数 decoration 是变妆编码，范围 1-22，默认为 21(萌兔妆)，

    返回：变妆后的图片。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(decoration, int):
        if error_flag == -1:
            error_msg += "、'decoration'"
        else:
            error_flag = -1
            error_msg += "'decoration'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if decoration < 1 or decoration > 22:
        if error_flag == -1:
            error_msg += "、'decoration'"
        else:
            error_flag = -1
            error_msg += "'decoration'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        file_path = os.path.abspath(filename)
        # 为了检测 file_path 参数是否合法，不合法抛出异常
        f = open(file_path)
        f.close()
        basename, suffix = os.path.splitext(filename)
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        _resize_img(file_path, temp_file)
        url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceDecoration.php'

        b64img = base64.b64encode(temp_file.read()).rstrip().decode('utf-8')
        data = {'b64img': b64img, 'decoration': decoration}
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()
            if res['ret'] == 0 and res['data']:
                new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + os.path.splitext(filename)[1]
                with open(new_file, 'wb') as f:
                    f.write(base64.b64decode(res['data']['image']))
                temp_file.close()
                return new_file
            else:
                return "图片中找不到人哦~"
        temp_file.close()
        raise ConnectionError("获取变妆图片失败", r.content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face')


def mofa(filename='', model=1):
    """
    功能：人脸融合。

    参数 filename 是待融合的图片，

    可选参数 model 是模特编码，范围 1-10，默认为 1，

    返回：融合后的图片。
    """

    error_flag = 1
    error_msg = ""
    if not isinstance(filename, str):
        error_flag = -1
        error_msg += "'filename'"
    if not isinstance(model, int):
        if error_flag == -1:
            error_msg += "、'filename'"
        else:
            error_flag = -1
            error_msg += "'model'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if not filename:
        error_flag = -1
        error_msg += "'filename'"
    if model < 1 or model > 10:
        if error_flag == -1:
            error_msg += "、'model'"
        else:
            error_flag = -1
            error_msg += "'model'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        file_path = os.path.abspath(filename)
        # 为了检测 file_path 参数是否合法，不合法抛出异常
        f = open(file_path)
        f.close()
        basename, suffix = os.path.splitext(filename)
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
        _resize_img(file_path, temp_file)
        url = __MERGE_URL

        b64img = base64.b64encode(temp_file.read()).rstrip().decode('utf-8')
        data = {'image': b64img, 'model': model}

        headers = {'content-type': "application/json"}

        for i in range(3):
            r = requests.post(url, json=data, headers=headers)
            if r.status_code == 200:
                res = r.json()
                if res['ret'] == '0' and res['img_base64']:
                    new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_ronghe' + '.png'
                    with open(new_file, 'wb') as f:
                        f.write(base64.b64decode(res['img_base64']))
                    temp_file.close()
                    return _resize_img(new_file)
                else:
                    return "图片中找不到人哦~"
        temp_file.close()
        raise ConnectionError("获取融合图片失败", r.content)

    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_face')


def main():
    # pass
    # import ybc_box as box
    print(info('test.jpg'))
    print(info_all('three.jpg'))
    # print(_get_info('test.jpg'))
    # print(info('rgba.png'))
    # print(mofa('test.jpg'))
    # ps('test.jpg')
    # filename = camera()
    # res = age(filename)
    # print(res)
    # res = gender(filename)
    # print(res)
    # res = glass(filename)
    # print(res)
    # res = beauty(filename)
    # print(res)
    # res = info('2.jpg')
    # print(res)
    # res = info_all('3.jpg')
    # print(res)
    # res = age('5.jpg')
    # print(res)
    # res = gender('5.jpg')
    # print(res)
    # res = glass('5.jpg')
    # print(res)
    # res = beauty('5.jpg')
    # print(res)


if __name__ == '__main__':
    main()
