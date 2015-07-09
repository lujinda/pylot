#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-07-08 12:54:28
# Filename      : psql.py
# Description   : 
import psycopg2
from psycopg2 import extras
import logging

sql_log = logging.getLogger('psql')

def config_logging():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(filename)s:%(lineno)s %(message)s')
    handler.setFormatter(formatter)
    sql_log.addHandler(handler)
    sql_log.setLevel(logging.DEBUG)


class Record(object):
    def __init__(self, _cur):
        self._cur = _cur

    def __iter__(self):
        while True:
            record = self.next()
            if not record:
                break
            else:
                yield record

    def next(self):
        return self._cur.fetchone()

class PsqlTable(object):
    def __init__(self, table_name, conn = None, cur = None, debug = False): # conn是指psql的connect产生的对象
        self.table_name = table_name
        self._cur = cur or conn.cursor()
        self.debug = debug

    def find(self, cond = None, column = None, **ext_kwargs):
        cond = cond or {}
        column = column or []
        assert isinstance(cond, dict) and isinstance(column, (list, tuple))
        column_string = self.__cat_column_string(column)
        cond_string = self.__cat_cond_string(cond)
        ext_string = self.__cat_ext_string(**ext_kwargs)
        sql_string = "SELECT {column} FROM {table_name} ".format(
                column = column_string, table_name = self.table_name)
        if cond:
            sql_string += 'WHERE %s ' %(cond_string)
        sql_string += ext_string

        self.execute_sql(sql_string)
        return Record(self._cur)

    def find_one(self, *args, **kwargs):
        record_iter = self.find(*args, **kwargs)
        record = record_iter.next() or {}
        del record_iter
        return record

    def update(self, set_value, cond = None, returning = None):
        """这里比较low，只允许简单的update set， 跟mongodb不同的是，条件在后面[]"""
        cond = cond or {}
        assert isinstance(cond, dict) and isinstance(set_value, dict)
        set_string = self.__cat_set_string(set_value)
        cond_string = self.__cat_cond_string(cond)
        sql_string = 'UPDATE ' + self.table_name + ' set ' + set_string
        if cond:
            sql_string += ' WHERE ' + cond_string

        return self.execute_sql(sql_string, returning)

    def remove(self, cond = None, returning = None):
        cond = cond  or {}
        sql_string = 'DELETE FROM ' + self.table_name
        cond_string = self.__cat_cond_string(cond)
        if cond:
            sql_string += ' WHERE ' + cond_string

        return self.execute_sql(sql_string, returning)

    def insert(self, record_list, returning = None):
        """returning 可以接受一个列表，表示insert后要返回的字段，空列表表示返回所有字段"""
        result = []
        if isinstance(record_list, dict):
            record_list = [record_list]
        for record in record_list:
            sql_string = 'INSERT INTO ' + self.table_name + ' ('
            sql_string += ', '.join(record.keys()) + ') VALUES('
            sql_string += ', '.join(["%({})s".format(k) for k in record.keys()]) + ') '
            sql_string = self._cur.mogrify(sql_string, record)
            result.append(self.execute_sql(sql_string, returning))

        if len(result) == 1:
            return result[0]
        return result

    def __cat_set_string(self, set_value):
        _set_list = []
        for _k, _v in set_value.items():
            _set_list.append(self._cur.mogrify('{name}=%({name})s'.format(
                name = _k), {_k: _v}))

        return ', '.join(_set_list)

    def __cat_ext_string(self, **ext):
        if not ext:
            return ''
        _ext_list = []
        for _k, _v in ext.items():
            _k = _k.replace('_', ' ').upper()
            _ext_list.append("%s %s" %(_k, _v))

        return ' '.join(_ext_list)

    def execute_sql(self, sql, returning = None):
        if isinstance(returning, list):
            sql += ' RETURNING ' + (returning and ', '.join(returning) or '*')

        if sql[-1] != ';':
            sql += ';'

        if self.debug:
            sql_log.debug(sql)
        self._cur.execute(sql)

        if returning == None:
            return

        return_data = self._cur.fetchall()
        if not return_data:
            return {}

        if len(return_data) == 1:
            return return_data[0]

        return return_data

    def __cat_column_string(self, column):
        if column == []:
            return '*'
        return ', '.join(column)

    def __cat_cond_string(self, cond):
        _cond = ''
        for _k, _v in cond.items():
            if _k[0] == '$':
                _conn_opera = _k[1:].upper()
                _sub_cond_string = ''
                for _sub_cond in _v:
                    _sub_cond_string += (_sub_cond_string and " %s " % _conn_opera or '') + self.__cat_cond_string(_sub_cond)
                _cond += '(' + _sub_cond_string + ')'

            else:
                _cond += (_cond and ' AND ' or '') + self.__made_real(_k, _v)

        return _cond

    def __made_real(self, key, value, opera = 'eq'): # 产生关系表达式，像xx = yy或xx > yy这样的
        _real = ''
        all_real_opera = {'eq': '=', 'in': 'IN', 'not': 'NOT', 'gt': '>', 'gte': '>=', 'ne': '!=', 
                'lt': '<', 'lte': '<='}
        opera = all_real_opera.get(opera.lower())
        if isinstance(value, dict):
            for _k, _v in value.items():
                assert _k[0] == '$'
                _real_opera = _k[1:]
                _real += (_real and ' AND ' or '') + self.__made_real(key, _v, _real_opera)
        else:
            if isinstance(value, list):
                value = tuple(value)
            _real = (_real and ' AND ' or '') + self._cur.mogrify("{name} {real_opera} %({name})s".format(
                name = key, real_opera = opera), {key: value})

        return _real

class Cursor(object): 
    def __init__(self, cur, debug): 
        self._cur = cur
        self.debug = debug

    def __getattr__(self, name):
        if name in dir(self._cur):
            return getattr(self._cur, name)
        else:
            return PsqlTable(name, cur = self._cur, debug = self.debug)

    def __getitem__(self, name):
        return self.__getattr__(name)

    
class PsqlConnection(object):
    _conn = None
    def __init__(self, *args, **kwargs):
        self.args = args
        kwargs.setdefault('cursor_factory', extras.RealDictCursor)
        self.kwargs = kwargs
        self.debug = kwargs.pop('debug', False)
        if self.debug:
            config_logging()
    
    @property
    def __conn(self):
        if self._conn == None or self._conn.closed:
            self._conn = self.made_connect()

        return self._conn

    def made_connect(self):
        conn = psycopg2.connect(*self.args, **self.kwargs)
        print('psql connect')
        return conn

    def __getattr__(self, name): 
        if name in dir(self.__conn):
            return getattr(self.__conn, name)
        else:
            return PsqlTable(name, conn = self.__conn, debug = self.debug)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def cursor(self, *args, **kwargs):
        return Cursor(self.__conn.cursor(*args, **kwargs),
                self.debug)

