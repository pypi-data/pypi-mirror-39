# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json
from typing import List

from httpbase import HTTPBaseClient, Route, HTTPMethods, HTTPResponseCodes, Response


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ShortenerException(Exception):
    pass


class ShortenerServerException(ShortenerException):
    pass


class ShortenerClientException(ShortenerException):
    pass


class DuplicateEndingException(ShortenerException):
    pass


class StatTypes:
    day = "day"
    country = "country"
    referer = "referer"


def get_hours_ago(dt: datetime=None, hours=12):
    if dt is None:
        dt = datetime.now()
    one_week_ago = dt - timedelta(hours=hours)
    return one_week_ago.strftime(DATE_FORMAT)


def get_days_ago(dt: datetime=None, days=3):
    return get_hours_ago(dt, hours=days * 24)


def get_weeks_ago(dt: datetime=None, weeks=1):
    return get_hours_ago(dt, weeks * 7 * 24)


class Polr(HTTPBaseClient):
    ShortenerException = ShortenerException
    ShortenerServerException = ShortenerServerException
    ShortenerClientException = ShortenerClientException
    DuplicateEndingException = DuplicateEndingException

    def __init__(self, url: str, api_key: str):
        """
        Args:
            url: Base URL for the Polr service, don't include the api path.: Example: https://polr.example.com
            api_key: An API key for the Polr link shortener service.

        Raises:
            ShortenerException: Raised if ``api_key`` is a falsey value or ``None``
        """
        if not api_key:
            raise ShortenerException("API key is required!")
        if url.endswith("/"):
            url = url[:-1]
        super().__init__(baseurl=url)
        self.api_key = api_key

    def shorten(self, url: str, ending: str= "", is_secret: bool=False, raise_on_exists: bool=False) -> str:
        """
        Get a shortened URL from the Polr service. Accepts a parameter for a custom ending. If a link with the
        same custom ending already exists the link is returned. An exception is raised if in that situation if
        ``raise_on_exists`` is ``True``.

        Args:
            url: The URL to be shortened
            ending: An optional custom ending for the link: Default: ""
            is_secret: whether the URL should be a secret URL or not. Default: False
            raise_on_exists: Raise an exception if a link with the given ``ending``
                already exists. Default: False

        Raises:
            ShortenerClientException: raised if a bad request is made and a 4XX class response is received.
            ShortenerServerException: Raised if there is an error communicating with the service.
            ShortenerException: An unexpected response code is received
            DuplicateEndingError: Raised if a link with the given ``ending`` already exists and
                ``raise_on_exists`` is ``True``.
        """
        route = Route("/api/v2/action/shorten", HTTPMethods.POST, {"key", "ending", "url", "is_secret"})
        params = {"key": self.api_key, "url": url, "is_secret": is_secret}
        if ending:
            if self.exists(ending):
                if raise_on_exists:
                    raise DuplicateEndingException(f"link with the ending {ending} already exists")
                else:
                    return f"{self.baseurl}/{ending}"

            params["custom_ending"] = ending

        resp = self._make_request(route, params=params)
        self._raise_on_error_code(resp)
        if resp.status_code == HTTPResponseCodes.OK:
            return resp.content.decode("utf8")
        else:
            raise ShortenerException(f"unexpected response code {resp.status_code}: {resp.content.decode('utf8')}")

    def shorten_bulk(self, links: List[dict]) -> dict:
        """
        Used for shortening a list of links in a single call.

        Args:
            links: A list of link definitions. A link definition has the following structure::

                {
                    "url": "https://polrproject.org/",
                    "is_secret": [True|False],
                    "custom_ending": "my-ending",
                }

        Raises:
            ShortenerClientException: raised if a bad request is made and a 4XX class response is received.
            ShortenerServerException: Raised if there is an error communicating with the service.
            ShortenerException: An unexpected response code is received
            DuplicateEndingError: Raised if a link with the given ``custom_ending`` already exists and
                ``raise_on_exists`` is ``True``.
        """
        route = Route("/api/v2/action/shorten_bulk", HTTPMethods.POST, {"key", "data"})
        js = json.dumps({"links": links})
        resp = self._make_request(route, params={"key": self.api_key, "data": js})
        if resp.status_code == HTTPResponseCodes.BAD_REQUEST:
            err_data = resp.json()
            raise ShortenerClientException(f"{err_data['status_code']} {err_data['error_code']}: {err_data['error']}")
        elif HTTPResponseCodes.is_4xx_code(resp.status_code):
            raise ShortenerClientException(f"error making request: {resp.content}")
        elif HTTPResponseCodes.is_5xx_code(resp.status_code):
            raise ShortenerServerException(f"error communicating with Polr server: {resp.content}")
        elif resp.status_code == HTTPResponseCodes.OK:
            return resp.json()
        else:
            raise ShortenerException(f"unexpected response code {resp.status_code}: {resp.content}")

    def exists(self, ending: str) -> bool:
        """
        Check to see if a link with the given ending already exists.

        Args:
            ending: The ending to check

        Raises:
            ShortenerException: Raised if there is an error communicating with the service.
        """
        route = Route("/api/v2/data/lookup", HTTPMethods.GET, {"key", "url_ending"})
        params = {"key": self.api_key, "url_ending": ending}
        resp = self._make_request(route, params=params)
        if resp.status_code == HTTPResponseCodes.NOT_FOUND:
            return False
        elif resp.status_code == HTTPResponseCodes.OK:
            return True
        else:
            raise ShortenerException(f"error looking up link: {resp.content}")

    def lookup(self, ending: str) -> str:
        route = Route("/api/v2/action/lookup", HTTPMethods.GET, {"key", "url_ending"})
        resp = self._make_request(route, params={"key": self.api_key, "url_ending": ending})
        self._raise_on_error_code(resp)
        return resp.content.decode("utf8")

    def data(self, ending: str, start: str=None, end: str=None, stats_type: str=StatTypes.day) -> dict:
        """
        Fetch data for the given ``ending``. By default, this API endpoint will only allow users to fetch a maximum
        of 365 days of data. This setting can be modified in the .env configuration file on the server.

        Args:
            ending: The ending to look up
            start: a start date in the format: %Y-%M-%D %h:%m:%S
            end: an end date in the format: %Y-%M-%D %h:%m:%S
            stats_type: The type of stats to fetch:
                day: click counts for each day from ``start`` to ``end``
                country: click counts per country
                referer: click counts per referer

        Raises:
            ShortenerClientException: raised if a bad request is made and a 4XX class response is received.
            ShortenerServerException: Raised if there is an error communicating with the service.
            ShortenerException: An unexpected response code is received

        """
        if end is None:
            end = datetime.now()
        if start is None:
            start = get_weeks_ago(end)
        valid_params = {"key", "url_ending", "left_bound", "right_bound", "stats_type"}
        params = {
            "key": self.api_key,
            "url_ending": ending,
            "left_bound": start,
            "right_bound": end.strftime(DATE_FORMAT),
            "stats_type": stats_type,
        }
        route = Route("/api/v2/data/link", HTTPMethods.GET, valid_params)
        resp = self._make_request(
            route,
            params=params
        )
        if resp.status_code == HTTPResponseCodes.BAD_REQUEST:
            raise ShortenerClientException(f"error making request: {resp.content}")
        elif resp.status_code == HTTPResponseCodes.INTERNAL_SERVER_ERROR:
            raise ShortenerException(f"error communicating with Polr server: {resp.content}")
        elif resp.status_code == HTTPResponseCodes.NOT_FOUND:
            raise ShortenerClientException(f"{resp.content.decode('utf8')}")
        return resp.json()

    @staticmethod
    def _raise_on_error_code(resp: Response):
        if HTTPResponseCodes.is_4xx_code(resp.status_code):
            raise ShortenerClientException(f"error making request: {resp.content.decode('utf8')}")
        elif HTTPResponseCodes.is_5xx_code(resp.status_code):
            raise ShortenerServerException(f"error communicating with Polr server: {resp.content.decode('utf8')}")
