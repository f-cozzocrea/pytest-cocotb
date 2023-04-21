from typing import Any
from multiprocessing.managers import BaseManager

class CocotbManager(BaseManager): pass

class CocotbConnection():
    def __init__(self):
        self.__arg_dict = {}
        self.__error_dict = {}

    def get_args(self, testname: str) -> dict[str, Any]:
        return self.__arg_dict[testname]

    def add_args(self, testname: str, **kwargs) -> None:
        if testname in self.__arg_dict:
            self.__arg_dict[testname] = {**self.__arg_dict[testname], **kwargs}
        else:
            self.__arg_dict[testname] = kwargs

    def remove_args(self, testname: str) -> None:
        self.__arg_dict.pop(testname)

    def get_error(self, testname: str) -> list[AssertionError]:
        return self.__error_dict[testname]

    def add_error(self, testname: str, error: AssertionError) -> None:
        if testname in self.__error_dict:
            self.__error_dict[testname].append(error)
        self.__error_dict[testname] = [error]

    def remove_error(self, testname: str) -> None:
        self.__error_dict.pop(testname)