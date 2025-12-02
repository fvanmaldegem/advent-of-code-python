#!/bin/env python
import os
import argparse
import importlib
import time
from functools import cache
from typing import Optional, Iterable
from types import ModuleType
from collections.abc import Callable
from src.helper import Aoc

class App:
    __year: any
    __day: any
    __part: any
    __test: bool
    __perf: bool = False

    def __init__(self):
        self.__parse_args()
    
    def __parse_args(self) -> None:
        parser = argparse.ArgumentParser(
            prog='AdventOfCode',
            description="Advent Of Code in Python",
            epilog="by Floris van Maldegem"
        )

        parser.add_argument("-y", "--year", default=None)
        parser.add_argument("-d", "--day", default=None)
        parser.add_argument("-p", "--part", default=None)
        parser.add_argument("--test", action='store_true')
        parser.add_argument("--perf", action='store_true')

        args = parser.parse_args()

        self.__year = args.year
        self.__day  = args.day
        self.__part = args.part
        self.__test = args.test 
        self.__perf = args.perf

    @staticmethod
    @cache
    def __get_module(year: int, day: int) -> ModuleType:
        project_path = os.path.dirname(__file__)
        d  = f"{day:02}"
        module_name = f"src.y{year}.d{d}"
        module_path = module_name.replace('.', '/')
        module_file_path = f"{project_path}/{module_path}.py"

        if not os.path.exists(module_file_path):
            raise Exception(f"path '{module_file_path}' does not exist")
        
        return importlib.import_module(module_name)

    @staticmethod
    @cache
    def __get_class(module: ModuleType) -> Callable:
        if not hasattr(module, "Solution"):
            raise Exception("module does not contain Solution class")

        return getattr(module, "Solution")

    @staticmethod
    def __get_fn(solution: Callable, part: int) -> Callable[[str], int]:
        method_name = f"solve{part}"

        if not hasattr(solution, method_name):
            raise Exception(f"Solution does not contain {method_name}")
            
        return getattr(solution, method_name)

    def __scan_all(self) -> Iterable[int]:
        valid_years = []

        project_path = os.path.dirname(__file__)
        module_path = f"{project_path}/src"

        if not os.path.exists(module_path):
            raise Exception(f"path '{module_path}' does not exist")

        with os.scandir(module_path) as d:
            for e in d:
                if e.is_dir() and e.name.startswith('y'):
                    valid_years.append(int(e.name.removeprefix('y')))

        return valid_years

    def __scan_year(self, year: int) -> Iterable[int]:
        valid_days = []

        project_path = os.path.dirname(__file__)
        module_path = f"{project_path}/src/y{year}"

        if not os.path.exists(module_path):
            raise Exception(f"path '{module_path}' does not exist")

        with os.scandir(module_path) as d:
            for e in d:
                if e.is_file() and e.name.startswith('d'):
                    n = e.name.removeprefix('d').removesuffix('.py')
                    valid_days.append(int(n))

        return valid_days

    def __get_year(self) -> Optional[int]:
        if self.__year is not None:
            return parse_int_without_prefix(self.__year, 'y')

    def __get_day(self) -> Optional[int]:
        if self.__day is not None:
            return parse_int_without_prefix(self.__day, 'd')

    def __get_part(self) -> Optional[int]:
        if self.__part is not None:
            return parse_int_without_prefix(self.__part)

    def run(self):
        (y, d, p) = (self.__get_year(), self.__get_day(), self.__get_part())
        if y is None and d is None:
            return self.run_all()

        if d is None and p is None:
            return self.run_year(y)

        if p is None:
            return self.run_day(y, d)

        return self.run_part(y, d, p)

    def run_part(self, y: int, d: int, p: int):
        aoc = Aoc(y, d, self.__test)
        module = self.__get_module(y, d)
        solution = self.__get_class(module)
        fn = self.__get_fn(solution, p)

        start = time.perf_counter_ns()
        result = aoc.solve(fn)
        end = time.perf_counter_ns()

        if self.__perf:
            perf = end - start
            return print(f"{y}.{d}.{p} (took {perf} ns): {result}")

        print(f"{y}.{d}.{p}: {result}")

    def run_day(self, y: int, d: int):
        for p in [1, 2]:
            self.run_part(y, d, p)

    def run_year(self, y: int):
        days = self.__scan_year(y)
        for d in days:
            self.run_day(y, d)

    def run_all(self):
        years = self.__scan_all()
        for y in years:
            self.run_year(y)


def parse_int_without_prefix(s: any, prefix: str = '') -> int:
    if type(s) is int:
        return s

    if type(s) is not str:
        raise Exception("unknown type")
    
    s = str(s)
    if s.startswith(prefix):
        return int(s.removeprefix(prefix))

    return int(s)

if __name__ == '__main__':
    app = App()
    app.run()