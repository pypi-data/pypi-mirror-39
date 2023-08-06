from django.http import HttpResponse
import sense_core as sd
from .utils import NumpyEncoder
import json


class RequestResult(object):
    ERROR_PARAM_INVALID = 1
    ERROR_NOT_FOUND = 2
    PLEASE_LOGIN = 4
    NOT_BE_AUTHENTICATED = 5

    def get_error_message(self, code):
        if code == RequestResult.ERROR_PARAM_INVALID:
            return "参数错误"
        if code == RequestResult.ERROR_NOT_FOUND:
            return "数据无效"
        if code == RequestResult.PLEASE_LOGIN:
            return "请重新登录"
        if code == RequestResult.NOT_BE_AUTHENTICATED:
            return "未授权用户"
        if code == 0:
            return ""
        return "未知错误"

    def set_error_code(self, code):
        self.set_code_message(code, self.get_error_message(code))
        return self

    def __init__(self, code=0, msg='', data=None):
        self.__dict_item = dict()
        self.__dict_item['ret_code'] = code
        self.__dict_item['ret_msg'] = msg
        if data is not None:
            self.__dict_item['ret_data'] = data

    def set_error(self, message):
        self.set_code_message(-1, message)
        return self

    def set_code_message(self, code, message):
        self.__dict_item['ret_code'] = code
        self.__dict_item['ret_msg'] = message
        if code != 0 and 'ret_data' in self.__dict_item:
            del self.__dict_item['ret_data']
        return self

    def set_data(self, data):
        self.__dict_item['ret_data'] = data
        return self

    @classmethod
    def build_model_items(cls, items, type='list'):
        return sd.build_model_list(items, type)

    def add_data_item(self, key, val):
        if 'ret_data' not in self.__dict_item:
            self.__dict_item['ret_data'] = {}
        self.__dict_item['ret_data'][key] = val
        return self

    def package(self):
        return self.__dict_item

def build_response(result):
    return HttpResponse(json.dumps(result.package(), cls=NumpyEncoder), content_type="json")

def parse_param(request, key):
    if request.method == 'GET':
        return request.GET.get(key, '')
    if request.method == 'POST':
        return request.POST.get(key, '')
    return ''

def parse_pn_param(request):
    pn = parse_int_param(request, 'pn')
    return pn if pn >= 0 else 0

def parse_int_param(request, key, default=0):
    if request.method == 'GET':
        val = request.GET.get(key, '')
    elif request.method == 'POST':
        val = request.POST.get(key, '')
    else:
        val = ''
    if len(val) == 0:
        return default
    return int(val)

def get_request_uid(request):
    if request.user is None:
        return 0
    return request.user.id

def get_request_username(request):
    if request.user is None:
        return ''
    return request.user.username
