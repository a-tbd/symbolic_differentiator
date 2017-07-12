'''
Symbolic differentiation calculator
Input: Expression to be evaluated and the variable.
       Coefficients must be ints or floats (no constants or fractions).  
Output: Derivative of the expression with respect to the input variable.

Examples:
x^2 + 3x ==> 2x+3

z^4+.5z^2-6 ==> 4z^3+z
'''
import collections
import re
import pdb


class Calculator(object):
    def __init__(self):
        self.loop = True
        self.components = []

    def start(self):
        """Prompts user for expression and variable.
           Returns the derivative as a string.
           Continues looping until user exits."""
        while self.loop:
            exp = self.prompt_expression()
            if not self.is_exit(exp):
                var = self.prompt_variable()
                try:
                    self.components = self.parse_expression(exp, var)
                    dydx = [c.evaluate_derivative() for c in self.components]
                    self.display_derivative(dydx, var)
                except ValueError:
                    raise
            else:
                self.loop = False
            self.components = [] # is this enough to deal with stack overflow issues?

    def prompt_expression(self):
        print 'Enter your expression or e to exit:'
        exp = raw_input('-->')
        return exp

    def prompt_variable(self):
        print 'With respect to what variable?'
        var = raw_input('-->')
        return var
    
    def display_derivative(self, d, var):
        func = 'f\'(%s) = ' % var
        print func + ''.join(d)
    
    def is_exit(self, exp):
        return exp == 'exit' or exp == 'e'
    
    def parse_expression(self, exp, var):
        """Takes string expression, returns list of expressions. 
           Currently only supports single var poly"""
        exp = ''.join(exp.split())
        poly_regex = re.compile('[+-]?[a-z0-9^**.]*')
        poly_parse = poly_regex.findall(exp) 
        return [SingleVarPoly(poly_parse, var)] # this will continue to fill the stack with objects :/


class Expression(object):
    def __init__(self, exp, var):
        self.exp = exp 
        self.var = var
        self.dydx = None


class SingleVarPoly(Expression):
    def __init__(self, exp, var):
        Expression.__init__(self, exp, var)
    
    def evaluate_derivative(self):
        """Takes a single var polynomial as a string.
           Returns the derivative as a string."""
        terms = collections.defaultdict(list)
        for t in self.exp:
            if t:
                e, c = self.derivative_by_term(t)
                terms[e].append(c)
        # Combine like terms and sort in decreasing exponent order
        for e in terms:
            if len(terms[e]) > 1:
                terms[e] = [sum(terms[e])]
        dydx = self.format(terms)
        return ''.join(dydx)
  
    def derivative_by_term(self, term):
        """Takes term of polynomial as a string.
           Returns the derivative as a tuple (exp, coeff)."""
        if not self.var in term:
            return -1, 0 # constant term
        else:
            index_var = term.index(self.var)
            coeff = term[:index_var]
            exponent = term[index_var+1:]

            if '^' in exponent:
                exponent = exponent[1:]
            elif '**' in exponent:
                exponent = exponent[2:]
            
            if exponent == '':
                exponent = 1
            if coeff == '' or coeff == '+':
                coeff = 1
            elif coeff == '-':
                coeff = -1
            new_exponent = self.eval_exponent(exponent)
            new_coeff = self.eval_coefficient(coeff, exponent)
            return new_exponent, new_coeff

    def eval_exponent(self, exponent):
        try:
            new_e = int(exponent) - 1
            return new_e
        except ValueError:
            raise ValueError('Exponents must be positive integers.')

    def eval_coefficient(self, coeff, exponent):
        try:
            num_c = float(coeff)
            num_e = int(exponent)
            new_c = num_c * num_e
            if new_c.is_integer():
                return int(new_c)
            else:
                return new_c
        except ValueError:
            raise ValueError('Coefficients must be integers or floats.')

    def format(self, terms):
        """Takes dict of terms represented as {exponent: [coefficient]}
           Returns derivative as a string."""
        dydx = []
        keys = sorted([k for k in terms],reverse=True)
        for e in keys:
            exponent = e
            coeff = terms[e][0]
            op = ''
            if e != keys[0] and coeff > -1:
                op = '+'
            if coeff == 0 or exponent == -1:
                dydx.append('')
            elif exponent == 0:
                dydx.append(op + str(coeff))
            elif exponent == 1:
                if coeff == 1:
                    coeff = ''
                dydx.append(op + str(coeff) + self.var)
            else:
                dydx.append(op + str(coeff) + self.var + '^' + str(exponent))
        return dydx


def main():
    calculator = Calculator()
    calculator.start()


if __name__ == '__main__':
    main()
