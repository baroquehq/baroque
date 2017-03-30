from baroque.entities.reactor import Reactor


class ReactorFactory:
    """A factory class that exposes methods to quickly create useful
    :obj:`baroque.entities.reactor.Reactor` instances"""

    @classmethod
    def stdout(cls):
        """Factory method returning a reactor that prints events to stdout.

        Returns:
            :obj:`baroque.entities.reactor.Reactor`

        """
        def action(event):
            print(event)
        return Reactor(action)

    @classmethod
    def call_function(cls, obj, function_name, *args, **kwargs):
        """Factory method returning a reactor that calls a method on an object.

        Args:
            obj (object): the target object
            function_name (function): the function to be invoked on the object

        Returns:
            :obj:`baroque.entities.reactor.Reactor`

        """
        def action(event):
            getattr(obj, function_name)(*args, **kwargs)
        return Reactor(action)

    @classmethod
    def log_event(cls, logger, loglevel):
        """Factory method returning a reactor that logs on a logger at a
        specified loglevel.

        Args:
            logger (:obj:`logging.Logger`): the logger object
            loglevel (int): the logging level

        Returns:
            :obj:`baroque.entities.reactor.Reactor`

        """
        def action(event):
            logger.log(loglevel, str(event))
        return Reactor(action)

    @classmethod
    def json_webhook(cls, url, payload, query_params=None, headers=None):
        """Factory method returning a reactor that POSTs arbitrary
        JSON data to a webhook, along with the specified HTTP headers.

        Args:
            url (str): the webhook URL
            payload (dict): payload data dict to be dumped to JSON and sent
            query_params (dict): dict of query parameters
            headers (dict): dict of headers

        Returns:
            A dict containing the response HTTP status code (int) and payload
            (str), ie: ``{'status': 200, 'payload': None}``

        """
        import requests

        def action(event):
            resp = requests.post(url, params=query_params or dict(),
                                 headers=headers or dict(), json=payload)
            return dict(status=resp.status_code, payload=resp.json())
        return Reactor(action)
