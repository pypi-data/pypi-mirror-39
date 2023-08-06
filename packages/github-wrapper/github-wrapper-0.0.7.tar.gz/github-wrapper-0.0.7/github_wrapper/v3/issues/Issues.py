import requests


def list_issues(params=None, auth=None) -> requests.Response:
    """
    List all issues assigned to the authenticated user across all visible repositories
    including owned repositories, member repositories, and organization repositories.

    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def list_user_issues(params=None, auth=None) -> requests.Response:
    """
    List all issues across owned and member repositories assigned to the authenticated user:

    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/user/issues",
        params,
        auth=auth
    )


def list_organization_issues(org: str, params=None, auth=None) -> requests.Response:
    """
    List all issues for a given organization assigned to the authenticated user:

    :param org:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/orgs/{org}/issues".format(org=org),
        params,
        auth=auth
    )


def list_issues_for_a_repository(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/issues".format(owner=owner, repo=repo),
        params,
        auth=auth
    )


def get_a_single_issue(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    The API returns a 301 Moved Permanently status if the issue was transferred to another repository.\
    If the issue was transferred to or deleted from a repository where the authenticated user
    lacks read access, the API returns a 404 Not Found status. If the issue was deleted
    from a repository where the authenticated user has read access, the API returns a 410
    Gone status. To receive webhook events for transferred and deleted issues, subscribe to the issues webhook

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def create_an_issue(owner: str, repo: str, json=None, params=None, auth=None) -> requests.Response:
    """
    Any user with pull access to a repository can create an issue.

    :param owner:
    :param repo:
    :param json:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/issues".format(owner=owner, repo=repo),
        json=json,
        params=params,
        auth=auth
    )


def edit_an_issue(owner: str, repo: str, number: int, json=None, params=None, auth=None) -> requests.Response:
    """
    Issue owners and users with push access can edit an issue.

    :param owner:
    :param repo:
    :param number:
    :param json:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.patch(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}".format(owner=owner, repo=repo, number=number),
        json=json,
        auth=auth
    )


def lock_an_issue(owner: str, repo: str, number: int, params=None, auth=None) -> "Status: 204 No Content":
    """
    Users with push access can lock an issue or pull request's conversation.

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/lock".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def unlock_an_issue(owner: str, repo: str, number: int, auth=None) -> "Status: 204 No Content":
    """
    Users with push access can unlock an issue's conversation.

    :param owner:
    :param repo:
    :param number:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/lock".format(owner=owner, repo=repo, number=number),
        auth=auth
    )


# def custom_media_types(auth=basic_auth()):
#     return requests.get("")
