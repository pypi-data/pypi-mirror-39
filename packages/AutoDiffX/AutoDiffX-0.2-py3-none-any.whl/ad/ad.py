"""Implementation of core structures used in our graph-based automatic
differentiation library. +, -, *, /, and exponentiation is also implemented
here to support simple operator overloading.
"""
import numpy as np

__all__ = ['Expression', 'Variable', 'Constant']


class Expression(object):
    '''Base expression class that represents anything in our computational
    graph. Everything should be one of these.'''
    def __init__(self, grad=False):
        self.grad = grad
        self.children = []
        self.dep_vars = set()

    def eval(self, feed_dict):
        '''Evaluates the entire computation graph given a dictionary of
        variables mapped to values.'''
        return self._eval(feed_dict, dict())
    
    def _eval(self, feed_dict, cache_dict):
        '''Helper - Evaluates the computation graph recursively.'''
        raise NotImplementedError

    def d(self, feed_dict):
        '''Evaluates the derivative at the points given, returns to user'''
        res =  self._d(feed_dict, dict(), dict())
        if len(self.dep_vars) == 0:
            # No dependent variables - it is a constant
            return 0
        if len(res) == 1:
            # This is the non-vectorized case, scalar func of scalar
            # Return a number, not a dictionary
            return list(res.values())[0]

        return res

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        '''Helper - Evaluates the differentiation products recursively.
        @param: feed_dict: dictionary mapping var names 
        @param: e_cache_dict: cache for previously evaluated values
        @param: d_cache_dict: cache for previously calculated derivatives
        '''
        raise NotImplementedError('Jacobian not implemented for this expr')
    
    def hessian(self, feed_dict):
        '''Evaluates the hessian at the points given, returns to user as a 
        dictionary of dictionarys (to be indexed as [var1][var2] for the
        derivative with respect to var1 then var2)'''
        res = self._h(feed_dict, dict(), dict(), dict())
        if len(self.dep_vars) == 0:
            return 0
        elif len(self.dep_vars) == 1:
            # This is the 1D hessian case, so just a scalar
            return list(list(res.values())[0].values())[0]
        else:
            return res

    def _h(self, feed_dict, e_cache_dict, d_cache_dict, h_cache_dict):
        '''Helper - Evaluates the differentiation products recursively.
        @param: feed_dict: dictionary mapping var names 
        @param: e_cache_dict: cache for previously evaluated values
        @param: d_cache_dict: cache for previously calculated derivatives
        @param: h_cache_dict: cache for previously calculated double derivatives 
        '''
        raise NotImplementedError('Hessian not implemented for this expr')

    def d_expr(self, n=1):
        """Return n-th order derivative as an Expression.
        Scalar input only.
        """
        var = list(self.dep_vars)[0]
        di = self
        for i in range(n):
            di = di._d_expr(var)
        return di

    def _d_expr(self, var):
        """Helper - Evaluates the partial derivative as an Expression."""
        raise NotImplementedError

    def d_n(self, n, val):
        """Return the value of n-th order derivative. Scalar input only.

        Expressions that implements d_n method are: Variable, Constant,
        Negation, Addition, Subtraction, Multiplication, Division,
        Expression ** Constant, Sin, Cos, Exp, Log, and their combinations.
        """
        var = list(self.dep_vars)[0]
        return self._d_n(n, {var: val}, {}, {}) * np.math.factorial(n)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        """ Helper - Evaluates (the n-th order derivative) / (n!).

        @param: n: the order of derivative
        @param: feed_dict: dictionary mapping var names
        @param: e_cache_dict: cache for previously evaluated values
        @param: d_cache_dict: cache for previously calculated derivatives
        @return: the value of the n-th order derivative
        """
        raise NotImplementedError

    def __add__(self, other):
        try:
            # Propagate the need for gradient if one thing needs gradient
            # Need to call other.grad first since self.grad may shortcircuit
            return Addition(self, other, grad=(other.grad and self.grad))
        except AttributeError:
            return Addition(self, Constant(other), grad=self.grad)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        try:
            return Subtraction(self, other, grad=(other.grad and self.grad))
        except AttributeError:
            return Subtraction(self, Constant(other), grad=self.grad)

    def __rsub__(self, other):
        try:
            return Subtraction(other, self, grad=(other.grad and self.grad))
        except AttributeError:
            return Subtraction(Constant(other), self, grad=self.grad)

    def __mul__(self, other):
        try:
            return Multiplication(self, other, grad=(other.grad and self.grad))
        except AttributeError:
            return Multiplication(self, Constant(other), grad=self.grad)

    def __rmul__(self, other):
        # TODO: Multiplication not commutative if we enable matrix support
        return self.__mul__(other)

    def __truediv__(self, other):
        try:
            return Division(self, other, grad=(other.grad and self.grad))
        except AttributeError:
            return Division(self, Constant(other), grad=self.grad)

    def __rtruediv__(self, other):
        try:
            return Division(other, self, grad=(other.grad and self.grad))
        except AttributeError:
            return Division(Constant(other), self, grad=self.grad)

    def __neg__(self):
        return Negation(self, grad=self.grad)

    def __pow__(self, other):
        try:
            return Power(self, other, grad=(other.grad and self.grad))
        except AttributeError:
            return Power(self, Constant(other), grad=(self.grad))


