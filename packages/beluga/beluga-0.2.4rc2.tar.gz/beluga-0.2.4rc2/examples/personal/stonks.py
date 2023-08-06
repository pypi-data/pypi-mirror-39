from math import floor
import code
from matplotlib import pyplot as plt
import copy

flt = [1.2e9]
mktcap = 50e9
eps = [12]
sp = [mktcap/flt[-1]]
perq = 2.5e9

accel = 0.0

n = 36

m = 300
month = [-1]

for ii in range(n):
    flt.append(floor(flt[-1] - perq/sp[-1]/3))
    sp.append(mktcap/flt[-1])
    eps.append(sp[-1]/sp[-2]*eps[-1]*(accel/12 + 1))
    perq = perq*eps[-1]/eps[-2]
    month.append(ii)

month = [_+1 for _ in month]

plt.plot(month, sp)
plt.show()

code.interact(local=locals())

