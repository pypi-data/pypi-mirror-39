from typing import Iterator
import logging
from urllib.parse import urlparse
from functools import lru_cache

import gitlab
from gitlab.v4.objects import Project, Issue

from .base import AbstractService, AbstractBugEntry

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['GitlabTodoEntry', 'GitlabService']

_log = logging.getLogger(__name__)


class GitlabTodoEntry(AbstractBugEntry):

    def __init__(self, gitlab_issue: Issue, service: 'GitlabService') -> None:
        super().__init__(gitlab_issue.title)
        project = service.get_project_by_id(gitlab_issue.project_id)
        project_name = project.name
        self.issue_key = f"#{project_name}/{gitlab_issue.iid}"
        self.priority = service.default_priority
        self.update_gitlab_projects(service, project)
        self.add_context(service.default_context)
        # Remove https: from link to avoid collon
        parsed_url = urlparse(gitlab_issue.web_url)
        self.add_tag('link', f"{parsed_url.netloc}{parsed_url.path}")
        self.add_tag('service', service.service_name)
        if service.milestone_support and gitlab_issue.milestone is not None:
            due_date = gitlab_issue.milestone['due_date']
            start_date = gitlab_issue.milestone['start_date']
            self.add_tag('milestone', gitlab_issue.milestone['title'].replace(' ', ''))
            if due_date is not None:
                self.add_tag('due', due_date.split('T')[0])
            if start_date is not None:
                self.add_tag('t', start_date.split('T')[0])

    def update_gitlab_projects(self, service: 'GitlabService', project) -> None:
        if service.group_as_project and project.namespace['kind'] == 'group':
            self.add_project(project.namespace['full_path'])
        if service.user_as_project and project.namespace['kind'] == 'user':
            self.add_project(project.namespace['full_path'])
        if service.project_as_project:
            self.add_project(project.name)


class GitlabService(AbstractService):

    __slots__ = [
        'gitlab', 'assignee', "group_as_project", 'milestone_support',
        'default_priority', 'default_context', "project_as_project", "user_as_project"
    ]

    _service_type = 'gitlab'

    def __init__(
            self, link: str, token: str,
            assignee: str, default_priority: str,
            default_context: str, project_as_project: bool = True,
            user_as_project: bool = False, group_as_project: bool = False,
            milestone_support: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.gitlab = gitlab.Gitlab(link, token, api_version=4)
        self.assignee = assignee
        self.default_priority = default_priority
        self.default_context = default_context
        self.group_as_project = group_as_project
        self.user_as_project = user_as_project
        self.project_as_project = project_as_project
        self.milestone_support = milestone_support
        self.gitlab.auth()

    @lru_cache(None)
    def get_project_by_id(self, project_id: str) -> Project:
        project = self.gitlab.projects.get(id=project_id)
        return project

    def load_issue_list(self) -> Iterator[GitlabTodoEntry]:
        assignee_user = self.gitlab.users.list(username=self.assignee)[0]
        return (
            GitlabTodoEntry(issue, self)
            for issue
            in self.gitlab.issues.list(
                assignee_id=assignee_user.id,
                state='opened',
                scope='all',
                all=True
            )
        )
