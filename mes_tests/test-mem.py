import gc
from collections import namedtuple

TouchPt = namedtuple("TouchPt", ["id", "x", "y", "size","t"])

diff = 80
m0=gc.mem_alloc() ; m1=m0
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem2:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem3:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
l = [TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0),TouchPt(0,0,0,0,0)]

m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem2:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem3:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
l2 = l[0:2]
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem2:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem3:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
l2 = l[4:2]
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem2:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem3:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
l2 = l[7:2]
m=gc.mem_alloc(); print(f"Mem1:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem2:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
m=gc.mem_alloc(); print(f"Mem3:{m-m1:5d} / {m-m0:5d} / {m}") ; m1=m+diff
