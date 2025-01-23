import os

import git
from git.exc import GitCommandError

from dagster import (
    op,
    In,
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
)

from shared.decorators.fmydocstring import fmydocstring
from shared.ops.git import docstrings_git as docstrings_dict


@op(
    ins={
        "GIT_SSH": In(),
        "LOCAL_GIT_REPO_DIR": In(),
        "GIT_REPO_NAME": In(),
    },
)
@fmydocstring(docstrings_dict)
def clone(
        context: AssetExecutionContext,
        GIT_SSH: str,
        LOCAL_GIT_REPO_DIR: str,
        GIT_REPO_NAME: str,

) -> MaterializeResult:
    """
    Make sure that the dev branch exists on the remote.

    ```
    Args:
        context (dagster.AssetExecutionContext):
        GIT_SSH (str):            {docstrings_dict["GIT_SSH"]}
        LOCAL_GIT_REPO_DIR (str): {docstrings_dict["LOCAL_GIT_REPO_DIR"]}
        GIT_REPO_NAME (str):      {docstrings_dict["GIT_REPO_NAME"]}
    ```
    """

    # git ls-remote --heads origin refs/heads/<BRANCH_NAME>
    # git ls-remote --exit-code --heads git@github.com:michimussato/<REPO>.git refs/heads/BRANCH
    # git.Repo("~/pycharm/tickets/PTP-432/env/git/repos/michimussato/<REPO>").git.ls_remote()

    # g = git.cmd.Git()
    # g.ls_remote("--exit-code", "--heads", "git@github.com:michimussato/<REPO>.git", "refs/heads/BRANCH")

    local_git_folder = os.path.join(LOCAL_GIT_REPO_DIR, GIT_REPO_NAME)
    pre_exists = False

    try:
        git.Repo.clone_from(
            url=GIT_SSH,
            to_path=local_git_folder,
        )
    except GitCommandError:
        context.log.warning(f"Local Git repo already extists: {local_git_folder}")
        pre_exists = True

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            'Local Repo': MetadataValue.path(local_git_folder),
            'Pre Existed': MetadataValue.bool(pre_exists),
        }
    )
