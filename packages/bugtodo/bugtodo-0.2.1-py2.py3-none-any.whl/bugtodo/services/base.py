from abc import ABC, abstractmethod
import logging
from typing import List, Iterator, Set, Dict

from todotxt import TodoFile, TodoEntry

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['AbstractService']

_log = logging.getLogger(__name__)


class AbstractBugEntry(TodoEntry):

    __slots__ = ['issue_key']


class AbstractService(ABC):

    __slots__ = ['project_mapping', 'service_name']

    _service_type: str
    registered_services: Dict[str, 'AbstractService'] = {}

    def __init__(self, service_name: str, project_mapping: Dict[str, str] = None) -> None:
        if project_mapping is None:
            project_mapping = {}
        self.project_mapping = project_mapping
        self.service_name = service_name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.registered_services[cls._service_type] = cls

    @abstractmethod
    def load_issue_list(self) -> Iterator[AbstractBugEntry]:
        pass

    def _replace_projects(self, bug_entry: AbstractBugEntry) -> AbstractBugEntry:
        for project in bug_entry.projects:
            if project in self.project_mapping:
                target_project = self.project_mapping.get(project)
                _log.debug('Replace project %s with project %s in issue %s', project, target_project, bug_entry.issue_key)
                bug_entry.remove_project(project)
                bug_entry.add_project(self.project_mapping.get(project))
        return bug_entry

    def _processed_issue_list(self) -> Iterator[AbstractBugEntry]:
        issue_list_generator = self.load_issue_list()
        return map(self._replace_projects, issue_list_generator)

    def _load_issues(self, todo_file: TodoFile, service_exists_issues: List[TodoEntry]) -> Set[str]:
        _log.info('Start load issues for service %s', self.service_name)
        loaded_issues = set()
        for service_issue in self._processed_issue_list():
            link = service_issue.tags.get('link')
            loaded_issues.add(link)
            # I guess fine with this, because we use list here
            similar_issues = list(filter(lambda x: x.tags.get('link') == link, service_exists_issues))  # pylint: disable=cell-var-from-loop
            if similar_issues:
                if len(similar_issues) == 1:
                    if str(service_issue) in str(similar_issues[0]):
                        _log.info('%s already in todo.txt, skip this entry', service_issue.issue_key)
                        continue
                _log.info('Merge new service issue %s with another issues', service_issue.issue_key)
                for similar_issue in similar_issues:
                    service_issue.merge(similar_issue)
                _log.info('Remove old todo notes')
                todo_file.remove_entries(similar_issues)
            _log.info('Add new issue %s', service_issue.issue_key)
            todo_file.add_entry(service_issue)
        return loaded_issues

    def _cleanup_old_issues(
            self, todo_file: TodoFile, loaded_issues_links: Set[str],
            service_exists_issues: List[AbstractBugEntry]) -> None:
        _log.info('Start remove old issues for service %s', self.service_name)
        for service_exists_issue in service_exists_issues:
            if service_exists_issue.tags.get('link') not in loaded_issues_links:
                _log.info('Remove completed issue %s', service_exists_issue)
                todo_file.remove_entry(service_exists_issue)

    def fetch_issues(self, todo_file: TodoFile) -> None:
        service_exists_issues = list(
            filter(lambda x: x.tags.get('service') == self.service_name, todo_file.todo_entries)
        )
        loaded_issues_links = self._load_issues(todo_file, service_exists_issues)
        self._cleanup_old_issues(todo_file, loaded_issues_links, service_exists_issues)
