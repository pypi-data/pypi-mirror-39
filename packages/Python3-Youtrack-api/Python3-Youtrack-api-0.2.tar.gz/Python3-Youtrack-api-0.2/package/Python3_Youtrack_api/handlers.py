from .models import BaseModel


class BaseHandler:
    connection = None
    param_data = None
    json_data = None
    schema = None
    url = None
    context = None
    is_fields_dependent = False

    @property
    @classmethod
    def function_handler(cls):
        pass

    @function_handler.setter
    @classmethod
    def function_handler(cls, val):
        cls.function_handler = val

    @function_handler.getter
    @classmethod
    def function_handler(cls):
        return getattr(cls, 'function_handler')

    @property
    @classmethod
    def schema(cls):
        pass

    @classmethod
    def get_function_handler(cls):
        raise NotImplemented

    @classmethod
    def make_url(cls):
        raise NotImplemented
        # pass

    @classmethod
    def make_json_data(cls):
        # raise NotImplemented
        pass

    @classmethod
    def make_param_data(cls):
        # raise NotImplemented
        pass

    def __new__(cls, connection, context):
        cls.connection = connection
        cls.get_function_handler()
        cls.context = context
        cls.make_url()
        print(cls.url)
        cls.make_json_data()
        cls.make_param_data()

        return cls.function_handler(cls.url, json=cls.json_data, params=cls.param_data)


class Context(dict):

    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            self[k] = v


class AddTimeToIssueHandler(BaseHandler):

    @classmethod
    def make_url(cls):
        cls.url = cls.connection.url + '/api/issues/{}/timeTracking/workItems'.format(cls.context.get('entry_id'))

    @classmethod
    def make_json_data(cls):
        cls.json_data = {
            "date": cls.context.get('date'),
            "duration": {
                "minutes": cls.context.get('duration_minutes')
            },
        }

    @classmethod
    def get_function_handler(cls):
        """
        setting handler
        :return:
        """
        cls.function_handler = cls.connection.session.post


class GetAccessibleProjectsHandler(BaseHandler):

    @classmethod
    def make_url(cls):
        cls.url = cls.connection.url + '/api/admin/projects/?&fields=id,name'

    @classmethod
    def get_function_handler(cls):
        """
        setting handler
        :return:
        """
        cls.function_handler = cls.connection.session.get


class GetProjectHandler(BaseHandler):

    @classmethod
    def make_url(cls):
        cls.url = cls.connection.url + '/api/admin/projects/{}/?&fields=id,name'.format(cls.context.get('project_id'))

    @classmethod
    def get_function_handler(cls):
        """
        setting handler
        :return:
        """
        cls.function_handler = cls.connection.session.get


class GetIssueHandler(BaseHandler):

    @classmethod
    def make_url(cls):
        cls.url = cls.connection.url + '/api/issues/{}/?&fields=id,name'.format(cls.context.get('issue_id'))

    @classmethod
    def get_function_handler(cls):
        """
        setting handler
        :return:
        """
        cls.function_handler = cls.connection.session.get


class GetIssuesHandler(BaseHandler):

    @classmethod
    def make_url(cls):
        cls.url = cls.connection.url + '/api/issues/'

    @classmethod
    def get_function_handler(cls):
        """
        setting handler
        :return:
        """
        cls.function_handler = cls.connection.session.get


class ResponseHandler:
    def __new__(cls, response, *args, **kwargs):
        print(dir(response))
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                return BaseModel(data)
            if isinstance(data, list):
                return [BaseModel(d) for d in data]
        else:
            raise Exception("BadResponse")
