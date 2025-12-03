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
    _input: str

    def __init__(
        self,
        year: int,
        day: int,
        aoc_url: str = ADVENT_OF_CODE_URL,
        input_str: str = None
    ):
        self._year = year
        self._day = day
        self._aoc_url = aoc_url
        self.__set_environment()

        if input_str is not None:
            self.set_input(input_str)
        else:
            self.set_input(self.__get_input_from_url())


    def solve(self, fn: Callable[[str], int]) -> int:
        return fn(self._input)

    def set_input(self, s: str) -> None:
        self._input = s

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
