# import math
# import autodif
# # f1 = "e*pi"
# # vd = "x:2,y:3,z:4"
# # F1 = autodif.AD(f1)
# # print(F1.val(vd))
# # print(F1.diff_all(vd))
# # print(F1.diff("x"))

# f1 = "pow(x,3)*y*y"
# vd = "x:2,y:3"
# F1 = autodif.AD(f1)
# F1.set_point(vd)
# ret = F1.symbolic_diff("x", order=2)
# print(ret)
# ret = F1.symbolic_diff("y")
# print(ret)

# AD
import math
class FD:
    def __init__(self, string, value, d_seed):
        self.value = value
        self.dual = d_seed
        self.string = string

    def __str__(self):
        return self.string

    def grad(self):
        return self.dual

    def __add__(self, other):
        n = str(self) + "+" + str(other)
        if not isinstance(other, FD):
            z = FD(n, self.value + other, self.dual)
            return z
        z = FD(n, self.value + other.value, self.dual + other.dual)
        return z

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        n = "(" + str(self) + ")" + "-(" + str(other) + ")"
        if not isinstance(other, FD):
            z = FD(n, self.value - other, self.dual)
            return z
        z = FD(n, self.value - other.value, self.dual - other.dual)
        return z

    def __rsub__(self, other):
        n = str(other) + "-(" + str(self) + ")"
        z = FD(n, other - self.value, -self.dual)
        return z

    def __mul__(self, other):
        n = "(" + str(self) + ")" + "*(" + str(other) + ")"
        if not isinstance(other, FD):
            z = FD(n, self.value * other, self.dual*other)
            return z
        z = FD(n, self.value * other.value, self.value*other.dual + self.dual*other.value)
        return z
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        n = "(" + str(self) + ")" + "/(" + str(other) + ")"
        if not isinstance(other, FD):
            z = FD(n, self.value / other, self.dual/other)
            return z
        z = FD(n, self.value / other.value, (other.value*self.dual - self.value*other.dual)/(other.value**2))
        return z

    def __rtruediv__(self, other):
        n = str(other) + "/" + str(self)
        z = FD(n, other / self.value, -other*self.dual / self.value**2)
        return z

    def __pow__(self, other):
        n = "POW(" + str(self) + "," + str(other) + ")"
        if not isinstance(other, FD):
            z = FD(n, self.value ** other, other*self.value**(other-1)*self.dual)
            return z
        nd = (self.value**other.value) * ((other.value/self.value*self.dual) + (other.dual * math.log(self.value)))
        z = FD(n, self.value ** other.value, nd)
        return z

    def __rpow__(self, other):
        n = "POW(" + str(other) + "," + str(self) + ")"
        z = FD(n, other ** self.value, self.dual*math.log(other)*other**self.value)
        return z

def sin(x):
    if not isinstance(x, FD):
        return math.sin(x)
    n = "SIN(" + str(x) + ")"
    z = FD(n, math.sin(x.value), x.dual*math.cos(x.value))
    return z

'''
x = FD("x", 2, 0)
y = FD("y", 3, 0)
z = FD("z", 4, 1)
d = x*(x**y**z)/(y*z-x+z)

d.grad_value = 1.0

print(str(d))
print(d.grad())
'''
