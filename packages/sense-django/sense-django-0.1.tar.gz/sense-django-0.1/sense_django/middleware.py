#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from .utils import decode_token,str2int
from .request_utils import RequestResult as Result
from .request_utils import parse_param,parse_int_param,get_request_uid,get_request_username
from .models import UserTokens,UserPerms,UserPermGroups,UserRoleRelations,UserRolePerms,AuthUser
import sense_core as sd
import json
import datetime
import re


class UserTokenCheck(MiddlewareMixin):

	def process_request(self,request):

		res = Result(Result.PLEASE_LOGIN,Result().get_error_message(Result.PLEASE_LOGIN))
		_token = request.META.get("HTTP_TOKEN")
		if not _token:
			return None
		lis = decode_token(_token)
		if lis == None:
			return HttpResponse(json.dumps(res.package()))
		user_token = UserTokens.find_one_by(token=lis[0])
		if user_token:
			if user_token.system!=lis[1]:
				return HttpResponse(json.dumps(res.package()))
			uid = user_token.user_id
			user = AuthUser.find_one_by(id=uid)
			if user and hasattr(request,'user'):
				request.user = user
			return None
		else:
			return HttpResponse(json.dumps(res.package()))


class PermissionCheckMiddleware(MiddlewareMixin):

	def process_request(self,request):

		res = Result(Result.NOT_BE_AUTHENTICATED,Result().get_error_message(Result.NOT_BE_AUTHENTICATED))
		url_path = request.path
		# 1 TODO : traverse through groups and perms to find one perm match the request path, if not return None
		perm_id = UserPerms.find_perm_by_path(url_path)
		if not perm_id:
			return None
		
		# 2 TODO : get user's perm list
		if not hasattr(request,'user'):
			return HttpResponse(json.dumps(res.package()))
		user = request.user
		perm_list = UserRolePerms.find_permlist_by_uid(user.id)

		# 3 TODO : compare path perm and user perm list, pass or deny
		if perm_id in perm_list:
			return None
		else:
			return HttpResponse(json.dumps(res.package()))


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