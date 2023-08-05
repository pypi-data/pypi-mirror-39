from django.urls import reverse

import mock
import pytest
from bitbucket.exceptions import (
    BadRequestAPIException, ProjectNotFoundAPIException, ReposNotFound, ReposNotFoundAPIException,
)
from bitbucket.models import KatkaProject
from requests import HTTPError, Response
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class TestGetRepos:
    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_get_existing_repos(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        result.get_repos.return_value = [
            {'name': 'super_man', 'slug': 'super'},
            {'name': 'batman', 'slug': 'bat'},
        ]
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7', 'limit': 10, 'start': 2}
        )

        assert response.status_code == 200
        assert len(response.data) == 2

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_repos_not_found(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        result.get_repos.side_effect = ReposNotFound
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert response.status_code == 404
        assert str(response.data['detail']) == ReposNotFoundAPIException.default_detail

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_project_not_found(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        result.get_repos.side_effect = KatkaProject.DoesNotExist
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert response.status_code == 404
        assert str(response.data['detail']) == ProjectNotFoundAPIException.default_detail

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_bitbucket_project_not_found(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        response = Response()
        response.status_code = 404
        response._content = b'{"errors":[{"exceptionName":"com.atlassian.bitbucket.project.NoSuchProjectException"}]}'
        result.get_repos.side_effect = HTTPError(response=response)
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert response.status_code == 404
        assert str(response.data['detail']) == ProjectNotFoundAPIException.default_detail

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_project_http_error_no_error_message(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        response = Response()
        response.status_code = 400
        result.get_repos.side_effect = HTTPError(response=response)
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert response.status_code == 400
        assert str(response.data['detail']) == BadRequestAPIException.default_detail

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_project_http_no_detail(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        response = Response()
        response.status_code = 503
        response._content = b'{"errors":[{"message":"Some unknown problem"}]}'
        result.get_repos.side_effect = HTTPError(response=response)
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert response.status_code == 500

    @pytest.mark.parametrize(
        'code, detail', [(401, AuthenticationFailed.default_detail), (403, PermissionDenied.default_detail)]
    )
    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_auth_exceptions(self, mock_bitbucket_repos, code, detail, client):
        result = mock.Mock()
        response = Response()
        response.status_code = code
        response._content = b'{"errors":[{"message":"Some unknown problem"}]}'
        result.get_repos.side_effect = HTTPError(response=response)
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_id': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert str(response.data['detail']) == detail
