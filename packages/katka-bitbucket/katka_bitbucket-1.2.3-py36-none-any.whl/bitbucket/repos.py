import logging

from dataclasses import dataclass

from .exceptions import ReposNotFound
from .service import BitbucketService

log = logging.getLogger(__name__)


@dataclass
class BitbucketRepos(BitbucketService):
    project_id: str = None

    def __post_init__(self):
        """
        Raises:
            ValueError: In case project_key is null or empty
        """
        if not self.project_id:
            raise ValueError('project_id can\'t be null or empty')

        super().__post_init__()

        self.path = f'projects/{self.project_id}/repos'

    def get_repos(self) -> list:
        '''
        Retrieves the list of repos for a project

        Returns:
            list(dict): The list of repos under the `project_id`

        Raises:
            ReposNotFound: In case the project does not have repos
        '''
        repos = self.get() or {}
        fine_repos = []

        if repos.get('values'):
            repos = repos['values']

            for repo in repos:
                fine_repo = {key: repo[key] for key in ('slug', 'name') if repo.get(key)}
                if fine_repo:
                    fine_repos.append(fine_repo)

            repos = fine_repos

        if not fine_repos:
            log.warning(f'No repos found under {self.project_id} project')
            raise ReposNotFound()

        return repos
