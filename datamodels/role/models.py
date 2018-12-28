import traceback

from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError
from django.db.models import F

from datamodels.sms.models import mm_SMSCode
from lib.common import BaseManger
from lib.exceptions import DBException
from lib.im import IMServe


class BaseRole(models.Model):
    GENDER_CHOICE = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=20)
    age = models.PositiveSmallIntegerField('年龄', null=True, blank=True)
    gender = models.IntegerField('性别', choices=GENDER_CHOICE, default=0)
    avatar_url = models.CharField('头像', max_length=120, blank=True)
    account = models.CharField('电话', max_length=11, unique=True)
    wechat_id = models.CharField('微信号', max_length=24, blank=True)
    intro = models.CharField('自我简介', max_length=120, blank=True)
    address_home = models.CharField('家庭住址', max_length=100, blank=True)
    address_company = models.CharField('公司地址', max_length=100, blank=True)
    im_token = models.CharField('融云token', max_length=100, blank=True)
    relationships = models.ManyToManyField('self', through='RelationShip', symmetrical=False, related_name='relations')
    last_request_at = models.DateTimeField(null=True, blank=True)
    following_count = models.PositiveIntegerField('我的关注总数', default=0)
    followers_count = models.PositiveIntegerField('关注总数', default=0)
    blocked_count = models.PositiveIntegerField('屏蔽总数', default=0)
    is_manager = models.BooleanField('管理员', default=False)
    is_shop_keeper = models.BooleanField('商家', default=False)
    skills = models.TextField('技能描述', max_length=200, blank=True, null=True)
    is_show_skill = models.BooleanField('展示技能', default=False)
    is_rut = models.BooleanField('相亲状态', default=False)
    expect_desc = models.CharField('异性要求', blank=True, null=True, max_length=200)

    class Meta:
        abstract = True


class CustomerManager(BaseManger):

    def add(self, account, password):
        try:
            with transaction.atomic():
                user = self._add_user(account, password)
                im_token = IMServe.gen_token(user.id, account)['token']
                customer = self.create(user=user, account=account, im_token=im_token)
                return customer
        except IntegrityError:
            raise DBException('账号已注册')
        except:
            msg = traceback.format_exc()
            raise DBException(msg)

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

    def customers_need_paired(self):
        return self.all().filter(is_rut=True).order_by('-last_request_at')


class Customer(BaseRole):
    objects = CustomerManager()

    def __str__(self):
        return self.account

    class Meta:
        db_table = 'lv_customers'

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

    def get_following_ids(self):
        return self.get_following_recoreds().values_list('to_customer_id', flat=True)

    def get_unfollowing_customers(self):
        return mm_Customer.all().exclude(pk__in=self.get_following_ids()).order_by('-last_request_at')


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

        if status == RELATIONSHIP_BLOCKED:
            rows = self.filter(from_customer_id=to_customer_id, to_customer_id=from_customer_id).exclude(
                status=RELATIONSHIP_BLOCKED).update(status=RELATIONSHIP_FOLLOWING)
            if rows:
                mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') + 1)
        else:
            rows = self.filter(from_customer_id=to_customer_id, to_customer_id=from_customer_id,
                               status=RELATIONSHIP_FOLLOWING).update(status=RELATIONSHIP_BOTH_FOLLOWING)
            if rows:
                status = RELATIONSHIP_BOTH_FOLLOWING
                mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') + 1)

        relationship, created = self.get_or_create(
            from_customer_id=from_customer_id,
            to_customer_id=to_customer_id,
            status=status)
        if created:
            mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') + 1)

        return relationship

    def remove_relation(self, from_customer_id, to_customer_id):
        relation = self.filter(from_customer_id=from_customer_id, to_customer_id=to_customer_id).first()
        if relation:
            if relation.status == RELATIONSHIP_BOTH_FOLLOWING:
                self.filter(from_customer_id=to_customer_id, to_customer_id=from_customer_id, status=RELATIONSHIP_BOTH_FOLLOWING).update(status=RELATIONSHIP_FOLLOWING)

            if relation.status == RELATIONSHIP_BLOCKED:
                mm_Customer.filter(id=from_customer_id).update(blocked_count=F('blocked_count') - 1)
            else:
                mm_Customer.filter(id=from_customer_id).update(following_count=F('following_count') - 1)
                mm_Customer.filter(id=to_customer_id).update(followers_count=F('followers_count') - 1)
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


mm_Customer = Customer.objects
mm_RelationShip = RelationShip.objects
