from authomatic.adapters import WebObAdapter

class Webapp3Adapter(WebObAdapter):
    """
    Authomatic Adapter for the |webapp2|_ framework.


    """

    def __init__(self, handler):
        """
        :param handler:
            A :class:`webapp2.RequestHandler` instance.
        """
        self.request = handler.request
        self.response = handler.response