class Variable(Expression):
    def __init__(self, name=None, grad=True):
        self.grad = grad
        self.name = None if not name else str(name)

        # A variable only depends on itself
        self.dep_vars = set([self])

    def _eval(self, feed_dict, cache_dict):
        # Check if the user specified either the object in feed_dict or
        # the name of the object in feed_dict
        if self in feed_dict:
            return feed_dict[self]
        elif self.name in feed_dict:
            return feed_dict[self.name]
        else:
            raise ValueError('Unbound variable %s' % self.name)

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        return {self: 1.0}
    
    def _h(self, feed_dict, e_cache_dict, d_cache_dict, h_cache_dict):
        return {self: {self: 0}}

    def _d_expr(self, var):
        if var == self:
            return Constant(1.0)
        else:
            return Constant(0)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if n == 0:
            return self._eval(feed_dict, e_cache_dict)
        elif n == 1:
            return 1.0
        else:
            return 0.0

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return "Var"


class Constant(Expression):
    '''Represents a constant.'''
    def __init__(self, val, grad=False):
        super().__init__(grad=grad)
        self.val = val
        self.dep_vars = set()

    def _eval(self, feed_dict, cache_dict):
        return self.val

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        return {}

    def _d_expr(self, var):
        return Constant(0.0)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if n == 0:
            return self.val
        else:
            return 0.0

    def _h(self, feed_dict, e_cache_dict, d_cache_dict, h_cache_dict):
        return {}


class Unop(Expression):
    """Utilities common to all unary operations in the form Op(a)

    Attributes
    ----------
    expr1: Expression
        Input of the unary function
    children: list of Expression
        The children of the unary function, i.e. expr1
    """
    def __init__(self, expr1, grad=False):
        """
        Parameters
        ----------
        expr1 : Expression
            Input of the unary function.
        grad : bool, optional
            If True, then allow the Expression to calculate the derivative.
        """
        super().__init__(grad=grad)
        self.expr1 = expr1
        self.children = [self.expr1]
        # Deep copy the set
        self.dep_vars = set(expr1.dep_vars)


