import re
import json
import numpy
import pypinyin
import datetime
import base64


def chinese_to_pinyin(word, first=True):
    _res = []
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        if first:
            _res.extend(i[0][0])
        else:
            _res.extend(i)
    return _res


def chinese_to_pinyin_str(word, first=True):
    return ''.join(chinese_to_pinyin(word, first))


def filter_html_tag(html, tag_name=''):
    if tag_name == '':
        return re.sub(r'</?\w+[^>]*>', '', html)
    return re.sub(r'</?' + tag_name + '>', '', html)


def format_zh_time(time):
    d1 = datetime.datetime.now()
    d2 = datetime.datetime.fromtimestamp(time)
    diff = int(round(d1.timestamp() - time))
    if diff < 60:
        return '刚刚'
    min = diff / 60
    if min < 60:
        return str(int(min)) + '分钟前'
    hour = diff / 3600
    if hour < 24 and d1.day == d2.day:
        return str(int(hour)) + '小时前'
    return d2.strftime('%Y-%m-%d')


def encode_token(*args):
    param = list(args)
    _data = str(param.pop(0))
    if len(param) == 0:
        raise ValueError('Encode_token:param must more than 2')
    for item in param:
        _data += ',' + str(item)
    token = base64.encodestring(_data.encode()).decode()
    return token


def decode_token(param):
    try:
        token = param.encode()
        data = base64.decodebytes(token)
        lis = data.decode().split(',')
        return lis
    except:
        return None


def str2int(param):
    try:
        item = int(param)
    except:
        item = None
    return item


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj)
        else:
            return super(NumpyEncoder, self).default(obj)


if __name__ == "__main__":
    t = datetime.datetime.now().timestamp() - 4500 * 12
    print(format_zh_time(t))
