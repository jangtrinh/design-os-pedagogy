"""Errors that can be shown without exposing database or filesystem details."""


class RehearsalError(Exception):
    def __init__(self, message, code="invalid_request", status=400):
        super().__init__(message)
        self.code, self.status = code, status
