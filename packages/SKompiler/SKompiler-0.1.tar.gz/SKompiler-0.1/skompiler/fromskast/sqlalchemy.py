"""
SKompiler: Generate Sympy expressions from SKAST.
"""
#pylint: disable=wildcard-import,unused-wildcard-import
from functools import reduce
import warnings
import numpy as np
import sqlalchemy as sa
from ..ast import ASTProcessor, IndexedIdentifier, NumberConstant

def translate(node, dialect=None, assign_to='y', component=None):
    """Translates SKAST to an SQLAlchemy expression (or a list of those, if the output should be a vector).

    If dialect is not None, further compiles the expression(s) to a given dialect via to_sql.
    
    Kwargs:
       assign_to (None/string/list of str): See to_sql
    
    >>> from skompiler.toskast.string import translate as skast
    >>> expr = skast('[2*x[0], 1] if x[1] <= 3 else [12.0, 45.5]')
    >>> print(translate(expr, 'sqlite'))
    CASE WHEN (x2 <= 3) THEN 2 * x1 ELSE 12.0 END as y1,
    CASE WHEN (x2 <= 3) THEN 1 ELSE 45.5 END as y2
    """
    saexprs = SQLAlchemyWriter()(node)
    if component is not None:
        saexprs = saexprs[component]
    if dialect is None:
        return saexprs
    else:
        return to_sql(saexprs, dialect, assign_to=assign_to)


def _is(val):
    return lambda self, node: val

def _sum(iterable):
    "The built-in 'sum' does not work for us as we need."
    return reduce(lambda x, y: x+y, iterable)

def _iif(cond, iftrue, iffalse):
    return sa.case([(cond, iftrue)], else_=iffalse)

def _sklearn_softmax(xs):
    x_max = _max(xs)
    return _vecsumnormalize([sa.func.exp(x - x_max) for x in xs])

def _matvecproduct(M, x):
    return [_sum(m_i[j] * x[j] for j in range(len(x))) for m_i in M]

def _dotproduct(xs, ys):
    return _sum(x * y for x, y in zip(xs, ys))

def _vecsumnormalize(xs):
    return [x / _sum(xs) for x in xs]

def _step(x):
    return _iif(x > 0, 1, 0)

def _max(xs):
    return reduce(greatest, xs)

def _argmax(xs):
    return sa.case([(x == _max(xs), i)
                    for i, x in enumerate(xs[:-1])],
                   else_=len(xs)-1)

def _sigmoid(x):
    return 1.0/(1.0 + sa.func.exp(-x))

def _tolist(x):
    if hasattr(x, 'tolist'):
        return x.tolist()
    else:
        return list(x)
    
