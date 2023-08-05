# -*- coding:utf-8 -*-

import six
from datetime import datetime
from krux.random import gen_uuid32
from dt_utils.timers import RetryTimer
import json
import redis

REDIS_VERSION = tuple(int(item) for item in redis.__version__.split('.'))

__all__ = ['CRUDLocker']


class CRUDLocker(object):
    class NeedRetry(Exception): pass
    class Timeout(Exception): pass

    permitted_actions = {
        # CURRENT_STATUS: ACTION
        "create": [],
        "retrieve": ["retrieve"],
        "update": [],
        "delete": []
    }

    prefix = 'crud_lock'
    mark_prefix = 'crud_mark'
    lru_prefix = 'crud_lru'

    def __init__(self,
                 name,
                 redis_connecton,
                 default_ttl=1000,
                 mark_max_wait=100,
                 mark_ttl=10,
                 unmark_safe_time=1,
                 permitted_actions=None):
        self.name = name
        self.redis_connection = redis_connecton

        self.default_ttl = default_ttl
        self.mark_max_wait = mark_max_wait
        self.mark_ttl = mark_ttl
        self.unmark_safe_time = unmark_safe_time

        if permitted_actions:
            self.permitted_actions = permitted_actions

        self.lru_key = '{}:{}'.format(self.lru_prefix, self.name)

    def lock_do(self, resource, action='retrieve', ttl=None, max_wait=None, func=None, func_args=[], func_kwargs={}, *args, **kwargs):
        if not callable(func):
            return

        if ttl is None:
            ttl = self.default_ttl

        token = gen_uuid32()
        interval = ttl // 4
        if interval < 1:
            interval = 1

        max_wait_in_sec = max_wait if max_wait is None else max_wait / 1000.0
        timer = RetryTimer(max_wait=max_wait_in_sec, interval=interval/1000.0)
        while timer.retry():
            try:
                self.lock(resource, action=action, token=token, ttl=ttl)
                return func(*func_args, **func_kwargs)
            except CRUDLocker.NeedRetry:
                continue
            finally:
                self.unlock(resource, action=action, token=token)

        raise CRUDLocker.Timeout

    def lock(self, resource, action='retrieve', token='', ttl=None):
        key = self.resource2key(resource)
        status = {
            "token": token,
            "action": action
        }
        status_json = json.dumps(status)

        if ttl is None:
            ttl = self.default_ttl

        if self._mark(resource, token):
            try:
                current_status = self.get_status(resource)
                if current_status is None or action in self.permitted_actions[current_status['action']]:
                    result = self.redis_connection.set(key, status_json, px=ttl)
                    if result is None:
                        raise CRUDLocker.CanNotLock

                    if action == 'delete':
                        self._delete_lru_record(resource)
                    else:
                        self._update_lru_record(resource)

                    return status
                else:
                    raise CRUDLocker.NeedRetry
            finally:
                self._unmark(resource, token)
        else:
            raise CRUDLocker.NeedRetry

    def unlock(self, resource, action='retrieve', token='', force=False):
        key = self.resource2key(resource)
        if force:
            self.redis_connection.delete(key)
            return

        if self._mark(resource, token):
            try:
                current_status = self.get_status(resource)
                if current_status is not None and (action == current_status['action'] and token == current_status['token']):
                    self.redis_connection.delete(key)
            finally:
                self._unmark(resource, token)

    def touch(self, resource):
        return self._update_lru_record(resource)

    def get_status(self, resource):
        contents = self.redis_connection.get(self.resource2key(resource))
        if contents is None:
            return None
        else:
            if six.PY3:
                contents = contents.decode('utf-8')
            return json.loads(contents, strict=False)

    def resource2key(self, resource):
        return '{}:{}:{}'.format(self.prefix, self.name, resource)

    def resource2mark(self, resource):
        return '{}:{}:{}'.format(self.mark_prefix, self.name, resource)

    def _mark(self, resource, token):
        interval = self.mark_ttl // 2
        if interval == 0:
            interval = 1
        timer = RetryTimer(max_wait=self.mark_max_wait/1000.0, interval=interval/1000.0)
        while timer.retry():
            try:
                mark_key = self.resource2mark(resource)
                result = self.redis_connection.set(mark_key, token, nx=True, px=self.mark_ttl)
                if result is not None:
                    return True
            except:
                continue
        return False

    def _unmark(self, resource, token):
        mark_key = self.resource2mark(resource)
        pttl = self.redis_connection.pttl(mark_key)
        if pttl == -2:
            # No mark
            return
        elif pttl == -1 or pttl >= self.unmark_safe_time:
            result = self.redis_connection.get(mark_key)
            if result is not None and six.PY3:
                result = result.decode('utf-8')
            if result == token:
                self.redis_connection.delete(mark_key)
        else:
            # Let the mark expires.
            pass

    def _update_lru_record(self, resource):
        if REDIS_VERSION[0] >= 3:
            self.redis_connection.zadd(self.lru_key, {resource: datetime.now().timestamp()})
        else:
            self.redis_connection.zadd(self.lru_key, resource, datetime.now().timestamp())

    def _delete_lru_record(self, resource):
        self.redis_connection.zrem(self.lru_key, resource)

    def lru_count(self):
        return self.redis_connection.zcard(self.lru_key)

    def lru_get_oldest(self, count=1):
        if count >= 1:
            count -= 1
        results = self.redis_connection.zrange(self.lru_key, 0, count)
        if six.PY3:
            results = [item.decode('utf-8') for item in results]

        return results

    def lru_reset(self):
        items = self.redis_connection.zrange(self.lru_key, 0, -1)
        self.redis_connection.zrem(self.lru_key, *items)
