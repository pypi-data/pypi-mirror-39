import mock
import pytest
from bitbucket.exceptions import ReposNotFound
from bitbucket.repos import BitbucketRepos


class TestBitbucketRepos:
    @mock.patch('bitbucket.service.BitbucketService.get')
    @mock.patch('bitbucket.service.KatkaProject.objects')
    def test_get_repos(self, mock_db_katka_project, mock_get_request):
        mock_get_request.return_value = {
            'something_else': 'value',
            'values': [
                {'name': 'super_man', 'slug': 'super', 'something_else': 'value'},
                {'name': 'batman', 'slug': 'bat'},
            ]
        }

        service = BitbucketRepos(katka_project_id='wonder_woman', project_id='the_wasp')
        repos = service.get_repos()

        assert service.path == 'projects/the_wasp/repos'
        assert repos == [
            {'name': 'super_man', 'slug': 'super'},
            {'name': 'batman', 'slug': 'bat'},
        ]

    def test_empty_project_id(self):
        with pytest.raises(ValueError):
            BitbucketRepos(katka_project_id='wonder_woman', project_id=None)

    @mock.patch('bitbucket.service.BitbucketService.get')
    @mock.patch('bitbucket.service.KatkaProject.objects')
    def test_not_expected_params(self, mock_db_katka_project, mock_get_request):
        mock_get_request.return_value = {
            'something_else': 'value',
            'values': [
                {'something_else': 'value'},
            ]
        }
        service = BitbucketRepos(katka_project_id='wonder_woman', project_id='the_wasp')

        with pytest.raises(ReposNotFound):
            service.get_repos()

    @mock.patch('bitbucket.service.BitbucketService.get')
    @mock.patch('bitbucket.service.KatkaProject.objects')
    def test_nno_repos(self, mock_db_katka_project, mock_get_request):
        mock_get_request.return_value = {}
        service = BitbucketRepos(katka_project_id='wonder_woman', project_id='the_wasp')

        with pytest.raises(ReposNotFound):
            service.get_repos()
