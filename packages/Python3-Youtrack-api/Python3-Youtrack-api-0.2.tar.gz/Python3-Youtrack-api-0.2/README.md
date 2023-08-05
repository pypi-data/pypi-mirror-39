# Python3-Youtrack-api
[![PyPI](https://img.shields.io/badge/pypi-0.2-orange.svg)](https://pypi.org/project/Python3-Youtrack-api/) [![PyPI](https://img.shields.io/badge/python-3-blue.svg)](https://pypi.org/project/Python3-Youtrack-api/)

python 3 api for youtrack

What's implemented:
- get_issues
- get_issue
- get_project
- get_accessible_projects
- add_time_entry

Usage
```python
from youtrack.client import Connection

yt = Connection('yt.example.com', auth=('admin', 'admin'))

issue_name = 'prj-1'
date_timestamp = 1543525200000
minutes_spent = 720

yt.add_time_entry(issue_name, date_timestamp, minutes_spent)

```
