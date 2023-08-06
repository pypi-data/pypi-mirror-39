from beluga.liepack.domain.liealgebras import so, rn
from beluga.liepack import Adjoint, Commutator, dexpinv, exp
from beluga.utils import Bernoulli
import numpy as np

x = so(3)
y = so(3)
z = so(3)

x.set_vector([0,0.025,0])
y.set_vector([0.000625,1,-0.025])

print(x.data)
print(y.data)
print(dexpinv(x,y,order=3).data)

# X = exp(y*np.pi/2)
# print(x.get_vector())
# print(X.data)
#
# Ad = Adjoint(X)
#
# print(Ad(x).get_vector())

# y.set_vector([0,1,0,1])

# print((x*y).get_vector())