class Negation(Unop):
    """Negation, in the form - A"""
    def _eval(self, feed_dict, cache_dict):
        if id(self) not in cache_dict:
            res1 = self.expr1._eval(feed_dict, cache_dict)
            cache_dict[id(self)] = -res1
        return cache_dict[id(self)]

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        if id(self) not in d_cache_dict:
            d1 = self.expr1._d(feed_dict, e_cache_dict, d_cache_dict)
            ret = {}
            for var in self.dep_vars:
                ret[var] = -d1.get(var, 0)
            d_cache_dict[id(self)] = ret
        return d_cache_dict[id(self)]
    
    def _h(self, feed_dict, e_cache, d_cache, h_cache):
        if id(self) not in h_cache:
            # Both dx^2 and dxdy are just the negations too
            h1 = self.expr1._h(feed_dict, e_cache, d_cache, h_cache)
            ret = {var:{} for var in self.dep_vars}
            for var1 in self.dep_vars:
                for var2 in self.dep_vars:
                    ret[var1][var2] = - h1.get(var1, {}).get(var2, 0)
            h_cache[id(self)] = ret
        return h_cache[id(self)]

    def _d_expr(self, var):
        return - self.expr1._d_expr(var)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if (id(self), n) in d_cache_dict:
            return d_cache_dict[(id(self), n)]
        if n == 0:
            res1 = self.expr1._eval(feed_dict, e_cache_dict)
        else:
            res1 = self.expr1._d_n(n, feed_dict, e_cache_dict, d_cache_dict)
        d_cache_dict[(id(self), n)] = -res1
        return d_cache_dict[(id(self), n)]


class Binop(Expression):
    '''Utilities common to all binary operations in the form Op(a, b)'''
    def __init__(self, expr1, expr2, grad=False):
        super().__init__(grad=grad)
        try:
            expr1.grad
        except AttributeError:
            expr1 = Constant(expr1)
        try:
            expr2.grad
        except AttributeError:
            expr2 = Constant(expr1)
        self.expr1 = expr1
        self.expr2 = expr2
        self.children = [self.expr1, self.expr2]
        self.dep_vars = expr1.dep_vars | expr2.dep_vars


