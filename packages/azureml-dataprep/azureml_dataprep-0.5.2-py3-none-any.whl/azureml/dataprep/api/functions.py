# Copyright (c) Microsoft Corporation. All rights reserved.
""" Module containing higher level function expressions. 
"""

from .expressions import (Expression, InvokeExpression, IdentifierExpression, ValueExpression, _ensure_expression,
                          _assert_expression, IntExpressionLike, BoolExpressionLike)
from .engineapi.typedefinitions import TrimType


def round(value: Expression, decimal_places: IntExpressionLike) -> Expression:
    """
    Creates an expression that will round the result of the expression specified by the desired number of decimal places.

    :param value: An expression that returns the value to round.
    :param decimal_places: The number of desired decimal places. Can be a value or an expression.
    :return: An expression that results in the rounded number.
    """
    _assert_expression(value)
    decimal_places = _ensure_expression(decimal_places)
    return InvokeExpression(InvokeExpression(IdentifierExpression('AdjustColumnPrecision'), [decimal_places]), [value])


def trim_string(value: Expression,
                trim_left: BoolExpressionLike=True,
                trim_right: BoolExpressionLike=True) -> Expression:
    """
    Creates an expression that will trim the string resulting from the expression specified.

    :param value: An expression that returns the value to trim.
    :param trim_left: Whether to trim from the beginning. Can be a value or an expression.
    :param trim_right: Whether to trim from the end. Can be a value or an expression.
    :return: An expression that results in a trimmed string.
    """
    _assert_expression(value)
    return InvokeExpression(InvokeExpression(IdentifierExpression('TrimStringTransform'), [
        _ensure_expression(trim_left),
        _ensure_expression(trim_right),
        ValueExpression(TrimType.WHITESPACE.value),
        ValueExpression(None)
    ]), [value])
