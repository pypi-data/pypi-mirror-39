from simple_model.builder import model_builder


class ResponseFactory:
    """"
    Return a OANDA Response object
    """
    def __init__(self, response, response_type=None):
        self.response_type = response_type or 'OandaResult'
        self.response = response

    def __repr__(self):
        return '<{} object>'.format(self.response_type)

    def as_dict(self):
        return self.response

    def as_obj(self):
        result = self.as_dict()
        return model_builder(result)
