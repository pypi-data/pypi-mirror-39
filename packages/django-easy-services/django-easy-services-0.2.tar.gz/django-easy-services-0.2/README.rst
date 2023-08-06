========
Services
========

Services is a simple Django app to consume simple json services in a simple way.
You can make requests directly, async or recursive using failover services 
automatically while the services return errors.
Example::

       from services.models import Service

       service_example = Service(name='simple_service', method='get', url='http://example.com/?query_param=<data>')
       url_data = {'<data>': 'example_data'}
       service_response = service_example.request(url_data=get_data)

       if service_response['success']:
           respose_content = service_response['content'] # content is a dict
           print(response_content)

Post example::

       from services.models import Service

       service_example = Service(name='simple_service', method='post', url='http://example.com/', headers='{"Content-Type": "<content_type>"}', parameters= '{"query_param": "<data>"}')
       get_data = {'<data>': 'example_data'}
       header_data = {'<content_type>': 'application/json'}
       service_response = service_example.request(get_data=get_data, header_data=header_data)

       if service_response['success']:
           respose_content = service_response['content'] # content is a dict
           print(response_content)

Or simpler::


       from services.models import Service

       # This headers will be use for every request to this service
       service_example = Service(name='simple_service', method='post', url='http://example.com/', headers='{"Content-Type": "application/json"}')
       # parameters will be put directly to the body of the post request to the service
       parameters = {'query_param': 'example_data'}
       service_response = service_example.request(parameters=parameters)

       if service_response['success']:
           respose_content = service_response['content'] # content is a dict
           print(response_content)

You can also configure failover services, so if the primary service return some error code (for now >= 400) the failover/s will we call one by one untill some of them return a non error code::

       from services.models import Service, ServiceFailover

       service_01 = Service(name='registration_precheck', method='get', url='http://example_01.com/?query_param=<data>').save()
       service_02 = Service(name='registration_precheck', method='get', url='http://example_02.com/?query_param=<data>').save()
       service_03 = Service(name='registration_precheck', method='get', url='http://example_03.com/?query_param=<data>').save()

       ServiceFailover(service=service_01, failover=service_02, order=1).save()
       ServiceFailover(service=service_01, failover=service_03, order=2).save()

       url_data = {'<data>': 'example_data'}

       # Now if service_01 fails service_02 will be execute with the same context data,
       # the same for service_03 if service_02 fails in this call.
       service_response = service_example.request_recursive(url_data=get_data)

       if service_response['success']:
           respose_content = service_response['content'] # content is a dict
           print(response_content)

If you want to publish information to some service but you don't want to wait you can make async request::

       from services.models import Service

       service_example = Service(name='simple_service', method='post', url='http://example.com/', headers='{"Content-Type": "application/json"}')
       parameters = {'query_param': 'example_data'}
       # max_retry is the amount of retries do you want to execute the request while the answer is a error (0 if you want to retry "forever").
       # retry_interval is the amount of seconds you want to wait between retries.
       service_example.request_async(max_retry=10, retry_interval=1, parameters=parameters)


Quick start
-----------

1. Run `pip install django-easy-services`

2. Add "services" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = [
               ...
               'services',
       ]

3. Run `python manage.py migrate` to create the services models.

4. Start the development server and visit http://127.0.0.1:8000/admin/services
   to create a services (you'll need the Admin app enabled).
