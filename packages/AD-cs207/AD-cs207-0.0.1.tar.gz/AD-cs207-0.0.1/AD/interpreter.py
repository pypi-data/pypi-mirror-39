""" SPI - Simple Pascal Interpreter """
import copy
import math
import unicodedata
###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, VAR, COS, SIN, EXP,POW, LOG, COMMA, TAN, ARCSIN, ARCCOS, ARCTAN, SINH, COSH, TANH = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'VAR', 'COS', 'SIN', 'EXP', 'POW', 'LOG', ',', 'TAN', 'ARCSIN', 'ARCCOS', 'ARCTAN', 'SINH', 'COSH', 'TANH'
)

def is_number(s):
    """ checks if passed in variable is a float """
    try:
        float(s)
        return True
    except:
        pass
    return False

# Inputted strings are broken down into tokens by Lexer
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Lexer takes a string and parses it into tokens
class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise NameError('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """ Skips any spaces """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) float consumed from the input."""
        index = 1
        cur = self.text[self.pos:self.pos+index]
        while(True):
            rem = len(self.text) - self.pos - index
            if rem > 2:
                a = cur + self.text[self.pos+index:self.pos+index+1]
                b = cur + self.text[self.pos+index:self.pos+index+2]
                c = cur + self.text[self.pos+index:self.pos+index+3]
            elif rem > 1:
                a = cur + self.text[self.pos+index:self.pos+index+1]
                b = cur + self.text[self.pos+index:self.pos+index+2]
                c = None
            elif rem > 0:
                a = cur + self.text[self.pos+index:self.pos+index+1]
                b = None
                c = None
            else:
                while index > 0:
                    self.advance()
                    index -= 1
                return float(cur)
            if is_number(c):
                # handles 1e-1
                cur = c
                index += 3
            elif is_number(b):
                # handles 1e1 / 1.1
                cur = b
                index += 2
            elif is_number(a):
                cur = a
                index += 1
            else:
                while index > 0:
                    self.advance()
                    index -= 1
                return float(cur)

    def word(self):
        """Return a multichar integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == ".":
                return Token(INTEGER, self.integer())
            
            # parse constants and constants
            if self.current_char.isalpha():
                wo = self.word()
                w = wo.upper()
                if(w == "E"):
                    return Token(INTEGER, math.e)
                elif(w == "PI"):
                    return Token(INTEGER, math.pi)
                elif(w == "COS"):
                    return Token(COS, self.word())
                elif(w == "SIN"):
                    return Token(SIN, self.word())
                elif(w == "EXP"):
                    return Token(EXP, self.word())
                elif(w == "POW"):
                    return Token(POW, self.word())
                elif(w == "LOG"):
                    return Token(LOG, self.word())
                elif(w == "TAN"):
                    return Token(TAN, self.word())
                elif(w == "ARCSIN"):
                    return Token(ARCSIN, self.word())
                elif(w == "ARCCOS"):
                    return Token(ARCCOS, self.word())
                elif(w == "ARCTAN"):
                    return Token(ARCTAN, self.word())
                elif(w == "SINH"):
                    return Token(SINH, self.word())
                elif(w == "COSH"):
                    return Token(COSH, self.word())
                elif(w == "TANH"):
                    return Token(TANH, self.word())
                else:
                    return Token(VAR, wo)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################
# AST objects combine tokens into an abstract syntax tree
class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

# parses tokens generated by a lexer to create an abstract syntax tree
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise NameError('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
            
    # parses "factors" which are defined using the context free grammer in the docstring
    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | VAR | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == VAR:
            self.eat(VAR)
            return Var(token)
        elif token.type == COS:
            self.eat(COS)
            self.eat(LPAREN)
            x = self.expr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node
        elif token.type == SIN:
            self.eat(SIN)
            self.eat(LPAREN)
            x = self.expr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node
        elif token.type == EXP:
            self.eat(EXP)
            self.eat(LPAREN)
            x = self.expr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node
        elif token.type == POW:
            self.eat(POW)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(COMMA)
            y = self.expr()
            self.eat(RPAREN)
            return BinOp(left = x, op = token, right = y)
        elif token.type == LOG:
            self.eat(LOG)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == TAN:
            self.eat(TAN)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == ARCSIN:
            self.eat(ARCSIN)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == ARCCOS:
            self.eat(ARCCOS)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == ARCTAN:
            self.eat(ARCTAN)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == SINH:
            self.eat(SINH)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == COSH:
            self.eat(COSH)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == TANH:
            self.eat(TANH)
            self.eat(LPAREN)
            x = self.expr()
            self.eat(RPAREN)
            return UnaryOp(token, x)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            raise NameError('Invalid character')

    # parses terms defined with the context free grammar in the docstring
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node
    
    # parses exprs defined with the context free grammar in the docstring
    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    # parses the lexer to return an abstract syntax tree
    def parse(self):
        node = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return node

    # similar to factor, but returns the symbolic derivative of a factor
    def dfactor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | VAR | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            x, dx = self.dfactor()
            node = UnaryOp(token, x)
            dnode = UnaryOp(token, dx)
            return node, dnode
        elif token.type == MINUS:
            self.eat(MINUS)
            x, dx = self.dfactor()
            node = UnaryOp(token, x)
            dnode = UnaryOp(token, dx)
            return node, dnode
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token), Num(Token(INTEGER, 0))
        elif token.type == VAR:
            self.eat(VAR)
            return Var(token), Var(Token(VAR, "d_" + token.value))
        elif token.type == COS:
            self.eat(COS)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node,  BinOp(left = UnaryOp(Token(MINUS, "-"), UnaryOp(Token(SIN, "sin"), x)), op=Token(MUL,'*'), right=dx)
        elif token.type == SIN:
            self.eat(SIN)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = UnaryOp(Token(COS, "cos"), x), op=Token(MUL,'*'), right=dx)
        elif token.type == TAN:
            self.eat(TAN)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left =  BinOp(left = Num(Token(INTEGER, 1)), op = Token(PLUS, '+'),right = BinOp(left = UnaryOp(Token(TAN, "tan"), x), op = Token(MUL, '*'), right = UnaryOp(Token(TAN, "tan"), x))), op=Token(MUL,'*'), right = dx)
        elif token.type == ARCSIN:
            self.eat(ARCSIN)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = BinOp(left = BinOp(left = Num(Token(INTEGER, 1)), op = Token(MINUS, '-'), right = BinOp(left = x, op = Token(MUL, '*'), right = x)), op = Token(POW, 'pow'), right = Num(Token(INTEGER, -0.5))), op=Token(MUL,'*'), right = dx)
        elif token.type == ARCCOS:
            self.eat(ARCCOS)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, UnaryOp(Token(MINUS, "-"),  BinOp(left = BinOp(left = BinOp(left = Num(Token(INTEGER, 1)), op = Token(MINUS, '-'), right = BinOp(left = x, op = Token(MUL, '*'), right = x)), op = Token(POW, 'pow'), right = Num(Token(INTEGER, -0.5))), op=Token(MUL,'*'), right = dx))
        elif token.type == ARCTAN:
            self.eat(ARCTAN)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = BinOp(left = BinOp(left = Num(Token(INTEGER, 1)), op = Token(PLUS, '+'), right = BinOp(left = x, op = Token(MUL, '*'), right = x)), op = Token(POW, 'pow'), right = Num(Token(INTEGER, -1.0))), op=Token(MUL,'*'), right = dx)
        elif token.type == SINH:
            self.eat(SINH)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = UnaryOp(Token(COSH, "cosh"), x), op=Token(MUL,'*'), right=dx)
        elif token.type == COSH:
            self.eat(COSH)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = UnaryOp(Token(SINH, "sinh"), x), op=Token(MUL,'*'), right=dx)
        elif token.type == TANH:
            self.eat(TANH)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = BinOp(left = Num(Token(INTEGER, 1.0)), op = Token(MINUS, '-'), right = BinOp(left = node,op = Token(MUL, '*'), right = node)), op=Token(MUL,'*'), right=dx)
        elif token.type == EXP:
            self.eat(EXP)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = node, op=Token(MUL,'*'), right=dx)
        elif token.type == POW:
            self.eat(POW)
            self.eat(LPAREN)
            x_cur = copy.deepcopy(self)
            x = self.expr()
            dx = x_cur.dexpr()
            self.eat(COMMA)
            y_cur = copy.deepcopy(self)
            y = self.expr()
            dy = y_cur.dexpr()
            self.eat(RPAREN)
            node = BinOp(left = x, op = token, right = y)
            return node, BinOp(left = node, op = Token(MUL, '*'), right = BinOp(left = BinOp(left = BinOp(left = y, op = Token(DIV,'/'), right = x), op = Token(MUL,'*'), right = dx), op = Token(PLUS, '+'), right = BinOp(left = dy, op = Token(MUL, '*'),right = UnaryOp(Token(LOG, 'LOG'), x))))
        elif token.type == LOG:
            self.eat(LOG)
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            x = self.expr()
            dx = cur.dexpr()
            node = UnaryOp(token, x)
            self.eat(RPAREN)
            return node, BinOp(left = dx, op=Token(DIV,'/'), right=x)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            cur = copy.deepcopy(self)
            node = self.expr()
            dnode = cur.dexpr()
            self.eat(RPAREN)
            return node, dnode
        else:
            raise NameError('Invalid character')

    # similar to term, but returns the symbolic derivative of a term
    def dterm(self):
        """term : factor ((MUL | DIV) factor)*"""
        node, dnode = self.dfactor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
                
            rnode, rdnode = self.dfactor()
            lowdhi = BinOp(left=dnode, op=Token(MUL,'*'), right=rnode)
            hidlow = BinOp(left=node, op=Token(MUL,'*'), right=rdnode)
            if token.type == MUL:
                # chain rule
                dnode = BinOp(left=lowdhi, op=Token(PLUS,'+'), right=hidlow)
                node = BinOp(left=node, op=Token(MUL,'*'), right=rnode)
            else:
                # quotient rule
                topnode = BinOp(left=lowdhi, op=Token(MINUS, '-'), right=hidlow)
                botnode = BinOp(left=rnode, op=Token(MUL,'*'), right=rnode)
                dnode = BinOp(left=topnode, op=Token(DIV,'/'), right=botnode)
                node = BinOp(left=node, op=Token(DIV,'/'), right=rnode)
        return dnode

    # similar to expr, but returns the symbolic derivative of an expr
    def dexpr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
        """
        dnode = self.dterm()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            dnode = BinOp(left=dnode, op=token, right=self.dterm())
        return dnode

    # similar to parse, but returns an abstract syntax tree representing the symbolic derivative
    def dparse(self):
        node = self.dexpr()
        if self.current_token.type != EOF:
            self.error()
        return node
    
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    """ 
    determines the correct visit method for nodes in the abstract syntax tree
    visit_ used to evaluate the numeric value of an abstract syntax tree
    str_visit_ used to evaluate the string form of an abstract syntax tree
    """
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def str_visit(self, node):
        method_name = 'str_visit_' + type(node).__name__
        str_visitor = getattr(self, method_name, self.generic_visit)
        return str_visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    """ 
    Interpreter utilizes visit_ and str_visit_ to evaluate the abstract syntax tree
    """
    def __init__(self, parser):
        self.parser = parser
        self.dtree = copy.deepcopy(parser).dparse()
        self.tree = copy.deepcopy(parser).parse()

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == POW:
            return math.pow(self.visit(node.left), self.visit(node.right))

    def str_visit_BinOp(self, node):
        if node.op.type == PLUS:
            l = self.str_visit(node.left)
            r = self.str_visit(node.right)
            if l == "0":
                return r
            if r == "0":
                return l
            return "(" + l + '+' + r + ")"
        elif node.op.type == MINUS:
            l = self.str_visit(node.left)
            r = self.str_visit(node.right)
            if r == "0":
                return l
            if l == "0":
                return "(-" + r + ")"
            return "(" + self.str_visit(node.left) + '-' + self.str_visit(node.right) + ")"
        elif node.op.type == MUL:
            l = self.str_visit(node.left) 
            r = self.str_visit(node.right)
            if l == "0" or r == "0":
                return "0"
            if l == "1":
                return r
            if r == "1":
                return l
            else:
                return "(" + l + "*" + r + ")"
        elif node.op.type == DIV:
            return "(" + self.str_visit(node.left) + '/' + self.str_visit(node.right) + ")"
        elif node.op.type == POW:
            return 'POW(' + self.str_visit(node.left) + ',' + self.str_visit(node.right) + ')'

    def visit_Num(self, node):
        return node.value

    def str_visit_Num(self, node):
        return str(node.value)

    def visit_Var(self, node):
        if self.vardict is None:
            raise NameError("no var dict passed in")
        if node.name not in self.vardict:
            raise NameError("var {} not in var dict".format(node.name))
        return self.vardict[node.name]

    def str_visit_Var(self, node):
        name = node.name
        if name[:2] == "d_":
            if self.vardict is None:
                raise NameError("no var dict passed in")
            if name not in self.vardict:
                raise NameError("var {} not in var dict".format(name))
            return str(self.vardict[name])
        else:
            return str(name)

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)
        elif op == COS:
            return math.cos(self.visit(node.expr))
        elif op == SIN:
            return math.sin(self.visit(node.expr))
        elif op == TAN:
            return math.tan(self.visit(node.expr))
        elif op == ARCSIN:
            return math.asin(self.visit(node.expr))
        elif op == ARCCOS:
            return math.acos(self.visit(node.expr))
        elif op == ARCTAN:
            return math.atan(self.visit(node.expr))
        elif op == SINH:
            return math.sinh(self.visit(node.expr))
        elif op == COSH:
            return math.cosh(self.visit(node.expr))
        elif op == TANH:
            return math.tanh(self.visit(node.expr))
        elif op == EXP:
            return math.exp(self.visit(node.expr))
        elif op == LOG:
            return math.log(self.visit(node.expr))

    def str_visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return "+" + self.str_visit(node.expr)
        elif op == MINUS:
            return "-" + self.str_visit(node.expr)
        elif op == COS:
            return "COS(" + self.str_visit(node.expr) + ")"
        elif op == SIN:
            return "SIN(" + self.str_visit(node.expr) + ")"
        elif op == TAN:
            return "TAN(" + self.str_visit(node.expr) + ")"
        elif op == ARCSIN:
            return "ARCSIN(" + self.str_visit(node.expr) + ")"
        elif op == ARCCOS:
            return "ARCCOS(" + self.str_visit(node.expr) + ")"
        elif op == ARCTAN:
            return "ARCTAN(" + self.str_visit(node.expr) + ")"
        elif op == SINH:
            return "SINH(" + self.str_visit(node.expr) + ")"
        elif op == COSH:
            return "COSH(" + self.str_visit(node.expr) + ")"
        elif op == TANH:
            return "TANH(" + self.str_visit(node.expr) + ")"
        elif op == EXP:
            return "EXP(" + self.str_visit(node.expr) + ")"
        elif op == LOG:
            return "LOG(" + self.str_visit(node.expr) + ")"

    def interpret(self, vd=None):
        """ numerical evaluation """
        self.get_vardict(vd)
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)

    def differentiate(self, vd=None, dv=None):
        """ evaluate numerical derivative, vd is the variable to derive on """
        self.get_vardict(vd)
        self.get_diffvar(dv)
        tree = self.dtree
        if tree is None:
            return ''
        return self.visit(tree)
    
    def symbolic_diff(self, vd=None, dv=None):
        """ evaluate symbolic derivative (return a string), vd is the variable to derive on """
        original_vd = vd
        self.get_vardict(vd)
        self.get_diffvar(dv)
        tree = self.dtree
        if tree is None:
            return ''
        return self.str_visit(tree)
        
    def diff_all(self, vd=None):
        """ returns all partial derivatives """
        self.get_vardict(vd)
        tree = self.dtree
        if tree is None:
            return ''
        variables = list(self.vardict.keys())
        ret = {}
        for v in variables:
            self.vardict["d_"+v] = 0
        for v in variables:
            self.vardict["d_"+v] = 1
            ret["d_{}".format(v)]=self.visit(tree)
            self.vardict["d_"+v] = 0
        return ret

    def get_vardict(self, vd=None):
        """ expects vardict to be formatted as x:10, y:20, z:3 """
        vdict = {}
        if vd is None:
            text = input('vardict> ')
            if not text:
                self.vardict = None
                return
        else:
            text = vd
        text = text.replace(" ", "")
        for var in text.split(','):
            vals = var.split(':')
            vdict[str(vals[0])] = float(vals[1])
        self.vardict = vdict
        return

    def get_diffvar(self, dv=None):
        """ sets the variable to derive on """
        if dv is None:
            text = input('d_var> ')
        else:
            text = dv
        text = text.replace(" ", "")
        if text not in self.vardict.keys():
            raise NameError("d_var not in vardict")
        for v in list(self.vardict.keys()):
            self.vardict["d_"+v]=0
        self.vardict["d_"+text]=1
        return



# def main():
    # if run as main, can take inputs from command line
    # while True:
    #     try:
    #         try:
    #             text = raw_input('spi> ')
    #         except NameError:  # Python3
    #             text = input('spi> ')
    #     except EOFError:
    #         break
    #     if not text:
    #         continue

    #     lexer = Lexer(text)
    #     parser = Parser(lexer)
    #     interpreter = Interpreter(parser)
    #     result = interpreter.differentiate()
    #     print(result)

# if __name__ == '__main__':
#     main()

'''
Based off of the open source tutorial: Let's Build a Simple Interpreter
https://github.com/rspivak/lsbasi/tree/master/part8/python
'''
