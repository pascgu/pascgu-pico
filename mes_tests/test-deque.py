import gc
from collections import deque
from utime import ticks_us, ticks_diff

class Control:
    def __init__(self,x) -> None:
        self.x = x
    def __str__(self):
        return f"C({self.x})"
    def __repr__(self):
        return f"C({self.x})"

diff = 80
m0=gc.mem_alloc() ; m1=m0
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem2:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem3:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
dq = deque((),10)

m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
a = Control(1)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
dq.append(a)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(2)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(3)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(4)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(5)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(6)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(7)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(8)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(9)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
b = Control(10)
dq.append(b)
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
if a in dq:
    m=gc.mem_alloc(); print(f"OK  :{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
else:
    m=gc.mem_alloc(); print(f"Fail:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
if b in dq:
    m=gc.mem_alloc(); print(f"OK  :{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
else:
    m=gc.mem_alloc(); print(f"Fail:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
print(list(dq))
b = Control(11)
dq.append(b)
print(list(dq))
if a in dq:
    m=gc.mem_alloc(); print(f"OK") ; m1=m+diff
else:
    m=gc.mem_alloc(); print(f"Fail") ; m1=m+diff



print()

dq = deque((),1000)
for i in range(1000):
    dq.append(Control(i))

last_t_us = ticks_us()
x = a in dq
t_us = ticks_us()
diff = ticks_diff(t_us, last_t_us)

print(f"a in deque ({len(dq)}): {x} in {diff} us")

l = list(dq)
print("list",l[0:3])

last_t_us = ticks_us()
x = a in l
t_us = ticks_us()
diff = ticks_diff(t_us, last_t_us)

print(f"a in list ({len(l)}): {x} in {diff} us")


dq = deque((),5)
dq.append(Control(1))
dq.append(Control(2))
print("list",list(dq))
while dq: # on s'arrête bien quand la liste est vide
    print(f"item",dq.popleft())