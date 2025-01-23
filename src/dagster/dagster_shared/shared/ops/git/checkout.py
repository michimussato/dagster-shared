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
        "BRANCH_NAME": In(
            description=docstrings_dict["BRANCH_NAME"],
        ),
        "GIT_REPO_NAME": In(
            description=docstrings_dict["GIT_REPO_NAME"],
        ),
        "MASTER_BRANCH": In(
            description=docstrings_dict["MASTER_BRANCH"],
        ),
        "LOCAL_GIT_REPO_DIR": In(
            description=docstrings_dict["LOCAL_GIT_REPO_DIR"],
        ),
    },
)
@fmydocstring(docstrings_dict)
def checkout(
        context: AssetExecutionContext,
        BRANCH_NAME: str,
        GIT_REPO_NAME: str,
        MASTER_BRANCH: str,
        LOCAL_GIT_REPO_DIR: str,

) -> MaterializeResult:
    """
    Does what you would expect from
    `git checkout -b <BRANCH_NAME>`.
    Locally check out a branch and create it
    if it does not exist.

---

# Docs

## Usage

Todo

## Refs

- [`git checkout`](https://git-scm.com/docs/git-checkout)
- [Google Docstrings](https://google.github.io/styleguide/pyguide.html)
- [Markdown](https://www.markdownguide.org/basic-syntax/)

## Args

```
Args:
    context (dagster.AssetExecutionContext):
    BRANCH_NAME (str):        {docstrings_dict["BRANCH_NAME"]}
    GIT_REPO_NAME (str):      {docstrings_dict["GIT_REPO_NAME"]}
    MASTER_BRANCH (str):      {docstrings_dict["MASTER_BRANCH"]}
    LOCAL_GIT_REPO_DIR (str): {docstrings_dict["LOCAL_GIT_REPO_DIR"]}
```

## Returns

```
Returns:
```

## Yields

```
Yields:
```

## Raises

```
Raises:
```

    """

    repo = git.Repo(os.path.join(LOCAL_GIT_REPO_DIR, GIT_REPO_NAME))

    try:
        # -b means create (if it does not exist) and
        # checkout BRANCH_NAME
        # Todo
        #  test with
        #  repo.create_head(BRANCH_NAME)
        result = repo.git.checkout(MASTER_BRANCH, b=BRANCH_NAME)
        # push = repo.git.push("--set-upstream", repo.remote().name, BRANCH_NAME)
    except GitCommandError as checkout_err:
        context.log.warning(checkout_err)
        result = repo.git.checkout(BRANCH_NAME)
        # push = None
    finally:
        try:
            push = repo.git.push("--set-upstream", repo.remote().name, BRANCH_NAME)
        except GitCommandError as push_err:
            push = "Maybe branch already exists on remote"
            # raise Exception("Maybe branch already exists on remote?") from push_err
            context.log.warning(f"{push}:\n{push_err}")

    yield MaterializeResult(
        asset_key=context.asset_key,
        metadata={
            'Result': MetadataValue.json(result),
            'Push': MetadataValue.json(push),
        }
    )
