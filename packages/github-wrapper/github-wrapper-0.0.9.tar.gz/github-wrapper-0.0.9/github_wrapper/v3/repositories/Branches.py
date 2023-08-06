import requests


def list_branches(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )



def get_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )



def get_branch_protection(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )



def update_branch_protection(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )



def remove_branch_protection(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )


def get_required_status_checks_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks",
        params=params,
        auth=auth
    )


def update_required_status_checks_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.patch(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )


def remove_required_status_checks_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )


def list_required_status_checks_contexts_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )


def replace_required_status_checks_contexts_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )


def add_required_status_checks_contexts_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )


def remove_required_status_checks_contexts_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )


def get_pull_request_review_enforcement_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )

def update_pull_request_review_enforcement_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.patch(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )

def remove_pull_request_review_enforcement_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )

def get_required_signatures_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_signatures".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )

def add_required_signatures_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_signatures".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )

def remove_required_signatures_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_signatures".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )

def get_admin_enforcement_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )

def add_admin_enforcement_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )

def remove_admin_enforcement_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )


def get_restrictions_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )


def remove_restrictions_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )


def list_team_restrictions_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )


def replace_team_restrictions_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )


def add_team_restrictions_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )


def remove_team_restrictions_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )


def list_user_restrictions_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )


def replace_user_restrictions_of_protected_branch(owner: str, repo: str, branch: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users".format(owner=owner, repo=repo, branch=branch),
        json=json,
        auth=auth
    )


def add_user_restrictions_of_protected_branch(owner: str, repo: str, branch: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users".format(owner=owner, repo=repo, branch=branch),
        params=params,
        auth=auth
    )


def remove_user_restrictions_of_protected_branch(owner: str, repo: str, branch: str, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param branch:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users".format(owner=owner, repo=repo, branch=branch),
        auth=auth
    )