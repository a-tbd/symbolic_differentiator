'''
Symbolic differentiation calculator
Input: Expression to be evaluated and the variable.
       Coefficients must be ints or floats (no constants or fractions).  
Output: Derivative of the expression with respect to the input variable.

Examples:
x^2 + 3x ==> 2x+3

z^4+.5z^2-6 ==> 4z^3+1z
'''

#expression = 'x^2 * 2x+3-8x^(1/2)'
#print list(expression)
import sys
import pdb

class StateMachine(object):
    def transduce(self, inputs):
        inputs += ' '
        self.exp = inputs
        return [self.step(i, c) for i, c in enumerate(inputs)]

    def step(self, index, inp):
        (s, o) = self.next_step(self.state, index, inp)
        self.state = s
        return o


class Tokenizer(StateMachine):
    def __init__(self, delim):
        self.state = ''
        self.delim = delim
        self.exp = None

    def next_step(self, state, index, inp):
        if index == (len(self.exp) - 1):
            return '', self.state
        elif not inp in self.delim:
            state += inp
            return state, ''
        else:
            return inp, self.state


class Calculator(object):
    def __init__(self):
        self.tk = Tokenizer(['+','-'])
        self.polynomial = {}

    def start(self):
        while True:
            exp = self.prompt_expression()
            if not self.is_exit(exp):
            	var = self.prompt_variable()
                tokens = [Expression(t) for t in self.tk.transduce(exp) if t != '']
                derivative = {exp.exponent: exp.eval_derivative(var) for exp in tokens}
                sorted_exponents = [derivative[k] for k in sorted(derivative.iterkeys())]
                self.display_derivative(sorted_exponents, var)
            else:
                sys.exit()

    def prompt_expression(self):
        print 'Enter your expression:'
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


class Expression(object):
    def __init__(self, exp):
        self.exp = exp
        self.operator = ''
        self.coeff = ''
        self.index_var = None
        self.exponent = ''
        self.dydx = ''

    def split_expression(self, var):
        self.set_index_var(var)
        self.set_operator()
        self.set_coefficient()
        self.set_exponent()

    def set_index_var(self, var):
        if var in self.exp:
            self.index_var = self.exp.index(var)

    def set_operator(self):
        if self.exp[0] in ['+', '-']:
            self.operator = self.exp[0]

    def set_coefficient(self):
        start = 0
        end = -1
        if self.operator:
            start = 1
        if not self.index_var is None:
            end = self.index_var
        self.coeff = self.exp[start:end]
        if self.coeff == '':
            self.coeff = 1

    def set_exponent(self):
        if not self.index_var is None:
            self.exponent = self.exp[self.index_var + 2:]
            if self.exponent == '':
                self.exponent = 1

    def eval_derivative(self, var):
        self.split_expression(var)
        if self.index_var is None:
            self.dydx = ''
        else:
            new_exponent = self.eval_exponent()
            new_coeff = self.eval_coefficient()
            self.dydx = self.format(new_coeff, new_exponent, var)
        return self.dydx

    def eval_exponent(self):
        try:
            new_e = int(self.exponent) - 1
        except ValueError:
            print 'ValueError: Exponents must be positive integers.'
            main()
        return new_e

    def eval_coefficient(self):
        try:
            num_c = float(self.coeff)
            num_e = int(self.exponent)
        except ValueError:
            print 'ValueError: Coefficients must be integers or floats.'
            main()
        new_c = num_c * num_e
        if new_c.is_integer():
            return int(new_c)
        else:
            return new_c

    def format(self, coeff, exponent, var):
        right = self.format_right(exponent, var)
        if coeff == 0:
            return ''
        elif right == 1:
            return self.operator + str(coeff * right) 
        else:
            return self.operator + str(coeff) + str(right)

    def format_right(self, exponent, var):
        if exponent == 0:
            return 1
        elif exponent == 1:
            return var
        else:
            return var + '^' + str(exponent)

def main():
    calculator = Calculator()
    calculator.start()

if __name__ == '__main__':
    main()