class Power(Binop):
    """Power function, the input is raised to the power of exponent.

    Examples
    --------
    >>> import ad
    >>> x = ad.Variable('x')
    >>> y = x ** 2
    >>> y.eval({x: 10.0})
    100.0
    >>> y.d({x: 10.0})
    20.0
    """
    def _eval(self, feed_dict, cache_dict):
        if id(self) not in cache_dict:
            res1 = self.expr1._eval(feed_dict, cache_dict)
            res2 = self.expr2._eval(feed_dict, cache_dict)
            # cast to float necessary, numpy complains about raising
            # integers to negative integer powers otherwise.
            cache_dict[id(self)] = np.power(float(res1), res2)
        return cache_dict[id(self)]

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        """derivative is  y x^(y-1) x_dot + x^y log(x) y_dot"""
        if id(self) not in d_cache_dict:
            res1 = self.expr1._eval(feed_dict, e_cache_dict)
            res2 = self.expr2._eval(feed_dict, e_cache_dict)
            d1 = self.expr1._d(feed_dict, e_cache_dict, d_cache_dict)
            d2 = self.expr2._d(feed_dict, e_cache_dict, d_cache_dict)
            ret = {}
            # cast to float necessary, numpy complains about raising
            # integers to negative integer powers otherwise.
            for var in self.dep_vars:
                # Short circuit to prevent taking log of zero
                if d2.get(var, 0) == 0:
                    ret[var] = res2 * np.power(float(res1), res2 - 1) * d1.get(var, 0) 
                else:
                    ret[var] = res2 * np.power(float(res1), res2 - 1) * d1.get(var, 0) + \
                            np.power(float(res1), res2) * np.log(res1) * d2.get(var, 0)
            d_cache_dict[id(self)] = ret
        return d_cache_dict[id(self)]

    def _d_expr(self, var):
        if var not in self.dep_vars:
            return Constant(0)
        if isinstance(self.expr1, Constant):
            return np.log(self.expr1.val) * (self.expr1 ** self.expr2)
        elif isinstance(self.expr2, Constant):
            return self.expr2.val * (self.expr1 ** (self.expr2.val - 1))
        else:
            msg = "Do not support f(x) ** g(x)"
            raise NotImplementedError(msg)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if not isinstance(self.expr2, Constant):
            msg = "Do not support c ** g(x) or f(x) ** g(x)"
            raise NotImplementedError(msg)
        if (id(self), n) in d_cache_dict:
            return d_cache_dict[(id(self), n)]
        if n == 0:
            res = self._eval(feed_dict, e_cache_dict)
            d_cache_dict[(id(self), 0)] = res
            return d_cache_dict[(id(self), 0)]
        a = self.expr2.val
        if (id(self.expr1), 0) not in d_cache_dict:
            g_0 = self.expr1._d_n(0, feed_dict, e_cache_dict, d_cache_dict)
            d_cache_dict[(id(self.expr1), 0)] = g_0
        g_0 = d_cache_dict[(id(self.expr1), 0)]
        if np.isclose(g_0, 0):
            if a < 0:
                msg = "The exponent should be greater than 0 when the base is 0"
                raise ZeroDivisionError(msg)
            elif np.isclose(a, int(a)) or a >= n:
                d_cache_dict[(id(self), n)] = 0.0
                return 0.0
            else:
                msg = "If base of power is 0 and exponent is not an " \
                      "integer, the exponent should be greater than n"
                raise ZeroDivisionError(msg)
        res = 0
        for i in range(1, n+1):
            if (id(self.expr1), i) not in d_cache_dict:
                g_i = self.expr1._d_n(i, feed_dict, e_cache_dict, d_cache_dict)
                d_cache_dict[(id(self.expr1), i)] = g_i
            if (id(self), n-i) not in d_cache_dict:
                ga_ni = self._d_n(n-i, feed_dict, e_cache_dict, d_cache_dict)
                d_cache_dict[(id(self), n-i)] = ga_ni
            g_i = d_cache_dict[(id(self.expr1), i)]
            ga_ni = d_cache_dict[(id(self), n-i)]
            res += (float(a + 1) * i / n - 1) * g_i * ga_ni
        res /= g_0
        d_cache_dict[(id(self), n)] = res
        return d_cache_dict[(id(self), n)]

    def _h(self, feed_dict, e_cache, d_cache, h_cache):
        """For expressions in the form x^y, I was only able to get a closed
        form solution for if y is a constant. The general case is way to
        complicated for me to solve on a piece of paper"""
        if id(self) not in h_cache:
            # Both dx^2 and dxdy are just the additions 
            h1 = self.expr1._h(feed_dict, e_cache, d_cache, h_cache)
            h2 = self.expr2._h(feed_dict, e_cache, d_cache, h_cache)
            if h2 != {}:
                msg = 'Hessian only implemented for x^[constant]'
                raise NotImplementedError(msg)
            d1 = self.expr1._d(feed_dict, e_cache, d_cache)
            v1 = self.expr1._eval(feed_dict, e_cache)
            v2 = self.expr2._eval(feed_dict, e_cache)
            ret = {var:{} for var in self.dep_vars}
            for var1 in self.dep_vars:
                for var2 in self.dep_vars:
                    dxy1 = h1.get(var1, {}).get(var2, 0)
                    dx1, dx2 = d1.get(var1, 0), d1.get(var2, 0)
                    term1 = (v2 - 1) * v2 * (v1 ** (v2 - 2)) * dx1 * dx2
                    term2 = v2 * (v1 ** (v2 - 1)) * dxy1 
                    ret[var1][var2] = term1 + term2
            h_cache[id(self)] = ret
        return h_cache[id(self)]


