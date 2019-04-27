#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/27 下午12:21
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : 01_migrate_relationship.py
from collections import Counter

from datamodels.role.models import mm_RelationShip, mm_Customer


def init_user_stats():
    #     following_count = models.PositiveIntegerField('我的关注总数', default=0)
    #     following_both_count = models.PositiveIntegerField('相互关注总数', default=0)
    #     followers_count = models.PositiveIntegerField('关注总数', default=0)
    #     blocked_count = models.PositiveIntegerField('屏蔽总数', default=0)
    mm_Customer.update(following_count=0, following_both_count=0, followers_count=0, blocked_count=0)


def run():
    init_user_stats()
    for c in mm_Customer.all():
        following = mm_RelationShip.filter(from_customer_id=c.id).values_list('status', flat=True)
        following_counter = Counter(following)
        c.following_count = following_counter[1] + following_counter[2]
        c.following_both_count = following_counter[2]
        c.blocked_count = following_counter[0]
        followers = mm_RelationShip.filter(to_customer_id=c.id).exclude(status=0).count()
        c.followers_count = followers
        c.save()


if __name__ == '__main__':
    run()
