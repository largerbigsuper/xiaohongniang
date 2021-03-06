import json
import random
import string
import traceback
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError
from django.db.models import F

from LV.settings_lv import Platform
from datamodels.sms.models import mm_SMSCode
from lib.common import BaseManger
from lib.exceptions import DBException
from lib.im import IMServe
from lib.tools import Tool


class BaseRole(models.Model):
    GENDER_CHOICE = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    PROFESSION_CHOICE = (
        (0, '未知'),
        (1, '白领/一般职业'),
        (2, '公务员/事业单位'),
        (3, '自由职业/个体户/私营业主'),
        (4, '暂时无业'),
        (5, '退休'),
        (6, '学生'),
    )
    EDUCATION_CHOICE = (
        (0, '未知'),
        (1, '初中'),
        (2, '高中'),
        (3, '中专'),
        (4, '大专'),
        (5, '本科'),
        (6, '硕士'),
        (7, '博士'),
        (8, '院士'),
    )
    INCOME_CHOICE = (
        (0, '未知'),
        (1, '10万以下'),
        (2, '10万~20万'),
        (3, '20万~50万'),
        (4, '50万以上'),
    )
    MARITAL_STATUS_CHOICE = (
        (0, '未知'),
        (1, '未婚'),
        (2, '离异'),
        (3, '丧偶'),
    )
    CHILD_STATUS_CHOICE = (
        (0, '未知'),
        (1, '无'),
        (2, '有，和我在一起'),
        (3, '有，不和我在一起'),
    )
    AVATAR_STATUS = (
        (0, '未审核'),
        (1, '审核通过'),
        (2, '审核不通过'),
    )
    HOUSE_STATUS = (
        (0, '保密'),
        (1, '已购房'),
        (2, '未购房'),
    )
    CAR_STATUS = (
        (0, '保密'),
        (1, '已购车'),
        (2, '未购车'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=20)
    age = models.PositiveSmallIntegerField('年龄', null=True, blank=True)
    gender = models.IntegerField('性别', choices=GENDER_CHOICE, default=0)
    avatar_url = models.CharField('头像', max_length=300, blank=True)
    avatar_status = models.PositiveSmallIntegerField('头像审核状态', choices=AVATAR_STATUS, default=0)
    account = models.CharField('账号', max_length=11, unique=True)
    wechat_id = models.CharField('微信号', max_length=24, blank=True)
    intro = models.CharField('自我简介', max_length=120, blank=True)
    address_home = models.CharField('家庭住址', max_length=100, blank=True)
    address_company = models.CharField('公司地址', max_length=100, blank=True)
    im_token = models.CharField('融云token', max_length=100, blank=True)
    relationships = models.ManyToManyField('self', through='RelationShip', symmetrical=False, related_name='relations')
    last_request_at = models.DateTimeField(verbose_name='最后请求时间', null=True, blank=True)
    following_count = models.PositiveIntegerField('我的关注总数', default=0)
    following_both_count = models.PositiveIntegerField('相互关注总数', default=0)
    followers_count = models.PositiveIntegerField('关注总数', default=0)
    blocked_count = models.PositiveIntegerField('屏蔽总数', default=0)
    is_manager = models.BooleanField('管理员', default=False)
    is_shop_keeper = models.BooleanField('商家', default=False)
    skills = models.TextField('技能描述', max_length=200, blank=True, null=True)
    is_show_skill = models.BooleanField('展示技能', default=False)
    is_rut = models.BooleanField('相亲状态', default=False)
    expect_desc = models.CharField('异性要求', blank=True, null=True, max_length=200)
    latitude = models.FloatField(verbose_name='精度', null=True, blank=True)
    longitude = models.FloatField(verbose_name='维度', null=True, blank=True)
    birthday = models.DateTimeField(verbose_name='生日', null=True, blank=True)
    height = models.FloatField(verbose_name='身高', null=True, blank=True)
    profession = models.PositiveIntegerField(verbose_name='职业', choices=PROFESSION_CHOICE, default=0)
    education = models.PositiveIntegerField(verbose_name='学历', choices=EDUCATION_CHOICE, default=0)
    income = models.PositiveIntegerField(verbose_name='收入', choices=INCOME_CHOICE, default=0)
    marital_status = models.PositiveIntegerField(verbose_name='婚姻状况', choices=MARITAL_STATUS_CHOICE, default=0)
    child_status = models.PositiveIntegerField(verbose_name='有无小孩', choices=CHILD_STATUS_CHOICE, default=0)
    house_status = models.PositiveIntegerField(verbose_name='房产状态', choices=HOUSE_STATUS, default=0)
    car_status = models.PositiveIntegerField(verbose_name='车辆状态', choices=CAR_STATUS, default=0)
    years_to_marry = models.PositiveIntegerField(verbose_name='几年内结婚', default=0)
    score = models.PositiveIntegerField(verbose_name='自评分数', default=0)
    condition = models.TextField(verbose_name='择偶标准', max_length=1000, blank=True, default='{}')
    # {
    #     "age_range": [10, 20],
    #     "height_range": [180, 190],
    #     "profession": 1,
    #     "education": 1,
    #     "income": 1,
    #     "marital_status": 1,
    #     "child_status": 1,
    #     "years_to_marry": 1,
    # }
    images = models.TextField(verbose_name='相册', max_length=1000, blank=True, default='[]')
    service_vip_expired_at = models.DateTimeField(verbose_name='会员过期时间', null=True, blank=True)
    service_show_index_expired_at = models.DateTimeField(verbose_name='置顶有效期', null=True, blank=True)
    invitecode = models.CharField(verbose_name='邀请码', max_length=8, null=True, blank=True)
    mini_openid = models.CharField(verbose_name='小程序openid', max_length=60, null=True, blank=True)
    online_card_count = models.PositiveIntegerField(verbose_name='线上服务卡', default=0)
    offline_card_count = models.PositiveIntegerField(verbose_name='线下服务卡', default=0)
    is_idcard_verified = models.BooleanField(verbose_name='身份证认证', default=False)

    class Meta:
        abstract = True


class CustomerManager(BaseManger):

    Default_Password = '888888'

    #
    # def get_queryset(self):
    #     return super().get_queryset().exclude(avatar_url='').filter(avatar_status=1)

    def get_customer_with_avatar(self):
        # 返回有头像，且认证通过的用户
        return self.exclude(avatar_url='').filter(avatar_status=1)

    def add(self, account, password, **kwargs):
        try:
            with transaction.atomic():
                user = self._add_user(account, password)
                customer = self.create(user=user, account=account, **kwargs)
                customer.im_token = IMServe.gen_token(customer.id, account)['token']
                customer.save()

                return customer
        except IntegrityError:
            raise DBException('账号已注册')
        except:
            msg = traceback.format_exc()
            raise DBException(msg)

    def _create_miniprogram_account(self, mini_openid):
        account = 'mp_' + ''.join([random.choice(string.ascii_lowercase) for _ in range(6)])
        password = self.Default_Password
        customer = self.add(account, password, mini_openid=mini_openid)
        return customer

    def get_customer_by_miniprogram(self, mini_openid):
        """通过小程序获取customer"""
        customer = self.filter(mini_openid=mini_openid).first()
        if customer:
            return customer
        else:
            for _ in range(3):
                try:
                    customer = self._create_miniprogram_account(mini_openid)
                    return customer
                except:
                    pass
            else:
                raise DBException('注册用户失败')

    def reset_password_by_login(self, user_id, raw_password, new_password):
            user = User.objects.get(id=user_id)
            if user.check_password(raw_password):
                return self._reset_password(user, new_password)
            else:
                raise DBException('原始密码错误')

    def reset_password_by_sms(self, account, password, code):
        try:
            mm_SMSCode.is_effective(account, code)
            user = User.objects.get(username=account)
            return self._reset_password(user, password)
        except User.DoesNotExist:
            raise DBException('%s账号不存在' % account)

    @staticmethod
    def _reset_password(user: User, password: str) -> User:
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def _add_user(account, password):
        user = User.objects.create_user(username=account, password=password)
        return user

    def active_customers(self):
        return self.all().order_by('-last_request_at')

    def customers_with_skills(self):
        return self.all().filter(skills__isnull=False).order_by('-last_request_at')

    def customers_need_paired(self, customer):
        return self.exclude(gender=customer.gender).filter(is_rut=True).order_by('-last_request_at')

    def active_customer_in_days(self, days=5):
        last_request_at = datetime.now() - timedelta(days=days)
        return self.filter(last_request_at__gt=last_request_at)

    def customer_around(self, latitude, longitude, gender, distance=10000):
        latitude_range, longitude_range = Tool.get_lon_lat_range(latitude, longitude, distance)
        latitude_low, latitude_heigh = latitude_range
        longitude_low, longitude_heigh = longitude_range
        params = {
            'latitude_low': latitude_low,
            'latitude_heigh': latitude_heigh,
            'longitude_low': longitude_low,
            'longitude_heigh': longitude_heigh,
            'distance': distance,
            'latitude': latitude,
            'longitude': longitude,
            'gender': gender
        }
        sql = '''
        Select *, 
        st_distance_sphere(POINT({longitude}, {latitude} ), POINT(lv_customers.longitude, lv_customers.latitude)) AS distance
        FROM lv_customers
        WHERE id >= 1
        AND lv_customers.gender != {gender}
        AND lv_customers.latitude BETWEEN {latitude_low} AND  {latitude_heigh}
        AND lv_customers.longitude BETWEEN {longitude_low} AND {longitude_heigh}
        HAVING distance < {distance}
        ORDER BY distance;
        '''.format(**params)
        return mm_Customer.raw(sql)

    def show_in_home_page(self, gender):
        return self.get_customer_with_avatar().exclude(gender=gender).filter(service_show_index_expired_at__gt=datetime.now()).order_by('?')[:3]

    def recommend_customers(self, customer):
        timelimit = datetime.now() - timedelta(days=5)
        f = {
            'last_request_at__gte': timelimit,
        }
        #     "age_range": [10, 20],
        #     "height_range": [180, 190],
        #     "profession": 1,
        #     "education": 1,
        #     "income": 1,
        #     "marital_status": 1,
        #     "child_status": 1,
        #     "years_to_marry": 1,
        for k, v in customer.condition_json.items():
            if k in ['age_range', 'height_range']:
                prefix = k.split('_')[0]
                heigh, low = v
                if heigh:
                    f[prefix + '__gte'] = heigh
                if low:
                    f[prefix + '__lte'] = low
            else:
                if v:
                    f[k] = v

        return self.filter(**f).exclude(gender=customer.gender).order_by('-last_request_at', 'id')

    def get_kefu_id(self):
        kefu = mm_Customer.filter(account='10000000000').first()
        if kefu:
            return kefu.id
        else:
            return -1


class Customer(BaseRole):
    objects = CustomerManager()

    def __str__(self):
        return self.account

    class Meta:
        db_table = 'lv_customers'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def add_relationship(self, customer_id, status):

        return mm_RelationShip.add_relation(self.id, customer_id, status)

    def remove_relationship(self, customer_id):
        mm_RelationShip.remove_relation(self.id, customer_id)

    def get_relationships(self, status):
        return self.relationships.filter(
            to_customer__status=status,
            to_customer__from_customer=self)

    def get_related_to(self, status):
        return self.relations.filter(
            from_customer__status=status,
            from_customer__to_customer=self)

    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)

    def get_relationship_records(self, status):
        if not status == 0:
            return RelationShip.objects.filter(from_customer=self, status__gte=status)
        return RelationShip.objects.filter(from_customer=self, status=status)

    def get_related_to_records(self, status):
        if not status == 0:
            return RelationShip.objects.filter(to_customer=self, status__gte=status)
        else:
            return RelationShip.objects.filter(to_customer=self, status=status)

    def get_following_recoreds(self):
        return self.get_relationship_records(RELATIONSHIP_FOLLOWING)

    def get_follower_recoreds(self):
        return self.get_related_to_records(RELATIONSHIP_FOLLOWING)

    def get_both_following_recoreds(self):
        return self.get_relationship_records(RELATIONSHIP_BOTH_FOLLOWING)

    def get_following_ids(self):
        return self.get_following_recoreds().values_list('to_customer_id', flat=True)

    def get_unfollowing_customers(self):
        return mm_Customer.all().exclude(pk__in=self.get_following_ids()).order_by('-last_request_at')

    @property
    def condition_json(self):
        return json.loads(self.condition)


