import requests


def list_issues(params=None, auth=None) -> requests.Response:
    """

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def list_user_issues(params=None, auth=None) -> requests.Response:
    """

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/user/issues",
        params,
        auth=auth
    )


def list_organization_issues(org: str, params=None, auth=None) -> requests.Response:
    """

    :param org:
    :param params:
    :param auth:
    :return:
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
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/issues".format(owner=owner, repo=repo),
        params,
        auth=auth
    )


def get_a_single_issue(owner: str, repo: str, number: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def create_an_issue(owner: str, repo: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param json:
    :param auth:
    :return:
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/issues".format(owner=owner, repo=repo),
        json=json,
        auth=auth
    )


def edit_an_issue(owner: str, repo: str, number: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param number:
    :param json:
    :param auth:
    :return:
    """
    return requests.patch(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}".format(owner=owner, repo=repo, number=number),
        json=json,
        auth=auth
    )


def lock_an_issue(owner: str, repo: str, number: str, params=None, auth=None) -> "Status: 204 No Content":
    """

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return:
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/lock".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def unlock_an_issue(owner: str, repo: str, number: str, auth=None) -> "Status: 204 No Content":
    """

    :param owner:
    :param repo:
    :param number:
    :param auth:
    :return:
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/lock".format(owner=owner, repo=repo, number=number)
    )


# def custom_media_types(auth=basic_auth()):
#     return requests.get("")
