import requests


def list_all_labels_for_this_repository(params=None, auth=None) -> requests.Response:
    """
    List all labels for this repository

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def get_a_single_label(params=None, auth=None) -> requests.Response:
    """
    Get a single label

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def create_a_label(params=None, auth=None) -> requests.Response:
    """
    Create a label

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def update_a_label(params=None, auth=None) -> requests.Response:
    """
    Update a label

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def delete_label(params=None, auth=None) -> requests.Response:
    """
    Delete a label

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def list_label_on_issue(params=None, auth=None) -> requests.Response:
    """
    List labels on an issue

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def add_labels_to_an_issue(params=None, auth=None) -> requests.Response:
    """
    Add labels to an issue

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def remove_a_label_from_an_issue(params=None, auth=None) -> requests.Response:
    """
    Remove a label from an issue

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def replace_all_labels_for_an_issue(params=None, auth=None) -> requests.Response:
    """
    Replace all labels for an issue

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def remove_all_labels_from_an_issue(params=None, auth=None) -> requests.Response:
    """
    Remove all labels from an issue

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )


def get_labels_for_every_issue_in_a_milestone(params=None, auth=None) -> requests.Response:
    """
    Remove all labels from an issue

    :param params:
    :param auth:
    :return:
    """
    return requests.get(
        "https://api.github.com/issues",
        params,
        auth=auth
    )