import requests
from .handlers import AddTimeToIssueHandler
from .handlers import Context
from .handlers import GetAccessibleProjectsHandler
from .handlers import GetIssueHandler
from .handlers import GetIssuesHandler
from .handlers import GetProjectHandler
from .handlers import ResponseHandler

from . import exceptions

codes_map = {
    requests.codes.unauthorized: exceptions.UnauthorizedYouTrackException,
    requests.codes.forbidden: exceptions.ForbiddenYouTrackException,
    requests.codes.not_found: exceptions.NotFoundYouTrackException
}


class BaseConnection:
    url = None
    rest_url = None
    _session = None

    def __init__(self, url, auth):
        url = url.rstrip('/')
        self.url = url
        self.rest_url = url + '/rest'
        self._session = requests.Session()
        self._session.hooks['response'].append(Connection._check_response)
        self._session.headers['Accept'] = 'application/json'
        self._session.auth = auth

    @property
    def session(self):
        if self._session:
            return self._session
        else:
            raise ValueError("Connection's session is empty")

    @staticmethod
    def _check_response(response, *args, **kwargs):
        if not response.ok:
            try:
                message = response.json().get('value')
            except (ValueError, KeyError):
                message = response.text or response.reason
            exc_class = codes_map.get(response.status_code, exceptions.YouTrackException)
            raise exc_class(message)

    def _get(self, path, params=None, **kwargs):
        return self._session.get(self.rest_url + path, params=params, **kwargs).json()

    def _post(self, path, data=None, params=None, **kwargs):
        return self._session.post(self.rest_url + path, data, params=params, **kwargs).json()

    def _put(self, path, data=None, params=None, **kwargs):
        return self._session.put(self.rest_url + path, data, params=params, **kwargs)

    def _delete(self, path, **kwargs):
        return self._session.delete(self.rest_url + path, **kwargs)


class Connection(BaseConnection):
    def get_me(self):
        raise NotImplemented

    def get_user(self, username):
        raise NotImplemented

    def get_issues(self):
        return ResponseHandler(GetIssuesHandler(self, Context(**dict())))

    def get_issue(self, issue_id):
        return ResponseHandler(GetIssueHandler(self, Context(**dict(issue_id=issue_id))))

    def create_issue(self, project_id, summary, description='', attachments={}, **kwargs):
        raise NotImplemented

    def delete_issue(self, issue_id):
        raise NotImplemented

    def create_attachment(self, issue_id, filename, data, author=None, created=None, group=None):
        raise NotImplemented

    def get_project(self, project_id):
        return ResponseHandler(GetProjectHandler(self, Context(**dict(project_id=project_id))))

    def get_accessible_projects(self):
        return ResponseHandler(GetAccessibleProjectsHandler(self, Context(**dict())))

    def add_time_entry(self, entry_id: str, date: int, duration_minutes: int):
        return ResponseHandler(AddTimeToIssueHandler(self,
                                                     Context(**dict(entry_id=entry_id, date=date,
                                                                    duration_minutes=duration_minutes))))