class Addition(Binop):
    '''Addition, in the form A + B'''
    def _eval(self, feed_dict, cache_dict):
        if id(self) not in cache_dict:
            res1 = self.expr1._eval(feed_dict, cache_dict)
            res2 = self.expr2._eval(feed_dict, cache_dict)
            cache_dict[id(self)] = res1 + res2
        return cache_dict[id(self)]

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        if id(self) not in d_cache_dict:
            d1 = self.expr1._d(feed_dict, e_cache_dict, d_cache_dict)
            d2 = self.expr2._d(feed_dict, e_cache_dict, d_cache_dict)
            ret = {}
            for var in self.dep_vars:
                ret[var] = d1.get(var, 0) + d2.get(var, 0)
            d_cache_dict[id(self)] = ret
        return d_cache_dict[id(self)]

    def _d_expr(self, var):
        if var not in self.dep_vars:
            return Constant(0)
        return self.expr1._d_expr(var) + self.expr2._d_expr(var)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if (id(self), n) in d_cache_dict:
            return d_cache_dict[(id(self), n)]
        if n == 0:
            res1 = self._eval(feed_dict, e_cache_dict)
        else:
            res1 = self.expr1._d_n(n, feed_dict, e_cache_dict, d_cache_dict) + \
                   self.expr2._d_n(n, feed_dict, e_cache_dict, d_cache_dict)
        d_cache_dict[(id(self), n)] = res1
        return d_cache_dict[(id(self), n)]
    
    def _h(self, feed_dict, e_cache, d_cache, h_cache):
        if id(self) not in h_cache:
            # Both dx^2 and dxdy are just the additions 
            h1 = self.expr1._h(feed_dict, e_cache, d_cache, h_cache)
            h2 = self.expr2._h(feed_dict, e_cache, d_cache, h_cache)
            ret = {var:{} for var in self.dep_vars}
            for var1 in self.dep_vars:
                for var2 in self.dep_vars:
                    dxy1 = h1.get(var1, {}).get(var2, 0) 
                    dxy2 = h2.get(var1, {}).get(var2, 0) 
                    ret[var1][var2] = dxy1 + dxy2
            h_cache[id(self)] = ret
        return h_cache[id(self)]
            

class Subtraction(Binop):
    '''Subtraction, in the form A - B'''
    def _eval(self, feed_dict, cache_dict):
        if id(self) not in cache_dict:
            res1 = self.expr1._eval(feed_dict, cache_dict)
            res2 = self.expr2._eval(feed_dict, cache_dict)
            cache_dict[id(self)] = res1 - res2
        return cache_dict[id(self)]

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        if id(self) not in d_cache_dict:
            d1 = self.expr1._d(feed_dict, e_cache_dict, d_cache_dict)
            d2 = self.expr2._d(feed_dict, e_cache_dict, d_cache_dict)
            ret = {}
            for var in self.dep_vars:
                ret[var] = d1.get(var, 0) - d2.get(var, 0)
            d_cache_dict[id(self)] = ret
        return d_cache_dict[id(self)]

    def _d_expr(self, var):
        if var not in self.dep_vars:
            return Constant(0)
        return self.expr1._d_expr(var) - self.expr2._d_expr(var)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if (id(self), n) in d_cache_dict:
            return d_cache_dict[(id(self), n)]
        if n == 0:
            res1 = self._eval(feed_dict, e_cache_dict)
        else:
            res1 = self.expr1._d_n(n, feed_dict, e_cache_dict, d_cache_dict) - \
                   self.expr2._d_n(n, feed_dict, e_cache_dict, d_cache_dict)
        d_cache_dict[(id(self), n)] = res1
        return d_cache_dict[(id(self), n)]

    def _h(self, feed_dict, e_cache, d_cache, h_cache):
        if id(self) not in h_cache:
            # Both dx^2 and dxdy are just the additions 
            h1 = self.expr1._h(feed_dict, e_cache, d_cache, h_cache)
            h2 = self.expr2._h(feed_dict, e_cache, d_cache, h_cache)
            ret = {var:{} for var in self.dep_vars}
            for var1 in self.dep_vars:
                for var2 in self.dep_vars:
                    dxy1 = h1.get(var1, {}).get(var2, 0) 
                    dxy2 = h2.get(var1, {}).get(var2, 0) 
                    ret[var1][var2] = dxy1 - dxy2
            h_cache[id(self)] = ret
        return h_cache[id(self)]


