"""ISOLATED LAB FIXTURE: never imported or exposed by the application."""


def calculate(expression):
    """Unsafe example for SAST detection only. Do not execute untrusted input."""
    return eval(expression)
