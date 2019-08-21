# -*- coding: utf-8 -*-

# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import IntEnum, unique
from typing import Optional


@unique
class ExceptionCode(IntEnum):
    OK = 0
    SYSTEM_ERROR = 1
    CONTRACT_NOT_FOUND = 2
    METHOD_NOT_FOUND = 3
    METHOD_NOT_PAYABLE = 4
    ILLEGAL_FORMAT = 5
    INVALID_PARAMETER = 6
    INVALID_INSTANCE = 7
    INVALID_CONTAINER_ACCESS = 8
    ACCESS_DENIED = 9
    OUT_OF_STEP = 10
    OUT_OF_BALANCE = 11
    TIMEOUT_ERROR = 12
    STACK_OVERFLOW = 13
    INVALID_PACKAGE = 14
    METHOD_NOT_ALLOWED = 15

    # Caused by revert call or user-defined exception.
    SCORE_ERROR = 32
    END = 99

    def __str__(self) -> str:
        return str(self.name).capitalize().replace('_', ' ')


class FatalException(BaseException):
    # if this exception is raised on invoke or commit, icon service will be closed
    pass


class InvalidBaseTransactionException(BaseException):
    pass


class IconServiceBaseException(BaseException):
    """All custom exceptions used in IconService should inherit from this
    """

    def __init__(self, message: Optional[str], code: ExceptionCode = ExceptionCode.OK):
        if message is None:
            message = str(code)
        self.__message = message
        self.__code = code

    @property
    def message(self):
        return self.__message

    @property
    def code(self):
        return self.__code

    def __str__(self):
        return f'{self.message} ({self.code})'


class ScoreNotFoundException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.CONTRACT_NOT_FOUND)


class MethodNotFoundException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.METHOD_NOT_FOUND)


class MethodNotPayableException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.METHOD_NOT_PAYABLE)


class InvalidParamsException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.INVALID_PARAMETER)


class AccessDeniedException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ACCESS_DENIED)


class DatabaseException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ACCESS_DENIED)


class InvalidInstanceException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.INVALID_INSTANCE)


class InvalidContainerAccessException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.INVALID_CONTAINER_ACCESS)


class IllegalFormatException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ILLEGAL_FORMAT)


class InvalidRequestException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ILLEGAL_FORMAT)


class InvalidExternalException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ILLEGAL_FORMAT)


class InvalidPayableException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ILLEGAL_FORMAT)


class InvalidEventLogException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ILLEGAL_FORMAT)


class InvalidInterfaceException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.ILLEGAL_FORMAT)


class OutOfBalanceException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.OUT_OF_BALANCE)


class TimeoutException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.TIMEOUT_ERROR)


class StackOverflowException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.STACK_OVERFLOW)


class InvalidPackageException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.INVALID_PACKAGE)


class MethodNotAllowedException(IconServiceBaseException):
    def __init__(self, message: Optional[str]):
        super().__init__(message, ExceptionCode.METHOD_NOT_ALLOWED)


class IconScoreException(IconServiceBaseException):
    # All the user-defined exceptions should inherit from this exception including revert call
    def __init__(self, message: Optional[str], index: int = 0):
        if not isinstance(index, int):
            raise InvalidParamsException('Invalid index type: not an integer')
        code = ExceptionCode.SCORE_ERROR + index
        if code < ExceptionCode.SCORE_ERROR:
            code = ExceptionCode.SCORE_ERROR
        elif code > ExceptionCode.END:
            code = ExceptionCode.END
        super().__init__(message, code)