class Multiplication(Binop):
    '''Multiplication, in the form A * B'''
    def _eval(self, feed_dict, cache_dict):
        if id(self) not in cache_dict:
            res1 = self.expr1._eval(feed_dict, cache_dict)
            res2 = self.expr2._eval(feed_dict, cache_dict)
            cache_dict[id(self)] = res1 * res2
        return cache_dict[id(self)]

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        if id(self) not in d_cache_dict:
            d1 = self.expr1._d(feed_dict, e_cache_dict, d_cache_dict)
            d2 = self.expr2._d(feed_dict, e_cache_dict, d_cache_dict)
            res1 = self.expr1._eval(feed_dict, e_cache_dict)
            res2 = self.expr2._eval(feed_dict, e_cache_dict)
            ret = {}
            for var in self.dep_vars:
                ret[var] = res1 * d2.get(var, 0) + res2 * d1.get(var, 0)
            d_cache_dict[id(self)] = ret
        return d_cache_dict[id(self)]
    
    def _h(self, feed_dict, e_cache, d_cache, h_cache):
        if id(self) not in h_cache:
            # Both dx^2 and dxdy are just the additions 
            h1 = self.expr1._h(feed_dict, e_cache, d_cache, h_cache)
            h2 = self.expr2._h(feed_dict, e_cache, d_cache, h_cache)
            d1 = self.expr1._d(feed_dict, e_cache, d_cache)
            d2 = self.expr2._d(feed_dict, e_cache, d_cache)
            v1 = self.expr1._eval(feed_dict, e_cache)
            v2 = self.expr2._eval(feed_dict, e_cache)
            ret = {var:{} for var in self.dep_vars}
            for var1 in self.dep_vars:
                for var2 in self.dep_vars:
                    dxy1 = h1.get(var1, {}).get(var2, 0) 
                    dxy2 = h2.get(var1, {}).get(var2, 0) 
                    ret[var1][var2] = (d1.get(var1, 0) * d2.get(var2, 0) + 
                        d1.get(var2, 0) * d2.get(var1, 0) +
                        v1 * dxy2 + v2 * dxy1)
            h_cache[id(self)] = ret
        return h_cache[id(self)]

    def _d_expr(self, var):
        if var not in self.dep_vars:
            return Constant(0)
        if isinstance(self.expr1, Constant):
            return self.expr1.val * self.expr2._d_expr(var)
        elif isinstance(self.expr2, Constant):
            return self.expr2.val * self.expr1._d_expr(var)
        else:
            return self.expr1 * self.expr2._d_expr(var) + self.expr2 * \
                   self.expr1._d_expr(var)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if (id(self), n) in d_cache_dict:
            return d_cache_dict[(id(self), n)]
        if n == 0:
            res = self._eval(feed_dict, e_cache_dict)
            d_cache_dict[(id(self), 0)] = res
            return d_cache_dict[(id(self), 0)]
        res = 0
        for i in range(n+1):
            if (id(self.expr1), i) not in d_cache_dict:
                f_i = self.expr1._d_n(i, feed_dict, e_cache_dict, d_cache_dict)
                d_cache_dict[(id(self.expr1), i)] = f_i
            if (id(self.expr2), n-i) not in d_cache_dict:
                g_ni = self.expr2._d_n(n-i, feed_dict, e_cache_dict,
                                       d_cache_dict)
                d_cache_dict[(id(self.expr2), n-i)] = g_ni
            f_i = d_cache_dict[(id(self.expr1), i)]
            g_ni = d_cache_dict[(id(self.expr2), n-i)]
            res += f_i * g_ni
        d_cache_dict[(id(self), n)] = res
        return d_cache_dict[(id(self), n)]


