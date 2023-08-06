import math

print('Importing Reverse Mode Automatic Differentiation')

class Var:
    """
    Var class used for reverse AD
    If derivative doesn't exist at a point for one of the variables, forward AD should be used
    """
    def __init__(self, name, value):
        self.value = value
        self.children = []
        self.grad_value = None
        self.name = name

    def __str__(self):
        """ returns the string of the formula """
        return self.name

    def grad(self):
        """ returns the gradient of the formula with respect to the variable """
        if self.grad_value is None:
            self.grad_value = sum(val * var.grad() for val, var in self.children)
        return self.grad_value

    def __add__(self, other):
        """ adds the vars, returns a new formula and appens children to the variables """
        n = str(self) + "+" + str(other)
        if not isinstance(other, Var):
            z = Var(n, self.value + other)
            self.children.append((1.0, z))
            return z
        z = Var(n, self.value + other.value)
        other.children.append((1.0, z))
        self.children.append((1.0, z))
        return z

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        """ subtracts the vars, returns a new formula and appens children to the variables """
        n = "(" + str(self) + ")" + "-(" + str(other) + ")"
        if not isinstance(other, Var):
            z = Var(n, self.value - other)
            self.children.append((1.0, z))
            return z
        z = Var(n, self.value - other.value)
        self.children.append((1.0, z))
        other.children.append((-1.0, z))
        return z

    def __rsub__(self, other):
        n = str(other) + "-(" + str(self) + ")"
        z = Var(n, other - self.value)
        self.children.append((-1.0, z))
        return z

    def __mul__(self, other):
        """ multiply the vars, returns a new formula and appens children to the variables """
        n = "(" + str(self) + ")" + "*(" + str(other) + ")"
        if not isinstance(other, Var):
            z = Var(n, self.value * other)
            self.children.append((other, z))
            return z
        z = Var(n, self.value * other.value)
        self.children.append((other.value, z))
        other.children.append((self.value, z))
        return z
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """ divides the vars, returns a new formula and appens children to the variables """
        n = "(" + str(self) + ")" + "/(" + str(other) + ")"
        if not isinstance(other, Var):
            z = Var(n, self.value / other)
            self.children.append((1/other, z))
            return z
        z = Var(n, self.value / other.value)
        self.children.append((1/other.value, z))
        other.children.append((-self.value/other.value**2, z))
        return z

    def __rtruediv__(self, other):
        n = str(other) + "/" + str(self)
        z = Var(n, other / self.value)
        self.children.append((-other/self.value**2, z))
        return z

    def __pow__(self, other):
        """ exponentiates the vars, returns a new formula and appens children to the variables """
        n = "POW(" + str(self) + "," + str(other) + ")"
        if not isinstance(other, Var):
            z = Var(n, self.value ** other)
            self.children.append((other*self.value**(other-1), z))
            return z
        z = Var(n, self.value ** other.value)
        self.children.append((other.value*self.value**(other.value-1), z))
        other.children.append((math.log(self.value)*self.value**other.value,z))
        return z

    def __rpow__(self, other):
        n = "POW(" + str(other) + "," + str(self) + ")"
        z = Var(n, other ** self.value)
        self.children.append((math.log(other)*other**self.value,z))
        return z

def sin(x):
    """ calculates sin of the formula/var x """
    if not isinstance(x, Var):
        print('Bingo')
        return math.sin(x)
    n = "sin(" + str(x) + ")"
    z = Var(n, math.sin(x.value))
    x.children.append((math.cos(x.value), z))
    return z

def cos(x):
    """ calculates cos of the formula/var x """
    if not isinstance(x, Var):
        return math.cos(x)
    n = "cos(" + str(x) + ")"
    z = Var(n, math.cos(x.value))
    x.children.append((-math.sin(x.value), z))
    return z

def tan(x):
    """ calculates tan of the formula/var x """
    if not isinstance(x, Var):
        return math.tan(x)
    n = "tan(" + str(x) + ")"
    z = Var(n, math.tan(x.value))
    x.children.append((1.0+math.tan(x.value)**2, z))
    return z

def sqrt(x):
    """ calculates sqrt of the formula/var x """
    if not isinstance(x, Var):
        return math.sqrt(x)
    n = "sqrt(" + str(x) + ")"
    z = Var(n, math.sqrt(x.value))
    x.children.append((0.5/(x.value)**0.5, z))
    return z

def ln(x):
    """ calculates ln of the formula/var x """
    if not isinstance(x, Var):
        return math.log(x)
    n = "ln(" + str(x) + ")"
    z = Var(n, math.log(x.value))
    x.children.append((1.0/x.value, z))
    return z    
    
def log(x, base):
    """ calculates log(x, base) of the formula/var x """
    if not isinstance(x, Var):
        return math.log(x)/math.log(base)
    n = "ln(" + str(x) + ")/ln(" + str(base) + ")"
    z = Var(n, math.log(x.value,base))
    x.children.append((1.0/(x.value*math.log(base)), z))
    return z

def arcsin(x):
    """ calculates arcsin of the formula/var x """
    if not isinstance(x, Var):
        return math.asin(x)
    n = "arcsin(" + str(x) + ")"
    z = Var(n, math.asin(x.value))
    x.children.append((1.0/math.sqrt(1.0-x.value**2), z))
    return z

def arccos(x):
    """ calculates arccos of the formula/var x """
    if not isinstance(x, Var):
        return math.acos(x)
    n = "arccos(" + str(x) + ")"
    z = Var(n, math.acos(x.value))
    x.children.append((-1.0/math.sqrt(1.0-x.value**2), z))
    return z

def arctan(x):
    """ calculates arctan of the formula/var x """
    if not isinstance(x, Var):
        return math.atan(x)
    n = "arctan(" + str(x) + ")"
    z = Var(n, math.atan(x.value))
    x.children.append((1.0/(1.0+x.value**2), z))
    return z

def sinh(x):
    """ calculates sinh of the formula/var x """
    if not isinstance(x, Var):
        return math.sinh(x)
    n = "sinh(" + str(x) + ")"
    z = Var(n, math.sinh(x.value))
    x.children.append((math.cosh(x.value), z))
    return z

def cosh(x):
    """ calculates cosh of the formula/var x """
    if not isinstance(x, Var):
        return math.cosh(x)
    n = "cosh(" + str(x) + ")"
    z = Var(n, math.cosh(x.value))
    x.children.append((math.sinh(x.value), z))
    return z

def tanh(x):
    """ calculates tanh of the formula/var x """
    if not isinstance(x, Var):
        return math.tanh(x)
    n = "tanh(" + str(x) + ")"
    z = Var(n, math.tanh(x.value))
    x.children.append((1.0-math.tanh(x.value)**2, z))
    return z
