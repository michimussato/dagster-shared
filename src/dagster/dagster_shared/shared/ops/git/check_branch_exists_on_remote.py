import git

from dagster import (
    op,
    In,
    Output,
    AssetExecutionContext,
    AssetMaterialization,
    MetadataValue,
)


@op(
    ins={
        "BRANCH_NAME": In(),
        "GIT_REPO": In(),
        "GIT_SSH": In(),
    },
)
def check_branch_exists_on_remote(
        context: AssetExecutionContext,
        BRANCH_NAME: str,
        GIT_REPO: str,
        GIT_SSH: str,

) -> bool:
    """
    Make sure that the dev branch exists on the remote.
    """

    # g = git.cmd.Git()
    # g.ls_remote("--exit-code", "--heads", "git@github.com:michimussato/<repo>.git", "refs/heads/<branch>")

    g = git.cmd.Git()

    try:
        # Todo: this does not work for packages deeper in the tree yet
        _ret = g.ls_remote("--exit-code", "--heads", GIT_SSH, f"refs/heads/{BRANCH_NAME}")
        yield Output(True)

        yield AssetMaterialization(
            asset_key=context.asset_key,
            metadata={
                'branch exists on remote': MetadataValue.bool(True),
                'ls-remote': MetadataValue.md(f"```{_ret}```"),
                'url': MetadataValue.url(
                    f"https://github.com/michimussato/{GIT_REPO}/tree/{BRANCH_NAME}"),
            }
        )
    except git.exc.GitCommandError as e:
        context.log.exception(e)
        raise Exception(
            f"Branch {BRANCH_NAME} "
            f"does not exist on remote {GIT_SSH}."
        ) from e
