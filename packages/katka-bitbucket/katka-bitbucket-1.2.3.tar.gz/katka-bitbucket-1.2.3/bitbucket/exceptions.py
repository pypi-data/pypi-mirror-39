import logging
from contextlib import contextmanager

from bitbucket.models import KatkaProject
from requests import HTTPError
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed, NotFound, PermissionDenied


class ReposNotFound(Exception):
    pass


class BitbucketBaseAPIException(APIException):
    pass


class ReposNotFoundAPIException(NotFound):
    default_detail = 'No repos found for that project_id.'


class ProjectNotFoundAPIException(NotFound):
    default_detail = 'Project not found.'


class BadRequestAPIException(BitbucketBaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'
    default_code = 'bad_request'


@contextmanager
def bitbucket_exception_to_api():
    try:
        yield
    except ReposNotFound:
        raise ReposNotFoundAPIException()
    except KatkaProject.DoesNotExist:
        raise ProjectNotFoundAPIException()
    except HTTPError as ex:
        if ex.response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise AuthenticationFailed()

        if ex.response.status_code == status.HTTP_403_FORBIDDEN:
            raise PermissionDenied()

        errors = ex.response.json().get('errors') if ex.response.content else None

        if errors and errors[0].get('exceptionName') == 'com.atlassian.bitbucket.project.NoSuchProjectException':
            logging.warning(errors[0].get('message'))
            raise ProjectNotFoundAPIException()

        if errors:
            logging.exception(f'Unexpected Bitbucket exception: {errors[0].get("message")}')
        else:
            logging.exception(f'Unexpected Bitbucket exception: {str(ex)}')

        if ex.response.status_code == status.HTTP_400_BAD_REQUEST:
            raise BadRequestAPIException()

        raise BitbucketBaseAPIException()
