#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .utils import decode_token, str2int
from .request_utils import RequestResult as Result
from .request_utils import parse_param, parse_int_param, get_request_uid, get_request_username, build_response
from .models import UserTokens, UserPerms, UserPermGroups, UserRoleRelations, UserRolePerms, AuthUser
import sense_core as sd


class UserTokenCheckMiddleware(MiddlewareMixin):

    def _process_user_request(self, request):
        debug = sd.config('settings', 'debug', '0')
        if debug != '1':
            return
        uid = parse_int_param(request, 'user_id')
        request.user = AuthUser.find_one_by(id=uid)

    def process_request(self, request):
        sd.log_init_config(root_path=sd.config('log_path'))
        try:
            self._process_user_request(request)
            if request.user and not isinstance(request.user,AnonymousUser):
                return None
            res = Result(Result.PLEASE_LOGIN)
            _token = request.META.get("HTTP_TOKEN")
            if not _token or len(_token) == 0:
                return None
            lis = decode_token(_token)
            print(lis)
            if lis is None or len(lis) != 2:
                sd.log_info('token is invalid')
                return build_response(res)
            user_token = UserTokens.find_one_by(token=lis[0])
            if not user_token or user_token.system != lis[1]:
                return build_response(res)
            user = AuthUser.find_one_by(id=user_token.user_id)
            if user and hasattr(request, 'user'):
                request.user = user
                mutable = request.GET._mutable
                request.GET._mutable = True
                request.GET.__setitem__('user_id',user.id)
                request.GET._mutable = mutable
            return None
        except Exception as ex:
            sd.log_exception(ex)
            return build_response(Result(Result.SYSTEM_ERROR))


class PermissionCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            res = Result(Result.NOT_BE_AUTHENTICATED)
            url_path = request.path
            perm_id = UserPerms.find_perm_by_path(url_path)
            if not perm_id:
                return None
            if not hasattr(request, 'user') or request.user is None:
                return build_response(res)
            user = request.user
            perm_list = UserRolePerms.find_permlist_by_uid(user.id)
            if perm_id in perm_list:
                return None
            else:
                return build_response(res)
        except Exception as ex:
            sd.log_exception(ex)
            return build_response(Result(Result.SYSTEM_ERROR))


class RequestLogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        info = '[start][' + request.META['REMOTE_ADDR'] + '][' + request.method + '][' + request.path + ']'
        sd.log_info(info)
        request.start_time = sd.get_current_millisecond()

    def process_response(self, request, response):
        cost = str(sd.get_current_millisecond() - request.start_time)
        info = '[end][' + request.META['REMOTE_ADDR'] + '][' + request.method + '][' + str(
            get_request_uid(request)) + '][' + get_request_username(
            request) + '][' + request.path + '][' + cost + ']'
        sd.log_info(info)
        return response
