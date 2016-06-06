#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
from pocsuite.thirdparty import requests
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.enums import CUSTOM_LOGGING


class Zoomeye(object):

    def __init__(self, token, host="api.zoomeye.org"):
        self._base_uri = "http://%s" % host
        self._headers = {"Authorization": "JWT %s" % token, "Content-Type": "application/json"}

    def _response_for(self, path):
        uri = "/".join([self._base_uri, path])
        response = requests.get(uri, headers=self._headers)
        if response.status_code == 200:
            body = self._handle_success(response, uri)
            return body
        else:
            self._handle_error(response, uri)

    def _handle_success(self, response, uri):
        try:
            return response.json()
        except ValueError as ex:
            logger.log(CUSTOM_LOGGING.ERROR, ex)

    def _handle_error(self, response, uri):
        status = response.status_code

        if 400 <= status < 500:
            self._handle_4xx_status(response, status, uri)
        elif 500 <= status < 600:
            self._handle_5xx_status(status, uri)
        else:
            self._handle_non_200_status(status, uri)

    def _handle_non_200_status(self, status, uri):
        errMsg = "Received a very surprising HTTP status %i for %s" % (status, uri)
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    def _handle_5xx_status(self, status, uri):
        errMsg = "Received a server error %i for %s" % (status, uri)
        logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    def _handle_4xx_status(self, response, status, uri):
        if not response.content:
            errMsg = "Received a %i error for %s with no body." % (status, uri)
            logger.log(CUSTOM_LOGGING.ERROR, errMsg)
        elif response.headers["Content-Type"].find("json") == -1:
            errMsg = "Received a %i for %s with the following body: %s" % (status, uri, response.content)
            logger.log(CUSTOM_LOGGING.ERROR, errMsg)

        try:
            body = response.json()
        except ValueError:
            errMsg = "Received a %i error for %s but it did not include the expected JSON body" % (status, uri)
            logger.log(CUSTOM_LOGGING.ERROR, errMsg)
        else:
            if "error" in body:
                self._handle_web_service_error(body.get("error"), status, uri)
            else:
                errMsg = "Response contains JSON but it does not specify code or error keys"
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)

    def _handle_web_service_error(self, message, status, uri):
        if message == "unauthorized":
            errMsg = "AuthenticationError, please check your Zoomeye Token"
            logger.log(CUSTOM_LOGGING.ERROR, errMsg)
        else:
            logger.log(CUSTOM_LOGGING.ERROR, message)

    def resource_info(self):
        return self._response_for("resources-info")

    def search(self, keyword, page=1, searchtype="web"):
        path = '%s/search?query="%s"&page=%s&fact=app,os' % (searchtype, keyword, page)
        return self._response_for(path)


if __name__ == "__main__":
    z = Zoomeye("RSjz3c")
    print z.search("port:80")
