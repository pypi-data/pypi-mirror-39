from collections import namedtuple, OrderedDict, Counter
from time import clock


dic = OrderedDict()
lst = list()
pos = list()
t1 = clock()
for i in xrange(1000000):
    dic[i] = i
t2 = clock()
for i in xrange(1000000):
    lst.append(i)
pos = list(xrange(len(lst)))
t3 = clock()

for v in dic.values():
    pass
t4 = clock()
for v in lst:
    pass
t5 = clock()

print t5-t4, t4-t3, t3-t2, t2-t1
