# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Func timer
count func time with decorator

Usage:
    @do_time()
    def do_print():
        print len([x for x in xrange(10000)])

    class A(object):
        @do_time(func=False)
        def do_print(self):
            print len([x for x in xrange(10000)])
"""


from logging import warning
from functools import wraps
from time import time


def do_class_time(method):
    """Get the given class function time"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        start_time = time()
        try:
            return method(self, *args, **kwargs)
        finally:
            spend = round(1000 * (time() - start_time), 3)
            warning('方法: {_class}.{func}, 消耗: {spend} ms'.format(
                    _class=self.__class__.__name__, func=method.__name__, spend=spend))

    return wrapper


def do_func_time(method):
    """Get the given function time"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time()
        try:
            return method(*args, **kwargs)
        finally:
            spend = round(1000 * (time() - start_time), 3)
            warning('方法: {func}, 消耗: {spend} ms'.format(
                    func=method.__name__, spend=spend))

    return wrapper


def do_time(func=True):
    """Default to get function time
    otherwise if func is False then get the class function time.
    :param func: if the method is a class function or a normal function
    """
    return do_func_time if func else do_class_time


@do_time()
def do_print():
    print len([x for x in xrange(10000)])


class A(object):
    @do_time(func=False)
    def do_print(self):
        print len([x for x in xrange(10000)])


if __name__ == '__main__':
    do_print()
    a = A()
    a.do_print()


__all__ = ['do_time']
