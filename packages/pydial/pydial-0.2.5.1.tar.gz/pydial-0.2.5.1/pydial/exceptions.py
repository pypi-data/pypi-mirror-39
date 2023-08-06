class MappingException(Exception):
    pass


class RuleConfigurationException(Exception):
    pass


class NotApplicableException(Exception):

    def __init__(self, origin, fc_obj, message=None):
        super(NotApplicableException, self).__init__(message)
        self.origin = origin
        self.fc_obj = fc_obj

    def __str__(self):
        output = "{name} isn't applicable to {pid} :: {message}".format(
            name=self.origin,
            pid=self.fc_obj.pid,
            message=self.message
        )
        return output
