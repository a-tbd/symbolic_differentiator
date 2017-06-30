'''
Symbolic differentiator for single variable polynomial expressions.

Input: Expression (without spaces) to be evaluated and the variable.
       Coefficients and exponents must be ints or floats.  
       Exponents must be >= 0.
Output: Nested list containing elements of the derivative of the expression.

Examples:
x^2+3 x ==> 2x

z^4+2z^5-3.5z^1+82 z ==> 4x^3+10x^4-3.5
'''
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
            new_e = float(self.exponent) - 1
        except ValueError:
            print 'Exponents must be positive integers or floats'
            sys.exit(2)
        if new_e.is_integer():
            return int(new_e)
        else:
            return new_e

    def eval_coefficient(self):
        try:
            num_c = float(self.coeff)
            num_e = float(self.exponent)
        except ValueError:
            print 'Coefficients and exponents must be positive integers or floats.'
            sys.exit(2)
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


def get_derivative(exp, var):
    tk = Tokenizer(['+', '-'])
    tokens = [Expression(t) for t in tk.transduce(exp) if t != '']
    derivative = [exp.eval_derivative(var) for exp in tokens]
    return ''.join(derivative)


def main(argv):
    try:
        exp, var = argv
    except ValueError:
        print 'useage: symbolic_differentiator.py x^2+3x+5 x'
        sys.exit(2)
    d = get_derivative(exp, var)
    print d    


if __name__ == '__main__':
    main(sys.argv[1:])
