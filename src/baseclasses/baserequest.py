import logging

import allure

import requests


class BaseRequest:
    def __init__(self, base_url: str, logger: logging, token: str = ''):
        self.base_url = base_url
        self.logger = logger
        self.token = token

    @allure.step("Making {method} request to '{path}'")
    def _request(self, method: str, path: str, params: dict = None, data: dict = None, headers: dict = None,
                 retry_count: int = 3) -> tuple[requests.Response, logging]:
        """
        Request wrapper - adds request retry and logging functionality
        """
        if params is None:
            params = {}

        url = f"{self.base_url}{path}"

        if self.token != '':
            params.update({"api_token": self.token})

        self.logger.info(f"Making {method} request to {url}")
        self.logger.info(f"Authorization params {params}")
        stop_flag = False
        attempt = 0

        response = None
        while not stop_flag:
            attempt += 1
            try:

                match method:
                    case "GET":
                        response = requests.get(url, params=params, headers=headers)
                    case "POST":
                        response = requests.post(url, params=params, data=data, headers=headers)
                    case "DELETE":
                        response = requests.delete(url)
                    case _:
                        raise NotImplementedError

            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout error, retry attempt {attempt}")
            except requests.exceptions.TooManyRedirects:
                self.logger.warning(f"TooManyRedirects error, retry attempt {attempt}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error {e}")
                raise requests.exceptions.RequestException(e)

            if response.ok or attempt > retry_count:
                stop_flag = True

        return response, self.logger

    def get(self, path: str = "/", params: dict = None, headers: dict = None):
        return self._request("GET", path=path, params=params, headers=headers)

    def post(self, path: str = "/", params: dict = None, data: dict = None, headers: dict = None):
        return self._request("POST", path=path, params=params, data=data, headers=headers)

    def delete(self, path: str = "/"):
        return self._request("DELETE", path=path)
