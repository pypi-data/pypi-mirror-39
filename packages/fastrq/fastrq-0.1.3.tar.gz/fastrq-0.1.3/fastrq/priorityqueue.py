from __future__ import absolute_import

from .base import Base
from .loader import load


class PriorityQueue(Base):
    def __len__(self):
        return self.connect().zcard(self._key)
    
    def push(self, values):
        script = load('priority_queue_push')
        return self._run_lua_script(script, (self._key,), self._makevalues(values))
    
    def push_ni(self, member, score):
        """ Push only if the member not inside the queue
        """
        script = load('priority_queue_push_not_in')
        rs = self._run_lua_script(script, (self._key,), (score, member))
        print('pq-push-ni', rs)
        return [rs[0], bool(rs[1])] if isinstance(rs, list) else rs
    
    def pop(self, count=1):
        script = load('priority_queue_pop')
        p = self._run_lua_script(script, (self._key,), (count,))
        r = self._makereturn(p)
        return r if count > 1 else (r[0] if len(r) > 0 else None)
    
    def range(self, low_score='-inf', high_score='+inf'):
        return self.connect().zrangebyscore(self._key, low_score, high_score, None, None, True, int)

    def indexofone(self, member):
        script = load('priority_queue_indexof')
        r = self._run_lua_script(script, [self._key], [member])
        return None if r[0] == -1 else r[0]

    def indexofmany(self, members):
        script = load('priority_queue_indexof')
        indexes = {}
        r = self._run_lua_script(script, [self._key], members)
        for i, m in enumerate(members):
            indexes[m] = None if r[i] == -1 else r[i]
        return indexes
    
    def _makevalues(self, values):
        vl = []
        for key in values:
            vl += [values[key], key]
        return vl
    
    def _makereturn(self, raw):
        r = []
        for i in range(0, len(raw)):
            if i % 2 == 0:
                r.append(
                    (raw[i], int(raw[i + 1]))
                )
        return r


class CappedPriorityQueue(PriorityQueue):
    def __init__(self, key, cap):
        super(CappedPriorityQueue, self).__init__(key)
        self._cap = cap
    
    def push(self, values):
        script = load('capped_priority_queue_push')
        return self._run_lua_script(script, (self._key,), [self._cap] + self._makevalues(values))
    
    def push_ni(self, member, score):
        """ Push only if the member not inside the queue
        """
        script = load('capped_priority_queue_push_not_in')
        rs = self._run_lua_script(script, (self._key,), (self._cap, score, member))
        return [rs[0], bool(rs[1])] if isinstance(rs, list) else rs
    

class OfCappedPriorityQueue(CappedPriorityQueue):
    def push(self, values):
        script = load('of_capped_priority_queue_push')
        p = self._run_lua_script(script, (self._key,), [self._cap] + self._makevalues(values))
        return [p[0], self._makereturn(p[1])]

    def push_ni(self, member, score):
        """ Push only if the member not inside the queue
        """
        script = load('of_capped_priority_queue_push_not_in')
        rs = self._run_lua_script(script, (self._key,), (self._cap, score, member))
        return [rs[0], self._makereturn(rs[1]), bool(rs[2])] if isinstance(rs, list) else rs

