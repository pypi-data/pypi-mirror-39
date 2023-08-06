import AD.interpreter as ast
import sympy

class SD():
    """
    User friendly interface for the AST interpreter.
    """

    def __init__(self, frmla):
        self.formula = frmla
        self.lexer = ast.Lexer(frmla)
        self.parser = ast.Parser(self.lexer)
        self.interpreter = ast.Interpreter(self.parser)
        self.vd = None

    def set_point(self, vd):
        """
        sets the point to derive at
        """
        if vd is not None:
            self.vd = vd
        if self.vd is None:
            raise NameError("Must set point to evaluate")
    
    def diff(self, dv, vd=None, order=1):
        """
        returns numeric derivative with respect to variable dv
        vd is used to set a new point
        order is the order of the derivative to take
        """
        self.set_point(vd)
        new_interpreter = self.interpreter
        for i in range(order-1):
            new_frmla = new_interpreter.symbolic_diff(self.vd, dv)
            new_lexer = ast.Lexer(new_frmla)
            new_parser = ast.Parser(new_lexer)
            new_interpreter = ast.Interpreter(new_parser)
        return new_interpreter.differentiate(self.vd, dv)
    
    def symbolic_diff(self, dv, vd=None, order=1, output='default'):
        """
        returns symbolic derivative with respect to variable dv
        vd is used to set a new point
        order is the order of the derivative to take
        """
        self.set_point(vd)
        new_interpreter = self.interpreter
        for i in range(order-1):
            new_frmla = new_interpreter.symbolic_diff(self.vd, dv)
            new_lexer = ast.Lexer(new_frmla)
            new_parser = ast.Parser(new_lexer)
            new_interpreter = ast.Interpreter(new_parser)
        formul = new_interpreter.symbolic_diff(self.vd, dv)
        simplified = self.symplify(formul, output)
        return simplified
    
    def diff_all(self, vd=None):
        """
        returns numeric derivative of all variables
        """
        self.set_point(vd)
        return self.interpreter.diff_all(self.vd)
    
    def val(self, vd=None):
        """
        returns the value of the function at the point
        """
        self.set_point(vd)
        return self.interpreter.interpret(self.vd)
    
    def new_formula(self, frmla):
        """
        sets a new formula for the object
        """
        self.formula = frmla
        self.lexer = ast.Lexer(frmla)
        self.parser = ast.Parser(self.lexer)
        self.interpreter = ast.Interpreter(self.parser)
        self.vd = None

    def symplify(self, formul, output):
        """ simplifies a formula string, output changes output format """
        def POW(a, b):
            return a ** b
            
        def EXP(a):
            return sympy.exp(a)
            
        def LOG(a):
            return sympy.log(a)
            
        def COS(a):
            return sympy.cos(a)
            
        def SIN(a):
            return sympy.sin(a)
            
        def TAN(a): # Tangent Function
            return sympy.tan(a)

        def SINH(a): # Inverse trigonometric functions: inverse sine or arcsine
            return sympy.sinh(a)
            
        def COSH(a): # Inverse trigonometric functions: inverse cosine or arccosine    
            return sympy.cosh(a)
            
        def TANH(a): # Inverse trigonometric functions: inverse tangent or arctangent    
            return sympy.tanh(a)
        
        def ARCSIN(a): # Inverse trigonometric functions: inverse sine or arcsine    
            return sympy.asin(a)
        def ARCCOS(a): # Inverse trigonometric functions: inverse cosine or arccosine    
            return sympy.acos(a)
        def ARCTAN(a): # Inverse trigonometric functions: inverse tangent or arctangent    
            return sympy.atan(a)
        
        string_for_sympy=""
        string_for_sympy2=""
        split_variables=self.vd.split(",")
        
        for var in split_variables:
            l=var.split(":")
            string_for_sympy=string_for_sympy+l[0]+" "	
            string_for_sympy2=string_for_sympy2+l[0]+", "
            
        exec(string_for_sympy2[:-2] + "= sympy.symbols('" + string_for_sympy+ "')")
            
        if output == 'default':
            return sympy.simplify(eval(formul))
            
        if output == 'latex':
            return sympy.latex(sympy.simplify(eval(formul)))
            
        if output == 'pretty':
            sympy.pprint(sympy.simplify(eval(formul)))
            return sympy.simplify(eval(formul))
            
        if output == 'all':
            print('\nSymbolic differentiation result:')
            print(formul)
            print('\nSimplified Pretty Print:\n') ; sympy.pprint(sympy.simplify(eval(formul)))
            print('\nSimplified Latex code:')
            print(sympy.latex(sympy.simplify(eval(formul))))
            print('\nSimplified Default:')
            print(sympy.simplify(eval(formul)),'\n')
            return sympy.simplify(eval(formul))
