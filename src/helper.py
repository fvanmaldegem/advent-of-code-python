import requests
import time
from functools import cache
from dotenv import dotenv_values
from collections.abc import Callable

ADVENT_OF_CODE_URL: str = "https://adventofcode.com/"
ENV_SESSION_TOKEN: str = "SESSION_TOKEN"

class Aoc:
    _year: int
    _day: int
    _aoc_url: str
    _session_token: str
    _test: bool

    def __init__(
        self,
        year: int,
        day: int,
        test: bool = False,
        aoc_url: str = ADVENT_OF_CODE_URL
    ):
        self._year = year
        self._day = day
        self._test = test
        self._aoc_url = aoc_url
        self.__set_environment()

    def solve(self, fn: Callable[[str], int]) -> int:
        return fn(self.__get_input())


    def __get_input(self) -> str:
        if self._test:
            return self.__get_input_from_file()
        
        return self.__get_input_from_url()

    def __get_input_from_url(self) -> str:
        pass

    def __get_input_from_url(self) -> str:
        session = requests.Session()
        if self._session_token is None:
            exit(1)
        
        session.cookies.set("session", self._session_token)
        url = self.__format_aoc_url(self._aoc_url, self._year, self._day)

        response = session.get(url)
        if response.status_code != requests.codes["ok"]:
            exit(1)
        
        return response.text

    @staticmethod
    def __format_aoc_url(url: str, year: int, day: int) -> str:
        return f"{url}/{year}/day/{day}/input"


    def __set_environment(self) -> None:
        environment = dotenv_values()
        if environment[ENV_SESSION_TOKEN] is not None:
            self._session_token = environment[ENV_SESSION_TOKEN]
