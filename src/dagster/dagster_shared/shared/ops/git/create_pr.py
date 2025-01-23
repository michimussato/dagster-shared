import pathlib
import subprocess

from dagster import (
    op,
    In,
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
)


@op(
    ins={
        "BUILD_CWD": In(),
        "GH_EXE": In(),
        "PR_DRY_RUN": In(),
        "PR_READY_FOR_REVIEW": In(),
        "PR_ASSIGNEE": In(),
        "PR_REVIEWERS": In(),
        "BRANCH_NAME": In(),
        "PACKAGE_PR": In(),
        "PR_BODY": In(),
    },
)
def create_pr(
        context: AssetExecutionContext,
        BUILD_CWD: str,
        GH_EXE: str,
        PR_DRY_RUN: bool,
        PR_READY_FOR_REVIEW: bool,
        PR_ASSIGNEE: str,
        PR_REVIEWERS: list,
        BRANCH_NAME: str,
        PACKAGE_PR: str,
        PR_BODY: str,

) -> MaterializeResult:
    """
    Make sure that the dev branch exists on the remote.
    """

    reviewers = ",".join(PR_REVIEWERS)

    if not PACKAGE_PR:
        cmd = [
            GH_EXE,
            "pr",
            "create",
            "--assignee",
            f"{PR_ASSIGNEE}",
            "--reviewer",
            f"{reviewers}",
            "--title",
            f"{BRANCH_NAME}",
            "--body-file",
            PR_BODY,
        ]

        if PR_DRY_RUN:
            cmd.append(
                "--dry-run"
            )
        if not PR_READY_FOR_REVIEW:
            cmd.append(
                "--draft"
            )

        proc = subprocess.Popen(
            args=cmd,
            cwd=BUILD_CWD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = proc.communicate()
        return_code = proc.returncode

        context.log.info(stdout)
        context.log.error(stderr)
        context.log.info(return_code)

        # if stderr:
        #     raise Exception(stderr)

        if bool(return_code):
            raise Exception("PR failed.")

        context.log.warning("Make sure you add the PR URL to `PACKAGE_PR` "
                            "in `asset_factory_packages.py`. Otherwise, "
                            "you won't be able to edit this PR: "
                            f"{stdout}")

        yield MaterializeResult(
            asset_key=context.asset_key,
            metadata={
                'PR Body': MetadataValue.md(pathlib.Path(PR_BODY).read_text(encoding="utf-8")),
                'Reviewers': MetadataValue.text(reviewers),
                "Dry Run": MetadataValue.bool(PR_DRY_RUN),
                "Draft": MetadataValue.bool(not PR_READY_FOR_REVIEW),
                "PR": MetadataValue.url(stdout),
                'cmd': MetadataValue.md(f"`{cmd}`"),
                'cmd (str)': MetadataValue.path(" ".join(cmd)),
                'cwd': MetadataValue.path(BUILD_CWD),
                # 'repo': MetadataValue.path(repo),
                'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
                'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
            }
        )
    else:
        cmds = []

        # get reviewers:
        # gh pr view https://github.com/.../.../pull/1966

        cmd = [
            GH_EXE,
            "pr",
            "edit",
            PACKAGE_PR,
            "--body-file",
            PR_BODY,
        ]

        cmds.append(cmd)

        cmd_ready = [
            GH_EXE,
            "pr",
            "ready",
        ]
        if not PR_READY_FOR_REVIEW:
            cmd_ready.append("--undo")

        cmds.append(
            cmd_ready
        )

        for reviewer in PR_REVIEWERS:
            context.log.info(f"Adding reviewer: {reviewer}")
            cmd = [
                GH_EXE,
                "pr",
                "edit",
                PACKAGE_PR,
                "--add-reviewer",
                reviewer,
            ]

            proc_reviewer = subprocess.Popen(
                args=cmd,
                cwd=BUILD_CWD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout_reviewer, stderr_reviewer = proc_reviewer.communicate()
            return_code_reviewer = proc_reviewer.returncode

            context.log.info(stdout_reviewer)
            context.log.error(stderr_reviewer)
            context.log.info(return_code_reviewer)

        for cmd in cmds:

            proc = subprocess.Popen(
                args=cmd,
                cwd=BUILD_CWD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stdout, stderr = proc.communicate()
            return_code = proc.returncode

            context.log.info(stdout)
            context.log.error(stderr)
            context.log.info(return_code)

        yield MaterializeResult(
            asset_key=context.asset_key,
            metadata={
                'PR Body': MetadataValue.md(pathlib.Path(PR_BODY).read_text(encoding="utf-8")),
                'Reviewers': MetadataValue.text(reviewers),
                "Dry Run": MetadataValue.bool(PR_DRY_RUN),
                "Draft": MetadataValue.bool(not PR_READY_FOR_REVIEW),
                "PR": MetadataValue.url(PACKAGE_PR),
            }
        )

        # if stderr:
        #     raise Exception(stderr)

    # if bool(return_code):
    #     raise Exception("PR failed.")
