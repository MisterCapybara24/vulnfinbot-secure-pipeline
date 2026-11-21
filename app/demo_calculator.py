"""Remediated isolated example: parse a bounded decimal, never execute code."""
from decimal import Decimal, InvalidOperation


def calculate(expression):
    if not isinstance(expression, str) or len(expression) > 32:
        raise ValueError("Expected a short decimal number")
    try:
        value = Decimal(expression)
    except InvalidOperation as error:
        raise ValueError("Only decimal numbers are supported") from error
    if not value.is_finite():
        raise ValueError("Expected a finite decimal")
    return value
