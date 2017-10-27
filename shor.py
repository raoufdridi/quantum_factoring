import random
import math

class State(object):
    def __init__(self,clist):
        self.clist=clist

    def __repr__(self):
       return "State(%s)" % self.clist

    def __add__(self, other):
        if other==0: return self
        nst= State({})
        keys= set(self.clist.keys()).union(set(other.clist.keys()))
        for key in keys:
            nst.clist[key]= self.clist.get(key, 0)+ other.clist.get(key, 0)
            if nst.clist[key]==0: del nst.clist[key]
        return nst

    def __sub__(self, other):
        if other==0: return self
        nst= State({})
        keys= set(self.clist.keys()).union(set(other.clist.keys()))
        for key in keys:
            nst.clist[key]= self.clist.get(key, 0)- other.clist.get(key, 0)
            if nst.clist[key]==0: del nst.clist[key]
        return nst

    def __mul__(self, other):
        nst= State({})
        if other==0: return 0
        for key in set(self.clist.keys()):
            nst.clist[key]= self.clist.get(key)*other
            if nst.clist[key]==0: del nst.clist[key]
        return nst

    def __radd__(self, other):
        return self.__add__(other)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __rmul__(self, other):
        return self.__mul__(other)

    def measure_second_register(self):
        x=self.clist.keys()
        k= random.choice(x)[-2]
        for key in x:
            if key[-2] != k:
                del self.clist[key]


class UnitaryOperator(object):
    def __init__(self,clist):
        self.clist=clist

    def __repr__(self):
        return "UnitaryOperator(%s)" % self.clist

    def apply(self, st):
        if self.clist=={}: return st
        if str(st) in self.clist.keys(): return self.clist[str(st)]
        nst=0
        for key in st.clist.keys():
            nst= nst + self.clist.get(key, 0) * st.clist[key]
            return nst

###############
# Shor's algo #
###############

import numpy.fft

def nclist(N):
         clist ={}
         for i in range (0, N): clist[str([i, int(f(i))])]=1
         return clist
        
def QFT(st):
    keys =map(eval, st.clist.keys())
    nl =[0 for i in xrange(0, N)]
    for key in keys:
        nl[key[0]]=1
    return State(list(numpy.fft.fft(nl)))
# In quantum world QFT is implemented with 2-qubits gates

def amplitudes_peaks (st):
    l = st.clist
    def foo(c):
        return c.conjugate()*c
    res= map(foo, l)
    for i in xrange(0, len(res)-1):
        if not res[i]==0:
            print i

# Example: for this example, the first register uses t=11 qubits
# [see Nielsen - page  224 (eq 5.35)]
def f(i):
        return 7**i % 15

#################
# Grover's algo #       
#################
def nclist2(N):
         clist ={}
         for i in range (0, N): clist[str([i])]=1
         return clist

def foo(k):
        if k==14: return 1
        else: return 0
        
def oracle(st):
        keys = st.clist.keys()
        for key in keys:
                st.clist[key]=(-1)**foo(eval(key)[0])*st.clist[key]

N=50

st=1/math.sqrt(N)*State(nclist2(N))

G=UnitaryOperator({str(st):st})
for k in range(0,N):
                G.clist[str([k])]=State(nclist2(N))
Id = UnitaryOperator({})

for i in range(1,10):
        oracle(st)
        st=2*G.apply(st)-Id.apply(st)
