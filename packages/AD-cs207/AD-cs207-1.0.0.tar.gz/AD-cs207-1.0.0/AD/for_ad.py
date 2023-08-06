import math
class FD:
    """ implementation of forward AD using dual numbers """
    def __init__(self, string, value, d_seed):
        self.value = value
        self.dual = d_seed
        self.string = string

    def __str__(self):
        """ returns the string value of the function """
        return self.string

    def grad(self):
        """ returns the derivative of the function based on seed """
        return self.dual

    """ Implementation of operators using operator overloading """
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
    
    """ implement unary operations for forward div """
    def sin(x):
        if not isinstance(x, FD):
            return math.sin(x)
        n = "SIN(" + str(x) + ")"
        z = FD(n, math.sin(x.value), x.dual*math.cos(x.value))
        return z
    
    def cos(x):
        if not isinstance(x, FD):
            return math.cos(x)
        n = "COS(" + str(x) + ")"
        z = FD(n, math.cos(x.value), -x.dual*math.sin(x.value))
        return z

    def tan(x):
        if not isinstance(x, FD):
            return math.tan(x)
        n = "TAN(" + str(x) + ")"
        z = FD(n, math.tan(x.value), x.dual/(math.cos(x.value)**2))
        return z
    
    def ln(x):
        if not isinstance(x, FD):
          return math.log(x)
        n = "ln(" + str(x) + ")"
        z = FD(n, math.log(x.value), x.dual/x.value)
        return z
    
    def log(x, base):
        if not isinstance(x, FD):
          return math.log(x,base)
        n = "log(" + str(x) + ")/log(" + str(base) + ")"
        z = FD(n, math.log(x.value)/math.log(base), x.dual/(x.value*math.log(base)) )
        return z
        
    def arcsin(x):
        if not isinstance(x, FD):
          return math.asin(x)
        n = "arcsin(" + str(x) + ")"
        z = FD(n, math.asin(x.value), x.dual/math.sqrt(1.0-x.value**2))
        return z
    
    def arccos(x):
        if not isinstance(x, FD):
          return math.acos(x)
        n = "arccos(" + str(x) + ")"
        z = FD(n, math.acos(x.value), -1.0*x.dual/math.sqrt(1.0-x.value**2))
        return z

    def arctan(x):
        if not isinstance(x, FD):
          return math.atan(x)
        n = "arctan(" + str(x) + ")"
        z = FD(n, math.atan(x.value), x.dual/(1.0+x.value**2))
        return z
    
    def sinh(x):
        if not isinstance(x, FD):
          return math.sinh(x)
        n = "sinh(" + str(x) + ")"
        z = FD(n, math.sinh(x.value), x.dual*math.cosh(x.value))
        return z

    def cosh(x):
        if not isinstance(x, FD):
          return math.cosh(x)
        n = "cosh(" + str(x) + ")"
        z = FD(n, math.cosh(x.value), x.dual*math.sinh(x.value))
        return z
    
    def tanh(x):
        if not isinstance(x, FD):
          return math.tanh(x)
        n = "tanh(" + str(x) + ")"
        z = FD(n, math.tanh(x.value), x.dual*(1.0-math.tanh(x.value)**2))
        return z
    
    def sqrt(x):
        if not isinstance(x, FD):
          return math.sqrt(x)
        n = "sqrt(" + str(x) + ")"
        z = FD(n, math.sqrt(x.value), 0.5*x.dual/math.sqrt(x.value) )
        return z
       
