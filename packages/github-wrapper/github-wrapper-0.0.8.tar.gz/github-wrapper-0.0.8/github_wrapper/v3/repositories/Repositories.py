import requests


def list_your_repositories(params=None, auth=None) -> requests.Response:
    """
    List repositories that the authenticated user has explicit 
    permission (:read, :write, or :admin) to access.
    
    The authenticated user has explicit permission to access repositories 
    they own, repositories where they are a collaborator, and repositories 
    that they can access through an organization membership.

    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/user/repos",
        params=params,
        auth=auth
    )


def list_user_repositories(username: str, params=None, auth=None) -> requests.Response:
    """
    List public repositories for the specified user.

    :param username:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/users/{username}/repos".format(username=username),
        params=params,
        auth=auth
    )

def list_organization_repositories(org: str, params=None, auth=None) -> requests.Response:
    """
    List repositories for the specified org.

    :param org:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/orgs/{org}/repos".format(org=org),
        params=params,
        auth=auth
    )

def list_all_public_repositories(params=None, auth=None) -> requests.Response:
    """
    This provides a dump of every public repository, in the order that they were created.

    Note: Pagination is powered exclusively by the since parameter. Use the Link 
    header to get the URL for the next page of repositories.

    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repositories",
        params=params,
        auth=auth
    )

def repository_create(json=None, auth=None) -> requests.Response:
    """

    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/user/repos",
        json=json,
        auth=auth
    )

def repository_org_create(org: str, json=None, auth=None) -> requests.Response:
    """
    Create a new repository in this organization. The authenticated user must be a member of the specified organization.

    :param owner:
    :param repo:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/orgs/{org}/repos".format(org=org),
        json=json,
        auth=auth
    )

def repository_get(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )

def repository_edit(owner: str, repo: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.patch(
        "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo),
        json=json,
        auth=auth
    )

def list_all_topics_for_a_repository(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/topics".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )

def replace_all_topics_for_a_repository(owner: str, repo: str, json=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.put(
        "https://api.github.com/repos/{owner}/{repo}/topics".format(owner=owner, repo=repo),
        json=json,
        auth=auth
    )

def list_contributors(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    Lists contributors to the specified repository and sorts them by the number of commits
    per contributor in descending order. This endpoint may return information that
    is a few hours old because the GitHub REST API v3 caches contributor
    data to improve performance.

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/contributors".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )

def list_languages(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    Lists languages for the specified repository. The value shown for each language 
    is the number of bytes of code written in that language.

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/languages".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )

def list_teams(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/teams".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )

def list_tags(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.get(
        "https://api.github.com/repos/{owner}/{repo}/tags".format(owner=owner, repo=repo),
        params=params,
        auth=auth
    )

def delete_a_repository(owner: str, repo: str, params=None, auth=None) -> requests.Response:
    """
    Deleting a repository requires admin access. 
    If OAuth is used, the delete_repo scope is required.

    :param owner:
    :param repo:
    :param params:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.delete(
        "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo),
        auth=auth
    )

def transfer_a_repository(owner: str, repo: str, json=None, auth=None) -> requests.Response:
    """
    A transfer request will need to be accepted by the new owner when 
    transferring a personal repository to another user. The response will 
    contain the original owner, and the transfer will continue asynchronously. 
    For more details on the requirements to transfer personal and 
    organization-owned repositories, see about repository transfers.

    :param owner:
    :param repo:
    :param json:
    :param auth:
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    return requests.post(
        "https://api.github.com/repos/{owner}/{repo}/transfer".format(owner=owner, repo=repo),
        json=json,
        auth=auth
    )