RELATIONSHIP_BLOCKED = 0
RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BOTH_FOLLOWING = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_BLOCKED, '屏蔽'),
    (RELATIONSHIP_FOLLOWING, '正在关注'),
    (RELATIONSHIP_BOTH_FOLLOWING, '互相关注'),
)


class RelationShipManager(BaseManger):

    def add_relation(self, from_customer_id, to_customer_id, status):
        """
        关注与屏蔽功能
        关注某人：
        1.如果已关注则返回
        2.1如果屏蔽了某人，需先取消屏蔽，再进行关注。
        2.2 如果我关注的人也关注了我则设为互相关注
        屏蔽：1.如果已屏蔽则返回
        2.1如果是关注状态
        2.2 如果是单方面关注， 则改为屏蔽关系。 如果是互相关注则取消双方互相关注状态
        """
        _relation = self.filter(from_customer_id=from_customer_id, to_customer_id=to_customer_id).first()
        relaton_tome = self.filter(from_customer_id=to_customer_id, to_customer_id=from_customer_id).first()
        if status == RELATIONSHIP_FOLLOWING:  # 添加关注
            if _relation:
                if _relation.status == RELATIONSHIP_BLOCKED:  # 屏蔽状态，先去除屏蔽， 再判断双方关注状态
                    if relaton_tome:  # 判断该用户对我的关注状态
                        if relaton_tome.status == RELATIONSHIP_FOLLOWING:
                            _relation.status = RELATIONSHIP_BOTH_FOLLOWING
                            relaton_tome.status = RELATIONSHIP_BOTH_FOLLOWING
                            relaton_tome.save()
                            mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') - 1,
                                                                           following_count=F('following_count') + 1,
                                                                           following_both_count=F(
                                                                               'following_both_count') + 1
                                                                           )
                            mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1,
                                                                         following_both_count=F(
                                                                             'following_both_count') + 1)
                        else:
                            _relation.status = RELATIONSHIP_FOLLOWING
                            mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') - 1,
                                                                           following_count=F('following_count') + 1)
                            mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1)
                    else:
                        _relation.status = RELATIONSHIP_FOLLOWING
                        mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') - 1,
                                                                       following_count=F('following_count') + 1)
                        mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1)

                    _relation.save()
                    return _relation
                else:  # 已关注，直接返回
                    return _relation

            else:
                if relaton_tome:  # 判断该用户对我的关注状态
                    if relaton_tome.status == RELATIONSHIP_FOLLOWING:
                        status = RELATIONSHIP_BOTH_FOLLOWING
                        relaton_tome.status = RELATIONSHIP_BOTH_FOLLOWING
                        relaton_tome.save()
                        mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') + 1,
                                                                       following_both_count=F(
                                                                           'following_both_count') + 1
                                                                       )
                        mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1,
                                                                     following_both_count=F(
                                                                         'following_both_count') + 1)
                    else:
                        status = RELATIONSHIP_FOLLOWING
                        mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') + 1)
                        mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1)
                else:
                    status = RELATIONSHIP_FOLLOWING
                    mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') + 1)
                    mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1)
                relation = self.create(from_customer_id=from_customer_id, to_customer_id=to_customer_id, status=status)
                return relation

        elif status == RELATIONSHIP_BLOCKED:  # 拉黑
            if _relation:
                if _relation.status == RELATIONSHIP_FOLLOWING:
                    mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') + 1,
                                                                   following_count=F('following_count') - 1)

                elif _relation.status == RELATIONSHIP_BOTH_FOLLOWING:
                    mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') + 1,
                                                                   following_count=F('following_count') - 1,
                                                                   following_both_count=F('following_both_count') - 1)
                    mm_Customer.filter(id=to_customer_id).update(following_both_count=F('following_both_count') - 1)
                    relaton_tome.status = RELATIONSHIP_FOLLOWING
                    relaton_tome.save()
                _relation.status = RELATIONSHIP_BLOCKED
                _relation.save()
                return _relation
            else:
                relation = self.create(from_customer_id=from_customer_id, to_customer_id=to_customer_id, status=status)
                mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') + 1)
                return relation
        else:
            pass

    def remove_relation(self, from_customer_id, to_customer_id):
        relation = self.filter(from_customer_id=from_customer_id, to_customer_id=to_customer_id).first()
        if relation:
            if relation.status == RELATIONSHIP_BOTH_FOLLOWING:
                self.filter(from_customer_id=to_customer_id,
                            to_customer_id=from_customer_id,
                            status=RELATIONSHIP_BOTH_FOLLOWING
                            ).update(status=RELATIONSHIP_FOLLOWING)
                mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') - 1,
                                                               following_both_count=F('following_both_count') - 1
                                                               )
                mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') - 1,
                                                             following_both_count=F('following_both_count') - 1)
            elif relation.status == RELATIONSHIP_FOLLOWING:
                mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') - 1)
                mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') - 1)

            elif relation.status == RELATIONSHIP_BLOCKED:
                mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') - 1)
            else:
                pass

            relation.delete()

    def get_following_customer_ids_map(self, from_customer_id):
        relations = self.filter(from_customer_id=from_customer_id).values_list('to_customer_id', 'status')
        return {customer_id: status for customer_id, status in relations}


