from typing import Iterator, Dict
import logging
from urllib.parse import urlparse

from jira import JIRA, Issue

from .base import AbstractService, AbstractBugEntry

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['JiraTodoEntry', 'JiraService', 'DEFAULT_PRIORITY_MAPPING']

_log = logging.getLogger(__name__)

DEFAULT_PRIORITY_MAPPING = {
    "High": "A",
    "Highest": "A",
    "Medium": "B",
    "Low": "C",
    "Lowest": "C"
}


class JiraTodoEntry(AbstractBugEntry):

    __slots__ = ['issue_key']

    def __init__(
            self, jira_issue: Issue, priority_mapping: Dict[str, str],
            service_name: str, context: str) -> None:
        super().__init__(jira_issue.fields.summary)
        self.issue_key = jira_issue.key
        self.priority = priority_mapping.get(jira_issue.fields.priority.name)
        self.add_project(jira_issue.fields.project.key)
        self.add_context(context)
        # Remove https: from link to avoid collon
        parsed_url = urlparse(jira_issue.permalink())
        self.add_tag('link', f"{parsed_url.netloc}{parsed_url.path}")
        self.add_tag('service', service_name)


class JiraService(AbstractService):

    __slots__ = ['jira', 'search_query', 'priority_mapping', 'default_context']

    _service_type = 'jira'

    def __init__(
            self, link: str, login: str, password: str,
            search_query: str, default_context: str,
            priority_mapping: Dict[str, str] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        if priority_mapping is None:
            priority_mapping = DEFAULT_PRIORITY_MAPPING
        self.jira = JIRA(link, basic_auth=(login, password))
        self.search_query = search_query
        self.priority_mapping = priority_mapping
        self.default_context = default_context

    def load_issue_list(self) -> Iterator[JiraTodoEntry]:
        return (
            JiraTodoEntry(
                issue, self.priority_mapping,
                self.service_name, self.default_context
            )
            for issue in self.jira.search_issues(self.search_query)
        )
