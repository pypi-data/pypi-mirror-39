import requests


# def link_Relations(params=None, auth=None) -> requests.Response:
#     """
#     Link Relations
#
#     :param params:
#     :param auth:
#     :return:
#     """
#     return requests.get(
#         "https://api.github.com",
#         params,
#         auth=auth
#     )


def list_pull_requests(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    List pull requests

    :param owner:
    :param repo:string
    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls".format(owner=owner, repo=repo),
        params,
        auth=auth
    )


def get_a_single_pull_request(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Get a single pull request

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls/{number}".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def create_a_pull_request(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    Create a pull request

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls".format(owner=owner, repo=repo),
        params,
        auth=auth
    )


def update_a_pull_request(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Update a pull request

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls/{number}".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def list_commits_on_a_pull_request(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    List commits on a pull request

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls/{number}/commits".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def list_pull_requests_files(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    List pull requests files

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls/{number}/files".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def get_if_a_pull_request_has_been_merged(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Get if a pull request has been merged

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls/{number}/merge".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def merge_a_pull_request_button(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Merge a pull request (Merge Button)

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/pulls/{number}/merge".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


# def labels_assignees_and_milestones(owner: str, repo: str, params=None, auth=None) -> requests.Response:
#     """
#     Labels, assignees, and milestones
#
#     :param params:
#     :param auth:
#     :return:
#     """
#     return requests.get(
#         "https://api.github.com/repos/{owner}/{repo}/pulls".format(owner=owner, repo=repo),
#         params,
#         auth=auth
#     )
#
#
# def custom_media_types(owner: str, repo: str, params=None, auth=None) -> requests.Response:
#     """
#     Custom media types
#
#     :param params:
#     :param auth:
#     :return:
#     """
#     return requests.get(
#         "https://api.github.com/repos/{owner}/{repo}/pulls".format(owner=owner, repo=repo),
#         params,
#         auth=auth
#     )
