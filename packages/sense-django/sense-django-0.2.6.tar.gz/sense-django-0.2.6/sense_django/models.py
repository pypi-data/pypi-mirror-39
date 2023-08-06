from django.db import models
import datetime
import re


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

    @classmethod
    def find_map_by_ids(cls, ids):
        items = list(cls.objects.filter(id__in=ids))
        return {x.id: x for x in items}

    @classmethod
    def find_by_ids(cls, ids):
        map = cls.find_map_by_ids(ids)
        result = []
        for id in ids:
            if id in map:
                result.append(map[id])
        return result

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.objects.get(pk=id)
        except:
            return None

    @classmethod
    def find_many(cls, **kwargs):
        try:
            item = cls.objects.filter(**kwargs)
        except:
            item = None
        return item

    @classmethod
    def find_one_by(cls, **kwargs):
        try:
            item = cls.objects.get(**kwargs)
        except:
            item = None
        return item


class AuthUser(BaseModel):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=254)
    phone = models.CharField(max_length=64)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    is_staff = models.BooleanField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True)
    date_threshold = models.DateTimeField()
    company = models.CharField(max_length=256)
    is_initial = models.IntegerField(default=1)

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'auth_user'


_groups_ = None
_last_time_ = datetime.datetime.now() + datetime.timedelta(minutes=-5)


class UserPermGroups(BaseModel):
    name = models.CharField(max_length=64)
    rule_prefix = models.CharField(max_length=64, unique=True)
    module = models.CharField(max_length=64, null=True)
    rank = models.IntegerField()
    create_time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'user_perm_groups'

    @classmethod
    def match_request_path(cls, request_url, _now):
        for group in _groups_:
            if re.match(group.rule_prefix, request_url):
                return group.id
        return None

    @classmethod
    def update_groups(cls):
        global _groups_
        _groups_ = cls.objects.all().order_by('rank')


_perms_ = {}


class UserPerms(BaseModel):
    name = models.CharField(max_length=64)
    group_id = models.IntegerField(null=True)
    rule = models.CharField(max_length=64, unique=True)
    rank = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'user_perms'

    @classmethod
    def find_perm_by_path(cls, request_url):
        global _last_time_
        _now = datetime.datetime.now()
        if (_now - _last_time_).seconds >= 300:
            UserPerms.update_perms()
            UserPermGroups.update_groups()
            _last_time_ = _now
        group_id = UserPermGroups.match_request_path(request_url, _now)
        if not _perms_.__contains__(group_id):
            return None
        perms = _perms_[group_id]
        for perm in perms:
            if re.search(perm.rule, request_url):
                return perm.id
        return None

    @classmethod
    def update_perms(cls):
        global _perms_
        perms = cls.objects.all().order_by('rank')
        for item in perms:
            if not _perms_.__contains__(item.group_id):
                _perms_[item.group_id] = []
            _perms_[item.group_id].append(item)


class UserRoles(BaseModel):
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'user_roles'


class UserRoleRelations(BaseModel):
    uid = models.IntegerField()
    role_id = models.IntegerField()
    time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'user_role_relations'

    @classmethod
    def find_role_by_uid(cls, user_id):
        role_list = cls.find_many(uid=user_id).values_list('role_id', flat=True)
        return role_list


class UserRolePerms(BaseModel):
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'user_role_perms'

    @classmethod
    def find_permlist_by_uid(cls, uid):
        role_list = UserRoleRelations.find_role_by_uid(uid)
        perm_list = list(cls.objects.filter(role_id__in=role_list).values_list('perm_id', flat=True))
        return perm_list


class UserTokens(BaseModel):
    user_id = models.IntegerField()
    token = models.CharField(max_length=64, null=True)
    system = models.CharField(max_length=64, null=True)
    login_time = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        managed = False
        app_label = 'auth'
        db_table = 'user_tokens'
