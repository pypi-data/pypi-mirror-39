from typing import Iterator
import logging

import taiga

from .base import AbstractService, AbstractBugEntry

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['TaigaService', 'TaigaUserStory']

_log = logging.getLogger(__name__)


class TaigaUserStory(AbstractBugEntry):

    def __init__(
            self, user_story: taiga.models.models.UserStory,
            project: taiga.models.models.Project,
            service: 'TaigaService') -> None:
        super().__init__(user_story.subject)
        self.issue_key = f"#{project.slug}/{user_story.id}"
        self.priority = service.default_priority
        self.add_context(service.default_context)
        self.add_project(project.name.replace(' ', '_'))
        self.add_tag('service', service.service_name)
        self.add_tag('link', f'{service.host.replace("http://", "")}/project/{project.slug}/us/{user_story.id}')
        if user_story.due_date:
            self.add_tag('due', user_story.due_date)


class TaigaIssue(AbstractBugEntry):

    pass


class TaigaService(AbstractService):

    __slots__ = [
        'taiga', 'owner', 'default_priority',
        'default_context', 'host'
    ]

    _service_type = 'taiga'

    def __init__(
            self, host: str, user: str, password: str,
            owner: str, default_priority: str,
            default_context: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.host = host
        self.taiga = taiga.TaigaAPI(host=host)
        self.owner = owner
        self.default_priority = default_priority
        self.default_context = default_context
        self.taiga.auth(user, password)

    def load_issue_list(self) -> Iterator[TaigaUserStory]:
        project_list = self.taiga.projects.list()
        issue_list = []
        for project in project_list:
            issue_list.extend(
                [
                    TaigaUserStory(user_story, project, self)
                    for user_story in project.list_user_stories()
                    if user_story.owner_extra_info['username'] == self.owner and not user_story.is_closed
                ]
            )
        return iter(issue_list)
