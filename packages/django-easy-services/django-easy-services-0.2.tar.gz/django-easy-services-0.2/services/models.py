import json
import time
import urllib

import asyncio
import requests

from django.db import models


class Service(models.Model):
    METHOD_CHOICES = (
        (u'get', u'get'),
        (u'post', u'post'),
        (u'patch', u'patch'),
        (u'put', u'put'),
    )
    name = models.CharField(max_length=200, default='', db_index=True)
    url = models.URLField(max_length=200, default='')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='get')
    timeout = models.IntegerField(blank=True, null=True, default=None)
    verify = models.BooleanField(default=True)
    headers = models.TextField(blank=True, default='')
    parameters = models.TextField(blank=True, default='')
    service_failover = models.ManyToManyField("self", through='ServiceFailover', symmetrical=False,
                                              related_name='service_failover_relation')
    debug_url = models.URLField(max_length=200, blank=True, default='')
    debug_headers = models.TextField(blank=True, default='')
    debug_parameters = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    async def request_async_task(self, debug=False, max_retry=10, retry_interval=1,
                                 header_data=None, get_data=None, url_data=None, parse_data=None, parameters=None):
        service_response = self.request_recursive(debug=debug, header_data=header_data, get_data=get_data,
                                                  url_data=url_data, parse_data=parse_data,
                                                  parameters=parameters)
        current_try = 1
        while not service_response['success'] and (max_retry == 0 or max_retry < current_try):
            time.sleep(retry_interval)
            if max_retry != 0:
                current_try += 1
            service_response = self.request_recursive(debug=debug, header_data=header_data,
                                                      get_data=get_data,
                                                      url_data=url_data, parse_data=parse_data,
                                                      parameters=parameters)

    def request_async(self, debug=False, max_retry=10, retry_interval=1, header_data=None,
                      get_data=None, url_data=None, parse_data=None, parameters=None):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.request_async_task(debug=debug, max_retry=max_retry, retry_interval=retry_interval,
                                                        header_data=header_data, get_data=get_data, url_data=url_data,
                                                        parse_data=parse_data, parameters=parameters))
        loop.close()

    def request_recursive(self, debug=False, header_data=None, get_data=None, url_data=None, parse_data=None,
                          parameters=None):
        response = self.request(debug=debug, header_data=header_data, get_data=get_data,
                                url_data=url_data, parameters=parameters)
        if response.get('result') == 'OK':
            return response
        elif self.pk and self.service_failover.count() is not 0:
            response_failover_stack = []
            for service_for_failover in self.service_failover.all():
                response_failover, result_failover = service_for_failover.get_service_data(debug=debug,
                                                                                           header_data=header_data,
                                                                                           get_data=get_data,
                                                                                           url_data=url_data,
                                                                                           parse_data=parse_data,
                                                                                           parameters=parameters)
                if response_failover.get('result') == 'OK':
                    return response_failover, result_failover
                response_failover_stack.append(response_failover)
            response.update({'failovers': response_failover_stack})
        return response

    def request(self, debug=False, header_data=None, get_data=None, url_data=None, parameters=None):
        headers = {}

        if debug and self.debug_headers:
            service_headers = self.debug_headers
        else:
            service_headers = self.headers

        if service_headers:
            headers = json.loads(service_headers)
            for headers_key in headers:
                if header_data and headers[headers_key] and headers[headers_key] in header_data:
                    headers[headers_key] = header_data[headers[headers_key]]

        data = {}
        if debug and self.debug_parameters:
            service_parameters = self.debug_parameters
        else:
            service_parameters = self.parameters

        if service_parameters:
            data = json.loads(service_parameters)
            for data_key in data:
                if data[data_key] and get_data and data[data_key] in get_data:
                    data[data_key] = get_data[data[data_key]]
        elif parameters:
            data = parameters

        if debug and self.debug_url:
            service_url = self.debug_url
        else:
            service_url = self.url

        if url_data:
            for url_data_key in url_data:
                service_url = service_url.replace(url_data_key, url_data[url_data_key])

        response = self.get_from_service(service_url, headers, data)

        return response

    def get_from_service(self, url, headers, data):
        if self.timeout:
            timeout = self.timeout
        else:
            timeout = 10
        try:
            if self.method == 'post':
                result = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout, verify=self.verify)
            elif self.method == 'get':
                data = urllib.parse.urlencode(data)
                if data:
                    url = url + '?' + data
                result = requests.get(url, headers=headers, timeout=timeout, verify=self.verify)
            elif self.method == 'patch':
                result = requests.patch(url, data=json.dumps(data), headers=headers, timeout=timeout, verify=self.verify)
            elif self.method == 'put':
                result = requests.put(url, data=json.dumps(data), headers=headers, timeout=timeout, verify=self.verify)
            try:
                response = result.json()
            except:
                response = {}
            if result.status_code >= 400:
                response = {"result": "error", "success": False, "content": response, "code": result.status_code,
                            "elapsed": result.elapsed.seconds + result.elapsed.microseconds / 1000000.0}
            else:
                response = {"result": "ok", "success": True, "content": response, "code": result.status_code,
                            "elapsed": result.elapsed.seconds + result.elapsed.microseconds / 1000000.0}

        except requests.exceptions.Timeout:
            response = {"result": "error", "success": False, "content": 'service timeout', "elapsed": timeout,
                        "code": 408}
        except requests.exceptions.ConnectionError:
            response = {"result": "error", "success": False, "content": 'connection error', "code": 503}
        return response


class ServiceFailover(models.Model):
    service = models.ForeignKey(Service, related_name='service', on_delete=models.CASCADE)
    failover = models.ForeignKey(Service, related_name='failover', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField("order")

    def __str__(self):
        return self.service.__str__() + '-' + self.failover.__str__()

    class Meta:
        ordering = ['order']
