from unittest2pytest.fixes.fix_self_assert import parenthesize_expression, _method_map, FixSelfAssert
from lib2to3.fixer_util import (Name, Node, syms)
from functools import partial


def ReverseCompOp(op, left, right, kws):
    op = Name(op, prefix=" ")
    left = parenthesize_expression(left)
    right = parenthesize_expression(right)

    left.prefix = right.prefix
    right.prefix = left.prefix

    right.prefix = ""
    if '\n' not in left.prefix:
        left.prefix = " "

    return Node(syms.comparison, (right, op, left), prefix=" ")


_replace_method_map = {
    # simple ones
    'assertEqual': partial(ReverseCompOp, '=='),
    'assertNotEqual': partial(ReverseCompOp, '!='),
    'assertGreater': partial(ReverseCompOp, '>'),
    'assertGreaterEqual': partial(ReverseCompOp, '>='),
    'assertIn': partial(ReverseCompOp, 'in'),
    'assertIs': partial(ReverseCompOp, 'is'),
    'assertIsNot': partial(ReverseCompOp, 'is not'),
    'assertLess': partial(ReverseCompOp, '<'),
    'assertLessEqual': partial(ReverseCompOp, '<='),
    'assertNotIn': partial(ReverseCompOp, 'not in'),

    # types ones
    'assertDictEqual': partial(ReverseCompOp, '=='),
    'assertListEqual': partial(ReverseCompOp, '=='),
    'assertMultiLineEqual': partial(ReverseCompOp, '=='),
    'assertSetEqual': partial(ReverseCompOp, '=='),
    'assertTupleEqual': partial(ReverseCompOp, '=='),
}


class FixReverseSelfAssert(FixSelfAssert):
    explicit = True
    """Reverse of FixSelfAssert"""
    for key in _replace_method_map.keys():
        if key in _method_map:
            _method_map[key] = _replace_method_map[key]