class Division(Binop):
    '''Division, in the form A / B'''
    def _eval(self, feed_dict, cache_dict):
        if id(self) not in cache_dict:
            res1 = self.expr1._eval(feed_dict, cache_dict)
            res2 = self.expr2._eval(feed_dict, cache_dict)
            cache_dict[id(self)] = res1 / res2
        return cache_dict[id(self)]

    def _d(self, feed_dict, e_cache_dict, d_cache_dict):
        if id(self) not in d_cache_dict:
            d1 = self.expr1._d(feed_dict, e_cache_dict, d_cache_dict)
            d2 = self.expr2._d(feed_dict, e_cache_dict, d_cache_dict)
            res1 = self.expr1._eval(feed_dict, e_cache_dict)
            res2 = self.expr2._eval(feed_dict, e_cache_dict)
            ret = {}
            for var in self.dep_vars:
                ret[var] = (d1.get(var, 0) / res2) - (d2.get(var, 0) * res1 /
                                                      (res2 * res2))
            d_cache_dict[id(self)] = ret
        return d_cache_dict[id(self)]

    def _d_expr(self, var):
        if var not in self.dep_vars:
            return Constant(0)
        if isinstance(self.expr1, Constant):
            return - self.expr1.val * self.expr2._d_expr(var) / (self.expr2 *
                                                                 self.expr2)
        elif isinstance(self.expr2, Constant):
            return self.expr1._d_expr(var) * (1.0 / self.expr2.val)
        else:
            return self.expr1._d_expr(var) / self.expr2 - self.expr1 * \
                   self.expr2._d_expr(var) / (self.expr2 * self.expr2)

    def _d_n(self, n, feed_dict, e_cache_dict, d_cache_dict):
        if (id(self), n) in d_cache_dict:
            return d_cache_dict[(id(self), n)]
        if n == 0:
            res = self._eval(feed_dict, e_cache_dict)
            d_cache_dict[(id(self), 0)] = res
            return d_cache_dict[(id(self), 0)]
        res = 0
        for i in range(n):
            if (id(self), i) not in d_cache_dict:
                div_i = self._d_n(i, feed_dict, e_cache_dict, d_cache_dict)
                d_cache_dict[(id(self), i)] = div_i
            if (id(self.expr2), n-i) not in d_cache_dict:
                g_ni = self.expr2._d_n(n-i, feed_dict, e_cache_dict, d_cache_dict)
                d_cache_dict[(id(self.expr2), n-i)] = g_ni
            div_i = d_cache_dict[(id(self), i)]
            g_ni = d_cache_dict[(id(self.expr2), n-i)]
            res -= div_i * g_ni
        if (id(self.expr1), n) not in d_cache_dict:
            f_n = self.expr1._d_n(n, feed_dict, e_cache_dict, d_cache_dict)
            d_cache_dict[(id(self.expr1), n)] = f_n
        f_n = d_cache_dict[(id(self.expr1), n)]
        res += f_n
        if (id(self.expr2), 0) not in d_cache_dict:
            g_0 = self.expr2._eval(feed_dict, e_cache_dict)
            d_cache_dict[(id(self.expr2), 0)] = g_0
        g_0 = d_cache_dict[(id(self.expr2), 0)]
        res /= g_0
        d_cache_dict[(id(self), n)] = res
        return d_cache_dict[(id(self), n)]

    def _h(self, feed_dict, e_cache, d_cache, h_cache):
        if id(self) not in h_cache:
            # Both dx^2 and dxdy are just the additions 
            h1 = self.expr1._h(feed_dict, e_cache, d_cache, h_cache)
            h2 = self.expr2._h(feed_dict, e_cache, d_cache, h_cache)
            d1 = self.expr1._d(feed_dict, e_cache, d_cache)
            d2 = self.expr2._d(feed_dict, e_cache, d_cache)
            f = self.expr1._eval(feed_dict, e_cache)
            g = self.expr2._eval(feed_dict, e_cache)
            ret = {var:{} for var in self.dep_vars}
            for var1 in self.dep_vars:
                for var2 in self.dep_vars:
                    fxy = h1.get(var1, {}).get(var2, 0) 
                    gxy = h2.get(var1, {}).get(var2, 0) 
                    fx, fy = d1.get(var1, 0), d1.get(var2, 0)
                    gx, gy = d2.get(var1, 0), d2.get(var2, 0)
                    term1 = - (gx * fy + gy * fx) / (g ** 2)
                    term2 = (2 * f * gy * gx) / (g ** 3)
                    term3 = (fxy / g) - (f * gxy) / (g ** 2)
                    ret[var1][var2] = term1 + term2 + term3
            h_cache[id(self)] = ret
        return h_cache[id(self)]
