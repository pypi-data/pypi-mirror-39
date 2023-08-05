# Copyright 2016 Rakuten Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division, print_function

import tempfile
import time
import urllib.parse

import requests
import six

def delayable(func):
    """Decorator to allow delay in function calls. The decorator requires the
    function to have the ``_delay`` argument in kwargs.
    """
    def wrapped_func(*args, **kwargs):
        if '_delay' in kwargs:
            time.sleep(kwargs['_delay'])
        return func(*args, **kwargs)
    return wrapped_func

class Client:
    """Client to setup configuration needed for API requests.

    :param tenant: The tenant name assigned to user in their credentials.
    :type tenant: str

    :param token: The token assigned to user in their credentials.
    :type token: str
    """
    def __init__(self, rapidapi_key):
        self.url = "https://dev-rit-singapore-rit-machine-translation-v1.p.rapidapi.com/"
        self.rapidapi_key = rapidapi_key
        self.headers = {"X-RapidAPI-Key": "{}".format(self.rapidapi_key),
                        "Content-Type": "text/plain"}

    @delayable
    def poll_translation_job(self, job_id, _delay=0):
        """Poll the status of a particular translation job.

        :param job_id: Job ID from the ``start_translation_job`` response.
        :type job_id: str

        :param _delay: Allow delays before calling the function.
        :type _delay: int

        :returns: Returns a the response object
        :rtype: ``requests.models.Response``
        """
        service_url = urllib.parse.urljoin(self.url, '/'.join([self._version, 'tasks', job_id]))
        return requests.get(service_url, headers=headers)

    def translate(self, text, target_language, source_language='en'):

        task = 'translate/task/{}-{}'.format(source_language, target_language)
        service_url =self.url + task
        print(headers)
        return requests.post(service_url, headers=headers, data=text)