class RelationShip(models.Model):

    from_customer = models.ForeignKey(Customer, related_name='from_customer', on_delete=models.CASCADE)
    to_customer = models.ForeignKey(Customer, related_name='to_customer', on_delete=models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES, default=RELATIONSHIP_FOLLOWING)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RelationShipManager()

    class Meta:
        db_table = 'lv_relation_ship'
        unique_together = (
            ('from_customer', 'to_customer'),
        )


class CertificationManager(BaseManger):
    Property_IDCard = 1
    Property_Education = 2
    Property_Premise = 3

    Property_Choice = (
        (Property_IDCard, '身份证认证'),
        (Property_Education, '学历认证'),
        (Property_Premise, '房产认证'),
    )

    Status_Submited = 1
    Status_Failed = 2
    Status_Verified = 3

    Status_Chioce = (
        (Status_Submited, '已提交'),
        (Status_Failed, '未通过'),
        (Status_Verified, '通过'),
    )

    def my_certifications(self, customer_id):
        return self.filter(customer_id=customer_id).order_by('property_type')


class Certification(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    property_type = models.PositiveSmallIntegerField(verbose_name='认证类型',
                                                     choices=CertificationManager.Property_Choice,
                                                     default=CertificationManager.Property_IDCard)
    images = models.CharField(verbose_name='图片', max_length=500, default='[]')
    status = models.PositiveSmallIntegerField(verbose_name='认证状态',
                                              choices=CertificationManager.Status_Chioce,
                                              default=CertificationManager.Status_Submited)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modify_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    objects = CertificationManager()

    class Meta:
        db_table = 'lv_certifications'
        unique_together = [
            ('customer', 'property_type'),
        ]


class InviteRecordManager(BaseManger):

    Platform_Choice = (
        (Platform.WEB, Platform.Hans_Mapping[Platform.WEB]),
        (Platform.ANDROID, Platform.Hans_Mapping[Platform.ANDROID]),
        (Platform.IOS, Platform.Hans_Mapping[Platform.IOS]),
    )

    def add_record(self, inviter_id, invited_id, platform=Platform.WEB):
        try:
            self.create(inviter_id=inviter_id,
                        invited_id=invited_id,
                        platform=platform)
        except:
            pass

    def get_customer_records(self, customer_id):
        return self.filter(inviter_id=customer_id)

    def get_inviter(self, customer_id):
        return self.filter(invited_id=customer_id).first()


class InviteRecord(models.Model):

    inviter = models.ForeignKey('role.Customer', on_delete=models.DO_NOTHING, verbose_name='邀请人',
                                db_index=False, related_name='inviter_users')
    invited = models.ForeignKey('role.Customer', on_delete=models.DO_NOTHING, verbose_name='被邀请人',
                                db_index=False, related_name='invited_users')
    platform = models.PositiveSmallIntegerField(verbose_name='来源',
                                                choices=InviteRecordManager.Platform_Choice,
                                                default=Platform.WEB)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = InviteRecordManager()

    class Meta:
        db_table = 'lv_invite_records'
        ordering = ['-create_at']
        index_together = [
            ('inviter', 'invited')
        ]


class IDCardCertificationManager(BaseManger):
    pass


class IDCardCertification(models.Model):
    """身份证认证记录"""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    realname = models.CharField(max_length=20, verbose_name='真实姓名')
    idnumber = models.CharField(max_length=18, verbose_name='身份证号码')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = IDCardCertificationManager()

    class Meta:
        db_table = 'lv_idcard_certification'


class PictureManager(BaseManger):

    def add_picture(self, customer_id, url):
        return self.create(customer_id=customer_id, url=url)


class Picture(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    url = models.CharField(max_length=400, verbose_name='图片地址')
    is_verified = models.BooleanField(default=False, verbose_name='已审核')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = PictureManager()

    class Meta:
        db_table = 'lv_picture'
        ordering = ['-create_at']
        verbose_name = '头像审核'
        verbose_name_plural = '头像审核'


mm_Customer = Customer.objects
mm_RelationShip = RelationShip.objects
mm_Certification = Certification.objects
mm_InviteRecord = InviteRecord.objects
mm_IDCardCertification = IDCardCertification.objects
mm_Picture = Picture.objects

