import requests


def list_all_labels_for_this_repository(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    List all labels for this repository

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/labels".format(owner=owner, repo=repo),
        params,
        auth=auth
    )


def get_a_single_label(owner: str, repo: str, name: str, params=None, auth=None) -> requests.Response:
    """
    Get a single label

    :param owner:
    :param repo:
    :param name:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/labels/{name}".format(owner=owner, repo=repo, name=name),
        params,
        auth=auth
    )


def create_a_label(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    Create a label

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/labels".format(owner=owner, repo=repo),
        params,
        auth=auth
    )


def update_a_label(owner: str, repo: str, current_name:str, params=None, auth=None) -> requests.Response:
    """
    Update a label

    :param owner:
    :param repo:
    :param current_name:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.patch(
        "https://api.github.com/repos/{owner}/{repo}/labels/{current_name}".format(owner=owner, repo=repo, current_name=current_name),
        params,
        auth=auth
    )


def delete_label(owner: str, repo: str, name: str, params=None, auth=None) -> requests.Response:
    """
    Delete a label

    :param owner:
    :param repo:
    :param name:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/labels/{name}".format(owner=owner, repo=repo, name=name),
        params,
        auth=auth
    )


def list_label_on_issue(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    List labels on an issue

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/labels".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def add_labels_to_an_issue(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Add labels to an issue

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/labels".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def remove_a_label_from_an_issue(owner: str, repo: str, number: int, name: str, params=None, auth=None) -> requests.Response:
    """
    Remove a label from an issue

    :param owner:
    :param repo:
    :param number:
    :param name"
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/labels/{name}".format(owner=owner, repo=repo, number=number, name=name),
        params,
        auth=auth
    )


def replace_all_labels_for_an_issue(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Replace all labels for an issue

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/labels".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def remove_all_labels_from_an_issue(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Remove all labels from an issue

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/issues/{number}/labels".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )


def get_labels_for_every_issue_in_a_milestone(owner: str, repo: str, number: int, params=None, auth=None) -> requests.Response:
    """
    Remove all labels from an issue

    :param owner:
    :param repo:
    :param number:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/milestones/{number}/labels".format(owner=owner, repo=repo, number=number),
        params,
        auth=auth
    )