class SQLAlchemyWriter(ASTProcessor):
    """A SK AST processor, producing a SQLAlchemy expression (or a list of those)"""
    def __init__(self, positive_infinity=float(np.finfo('float64').max), negative_infinity=float(np.finfo('float64').min)):
        self.positive_infinity = positive_infinity
        self.negative_infinity = negative_infinity
    
    def Identifier(self, id):
        return sa.Column(id.id)

    def VectorIdentifier(self, id):
        return [self(IndexedIdentifier(id.id, i, id.size)) for i in range(id.size)]

    def IndexedIdentifier(self, sub):
        warnings.warn("SQL does not support vector types natively. "
                      "Numbers will be appended to the given feature name, "
                      "it may not be what you intend.", UserWarning)
        return sa.Column("{0}{1}".format(sub.id, sub.index+1))

    def NumberConstant(self, num):
        # Infinities have to be handled separately
        if np.isinf(num.value):
            return self.positive_infinity if num.value > 0 else self.negative_infinity
        else:
            return num.value

    def VectorConstant(self, vec):
        return [self(NumberConstant(v)) for v in _tolist(vec.value)]

    def MatrixConstant(self, mtx):
        return [[self(NumberConstant(v)) for v in _tolist(row)] for row in mtx.value]

    def MakeVector(self, vec):
        return [self(el) for el in vec.elems]

    def UnaryFunc(self, op):
        return self(op.op)(self(op.arg))

    def ElemwiseUnaryFunc(self, op):
        arg = self(op.arg)
        if not isinstance(arg, list):
            raise ValueError("Elementwise operations are only supported for vectors")
        return list(map(self(op.op), arg))

    def BinOp(self, op):
        return self(op.op)(self(op.left), self(op.right))
    CompareBinOp = BinOp

    def ElemwiseBinOp(self, op):
        left = self(op.left)
        right = self(op.right)
        op = self(op.op)
        if not isinstance(left, list) or not isinstance(right, list):
            raise ValueError("Elementwise operations are only supported for vectors")
        if len(left) != len(right):
            raise ValueError("Sizes of the arguments do not match")
        return [op(l, r) for l, r in zip(left, right)]

    def IfThenElse(self, node):
        tst, iftrue, iffalse = self(node.test), self(node.iftrue), self(node.iffalse)
        if isinstance(iftrue, list):
            if not isinstance(iffalse, list) or len(iftrue) != len(iffalse):
                raise ValueError("Mixed types in IfThenElse expressions are not supported")
            return [sa.case([(tst, ift)], else_=iff) for ift, iff in zip(iftrue, iffalse)]
        else:
            if isinstance(iffalse, list):
                raise ValueError("Mixed types in IfThenElse expressions are not supported")
            return sa.case([(tst, iftrue)], else_=iffalse)
    
    Mul = _is(lambda x, y: x * y)
    Div = _is(lambda x, y: x / y)
    Add = _is(lambda x, y: x + y)
    LtEq = _is(lambda x, y: x <= y)
    MatVecProduct = _is(_matvecproduct)
    Sub = _is(lambda x, y: x - y)
    USub = _is(lambda x: -x)
    DotProduct = _is(_dotproduct)
    Exp = _is(sa.func.exp)
    Log = _is(sa.func.log)
    Step = _is(_step)
    VecSum = _is(_sum)
    Sigmoid = _is(_sigmoid)
    VecSumNormalize = _is(_vecsumnormalize)
    SKLearnSoftmax = _is(_sklearn_softmax)
    ArgMax = _is(_argmax)

    def Let(self, let):
        # In principle we may consider compiling Let expressions into a series of separate statements, which
        # may be used in a sequence of "with" statements.
        raise NotImplementedError("Let expressions are not implemented. Use substitute_variables instead.")

    Reference = Definition = None



# ------- SQLAlchemy "greatest" function
# See https://docs.sqlalchemy.org/en/latest/core/compiler.html
#pylint: disable=wrong-import-position,wrong-import-order
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import Numeric

class greatest(expression.FunctionElement):
    type = Numeric()
    name = 'greatest'

@compiles(greatest)
def default_greatest(element, compiler, **kw):
    res = compiler.visit_function(element, **kw)
    return res

@compiles(greatest, 'sqlite')
@compiles(greatest, 'mssql')
@compiles(greatest, 'oracle')
def case_greatest(element, compiler, **kw):
    arg1, arg2 = list(element.clauses)
    return compiler.process(sa.case([(arg1 > arg2, arg1)], else_=arg2), **kw)

# Utilities ----------------------------------
import sqlalchemy.dialects
from sqlalchemy.dialects import *   # Must do it in order to getattr(sqlalchemy.dialects, ...)
def to_sql(sa_exprs, dialect_name='sqlite', assign_to='y'):
    """
    Helper function. Given a SQLAlchemy expression (or a list of those), returns the corresponding
    SQL string in a given dialect.

    If assign_to is None, the returned value is a list
    of strings (one for each output component).

    If assign_to is a list of column names,
    the returned value is a single string of the form
    "(first sql expr) as <first target name>,
     (second sql expr) as <second target name>,
     ...
     (last sql expr) as <last target name>"
    
     If assign_to is a single string <y>, the target columns are named '<y>1, <y>2, ..., <y>n',
     if there are several, or just '<y>', if there is only one..
     """
    
    dialect_module = getattr(sqlalchemy.dialects, dialect_name)
    if not isinstance(sa_exprs, list):
        sa_exprs = [sa_exprs]
    qs = [q.compile(dialect=dialect_module.dialect(),
                    compile_kwargs={'literal_binds': True}) for q in sa_exprs]

    if assign_to is None:
        return [str(q) for q in qs]

    if isinstance(assign_to, str):
        if len(qs) > 1:
            assign_to = ['{0}{1}'.format(assign_to, i+1) for i in range(len(qs))]
        else:
            assign_to = [assign_to]
    
    if len(assign_to) != len(qs):
        raise ValueError("The number of resulting SQL expressions does not match the number of "
                         "target column names.")

    return ',\n'.join(['{0} as {1}'.format(q, tgt) for q, tgt in zip(qs, assign_to)])
