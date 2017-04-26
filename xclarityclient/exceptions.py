import sys
import six


class XClarityClientException(Exception):
    """Base XClarity Client Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.
    """
    msg_fmt = "An exception occurred."
    code = 500

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if message is None:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                exc_info = sys.exc_info()
                six.reraise(*exc_info)

        self.message = message
        super(XClarityClientException, self).__init__(message)

    def get_message(self):
        # The first argument to XClarityClientException message,
        # it should be message (see __init__)
        return self.message


class NodeDetailsException(XClarityClientException):
    msg_fmt = 'Failed to get the details of node %(node_id)s: %(detail)s'


class BadRequestException(XClarityClientException):
    msg_fmt = 'Bad Request: %(action)s'
    code = 400


class FailToSetPowerStatusException(XClarityClientException):
    msg_fmt = 'Failed to set the power status of node %(node_id)s: %(action)s'
