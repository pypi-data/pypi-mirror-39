#!/usr/bin/python
# -*- coding:utf-8 -*-

from .models import UserPerms,UserRolePerms
import sense_core as sd

def check_perm_by_uid(path,user_id):
    try:
        perm_id = UserPerms.find_perm_by_path(path)
        perm_list = UserRolePerms.find_permlist_by_uid(user_id)
        if perm_id in perm_list:
            return True
        else:
            return False
    except Exception as e:
        sd.log_exception(e)
        return False