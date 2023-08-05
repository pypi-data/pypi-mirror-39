# -*- coding: utf-8 -*-
"""
@author: my.zhang
@time:   2018/11/27
@version:  
"""
from contextlib import contextmanager


class BulkInsert(object):
    def __init__(self, session, model, N):
        """
        Init insertion
        :param session: sqlalchemy db session
        :param model:   sqlalchemy db model
        :param N:       save batch size
        """
        self.data = []
        self.sess = session
        self.model = model
        self.N = N

    def _insert(self):
        self.sess.bulk_insert_mappings(self.model, self.data)
        self.sess.commit()

    def insert(self, item):
        if len(self.data) < self.N:
            self.data.append(item)
        else:
            self._insert()
            self.data = [item]

    def final_insert(self):
        self._insert()


@contextmanager
def bulk_insert(session, model, n=10000):
    bi = BulkInsert(session, model, n)
    yield bi
    bi.final_insert()
